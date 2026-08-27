Feature: 홈 팝업

  @popup @smoke
  Scenario: 오늘 안 보기 선택 시 팝업 숨김 날짜 저장
    Then 홈 팝업 이미지가 표시된다
    When [오늘 안 보기] 버튼을 클릭한다
    Then 오늘 날짜가 Local Storage에 저장된다

  @popup @smoke
  Scenario: 영어 선택 시 영어 홈 팝업 표시
    When 홈 팝업 [닫기] 버튼을 클릭한다
    When 언어 선택 버튼을 클릭한다
    When [English] 언어를 선택한다
    Then 영어 홈 팝업 이미지가 표시된다
