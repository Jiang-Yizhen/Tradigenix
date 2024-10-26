from io import BytesIO
import fal_client
import os
from PIL import Image
import requests
import time
from kolorsvton1024 import kolor_vton

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
save_directory = "downloads"

def user_dress_cat(user_pic, cloth_gen, index):
    time_1 = time.time()
    filename_1 = 'user_image.jpg'
    filename_2 = 'cloth_image.jpg'
    file_path_1 = os.path.join(UPLOAD_FOLDER, filename_1)
    file_path_2 = os.path.join(UPLOAD_FOLDER, filename_2)
    fal_file_path_1=fal_client.upload_file(file_path_1)
    fal_file_path_2=fal_client.upload_file(file_path_2)
    Image.fromarray(user_pic).save(file_path_1)
    Image.fromarray(cloth_gen).save(file_path_2)
    time_2 = time.time()
    save_time = time_2 - time_1
    print(f"save_time:{save_time}")
    time_1 = time.time()
    handler = fal_client.submit(
        "fal-ai/cat-vton",
        arguments={
            "human_image_url": fal_file_path_1,
            "garment_image_url": fal_file_path_2,
            "cloth_type": "overall"
        },
    )
    request_id = handler.request_id
    result = fal_client.result("fal-ai/cat-vton", request_id)
    time_2 = time.time()
    cat_time = time_2 - time_1
    print(f"cat_time:{cat_time}")
    time_1 = time.time()
    response = requests.get(result['image']['url'])
    time_2 = time.time()
    url_time = time_2 - time_1
    print(f"url_time:{url_time}")
    time_1 = time.time()

    if response.status_code == 200:
        filename = os.path.join(save_directory, f"cat-vton_{index}.png")
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image from {result['image']['url']}")
    time_2 = time.time()
    downloads_time = time_2 - time_1
    print(f"downloads_time:{downloads_time}")
    return os.path.join(save_directory, f"cat-vton_{index}.png")


def user_dress_kolor(user_pic, cloth_gen, index):
    time_1 = time.time()
    filename_1 = 'user_image.jpg'
    filename_2 = 'cloth_image.jpg'
    file_path_1 = os.path.join(UPLOAD_FOLDER, filename_1)
    file_path_2 = os.path.join(UPLOAD_FOLDER, filename_2)
    Image.fromarray(user_pic).save(file_path_1)
    Image.fromarray(cloth_gen).save(file_path_2)
    time_2 = time.time()
    save_time = time_2 - time_1
    print(f"save_time:{save_time}")
    time_1 = time.time()
    kolor_vton(file_path_1, file_path_2, index)
    time_2 = time.time()
    cat_time = time_2 - time_1
    print(f"kolor_time:{cat_time}")


def user_cloths(user_pic, cloth_gen):
    user_cloth = []
    for i in range(1, 4):
        user_cloth.append(user_dress_cat(user_pic, cloth_gen, i))
    # for i in range(4, 7):
    #     user_dress_kolor(user_pic, cloth_gen, i)
    #     user_cloth.append(os.path.join(save_directory, f"kolor/kolor_{i}.png"))
    user_dress_kolor(user_pic, cloth_gen, 4)#ddd
    user_cloth.append(os.path.join(save_directory, f"kolor/kolor_4.png"))
    return user_cloth
