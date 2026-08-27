from pytest_bdd import scenario


@scenario('../features/home_popup.feature', '오늘 안 보기 선택 시 팝업 숨김 날짜 저장')
def test_dismiss_home_popup_for_today():
    pass


@scenario('../features/home_popup.feature', '영어 선택 시 영어 홈 팝업 표시')
def test_show_english_home_popup_after_language_change():
    pass
