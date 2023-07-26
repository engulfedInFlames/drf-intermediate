import requests
from pprint import pprint
from getpass import getpass

auth_endpoint = "http://127.0.0.1:8000/api/auth/"
username = input("Enter your username: ")
password = getpass("Enter your password: ")


auth_reponse = requests.post(
    auth_endpoint,
    json={
        "username": "staff1",
        "password": password,
    },
)

if auth_reponse.status_code == 200:
    token = auth_reponse.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    endpoint = "http://127.0.0.1:8000/api/products"
    response = requests.get(
        endpoint,
        headers=headers,
    )
    pprint(response.json())
