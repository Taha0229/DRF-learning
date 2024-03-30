import requests

data = {
    "title": "testing update 2",
    "content": "updating the title, content and price",
    "price": 99.99,
}
endpoint = "http://localhost:8000/api/products/1/update/"

get_response = requests.put(endpoint, json=data)

print(get_response.json())


