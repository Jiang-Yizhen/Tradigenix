import fal_client
import pandas as pd
from prompt_gen import prompt_gen
import requests
import os

nv_prompt_file = pd.read_excel('汉服-女词库.xlsx')
na_prompt_file = pd.read_excel('汉服-男词库.xlsx')
nv_prompt = nv_prompt_file.to_string(index=False)
na_prompt = na_prompt_file.to_string(index=False)
save_directory = "downloads"


def pro_gen(advice, gender, index):
    prompt = prompt_gen(advice, gender)
    start_index = prompt.find("Begin")
    if start_index == -1:
        start_index = prompt.find("begin")
    intro_index = prompt.find("服饰风格介绍")
    cloth_intro = ""
    prompt__gen = ""
    if start_index != -1:
        start_index += len("Begin\n")
        end_index = prompt.find("End")
        if end_index != -1:
            prompt__gen = prompt[start_index:end_index]
            filename = os.path.join(save_directory, f"prompt_{index}.txt")
            with open(filename, "w") as file:
                file.write(prompt__gen)
            print(prompt__gen)
        else:
            print("No 'promptEnd' found after 'prompt'.")
    else:
        print("No 'prompt' found in the text.")
    if intro_index != -1:
        intro_index += len("服饰风格介绍\n")
        cloth_intro = ("汉服，是汉民族的传统服饰。又称衣冠、衣裳、汉装。汉服是中国“衣冠上国”“礼仪之邦”“锦绣中华”的体现，承载了中国的染织绣等杰出"
                       "工艺和美学，传承了30多项中国非物质文化遗产以及受保护的中国工艺美术。\n") + prompt[intro_index:]
        filename = os.path.join(save_directory, f"cloth_intro_{index}.txt")
        with open(filename, "w") as file:
            file.write(cloth_intro)
        print(cloth_intro)
    else:
        print("No '服饰风格介绍' found.")
    return prompt__gen


def generate(lora_path, prompt__gen, index):
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
            "num_images": 2,
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
            filename = os.path.join(save_directory, f"gen_cloth_{image_index}.jpeg")
            with open(filename, 'wb') as f:
                f.write(response.content)
            image_index += 1
        else:
            print(f"Failed to download image from {image['url']}")


def cloth_gen(gender):
    lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"
    if gender == "男":
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NA.safetensors"
    else:
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"

    cloth_image = []
    for i in range(1, 4):
        with open(os.path.join(save_directory, f"prompt_{i}.txt"), "r") as file:
            prompt__gen = file.read()
        generate(lora_path, prompt__gen, i)
        cloth_image.append(os.path.join(save_directory, f"gen_cloth_{i*2-1}.jpeg"))
        cloth_image.append(os.path.join(save_directory, f"gen_cloth_{i*2}.jpeg"))
    with open(os.path.join(save_directory, f"cloth_intro_1.txt"), "r") as file:
        cloth_intro = file.read()
    return cloth_image, cloth_image[0], cloth_intro
