import fal_client
import pandas as pd
from prompt_gen import prompt_gen
import requests
import os

nv_prompt_file = pd.read_excel('汉服-女词库.xlsx')
na_prompt_file = pd.read_excel('汉服-男词库.xlsx')
nv_prompt = nv_prompt_file.to_string(index=False)
na_prompt = na_prompt_file.to_string(index=False)

def cloth_gen(advice, gender):
    lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"
    if gender == "男":
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NA.safetensors"
    else:
        lora_path = "https://huggingface.co/PPSharks/PPSharksModels/resolve/main/NV.safetensors"

    prompt = prompt_gen(advice, gender)
    prompt_start = prompt.find("Prompt")
    if prompt_start != -1:
        prompt = prompt[prompt_start + len("Prompt"):].strip()
    else:
        print("No prompt found.")

    handler = fal_client.submit(
        "fal-ai/fast-sdxl",
        arguments={
            "prompt": prompt,
            "negative_prompt": "face, male, female, people, person, man, woman, Multiple clothes, cartoon, illustration, animation.",
            "image_size": "portrait_4_3",
            "num_inference_steps": 28,
            "guidance_scale": 7.5,
            "num_images": 6,
            "loras": [{"path": lora_path, "scale": 0.7}],
            "embeddings": [],
            "safety_checker_version": "v1",
            "format": "jpeg"
        },
    )

    request_id = handler.request_id
    result = fal_client.result("fal-ai/fast-sdxl", request_id)
    cloth_image = []
    save_directory = "downloads"
    image_index = 1
    for image in result['images']:
        response = requests.get(image['url'])
        if response.status_code == 200:
            filename = os.path.join(save_directory, f"gen_cloth_{image_index}.jpeg")
            cloth_image.append(filename)
            with open(filename, 'wb') as f:
                f.write(response.content)
            image_index += 1
        else:
            print(f"Failed to download image from {image['url']}")
    return cloth_image

# cloth_gen()