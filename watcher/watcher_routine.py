import unicodedata

from handler.browser_handler import BrowserHandler
from handler.twitch_handler import TwitchHandler
from watcher.watcher_data_container import WatcherOutputDataContainer, WatcherInputDataContainer, WatcherRoutineState
from misc.random_sleep import RandomSleep


class WatcherCriticalError(Exception):
    def __init__(self, message):
        super().__init__(message)


class WatcherError(Exception):
    def __init__(self, message):
        super().__init__(message)


def using_tab(index):
    def decorator(input_function):
        def wrapper(self, *args, **kwargs):
            # if needed tab is next and not open, open it
            if self._browser_handler.tab_index_max + 1 == index:
                self._browser_handler.browser_open_new_tab()
            self._browser_handler.browser_switch_to_tab(index)
            return_value = input_function(self, *args, **kwargs)
            return return_value

        return wrapper

    return decorator


class WatcherRoutine:
    def __init__(self, input_data_container: WatcherInputDataContainer):
        self._browser_handler = BrowserHandler()
        self._twitch_handler = TwitchHandler(self._browser_handler)
        self._input_data_container = input_data_container
        self.output_data_container = WatcherOutputDataContainer()

    def perform_browser_start(self) -> None:
        if not self._browser_handler.browser_start():
            raise WatcherCriticalError("Failed to start browser")
        url = "https://www.twitch.tv/"
        if not self._browser_handler.browser_import_cookies(self._input_data_container.cookie_data, url):
            raise WatcherCriticalError("Failed to import cookies")

    @using_tab(0)
    def perform_twitch_login_check(self) -> None:
        self._twitch_handler.twitch_login_page_open()
        """if not self._twitch_handler.twitch_login_page_open():
            raise WatcherCriticalError("Failed to open login page")"""
        if not self._twitch_handler.twitch_is_logged():
            raise WatcherCriticalError("Failed to login")

    @using_tab(0)
    def perform_twitch_accept_cookies(self) -> None:
        if self._twitch_handler.twitch_is_accept_cookies():
            self._twitch_handler.twitch_accept_cookies()

    @using_tab(0)
    def perform_channel_search(self) -> None:
        oc = self.output_data_container
        for channel in self._input_data_container.channels:
            if self._twitch_handler.twitch_channel_is_live(channel):
                oc.stream_channel = channel
                return
        oc.stream_channel = None

    @using_tab(0)
    def perform_stream_watch(self) -> None:
        self.output_data_container.routine_state = WatcherRoutineState.WATCHING
        self._twitch_handler.twitch_stream_player_open(self.output_data_container.stream_channel)
        self._twitch_handler.twitch_stream_player_confirm_warning()
        if not self._twitch_handler.twitch_stream_player_unmute():
            raise WatcherError(f"Failed to unmute {self.output_data_container.stream_channel}'s stream")

    @using_tab(0)
    def perform_stream_get_details(self) -> None:
        oc = self.output_data_container
        oc.stream_title = self._twitch_handler.twitch_stream_player_get_title()
        oc.stream_game = self._twitch_handler.twitch_stream_player_get_game()
        oc.stream_viewers = self._twitch_handler.twitch_stream_player_get_viewers()
        if oc.stream_title is None or oc.stream_game is None or oc.stream_viewers is None:
            raise WatcherError("Failed to get stream details")

    @using_tab(0)
    def perform_stream_is_still_live(self) -> bool:
        return self._twitch_handler.twitch_channel_is_live()

    @using_tab(1)
    def perform_chat_open(self, channel: str) -> None:
        self._twitch_handler.twitch_chat_open(channel)

    @using_tab(1)
    def perform_chat_get_details(self) -> None:
        oc = self.output_data_container
        points_string = self._twitch_handler.twitch_chat_get_points()
        if points_string is not None:
            oc.chat_points = unicodedata.normalize("NFKD", points_string)
            return
        raise WatcherError("Failed to get chat details")

    @using_tab(1)
    def perform_chat_collect_points(self) -> bool:
        if self._twitch_handler.twitch_chat_is_claimable():
            if not self._twitch_handler.twitch_chat_claim():
                raise WatcherError("Failed to claim chat points")
            oc = self.output_data_container
            if oc.chat_claimed_num is None:
                oc.chat_claimed_num = 0
            oc.chat_claimed_num += 1
            return True
        return False

    @using_tab(2)
    def perform_drop_inventory_open(self) -> None:
        self._twitch_handler.twitch_drop_inventory_open()

    @using_tab(2)
    def perform_drop_inventory_get_details(self) -> None:
        oc = self.output_data_container
        oc.latest_drop_game = self._twitch_handler.twitch_drop_inventory_latest_drop_get_game()
        oc.latest_drop_name = self._twitch_handler.twitch_drop_inventory_latest_drop_get_name()
        oc.latest_drop_time = self._twitch_handler.twitch_drop_inventory_latest_drop_get_time()
        if oc.latest_drop_game is None or oc.latest_drop_name is None or oc.latest_drop_time is None:
            raise WatcherError("Failed to get drop details")

    @using_tab(2)
    def perform_drop_inventory_collect_drop(self) -> bool:
        if self._twitch_handler.twitch_drop_inventory_is_claimable():
            if not self._twitch_handler.twitch_drop_inventory_claim():
                raise WatcherError("Failed to claim drop")
            oc = self.output_data_container
            if oc.drop_claimed_num is None:
                oc.drop_claimed_num = 0
            oc.drop_claimed_num += 1
            return True
        return False

    def perform_quit(self) -> None:
        try:
            self._browser_handler.browser_close()
        except Exception as e:
            self.output_data_container.critical_error = True
            self.output_data_container.error_message.append(str(e))
