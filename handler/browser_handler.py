import os.path

import playwright.async_api
from playwright.sync_api import sync_playwright

from misc.random_sleep import RandomSleep


class BrowserHandler:

    def __init__(self):
        self._cookie_data = None
        self._cookie_url = None
        self._browser = None
        self._page_list = []
        self._playwright = None
        self._tab_index_current = 0
        self._context = None

    @property
    def browser(self):
        return self._browser

    @property
    def tab_index_max(self):
        return len(self._page_list) - 1

    @property
    def tab_index_current(self):
        return self._tab_index_current

    def browser_import_cookies(self, cookie_data: dict, url: str) -> bool:
        try:
            self._context.add_cookies(cookie_data)
            return True
        except Exception:
            return False

    def _is_no_audio_pref_in_playwright_cfg(self) -> bool:
        browser_path = self._playwright.firefox.executable_path
        dir_path = os.path.dirname(browser_path)
        cfg_path = os.path.join(dir_path, "playwright.cfg")
        home_path = os.path.expanduser('~')
        modified_string = cfg_path.replace("/root", home_path)
        print(modified_string)
        with open(modified_string, "r") as file:
            lines = file.readlines()
            for line in lines:
                if 'pref("media.volume_scale", "0.0")' in line:
                    return True
        return False

    def _set_no_audio_pref_in_playwright_cfg(self):
        browser_path = self._playwright.firefox.executable_path
        dir_path = os.path.dirname(browser_path)
        cfg_path = os.path.join(dir_path, "playwright.cfg")
        home_path = os.path.expanduser('~')
        modified_string = cfg_path.replace("/root", home_path)
        print(modified_string)
        with open(modified_string, "a") as file:
            file.write('\n// Force Firefox volume to 0'
                       '\npref("media.volume_scale", "0.0");')

    def browser_start(self, headless: bool = True) -> bool:
        if self._browser is None:
            self._playwright = sync_playwright().start()
            if not self._is_no_audio_pref_in_playwright_cfg():
                print('           *adding pref("media.volume_scale", "0.0") to playwright.cfg')
                self._set_no_audio_pref_in_playwright_cfg()
            self._browser = self._playwright.firefox.launch(headless=headless)
            self._context = self._browser.new_context()
            return True
        return False

    def browser_close(self) -> bool:
        if self._browser is not None:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None
            return True
        return False

    def browser_open_new_tab(self) -> bool:
        self._page_list.append(self._context.new_page())
        return self.browser_switch_to_tab(self.tab_index_max)

    def browser_close_tab(self, tab_index: int) -> bool:
        if 0 <= tab_index < self.tab_index_max:
            self._page_list[tab_index].close()
            del self._page_list[tab_index]
            return True
        if tab_index == -1:
            current_index = self._tab_index_current
            self._page_list[current_index].close()
            del self._page_list[current_index]
            return True
        return False

    def browser_switch_to_tab(self, tab_index: int) -> bool:
        if 0 <= tab_index <= self.tab_index_max:
            self._tab_index_current = tab_index
            self._page_list[tab_index].bring_to_front()
            return True
        return False

    def browser_goto_page(self, url: str) -> None:
        page = self._page_list[self._tab_index_current]
        page.goto(url)

    def element_is_present(self, xpath: str, timeout: float = 5) -> playwright.async_api.ElementHandle:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, timeout=timeout * 1000)
            return element
        except playwright.sync_api.TimeoutError:
            pass

    def element_is_invisible_present(self, xpath: str, timeout: float = 5) -> playwright.async_api.ElementHandle:
        try:
            page = self._page_list[self._tab_index_current]
            return page.query_selector(xpath, timeout=timeout * 1000)
        except Exception:
            pass

    def element_is_enabled(self, xpath: str, timeout: float = 5) -> bool:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, state="attached", timeout=timeout * 1000)
            return element.is_enabled()
        except playwright.sync_api.TimeoutError:
            pass

    def element_click(self, xpath: str, timeout: float = 5) -> bool:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, timeout=timeout * 1000)
            element.click()
            RandomSleep.sleep(4, 3)
            return True
        except playwright.sync_api.TimeoutError:
            pass

    def element_force_click(self, xpath: str, timeout: float = 5) -> bool:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, timeout=timeout * 1000)
            page.evaluate('(element) => element.click()', element)
            RandomSleep.sleep(4, 3)
            return True
        except playwright.sync_api.TimeoutError:
            pass

    def element_get_name(self, xpath: str, attribute: str = 'class', timeout: float = 5) -> str:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, timeout=timeout * 1000)
            return element.get_attribute(attribute)
        except playwright.sync_api.TimeoutError:
            pass

    def element_get_text(self, xpath: str, timeout: float = 5) -> str:
        try:
            page = self._page_list[self._tab_index_current]
            element = page.wait_for_selector(xpath, timeout=timeout * 1000)
            return element.text_content()
        except playwright.sync_api.TimeoutError:
            pass

    def elements_is_any_present(self, xpath: str):
        page = self._page_list[self._tab_index_current]
        script = "return document.evaluate('" + xpath.replace("'", "\\'") + "', document, null, XPathResult.ANY_TYPE," \
                                                                            " null).iterateNext() !== null;"
        try:
            page.evaluate(script)
        except Exception:
            pass

    def elements_click_all(self, xpath: str):
        page = self._page_list[self._tab_index_current]
        script = "var buttons = document.evaluate('" + xpath.replace("'", "\\'") + "', document, null, " + \
                 "XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);for (var i = 0; i < buttons.snapshotLength; i++)" + \
                 " { buttons.snapshotItem(i).click(); }"
        try:
            page.evaluate(script)
        except Exception:
            pass
