from misc.random_sleep import RandomSleep


class TwitchHandler:
    def __init__(self, browser_handler):
        self._browser_handler = browser_handler

    def twitch_login_page_open(self) -> bool:
        self._browser_handler.browser_goto_page("https://www.twitch.tv/login")
        if self._browser_handler.element_is_present('//*[@id="login-username"]'):
            return True
        return False

    def twitch_is_logged(self) -> bool:
        element_name = self._browser_handler.element_get_name("body")
        if element_name is None or "logged-in" not in element_name:
            return False
        return True

    def twitch_stream_player_open(self, channel):
        self._browser_handler.browser_goto_page(
            f"https://player.twitch.tv/?channel={channel}&enableExtensions=true&muted=true&"
            f"parent=twitch.tv&player=popout&quality=160p30&volume=0.69")

    def twitch_stream_player_confirm_warning(self) -> bool:
        return self._browser_handler.element_click('//*[@id="channel-player-gate"]/div/div/div[4]/div/button')

    def twitch_stream_player_unmute(self) -> bool:
        RandomSleep.sleep(2, 3)
        volume_slider_element_xpath = '//input[@class="ScRangeInput-sc-q01wc3-0 ePJIVh tw-range"]'
        volume_slider_element = self._browser_handler.element_is_present(volume_slider_element_xpath)
        if volume_slider_element is None:
            return False
        if volume_slider_element.get_attribute('aria-valuenow') == '0':
            return self._browser_handler.element_click('//*[@id="channel-player"]/div/div[1]/div[2]/div/div[1]/button')
        return False

    def twitch_stream_player_get_game(self) -> str:
        stream_game_xpath = '//a[@data-a-target="player-info-game-name"]'
        return self._browser_handler.element_get_text(stream_game_xpath)

    def twitch_stream_player_get_title(self) -> str:
        stream_game_xpath = '//p[@data-test-selector="stream-info-card-component__subtitle"]'
        return self._browser_handler.element_get_text(stream_game_xpath)

    def twitch_stream_player_get_viewers(self) -> str:
        stream_game_xpath = '//p[@data-test-selector="stream-info-card-component__description"]'
        viewer_count_string = self._browser_handler.element_get_text(stream_game_xpath)
        if viewer_count_string is not None:
            viewer_number = ""
            for char in viewer_count_string:
                if char.isdigit():
                    viewer_number += char
            return viewer_number

    def twitch_channel_is_live(self, channel: str = None) -> bool:
        if channel is not None:
            self.twitch_stream_player_open(channel)
        if self._browser_handler.element_get_name(
                '//*[@id="root"]/div/div/div/div[1]/div/div[2]/div/div/div[3]'
                '/div[2]/div[1]/div/div/div[1]/div/div[1]/div/p') is None:
            return True
        return False

    def twitch_chat_open(self, channel) -> None:
        self._browser_handler.browser_goto_page(
            f"https://www.twitch.tv/popout/{channel}/chat?popout=")

    def twitch_chat_get_points(self) -> str:
        points_value_xpath = '//span[@class="ScAnimatedNumber-sc-1iib0w9-0"]'
        points_value = self._browser_handler.element_get_text(points_value_xpath, 5)
        return points_value

    def twitch_chat_is_claimable(self) -> bool:
        RandomSleep.sleep(4, 1)
        points_button_xpath = '//button[@class="ScCoreButton-sc-ocjdkq-0 ScCoreButtonSuccess-sc-ocjdkq-5 ' \
                              'ibtYyW kIlsPe"]'
        button_element = self._browser_handler.element_is_present(points_button_xpath)
        if button_element is None:
            return False
        return True

    def twitch_chat_claim(self) -> bool:
        points_button_xpath = '//*[@id="root"]/div/div[1]/div/div/section/div/div[6]/div[2]/div[2]/div[1]' \
                              '/div/div/div/div[2]'
        return self._browser_handler.element_click(points_button_xpath)

    def twitch_drop_inventory_open(self) -> None:
        self._browser_handler.browser_goto_page(
            "https://www.twitch.tv/drops/inventory")
        RandomSleep.sleep(4, 1)

    def twitch_drop_inventory_is_claimable(self) -> bool:
        drop_button_xpath = "//button[contains(@class, 'ScCoreButton-sc-ocjdkq-0 " \
                            "ScCoreButtonPrimary-sc-ocjdkq-1 dNGoHt hdAxZi')]"
        return self._browser_handler.elements_is_any_present(drop_button_xpath)

    def twitch_drop_inventory_claim(self) -> bool:
        drop_button_xpath = "//button[contains(@class, 'ScCoreButton-sc-ocjdkq-0 " \
                            "ScCoreButtonPrimary-sc-ocjdkq-1 dNGoHt hdAxZi')]"
        return self._browser_handler.elements_click_all(drop_button_xpath)

    def twitch_drop_inventory_latest_drop_get_name(self) -> str:
        latest_drop_name_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                                 '/div[2]/div[1]/div/div[1]/div[2]/div[2]/p'
        return self._browser_handler.element_get_text(latest_drop_name_xpath)

    def twitch_drop_inventory_latest_drop_get_game(self) -> str:
        latest_drop_game_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                                 '/div[2]/div[1]/div/div[2]/p'
        return self._browser_handler.element_get_text(latest_drop_game_xpath)

    def twitch_drop_inventory_latest_drop_get_time(self) -> str:
        last_drop_date_xpath = '//*[@id="root"]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div/div/div[1]/div[4]' \
                               '/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/p'
        return self._browser_handler.element_get_text(last_drop_date_xpath)
