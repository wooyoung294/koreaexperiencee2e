from typing import TYPE_CHECKING

from playwright.sync_api import Locator

if TYPE_CHECKING:
    from playwright.sync_api import Page


class ActionBase:
    page: 'Page'

    def click(self, target: str | Locator) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        locator.click()

    def fill(self, target: str | Locator, value: str) -> None:
        locator = target if isinstance(target, Locator) else self.page.locator(target)
        locator.fill(value)
