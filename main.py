import os

import openai
from config.api_key import api_key

openai.api_key = "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"

os.environ["HTTP_PROXY"] = "119.45.177.140:7890"
os.environ["HTTPS_PROXY"] = "119.45.177.140:7890"
model = "gpt-3.5-turbo"
message = [
        {"role": "system", "content": "你是一个AI机器人助手。"}
    ]
print("你好，欢迎使用chatGPT")
while True:
    user_message = input(">>")
    if user_message.strip() == "结束":
        break
    message.append({"role": "user", "content": user_message.strip()})
    response = openai.ChatCompletion.create(
        model=model,
        messages=message
    )
    result = ""
    for choice in response.choices:
        result += choice.message.content
    print(result)
    message.append({"role": "assistant", "content": result.strip()})

