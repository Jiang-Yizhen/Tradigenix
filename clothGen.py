import fal_client
import pandas as pd
from prompt_gen import prompt_gen
import requests
import os
from openai import OpenAI
import random
import shutil
from pathlib import Path
from PIL import Image

nv_prompt_file = pd.read_excel('汉服-女词库.xlsx')
na_prompt_file = pd.read_excel('汉服-男词库.xlsx')
nv_prompt = nv_prompt_file.to_string(index=False)
na_prompt = na_prompt_file.to_string(index=False)
save_directory = "downloads"
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_BASE_URL"] = "http://15.204.101.64:4000/v1"


def prompt_nan(prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.", },
            {"role": "user",
             "content": "Please showcase the overall appearance of this Hanfu robe against a contrasting white  "
                        "background. Highlight its intricate details and unique design elements, including" + prompt,
             }
        ]

    )
    print("change prompt: ")
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def pro_gen(advice, gender, index):
    prompt = prompt_gen(advice, gender)
    start_index = prompt.find("Begin")
    if start_index == -1:
        start_index = prompt.find("begin")
    prompt__gen = ""
    if start_index != -1:
        start_index += len("Begin\n")
        end_index = prompt.find("End")
        if end_index != -1:
            prompt__gen = prompt[start_index:end_index]
            # if gender == "男":
            #     prompt__gen = prompt_nan(prompt__gen)
            filename = os.path.join(save_directory, f"prompt_{index}.txt")
            with open(filename, "w") as file:
                file.write(prompt__gen)
            # print(prompt__gen)
        else:
            print("No 'promptEnd' found after 'prompt'.")
    else:
        print("No 'prompt' found in the text.")
    return prompt__gen


def generate(lora_path, prompt__gen, index):
    # print(prompt__gen)
    handler = fal_client.submit(
        "fal-ai/fast-sdxl",
        arguments={
            "prompt": prompt__gen,
            "negative_prompt": "human, people, person, man, woman, child, model, face, head, eyes, hands, arms, legs, "
                               "feet, hair, portrait, worst quality, low quality, normal quality, lowres, signature, "
                               "watermark, jpeg artifacts, logo, monochrome, grayscale, ugly",
            "image_size": "portrait_4_3",
            "num_inference_steps": 28,
            "guidance_scale": 7.5,
            "num_images": 1,
            "loras": [{"path": lora_path, "scale": 0.7}],
            "embeddings": [],
            "safety_checker_version": "v1",
            "format": "jpeg"
        },
    )

    request_id = handler.request_id
    result = fal_client.result("fal-ai/fast-sdxl", request_id)
    image_index = index * 2 - 1
    for image in result['images']:
        response = requests.get(image['url'])
        if response.status_code == 200:
            filename = os.path.join(save_directory, f"cloth_{image_index}.jpeg")
            with open(filename, 'wb') as f:
                f.write(response.content)
            image_index += 1
        else:
            print(f"Failed to download image from {image['url']}")

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.", },
            {"role": "user",
             "content": prompt__gen + "以上是一段对于一套汉服的描述，请根据描述内容对该套汉服进行介绍。要求以介绍的口吻输出内容",
             }
        ]

    )
    cloth_intro = ("汉服，是汉民族的传统服饰。又称衣冠、衣裳、汉装。汉服是中国“衣冠上国”“礼仪之邦”“锦绣中华”的体现，承载了中国的染织绣等杰出"
                   "工艺和美学，传承了30多项中国非物质文化遗产以及受保护的中国工艺美术。\n") + completion.choices[
                      0].message.content
    filename = os.path.join(save_directory, f"cloth_intro_{index * 2 - 1}.txt")
    with open(filename, "w") as file:
        file.write(cloth_intro)


def convert_image_to_jpeg(input_path, output_path):
    try:
        image = Image.open(input_path)
        if image.mode in ('RGBA', 'LA'):
            image = image.convert('RGB')
        image.save(output_path, 'JPEG')
    except Exception as e:
        print(f"转换图像时出错: {e}")


def pic_match(prompt__gen, cates, folder_path, intro_path, index):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant.", },
            {"role": "user",
             "content": prompt__gen + "以上是关于一套汉族服饰的描述，请根据描述内容从以下几种颜色中选择最符合描述的一种，可选颜色包括：" + cates
                        + ". 仅需输出一种颜色名称，不要带任何符号",
             }
        ]

    )
    print(f"Selected color: {completion.choices[0].message.content}")

    folder_path = os.path.join(folder_path, completion.choices[0].message.content)
    files = os.listdir(folder_path)
    random_file = random.choice(files)
    source_file_path = os.path.join(folder_path, random_file)
    file_prefix, file_ext = os.path.splitext(random_file)
    target_file_path = os.path.join(save_directory, f"cloth_{index * 2}.jpeg")
    convert_image_to_jpeg(source_file_path, target_file_path)

    file_extension = ".txt"
    search_path = Path(intro_path)
    for file in search_path.glob(f"{file_prefix}*{file_extension}"):
        if file.is_file():
            with open(file, "r") as f:
                content = f.read()
                client = OpenAI()
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system",
                         "content": "You are a helpful assistant.", },
                        {"role": "user",
                         "content": content + "以上是一段对于一套汉服的描述，请根据描述内容对该套汉服进行介绍。要求以介绍的口吻输出内容",
                         }
                    ]

                )
                cloth_intro = ("汉服，是汉民族的传统服饰。又称衣冠、衣裳、汉装。汉服是中国“衣冠上国”“礼仪之邦”“锦绣中华”的体现，承载了中国的染织绣等杰出"
                               "工艺和美学，传承了30多项中国非物质文化遗产以及受保护的中国工艺美术。\n") + \
                              completion.choices[0].message.content
                filename = os.path.join(save_directory, f"cloth_intro_{index * 2}.txt")
                with open(filename, "w") as file:
                    file.write(cloth_intro)

    return target_file_path


def cloth_gen(gender):
    cates = "Black, Blue, Green, Orange, Pink, Red, Violet, White, Yellow"
    lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"
    folder_path = "database/female"
    intro_path = "database/female_intro"
    if gender == "男":
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NA.safetensors"
        cates = "Black, Blue, Green, Brown, Red, Violet"
        folder_path = "database/male"
        intro_path = "database/male_intro"
    elif gender == "女":
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"
        cates = "Black, Blue, Green, Orange, Pink, Red, Violet, White, Yellow"
        folder_path = "database/female"
        intro_path = "database/female_intro"

    cloth_image = []
    for i in range(1, 4):
        with open(os.path.join(save_directory, f"prompt_{i}.txt"), "r") as file:
            prompt__gen = file.read()
        generate(lora_path, prompt__gen, i)
        cloth_image.append(os.path.join(save_directory, f"cloth_{i*2-1}.jpeg"))
        pic_path = pic_match(prompt__gen, cates, folder_path, intro_path, i)
        cloth_image.append(pic_path)

    with open(os.path.join(save_directory, f"cloth_intro_1.txt"), "r") as file:
        cloth_intro = file.read()
    return cloth_image, cloth_image[0], cloth_intro
