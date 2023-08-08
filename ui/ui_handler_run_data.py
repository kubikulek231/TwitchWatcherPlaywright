import time

from watcher.watcher_data_container import WatcherRoutineState, WatcherOutputDataContainer


class UIDataManager:
    def __init__(self):
        self._data = None
        self._is_new = True
        self._skip_show_num = 0
        self._start_time = time.time()
        self._watch_start = time.time()
        self._watch_time = 0

    @staticmethod
    def get_passed_time_string(time_to_convert) -> str:
        seconds = int(time_to_convert)
        minutes, hours = seconds // 60, seconds // 3600
        seconds %= 60
        minutes %= 60
        return_string = ""
        if hours > 0:
            return_string += f"{hours}h"
        if minutes > 0:
            if return_string != "":
                return_string += " "
            return_string += f"{minutes}m"
        if seconds > 0 or return_string == "":
            if return_string != "":
                return_string += " "
            return_string += f"{seconds}s"
        return return_string

    @staticmethod
    def get_current_time_string() -> str:
        time_struct = time.localtime()
        time_string = f"{time_struct.tm_hour:02d}:{time_struct.tm_min:02d}:{time_struct.tm_sec:02d}:"
        return time_string

    def _count_watch_time(self) -> None:
        current_time = time.time()
        self._watch_time += (current_time - self._watch_start)
        self._watch_start = current_time

    def _reset_watch_time_counter(self) -> None:
        self._watch_start = time.time()

    @staticmethod
    def _shorten_string(text, length):
        if len(text) <= length:
            return text
        else:
            return text[:length] + "..."

    @staticmethod
    def _format_string_to_list(text, length):
        return_list = []
        if len(text) <= length:
            return_list.append(text)
            return return_list
        else:
            for i in range(0, len(text), length):
                return_list.append(text[i:i + length])
            return return_list

    def _show_data(self) -> None:
        data = self._data
        spacer = "         "
        time_string = self.get_current_time_string()
        print("")
        match self._data.routine_state:
            case WatcherRoutineState.STARTING:
                print(f" {time_string} @Watcher: starting")
                self._reset_watch_time_counter()

            case WatcherRoutineState.CHECKING_LOGIN_STATUS:
                print(f" {time_string} @Watcher: checking login status")
                self._reset_watch_time_counter()

            case WatcherRoutineState.LOOKING_FOR_CHANNEL:
                print(f" {time_string} @Watcher: looking for channel")
                self._reset_watch_time_counter()

            case WatcherRoutineState.WATCHING:
                print(f" {time_string} @Watcher:        watching ")
                print(f" {spacer} -----------------------------------------------------------------------------")
                print(f" {spacer} - Stream:        {data.stream_channel} streaming {data.stream_game} "
                      f"for {data.stream_viewers} viewers ")
                title_list = self._format_string_to_list(data.stream_title, 60)
                print(f" {spacer} - Title:         {title_list[0]} ")
                for title in title_list[1:]:
                    print(f" {spacer}                  {title} ")
                print(f" {spacer} - Latest drop:   {data.latest_drop_time}")
                print(f" {spacer} - Drop name:     {data.latest_drop_name} for game {data.latest_drop_game}")
                print(f" {spacer} - Cha. points:   {data.chat_points}")
                print(f" {spacer} - Collected:     {data.chat_claimed_num} chat point bonuses, "
                      f"{data.drop_claimed_num} twitch drops so far.")
                print(f" {spacer} - Running for:   {self.get_passed_time_string(time.time() - self._start_time)}," +
                      f" of that watching: {self.get_passed_time_string(self._watch_time)} ")
                self._count_watch_time()

            case WatcherRoutineState.IDLING:
                print(f" {time_string} @Watcher: idling ")
                print(f" {spacer} No channel found online ")
                self._reset_watch_time_counter()

            case WatcherRoutineState.QUITING:
                print(f" {time_string} @Watcher: stopping ")
                self._reset_watch_time_counter()

    def update_data(self, data: WatcherOutputDataContainer) -> None:
        if self._data != data:
            self._data = data
            self._is_new = True

    def show_data(self) -> None:
        if self._data is None:
            return
        if self._is_new or self._skip_show_num > 10:
            self._show_data()
            self._is_new = False
            self._skip_show_num = 0
