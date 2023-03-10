import openai
from config.api_key import api_key

openai.api_key = api_key


class ChatGPT:
    def chat(self, prompt, model_engine="text-davinci-003"):
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5
        )
        message = completions.choices[0].text
        return message.strip()


if __name__ == '__main__':
    c = ChatGPT()
    print(c.chat("什么网站"))
