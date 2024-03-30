from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client

def perform_query(query, **kwargs):
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        
    index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v] or []
    
    client = get_client()
    individual_tags = [t for t in tags] or []
    
    results = client.multiple_queries(
        [
            {"indexName": "cfe_Product", "query": query, 'tagFilters':[tags, individual_tags], 'facetFilters': index_filters},
            {"indexName": "cfe_Article", "query": query, 'tagFilters':[tags, individual_tags], 'facetFilters': index_filters},
        ]
    )
    return results

#old plus new mix-> refer https://github.com/codingforentrepreneurs/Django-Rest-Framework-Tutorial/blob/35-start/backend/products/index.py
# def perform_query(query, **kwargs):
#     # index = get_index()
#     params = {}
#     tags = ""
#     if "tags" in kwargs:
#         tags = kwargs.pop("tags") or []
#         if len(tags) != 0:
#             params["tagFilters"] = tags
#     index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v] or []
#     if len(index_filters) != 0:
#         params["facetFilters"] = index_filters
#     client = get_client()
#     individual_tags = [t for t in tags] or []
#     print("params: ", params)
    
#     results = client.multiple_queries(
#         [
#             {"indexName": "cfe_Product", "query": query, 'tagFilters':[tags, individual_tags], 'facetFilters': index_filters},
#             {"indexName": "cfe_Article", "query": query, 'tagFilters':[tags, individual_tags]},
#         ]
#     )
#     return results
