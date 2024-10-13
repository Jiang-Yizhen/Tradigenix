# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage
import pandas as pd

nv_prompt_file = pd.read_excel('汉服-女词库.xlsx')
na_prompt_file = pd.read_excel('汉服-男词库.xlsx')
nv_prompt = nv_prompt_file.to_string(index=False)
na_prompt = na_prompt_file.to_string(index=False)
#
# #星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
# SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
# #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
# SPARKAI_APP_ID = '11ce2152'
# SPARKAI_API_SECRET = 'N2ExOTc3MDc1OWZjMTkyNzFlYjA3ZTAz'
# SPARKAI_API_KEY = '4f6313fa6c05dea06e4e18b46e63b20f'
# #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
# SPARKAI_DOMAIN = 'generalv3.5'
#
# def prompt_gen(advise):
#     spark = ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )
#     messages = [ChatMessage(
#         role="user",
#         content=advise + "\n根据建议，从触发词、种类、上衣、裙子、领子、袖子、袖口、腰饰、裙子详述中每个挑选一个词，分点描述，把英文也附在后面的括"
#                          "号里，最后下面加一条prompt，总结所有英文描述，用逗号间隔\n" + nv_prompt,
#     )]
#     print(messages[0].content)
#     handler = ChunkPrintHandler()
#     a = spark.generate([messages], callbacks=[handler])
#     print(a.generations[0][0].text)
#     return a.generations[0][0].text

import os

os.environ["OPENAI_API_KEY"] = "sk-vtyR3fdgk08jmJ5e3eF6F5Ef663c4a3bAd0166C3549a1a8e"  #输入网站发给你的转发key

os.environ["OPENAI_BASE_URL"] = "http://15.204.101.64:4000/v1"

from openai import OpenAI


def prompt_gen(advise, gender):
    if gender == "男":
        prompt = na_prompt
    else:
        prompt = nv_prompt
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.",},
            {"role": "user",
             "content": advise + "根据建议，从以下的触发词、种类、上衣、裙子、领子、袖子、袖口、腰饰、裙子详述中每个挑选一个词，分点描述，"
                                 "把英文也附在后面的括号里，最后下面加一条prompt，总结所有英文描述，用逗号间隔" + prompt,
             }
        ]

    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
