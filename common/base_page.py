from playwright.sync_api import Page

from common.base import Base


class BasePage(Base):
    """기존 코드와의 호환을 위한 공통 Page Object 베이스."""

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, path: str = '') -> None:
        self.page.goto(path or '/', wait_until='domcontentloaded')
