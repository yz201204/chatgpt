import openai
from config.api_key import api_key
import os

openai.api_key = api_key
os.environ["HTTP_PROXY"] = "119.45.177.140:7890"
os.environ["HTTPS_PROXY"] = "119.45.177.140:7890"


class ChatGPT:
    def __init__(self):
        self.message = [
            {"role": "system", "content": "你是一个AI机器人助手。"}
        ]
        os.environ["HTTP_PROXY"] = "119.45.177.140:7890"
        os.environ["HTTPS_PROXY"] = "119.45.177.140:7890"

    def chat(self, user="", model="gpt-3.5-turbo"):
        while True:
            if user.strip() == "结束":
                break
            self.message.append({"role": "user", "content": user.strip()})
            response = openai.ChatCompletion.create(
                model=model,
                messages=self.message
            )
            result = ""
            for choice in response.choices:
                result += choice.message.content
            print(result)
            self.message.append({"role": "assistant", "content": result.strip()})
            return result


if __name__ == '__main__':
    c = ChatGPT()
    os.environ["HTTP_PROXY"] = "119.45.177.140:7890"
    os.environ["HTTPS_PROXY"] = "119.45.177.140:7890"
    print(c.chat("chatGPT接口不如网页版"))
