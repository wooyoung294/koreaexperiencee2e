Feature: 로그인

  @login @smoke
  Scenario: 이메일 계정 로그인
    Given 로그인 페이지로 이동한다
    When 이메일 계정 정보를 입력한다
    When [로그인 / 회원가입] 버튼을 클릭한다
    Then 로그인 상태가 표시된다
