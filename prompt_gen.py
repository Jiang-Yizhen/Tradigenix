import pandas as pd
import os
from openai import OpenAI

nv_prompt_file = pd.read_excel('汉服-女词库.xlsx')
na_prompt_file = pd.read_excel('汉服-男词库.xlsx')
nv_prompt = nv_prompt_file.to_string(index=False)
na_prompt = na_prompt_file.to_string(index=False)

os.environ["OPENAI_API_KEY"] = "sk-HGnXvbVEeSkolzhm3423741621A54f39A3225247AcEcD338"
os.environ["OPENAI_BASE_URL"] = "http://15.204.101.64:4000/v1"


def prompt_gen(advise, gender):
    prompt = nv_prompt
    trigger = "a Hanfu"
    if gender == "男":
        prompt = na_prompt
        trigger = "A Hanfu"
    elif gender == "女":
        prompt = nv_prompt
        trigger = "a Hanfu"

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.",},
            {"role": "user",
             "content": advise + "根据上述建议，从以下prompt库中的触发词、种类、上衣、裙子、领子、袖子、袖口、腰饰、裙子详述中每个挑选一个词，分点描述，触发"
                                 "词固定选择为" + trigger + "，然后在最下面列出所有Prompt，以‘Begin’为开头后换行, 输出所有英文描述，用逗"
                                 "号间隔，再加上‘, white background’, 再然后换行后以'End'结尾。prompt库如下：" + prompt,
             }
        ]

    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
