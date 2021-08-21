import requests
from pprint import pprint as p
import json

user_agent_value = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

url = 'https://api.github.com/user'

token = ""

headers = {
    "User-Agent": user_agent_value,
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f'token {token}'
}

response = requests.get(url, headers=headers)

json_res = response.json()

p(json_res)

with open('auth.json', 'w') as file:
    json.dump(json_res, file)
