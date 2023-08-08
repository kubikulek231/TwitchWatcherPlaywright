from handler.json_handler import JsonFileHandler, JsonErrorState


class CookieHandler(JsonFileHandler):
    def __init__(self):
        super().__init__()
        self._cookie_data = None

    @property
    def cookie_data(self):
        return self._cookie_data

    def _repair_cookie_data(self) -> bool:
        if self._cookie_data is None:
            return False
        for cookie in self._cookie_data:
            if "unspecified" in cookie["sameSite"] or "no_restriction" in cookie["sameSite"]:
                cookie["sameSite"] = "None"
        return True

    def load_from_file(self, path: str = "data/cookies.json") -> JsonErrorState:
        error_state = super().load_from_file(path)
        if error_state is not None:
            return error_state
        self._cookie_data = self._json_file
        self._repair_cookie_data()

    def load_from_string(self, string: str) -> JsonErrorState:
        error_state = super().load_from_string(string)
        if error_state is not None:
            return error_state
        self._cookie_data = self._json_file
        self._repair_cookie_data()

    def save_to_file(self, path: str = "data/cookies.json") -> JsonErrorState:
        return super().save_to_file(path)
