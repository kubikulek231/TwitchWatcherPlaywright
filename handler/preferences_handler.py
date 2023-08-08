from enum import Enum

from handler.json_handler import JsonFileHandler, JsonErrorState


class ChannelErrorState(Enum):
    CHANNEL_DOES_NOT_EXIST = "Channel does not exist."
    CHANNEL_ALREADY_EXISTS = "Cannot add a channel that already exists."
    CHANNEL_NAME_IS_EMPTY = "Channel name cannot be empty."
    CHANNEL_ALREADY_ON_TOP = "Channel already on top."
    CHANNEL_ALREADY_ON_BOTTOM = "Channel already on bottom."


class PreferencesHandler(JsonFileHandler):
    def __init__(self):
        super().__init__()
        self._preferences = {
            "channels": [],
            "options": {"app_run_on_start": False,
                        "app_save_on_exit": True}
        }

    @property
    def channels(self):
        return self._preferences["channels"]

    @property
    def options(self):
        return self._preferences["options"]

    def option_set(self, option_name: str, option_value: bool) -> bool:
        try:
            self._preferences["options"][option_name] = option_value
        except KeyError:
            return False
        return True

    def channel_add(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        channel_name = channel_name.lower()
        if channel_name in self._preferences["channels"]:
            return ChannelErrorState.CHANNEL_ALREADY_EXISTS
        self._preferences["channels"].append(channel_name)

    def channel_remove(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        channel_name = channel_name.lower()
        if channel_name not in self._preferences["channels"]:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._preferences["channels"].remove(channel_name)

    def channel_move_to_top(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        channel_name = channel_name.lower()
        if channel_name not in self._preferences["channels"]:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        self._preferences["channels"].remove(channel_name)
        self._preferences["channels"].insert(0, channel_name)

    def channel_move_up(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        channel_name = channel_name.lower()
        if channel_name not in self._preferences["channels"]:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        index = self._preferences["channels"].index(channel_name)
        if index == 0:
            return ChannelErrorState.CHANNEL_ALREADY_ON_TOP
        self._preferences["channels"].remove(channel_name)
        self._preferences["channels"].insert(index - 1, channel_name)

    def channel_move_down(self, channel_name: str) -> ChannelErrorState:
        if channel_name == "":
            return ChannelErrorState.CHANNEL_NAME_IS_EMPTY
        channel_name = channel_name.lower()
        if channel_name not in self._preferences["channels"]:
            return ChannelErrorState.CHANNEL_DOES_NOT_EXIST
        index = self._preferences["channels"].index(channel_name)
        if index == len(self._preferences["channels"]) - 1:
            return ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM
        self._preferences["channels"].remove(channel_name)
        self._preferences["channels"].insert(index + 1, channel_name)

    def load_from_file(self, path: str = "data/preferences.json") -> JsonErrorState:
        error_state = super().load_from_file(path)
        if error_state is not None:
            return error_state
        self._preferences = self._json_file
        return super().load_from_file(path)

    def save_to_file(self, path: str = "data/preferences.json") -> JsonErrorState:
        self._json_file = self._preferences
        return super().save_to_file(path)
