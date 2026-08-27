from playwright.sync_api import Locator, Page

from common.base import Base


class Header(Base):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def language_select_button(self) -> Locator:
        return self.page.get_by_role('button', name='언어', exact=True)

    @property
    def english_option(self) -> Locator:
        return self.page.get_by_role('option', name='English', exact=True)

    @property
    def login_link(self) -> Locator:
        return self.page.get_by_role('link', name='로그인 / 회원가입', exact=True)

    @property
    def notifications_button(self) -> Locator:
        return self.page.get_by_role('button', name='Notifications', exact=True)

    def open_language_select(self) -> None:
        self.expect_visible(self.language_select_button)
        self.click(self.language_select_button)
        self.expect_visible(self.english_option)

    def select_english(self) -> None:
        self.expect_visible(self.english_option)
        self.click(self.english_option)
        self.page.wait_for_url('**/en', timeout=15_000)

    def open_login_page(self) -> None:
        self.expect_visible(self.login_link)
        self.click(self.login_link)
        self.page.wait_for_url('**/ko/login', timeout=15_000)

    def verify_logged_in(self) -> None:
        self.expect_visible(self.notifications_button, timeout=20_000)
        self.expect_not_visible(self.login_link)
