import openai
import requests
import os

openai.api_key  = os.getenv('OPENAI_API_KEY')
print(openai.api_key)

# completion = openai.ChatCompletion.create(
#     model = "gpt-3.5-turbo",
#     temperature = 0.8,
#     max_tokens = 2000,
#     messages = [
#         {"role": "system", "content": "You are a funny comedian who tells dad jokes."},
#         {"role": "user", "content": "Write a dad joke related to numbers."},
#         {"role": "assistant", "content": "Q: How do you make 7 even? A: Take away the s."},
#         {"role": "user", "content": "Write one related to programmers."},
#         {"role": "assistant", "content": "Why do programmers prefer dark mode? Because light attracts bugs."},
#         {"role": "user", "content": "Write one related to phd."},
#     ]
# )

# print(completion.choices[0].message)

URL = "https://api.openai.com/v1/chat/completions"

payload = {
    "model": "gpt-3.5-turbo",
    "temperature": 1.0,
    "messages": [
        {
            "role": "system",
            "content": f"You are an assistant who tells any random and very short fun fact about this world.",
        },
        {"role": "user", "content": f"Write a fun fact about programmers."},
        {"role": "assistant", "content": f"Programmers drink a lot of coffee!"},
        {
            "role": "user",
            "content": f"Write one related to the Python programming language.",
        },
    ],
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}",
}

response = requests.post(URL, headers=headers, json=payload)
response = response.json()

print(response["choices"][0]["message"]["content"])
