Feature: K-Perks 상세

  @smoke
  Scenario: 제천국제음악영화제 상세 정보 노출
    When 홈 K-Perks의 제천국제음악영화제 이미지를 클릭한다
    Then 제천국제음악영화제 제목과 소개가 표시된다
    Then 제천국제음악영화제 프로그램 정보가 표시된다
    Then 제천국제음악영화제 지역과 상태와 기간이 표시된다
