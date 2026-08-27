import allure
from playwright.sync_api import Page
from pytest_bdd import then, when

from pages.home_popup_page import HomePopupPage


def _verify_and_attach_popup_image(
    page: Page,
    image_src: str,
    attachment_name: str,
) -> None:
    image = HomePopupPage(page).verify_popup_image_is_displayed(image_src)
    allure.attach(
        image.screenshot(),
        name=attachment_name,
        attachment_type=allure.attachment_type.PNG,
    )


@then('홈 팝업 이미지가 표시된다')
@allure.step('홈 팝업 이미지 표시 확인')
def verify_home_popup_image(web_function_driver: Page):
    _verify_and_attach_popup_image(
        web_function_driver,
        HomePopupPage.KOREAN_POPUP_IMAGE_SRC,
        'Korean home popup image',
    )


@when('홈 팝업 [닫기] 버튼을 클릭한다')
@allure.step('홈 팝업 [닫기] 버튼 클릭')
def close_home_popup(web_function_driver: Page):
    HomePopupPage(web_function_driver).close_popup()


@when('[오늘 안 보기] 버튼을 클릭한다')
@allure.step('[오늘 안 보기] 버튼 클릭')
def click_dismiss_today(web_function_driver: Page):
    HomePopupPage(web_function_driver).click_dismiss_today()


@then('오늘 날짜가 Local Storage에 저장된다')
@allure.step('Local Storage에 오늘 날짜 저장 확인')
def verify_dismissed_date(web_function_driver: Page):
    popup = HomePopupPage(web_function_driver)
    saved_date = popup.verify_dismissed_date_is_today()
    allure.attach(
        f'{popup.DISMISSED_STORAGE_KEY}={saved_date}',
        name='Local Storage',
        attachment_type=allure.attachment_type.TEXT,
    )


@then('영어 홈 팝업 이미지가 표시된다')
@allure.step('영어 홈 팝업 이미지 표시 확인')
def verify_english_home_popup_image(web_function_driver: Page):
    _verify_and_attach_popup_image(
        web_function_driver,
        HomePopupPage.ENGLISH_POPUP_IMAGE_SRC,
        'English home popup image',
    )
