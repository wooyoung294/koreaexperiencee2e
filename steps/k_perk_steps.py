import allure
from playwright.sync_api import Page
from pytest_bdd import then, when

from pages.home_page import HomePage
from pages.k_perk_detail_page import KPerkDetailPage


@when('홈 K-Perks의 제천국제음악영화제 이미지를 클릭한다')
@allure.step('홈 K-Perks 제천국제음악영화제 이미지 클릭')
def open_jecheon_film_festival(web_function_driver: Page):
    HomePage(web_function_driver).open_jecheon_film_festival()


@then('제천국제음악영화제 제목과 소개가 표시된다')
@allure.step('제천국제음악영화제 제목 및 소개 표시 확인')
def verify_jecheon_film_festival_overview(web_function_driver: Page):
    KPerkDetailPage(web_function_driver).verify_overview()


@then('제천국제음악영화제 프로그램 정보가 표시된다')
@allure.step('제천국제음악영화제 프로그램 정보 표시 확인')
def verify_jecheon_film_festival_program_details(web_function_driver: Page):
    KPerkDetailPage(web_function_driver).verify_program_details()


@then('제천국제음악영화제 지역과 상태와 기간이 표시된다')
@allure.step('제천국제음악영화제 지역, 상태, 기간 표시 확인')
def verify_jecheon_film_festival_metadata(web_function_driver: Page):
    KPerkDetailPage(web_function_driver).verify_metadata()
