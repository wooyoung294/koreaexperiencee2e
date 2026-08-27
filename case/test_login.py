from pytest_bdd import scenario


@scenario('../features/login.feature', '이메일 계정 로그인')
def test_login_with_email_account():
    pass
