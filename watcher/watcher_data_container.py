from enum import Enum


class WatcherRoutineState(Enum):
    STARTING = 0
    CHECKING_LOGIN_STATUS = 1
    LOOKING_FOR_CHANNEL = 2
    WATCHING = 3
    IDLING = 4
    QUITING = 5


class WatcherInputDataContainer:
    def __init__(self, channels: list, cookie_data: dict,
                 channel_search_interval: int = 300,
                 channel_details_interval: int = 10,
                 chat_claim_interval: int = 60,
                 drop_inventory_interval: int = 180
                 ):
        self.channels = channels
        self.cookie_data = cookie_data
        self.channel_search_interval = channel_search_interval
        self.channel_details_interval = channel_details_interval
        self.chat_claim_interval = chat_claim_interval
        self.drop_inventory_interval = drop_inventory_interval


class WatcherOutputDataContainer:
    def __init__(self):
        self.critical_error = False
        self.error_message = None
        self.routine_state = None
        self.stream_channel = None
        self.stream_game = None
        self.stream_title = None
        self.stream_viewers = None
        self.chat_points = None
        self.chat_claimed_num = 0
        self.latest_drop_name = None
        self.latest_drop_game = None
        self.latest_drop_time = None
        self.drop_claimed_num = 0

    def __eq__(self, other):
        if not isinstance(other, WatcherOutputDataContainer):
            return False

        return (
                self.critical_error == other.critical_error and
                self.error_message == other.error_message and
                self.routine_state == other.routine_state and
                self.stream_channel == other.stream_channel and
                self.stream_game == other.stream_game and
                self.stream_title == other.stream_title and
                self.stream_viewers == other.stream_viewers and
                self.chat_points == other.chat_points and
                self.chat_claimed_num == other.chat_claimed_num and
                self.latest_drop_name == other.latest_drop_name and
                self.latest_drop_game == other.latest_drop_game and
                self.latest_drop_time == other.latest_drop_time and
                self.drop_claimed_num == other.drop_claimed_num
        )

    def __ne__(self, other):
        return not self.__eq__(other)
