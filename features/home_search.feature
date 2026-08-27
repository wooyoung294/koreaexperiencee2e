Feature: 홈 검색

  @smoke
  Scenario: 맛집 검색 결과 노출
    When 홈 검색창에 "맛집"을 입력한다
    When 홈 검색 버튼을 클릭한다
    Then "서울에서 꼭 가봐야 할 한국식 BBQ 맛집 (현지인들이 실제로 가는 곳)" 검색 결과가 표시된다

