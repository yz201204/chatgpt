import openai
from config.api_key import api_key

openai.api_key = api_key

model_engine = "text-davinci-003"
prompt = "接口模式和网页的chatGPT都有啥区别"
completions = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=2048,
    n=1,
    stop=None,
    temperature=0.5
)

# 获取回复
message = completions.choices[0].text
print(message)
