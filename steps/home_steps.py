import allure
from playwright.sync_api import Page
from pytest_bdd import parsers, then, when

from pages.home_page import HomePage


@when(parsers.parse('홈 검색창에 "{keyword}"을 입력한다'))
@allure.step('홈 검색창에 "{keyword}" 입력')
def fill_home_search_keyword(web_function_driver: Page, keyword: str):
    HomePage(web_function_driver).fill_search_keyword(keyword)


@when('홈 검색 버튼을 클릭한다')
@allure.step('홈 검색 버튼 클릭')
def click_home_search_button(web_function_driver: Page):
    HomePage(web_function_driver).click_search_button()


@then(parsers.parse('"{title}" 검색 결과가 표시된다'))
@allure.step('"{title}" 검색 결과 표시 확인')
def verify_home_search_result(web_function_driver: Page, title: str):
    HomePage(web_function_driver).verify_search_result_is_displayed(title)

