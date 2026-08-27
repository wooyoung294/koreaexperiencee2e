from playwright.sync_api import Page

from common.action_base import ActionBase
from common.expect_base import ExpectBase


class Base(ActionBase, ExpectBase):
    def __init__(self, page: Page):
        self.page = page

    def get_context_info(self) -> str:
        return self.page.url

