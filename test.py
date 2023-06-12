import openai
import requests
import os

response = requests.get("http://106.52.209.141:17000/buyer/member/evaluation/0555667502/goodsEvaluation?pageNumber=1&pageSize=10&grade=&goodsId=0555667502")
result = []
records = response.json()["result"]["records"]
for review in records:
    result.append(review["content"])
print(result)