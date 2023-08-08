import time
from enum import Enum
from multiprocessing import Event, Process, Queue

from watcher.watcher_data_container import WatcherInputDataContainer, WatcherOutputDataContainer, WatcherRoutineState
from watcher.watcher_routine import WatcherRoutine, WatcherCriticalError, WatcherError
from watcher.watcher_routine_timer import WatcherRoutineTimer


class WatcherErrorState(Enum):
    NOT_SET = "Watcher data container not set"
    ALREADY_RUNNING = "Watcher is already running"
    ALREADY_STOPPED = "Watcher is already stopped"


class Watcher:
    def __init__(self, input_data_container: WatcherInputDataContainer):
        self._input_data_container = input_data_container
        self._process = None
        self._stop_event = None
        self._running = False
        self._queue = None

    def start(self) -> WatcherErrorState:
        if self._running:
            return WatcherErrorState.ALREADY_RUNNING
        if self._input_data_container is None:
            return WatcherErrorState.NOT_SET
        self._queue = Queue()
        self._running = True
        self._stop_event = Event()
        self._process = Process(target=self._routine,
                                args=(self._input_data_container,
                                      self._stop_event,))
        self._process.start()

    def stop(self) -> WatcherErrorState:
        if not self._running:
            return WatcherErrorState.ALREADY_RUNNING
        self._stop_event.set()
        self._process.join()
        self._process = None
        self._running = False

    def get_output_data(self) -> WatcherOutputDataContainer:
        if self._queue is not None:
            try:
                return self._queue.get(block=False)
            except Exception:
                pass

    def _routine(self, input_data_container: WatcherInputDataContainer, stop_event: Event) -> None:
        watcher_routine = WatcherRoutine(input_data_container)
        oc = watcher_routine.output_data_container
        common_error_number = 0
        # browser and twitch setup
        try:

            if not stop_event.is_set():
                oc.routine_state = WatcherRoutineState.STARTING
                self.__queue_put(oc)
                watcher_routine.perform_browser_start()
            if not stop_event.is_set():
                oc.routine_state = WatcherRoutineState.CHECKING_LOGIN_STATUS
                self.__queue_put(oc)
                watcher_routine.perform_twitch_login_check()

        except WatcherCriticalError as e:
            oc.critical_error = True
            oc.critical_error_message = e
            self.__queue_put(oc)

        channel_search_timer = WatcherRoutineTimer(input_data_container.channel_search_interval)
        channel_details_timer = WatcherRoutineTimer(input_data_container.channel_details_interval)
        chat_points_timer = WatcherRoutineTimer(input_data_container.chat_claim_interval)
        drop_inventory_timer = WatcherRoutineTimer(input_data_container.drop_inventory_interval)

        channel_search_timer.set_temp_and_reset(0)
        channel_details_timer.set_temp_and_reset(0)
        chat_points_timer.set_temp_and_reset(0)
        drop_inventory_timer.set_temp_and_reset(0)

        while not stop_event.is_set() and not oc.critical_error:

            if channel_search_timer.check_and_reset():
                try:
                    oc.routine_state = WatcherRoutineState.LOOKING_FOR_CHANNEL
                    self.__queue_put(oc)
                    watcher_routine.perform_channel_search()
                    if oc.stream_channel is None:
                        channel_search_timer.set_temp_and_reset(30)
                        oc.latest_drop_game = oc.latest_drop_name = oc.latest_drop_time = oc.chat_points = None
                        oc.routine_state = WatcherRoutineState.IDLING
                    else:
                        watcher_routine.perform_stream_watch()
                        oc.routine_state = WatcherRoutineState.WATCHING
                        watcher_routine.perform_chat_open(oc.stream_channel)
                except WatcherError as e:
                    self.__on_common_error(str(e), common_error_number, channel_search_timer, oc)

            if channel_details_timer.check_and_reset():
                try:
                    if oc.stream_channel is not None:
                        watcher_routine.perform_stream_get_details()
                except WatcherError as e:
                    self.__on_common_error(str(e), common_error_number, channel_details_timer, oc)

            if chat_points_timer.check_and_reset():
                try:
                    if oc.stream_channel is not None:
                        watcher_routine.perform_chat_collect_points()
                        watcher_routine.perform_chat_get_details()
                except WatcherError as e:
                    self.__on_common_error(str(e), common_error_number, chat_points_timer, oc)

            if drop_inventory_timer.check_and_reset():
                try:
                    if oc.stream_channel is not None:
                        watcher_routine.perform_drop_inventory_open()
                        watcher_routine.perform_drop_inventory_collect_drop()
                        watcher_routine.perform_drop_inventory_get_details()
                except Exception as e:
                    self.__on_common_error(str(e), common_error_number, drop_inventory_timer, oc)

            self.__queue_put(oc)
            time.sleep(1)

        oc.routine_state = WatcherRoutineState.QUITING
        self.__queue_put(oc)

        time.sleep(1)

        watcher_routine.perform_quit()

    def __queue_put(self, output_data_container: WatcherOutputDataContainer) -> None:
        self._queue.put(output_data_container)

    @staticmethod
    def __on_common_error(error_message: str, common_error_number: int,
                          timer: WatcherRoutineTimer,
                          output_data_container: WatcherOutputDataContainer) -> None:
        timer.set_temp_and_reset(10)
        output_data_container.error_message = error_message
        common_error_number += 1
        if common_error_number > 3:
            output_data_container.critical_error = True
