from playwright.sync_api import Locator, Page

from common.base import Base


class HomePage(Base):
    SEARCH_PROMPT = '한국에서 무엇을 하고 싶으신가요?'
    JECHEON_FILM_FESTIVAL_TITLE = '제22회 제천국제음악영화제'
    JECHEON_FILM_FESTIVAL_PATH = '/ko/k-perks/1046'

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def search_input(self) -> Locator:
        return self.page.get_by_role(
            'searchbox',
            name=self.SEARCH_PROMPT,
            exact=True,
        )

    @property
    def search_form(self) -> Locator:
        return self.page.locator('form').filter(has=self.search_input)

    @property
    def search_button(self) -> Locator:
        return self.search_form.get_by_role(
            'button',
            name=self.SEARCH_PROMPT,
            exact=True,
        )

    @property
    def k_perks_section(self) -> Locator:
        return self.page.get_by_role('region', name='K-Perks', exact=True)

    @property
    def jecheon_film_festival_card(self) -> Locator:
        return self.k_perks_section.locator(
            f'a[href="{self.JECHEON_FILM_FESTIVAL_PATH}"]'
        )

    @property
    def jecheon_film_festival_image(self) -> Locator:
        return self.jecheon_film_festival_card.get_by_role(
            'img',
            name=self.JECHEON_FILM_FESTIVAL_TITLE,
            exact=True,
        )

    def fill_search_keyword(self, keyword: str) -> None:
        self.expect_visible(self.search_input)
        self.fill(self.search_input, keyword)
        self.expect_value(self.search_input, keyword)

    def click_search_button(self) -> None:
        self.expect_enabled(self.search_button)
        self.click(self.search_button)
        self.page.wait_for_url('**/search?q=*', timeout=15_000)

    def verify_search_result_is_displayed(self, title: str) -> None:
        result_heading = self.page.get_by_role('heading', name=title, exact=True)
        self.expect_visible(result_heading, timeout=20_000)

    def open_jecheon_film_festival(self) -> None:
        self.expect_visible(self.jecheon_film_festival_image, timeout=15_000)
        self.click(self.jecheon_film_festival_image)
        self.page.wait_for_url(
            f'**{self.JECHEON_FILM_FESTIVAL_PATH}',
            timeout=15_000,
        )
