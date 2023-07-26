from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name="alpha_Product"):
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(query, **kwargs):
    """
    perform_search("Hello World!", tags="lang", public=True)
    """
    index = get_index()
    params = {}
    tags = ""
    # 태그명과 함께 검색 가능
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags):
            params["tagFilters"] = tags
    # 추가 조건을 설정
    index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v]
    if len(index_filters):
        params["facetFilters"] = index_filters
    result = index.search(query, params)

    return result
