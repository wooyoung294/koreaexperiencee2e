import allure
from playwright.sync_api import Page
from pytest_bdd import given, then, when

from components.header import Header
from pages.login_page import LoginPage


@given('로그인 페이지로 이동한다')
@allure.step('로그인 페이지 이동')
def open_login_page(web_function_driver: Page):
    Header(web_function_driver).open_login_page()


@when('이메일 계정 정보를 입력한다')
@allure.step('이메일 계정 정보 입력')
def fill_login_credentials(web_function_driver: Page):
    LoginPage(web_function_driver).fill_credentials_from_env()


@when('[로그인 / 회원가입] 버튼을 클릭한다')
@allure.step('[로그인 / 회원가입] 버튼 클릭')
def submit_login(web_function_driver: Page):
    LoginPage(web_function_driver).submit_login()


@then('로그인 상태가 표시된다')
@allure.step('로그인 성공 상태 확인')
def verify_logged_in(web_function_driver: Page):
    Header(web_function_driver).verify_logged_in()
