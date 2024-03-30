import requests

endpoint = "http://localhost:8000/api/"

# get_response = requests.get(endpoint, json = {"query": "hello"})
get_response = requests.post(endpoint, params= {"abc": 123}, json={"title" : None, "content": "Test content 1 with basic.py"})

print(get_response.json())
print(get_response.status_code)

