from pytest_bdd import scenario


@scenario('../features/home_search.feature', '맛집 검색 결과 노출')
def test_search_restaurant_from_home():
    pass

