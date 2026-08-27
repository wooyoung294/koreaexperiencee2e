from playwright.sync_api import Locator, Page

from common.base import Base


class HomePopupPage(Base):
    KOREAN_POPUP_IMAGE_SRC = '/kx/popup/1_Korean.png'
    ENGLISH_POPUP_IMAGE_SRC = '/kx/popup/2_English.png'
    DISMISSED_STORAGE_KEY = 'home-popup-dismissed'

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def root(self) -> Locator:
        return self.page.get_by_role('dialog')

    @property
    def dismiss_today_button(self) -> Locator:
        return self.root.get_by_role('button', name='오늘 안 보기', exact=True)

    @property
    def close_button(self) -> Locator:
        return self.root.get_by_role('button', name='닫기', exact=True)

    def verify_popup_image_is_displayed(self, image_src: str) -> Locator:
        self.expect_visible(self.root, timeout=15_000)
        return self.expect_image_loaded(image_src, scope=self.root)

    def close_popup(self) -> None:
        self.expect_visible(self.close_button, timeout=15_000)
        self.click(self.close_button)

    def click_dismiss_today(self) -> None:
        self.expect_visible(self.dismiss_today_button, timeout=15_000)
        self.click(self.dismiss_today_button)
        self.page.wait_for_function(
            '(key) => window.localStorage.getItem(key) !== null',
            arg=self.DISMISSED_STORAGE_KEY,
        )

    def dismissed_storage_value(self) -> str | None:
        return self.page.evaluate(
            '(key) => window.localStorage.getItem(key)',
            self.DISMISSED_STORAGE_KEY,
        )

    def browser_today(self) -> str:
        return self.page.evaluate(
            "() => new Date().toISOString().slice(0, 10)"
        )

    def verify_dismissed_date_is_today(self) -> str:
        actual = self.dismissed_storage_value()
        expected = self.browser_today()
        assert actual == expected, (
            f'Local Storage 값 불일치: '
            f'{self.DISMISSED_STORAGE_KEY}={actual!r}, expected={expected!r}'
        )
        return actual
