from suggestion import generate_outfit_advice
from clothGen import pro_gen
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "sk-vtyR3fdgk08jmJ5e3eF6F5Ef663c4a3bAd0166C3549a1a8e"
os.environ["OPENAI_BASE_URL"] = "http://15.204.101.64:4000/v1"


def suggest_gene(user_name, height, weight, waist, chest, hip, shoulder_width, leg_length, arm_length, gender,
                 body_type, skin_color, style_preference, lifestyle_requirements, special_requirements,
                 feedback, user_pic):
    analyse = generate_outfit_advice(user_name, height, weight, waist, chest, hip, shoulder_width, leg_length,
                                     arm_length, gender, body_type, skin_color, style_preference,
                                     lifestyle_requirements, special_requirements, feedback, user_pic)
    prompts = ""
    for i in range(1, 4):
        prompts += pro_gen(analyse, gender, i)

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.", },
            {"role": "user",
             "content": "你是一位专业的民族服饰搭配大师，你需要充分了解中华民族的所有民族服饰的相关知识，包括不同民族服饰适合什么样的人群等。"
                        "以下是用户分析与三段提示词，请据此给出穿搭建议，要求以三段提示词为主要建议参考" + analyse + prompts,
             }
        ]

    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
