import os
import re

from playwright.sync_api import Locator, Page

from common.base import Base


class LoginPage(Base):
    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def email_input(self) -> Locator:
        return self.page.get_by_placeholder('이메일', exact=True)

    @property
    def password_input(self) -> Locator:
        return self.page.get_by_placeholder('비밀번호', exact=True)

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role(
            'button',
            name='로그인 / 회원가입',
            exact=True,
        )

    def fill_credentials_from_env(self) -> None:
        login_id = os.getenv('ID')
        password = os.getenv('PASSWORD')
        if not login_id or not password:
            raise RuntimeError('ID와 PASSWORD 환경변수가 필요합니다.')

        self.expect_visible(self.email_input)
        self.fill(self.email_input, login_id)
        self.fill(self.password_input, password)

    def submit_login(self) -> None:
        self.expect_enabled(self.login_button)
        self.click(self.login_button)
        self.page.wait_for_url(
            re.compile(r'^https://koreaexperience\.kr/ko(?:[?#].*)?$'),
            timeout=30_000,
        )
