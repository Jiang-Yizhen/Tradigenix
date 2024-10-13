from io import BytesIO
import fal_client
import os
from PIL import Image
import requests
import time

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

def user_dress(user_pic, cloth_gen):
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
    handler = fal_client.submit(
        "fal-ai/cat-vton",
        arguments={
            "human_image_url": fal_client.upload_file(file_path_1),
            "garment_image_url": fal_client.upload_file(file_path_2),
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
    save_directory = "downloads"
    if response.status_code == 200:
        filename = os.path.join(save_directory, f"cat-vton.png")
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image from {result['image']['url']}")
    time_2 = time.time()
    downloads_time = time_2 - time_1
    print(f"downloads_time:{downloads_time}")
    return os.path.join(save_directory, f"cat-vton.png")

# user_dress("8950.jpg")