import requests
from pprint import pprint
import json

user_agent_value = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

url = 'https://api.github.com/users/Aden-Kurmanov/repos'

headers = {
    "User-Agent": user_agent_value,
    "Accept": "application/vnd.github.v3+json",
}

response = requests.get(url, headers=headers)

json_res = response.json()

pprint(json_res)

print()

lst = list()

for it in json_res:
    lst.append(it.get("full_name"))

print("lst: ", lst)

with open("repos.json", 'w') as file:
    json.dump(lst, file)
