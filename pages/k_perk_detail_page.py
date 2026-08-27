import re

from playwright.sync_api import Locator, Page

from common.base import Base


class KPerkDetailPage(Base):
    TITLE = '제22회 제천국제음악영화제'
    INTRODUCTION = (
        '아시아를 대표하는 음악영화제인 제천국제음악영화제는 영화제이자 음악제로서의 '
        '정체성을 구축해 온 다분야 문화 플랫폼으로, 영화 상영 프로그램과 라이브 공연 중심의 '
        '음악 프로그램을 결합하고 있습니다.'
    )
    PROGRAM_DESCRIPTION = (
        'JIMFF의 영화 프로그램은 음악을 핵심 주제이자 서사 장치로 다루는 국내외 주요 작품을 '
        '지속적으로 발굴·소개하는 한편, 영화 음악 작곡가와 영화음악 자체의 예술적 가치에 '
        '주목하며 프로그램의 폭을 꾸준히 넓혀가고 있습니다.'
    )

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def article(self) -> Locator:
        return self.page.get_by_role('article')

    @property
    def title(self) -> Locator:
        return self.article.get_by_role(
            'heading',
            name=self.TITLE,
            exact=True,
        ).first

    def article_text(self, value: str) -> Locator:
        return self.article.get_by_text(value, exact=True)

    def metadata_value(self, label: str) -> Locator:
        term = self.article.locator('dt').filter(
            has_text=re.compile(f'^{re.escape(label)}$'),
            visible=True,
        )
        return term.locator('..').locator('dd').filter(visible=True)

    def verify_overview(self) -> None:
        self.expect_visible(self.article, timeout=15_000)
        self.expect_text(self.title, self.TITLE)
        self.expect_text(self.article_text(self.INTRODUCTION), self.INTRODUCTION)
        self.expect_text(
            self.article_text(self.PROGRAM_DESCRIPTION),
            self.PROGRAM_DESCRIPTION,
        )

    def verify_program_details(self) -> None:
        expected_values = (
            '2026년 9월 3일 ~ 9월 8일',
            '제천예술의전당',
            '준경쟁 국제영화제',
            '음악영화',
        )
        for value in expected_values:
            locator = self.article.locator('strong').get_by_text(value, exact=True)
            self.expect_text(locator, value)

    def verify_metadata(self) -> None:
        expected_metadata = {
            '지역': '충북',
            '상태': '진행 중',
            '기간': '2026. 8. 24. – 2026. 9. 8.',
        }
        for label, value in expected_metadata.items():
            self.expect_text(self.metadata_value(label), value)
