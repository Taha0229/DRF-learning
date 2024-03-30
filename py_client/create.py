import requests

data = {
    "title": "Single view using generic view api and mixins",
    # "content": "damnn this is soo coolll",
    "price": 55.99
}
endpoint = "http://localhost:8000/api/products/"

get_response = requests.post(endpoint, json=data)

print(get_response.json())
# print(get_response.status_code)

