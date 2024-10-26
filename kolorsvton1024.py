import time
import jwt
import requests
import json
import base64
import os


def image_to_base64(image_path):
    """
    将图片文件转换为Base64编码格式
    :param image_path: 图片文件路径
    :return: Base64编码字符串
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


ak = "c1748494bc5d42ed8db2b2d24ceb1a2b"  # 填写access key
sk = "1cf0bbef768746f79d30ef13630b393b"  # 填写secret key


def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


# 图片及回调配置
# HUMAN_IMAGE = image_to_base64(r"F:\codetest24\0903_lf\vton\people.jpg") # 替换为人物图片的Base64或URL
# CLOTH_IMAGE = image_to_base64(r"F:\codetest24\0903_lf\vton\hanfu.jpg")  # 替换为服饰图片的Base64或URL
# CALLBACK_URL = ""  # 可选，任务结果回调通知URL
SAVE_DIRECTORY = "downloads/kolor"
BASE_URL = "https://api.klingai.com/v1/images/kolors-virtual-try-on"


# ========== 步骤 1：创建虚拟试穿任务 ==========

def create_virtual_tryon_task(humen, cloth, HEADERS):
    """
    创建虚拟试穿任务
    """

    # ========== 配置参数 ==========


    # 请求体数据
    data = {
        "model_name": "kolors-virtual-try-on-v1",
        "human_image": image_to_base64(humen),
        "cloth_image": image_to_base64(cloth),
    }

    # 发起POST请求创建任务
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(data))

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        task_id = result['data']['task_id']
        print(f"创建任务成功，任务ID: {task_id}")
        return task_id
    else:
        print(f"创建任务失败: {response.status_code}, {response.text}")
        return None


# ========== 步骤 2：查询单个虚拟试穿任务状态并保存图片 ==========

def query_virtual_tryon_task(task_id, i, HEADERS):
    """
    根据任务ID查询任务状态，成功后保存生成的图片
    """
    # 请求URL
    url = f"{BASE_URL}/{task_id}"

    # 发起GET请求查询任务状态
    response = requests.get(url, headers=HEADERS)

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        task_status = result['data']['task_status']
        print(f"任务状态: {task_status}")

        # 如果任务成功，下载并保存生成的图片
        if task_status == 'succeed':
            images = result['data']['task_result']['images']
            for image in images:
                image_url = image['url']
                image_index = i
                save_image(image_url, image_index)

        # 返回任务状态
        return task_status
    else:
        print(f"查询任务失败: {response.status_code}, {response.text}")
        return None


# ========== 步骤 3：下载并保存图片 ==========

def save_image(image_url, image_index):
    """
    根据图片URL下载并保存到本地
    """
    response = requests.get(image_url)

    if response.status_code == 200:
        # 保存图片到本地
        image_path = os.path.join(SAVE_DIRECTORY, f"kolor_{image_index}.png")
        with open(image_path, "wb") as file:
            file.write(response.content)
        print(f"图片已保存到: {image_path}")
    else:
        print(f"下载图片失败: {response.status_code}, {response.text}")


# ========== 步骤 4：查询任务列表 ==========

def query_task_list(page_num=1, page_size=30, HEADERS=None):
    """
    查询任务列表
    """
    # 查询参数
    params = {
        "pageNum": page_num,
        "pageSize": page_size
    }

    # 发起GET请求查询任务列表
    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        print("任务列表:")
        for task in result['data']:
            print(f"任务ID: {task['task_id']}, 状态: {task['task_status']}, 创建时间: {task['created_at']}")
    else:
        print(f"查询任务列表失败: {response.status_code}, {response.text}")


# ========== 主流程 ==========

def kolor_vton(humen, cloth, i):
    # API 请求的基础配置
    api_token = encode_jwt_token(ak, sk)
    print(api_token)  # 打印生成的API_TOKEN
    # 请求头
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # 1. 创建虚拟试穿任务
    task_id = create_virtual_tryon_task(humen, cloth, HEADERS)

    # 如果任务创建成功，继续执行查询步骤
    if task_id:
        # 2. 定期查询该任务状态，直到任务完成
        while True:
            status = query_virtual_tryon_task(task_id, i, HEADERS)
            if status in ['succeed', 'failed']:
                break
            print("任务正在处理中，等待1秒后重试...")
            time.sleep(1)  # 等待1秒后重试

        # 3. 查询任务列表
        query_task_list(page_num=1, page_size=10, HEADERS=HEADERS)

# kolor_vton("uploads/user_image.jpg", "uploads/user_image.jpg", 1)