import requests

product_id = input("Enter a product id that you wish to delete\n")

try:
    product_id = int(product_id)
except:
    entered_id = product_id
    product_id = None
    print(f"{entered_id} is not a valid id")
    
if product_id:
    endpoint = f"http://localhost:8000/api/products/{product_id}/delete/"


get_response = requests.delete(endpoint)

print(get_response.status_code, get_response.status_code==204) #printing the status code and asserting to 204


