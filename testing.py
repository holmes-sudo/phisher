import requests
response = requests.get("http://localhost:3000/users")  # Your local API
print(response.json())  # Your server's response