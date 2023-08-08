import sys

from handler.cookie_handler import CookieHandler
from handler.preferences_handler import PreferencesHandler, ChannelErrorState
from ui.ui_handler_main import UIHandlerMain, UICleaner
from ui.ui_handler_run import UIHandlerRun
from ui.ui_handler_user_input import UIHandlerUserInput
from watcher.watcher_data_container import WatcherInputDataContainer


class App():
    def __init__(self):
        self.preference_handler = PreferencesHandler()
        self.cookie_handler = CookieHandler()

    def _run_on_start(self):
        UIHandlerMain.show_logo()
        # do countdown
        if UIHandlerMain.run_on_start_countdown():
            # run watcher
            on_start_input_data_container = WatcherInputDataContainer(self.preference_handler.channels,
                                                                      self.cookie_handler.cookie_data)
            UIHandlerRun(on_start_input_data_container).run()

    def run(self):
        are_cookies_loaded = self.cookie_handler.load_from_file() is None
        are_preferences_loaded = self.preference_handler.load_from_file() is None

        options = self.preference_handler.options
        channels = self.preference_handler.channels
        cookies = self.cookie_handler.cookie_data

        if options.get("app_run_on_start"):
            self._run_on_start()

        ui_handler = UIHandlerMain(are_cookies_loaded, are_preferences_loaded, options, channels)

        while True:
            option = ui_handler.run()
            ui_handler.print_ui = True
            ui_handler.clear_console = True
            match option:
                case 1:
                    # run watcher
                    if channels and cookies:
                        input_data_container = WatcherInputDataContainer(channels, cookies)
                        UIHandlerRun(input_data_container).run()
                    else:
                        ui_handler.on_begin_run_fail()
                case 2:
                    # add new channel
                    prompt = " - Add new channel menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        UIHandlerUserInput.channel_add_result(self.preference_handler.channel_add(channel))
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 3:
                    # remove channel
                    prompt = " - Remove channel menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        UIHandlerUserInput.channel_remove_result(self.preference_handler.channel_remove(channel))
                    # update the main menu ui with changes
                    ui_handler.update(options, channels)
                case 4:
                    # move channel up
                    prompt = " - Move channel up menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        move_result = self.preference_handler.channel_move_up(channel)
                        if move_result is None:
                            UIHandlerUserInput.channel_move_success(True, channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_TOP:
                            UIHandlerUserInput.channel_move_already_on(True)
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            UIHandlerUserInput.channel_move_not_exist()
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 5:
                    # move channel down
                    prompt = " - Move channel down menu"
                    UIHandlerUserInput.clear_and_show_logo()
                    while True:
                        channel = UIHandlerUserInput.channel_input_menu(channels, prompt, True)
                        if channel is None:
                            break
                        move_result = self.preference_handler.channel_move_down(channel)
                        if move_result is None:
                            UIHandlerUserInput.channel_move_success(False, channels)
                        if move_result == ChannelErrorState.CHANNEL_ALREADY_ON_BOTTOM:
                            UIHandlerUserInput.channel_move_already_on(False)
                        if move_result == ChannelErrorState.CHANNEL_DOES_NOT_EXIST:
                            UIHandlerUserInput.channel_move_not_exist()
                    # update the main menu ui with changes on return
                    ui_handler.update(options, channels)
                case 6:
                    # toggle run on start
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_run_on_start",
                                                       not self.preference_handler.options.get("app_run_on_start"))
                case 7:
                    # toggle save on exit
                    UICleaner.clear_console()
                    self.preference_handler.option_set("app_save_on_exit",
                                                       not self.preference_handler.options.get("app_save_on_exit"))
                case 8:
                    # save preferences and cookies to file
                    UIHandlerUserInput.save_preferences_result(self.preference_handler.save_to_file())
                    UIHandlerUserInput.save_cookies_result(self.cookie_handler.save_to_file(), end="\n")
                    ui_handler.print_ui = False
                    ui_handler.clear_console = False
                case 9:
                    # load cookies from clipboard
                    while True:
                        cookie_file = UIHandlerUserInput.input_cookie_json_file()
                        if cookie_file is None:
                            break
                        load_result = self.cookie_handler.load_from_string(cookie_file)
                        UIHandlerUserInput.load_cookies_result(load_result)
                        if load_result is None:
                            break
                case 0:
                    # exit
                    UICleaner.clear_console()
                    UIHandlerMain.show_logo()
                    if self.preference_handler.options.get("app_save_on_exit"):
                        UIHandlerUserInput.save_preferences_result(self.preference_handler.save_to_file())
                        UIHandlerUserInput.save_cookies_result(self.cookie_handler.save_to_file(), end="\n")
                    print(" Exiting\n")
                    sys.exit(0)
                case _:
                    print(" Invalid option. Try again.")
