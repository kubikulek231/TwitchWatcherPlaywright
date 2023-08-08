from ui.ui_handler_main import UICleaner, UIHandlerMain


class UIHandlerUserInput:
    def __init__(self):
        pass

    @staticmethod
    def clear_and_show_logo():
        UICleaner.clear_console()
        UIHandlerMain.show_logo()

    @staticmethod
    def channel_input_menu(channels: list, prompt: str, print_channel_bar: bool = False) -> str:
        print(prompt)
        if print_channel_bar:
            UIHandlerMain.print_channel_bar(channels)
        while True:
            channel = UIHandlerUserInput._input_channel()
            if channel is None:
                break
            print("")
            return channel

    @staticmethod
    def channel_add_result(success) -> None:
        print(" Channel added successfully.\n" if success is None else " Channel already exists.\n")

    @staticmethod
    def channel_remove_result(success) -> None:
        print(" Channel removed successfully.\n" if success is None else " Channel does not exist.\n")

    @staticmethod
    def channel_move_not_exist() -> None:
        print(" Channel does not exist.\n")

    @staticmethod
    def channel_move_already_on(top: bool) -> None:
        direction = "top" if top else "bottom"
        print(f" Channel already on {direction}.\n")

    @staticmethod
    def channel_move_success(up: bool, channels: list = None) -> None:
        if channels:
            UIHandlerMain.print_channel_bar(channels)
        direction = "up" if up else "down"
        print(f" \nChannel successfully moved {direction}.\n")

    @staticmethod
    def save_preferences_result(success, end: str = "") -> None:
        print((" Preferences saved successfully." if success is None else " Could not save preferences.") + end)

    @staticmethod
    def save_cookies_result(success, end: str = "") -> None:
        print((" Cookies saved successfully." if success is None else " Could not save cookies.") + end)

    @staticmethod
    def _input_channel() -> str:
        print("")
        print(" Enter '_' to return.")
        while True:
            try:
                channel = input(" Enter channel name: ")
                if channel == '_':
                    break
                if channel == "":
                    print(" Channel name cannot be empty.")
                    continue
                return channel
            except ValueError:
                print(" Invalid channel. Try again.")

    @staticmethod
    def input_cookie_json_file() -> str:
        UIHandlerUserInput.clear_and_show_logo()
        print(" - Load cookies from clipboard menu")
        print("    Enter '_' to return.")
        while True:
            try:
                print("    Pasted JSON must have the compact format.")
                print("    Use online formatter like https://jsonformatter.curiousconcept.com/")
                cookie_file = input("    Paste cookie JSON from clipboard: ")
                print("")
                if cookie_file == '_':
                    break
                if cookie_file == "":
                    print("    Cookie JSON cannot be empty.")
                    continue
                return cookie_file
            except ValueError:
                print("    Invalid cookie JSON. Try again.")

    @staticmethod
    def load_cookies_result(success) -> None:
        print("    Cookies loaded successfully.\n" if success is None else "    Could not load cookies.\n")
        input("    Press any key to return to menu...") if success is None else input("    Press any key and again...")
