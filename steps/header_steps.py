import allure
from playwright.sync_api import Page
from pytest_bdd import when

from components.header import Header


@when('언어 선택 버튼을 클릭한다')
@allure.step('언어 선택 버튼 클릭')
def open_language_select(web_function_driver: Page):
    Header(web_function_driver).open_language_select()


@when('[English] 언어를 선택한다')
@allure.step('[English] 언어 선택')
def select_english(web_function_driver: Page):
    Header(web_function_driver).select_english()

