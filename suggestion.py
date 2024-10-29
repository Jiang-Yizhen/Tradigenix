import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket  # 使用websocket_client
from PIL import Image
import io
import gradio as gr

appid = ""  #填写控制台中获取的 APPID 信息
api_secret = ""  #填写控制台中获取的 APISecret 信息
api_key = ""  #填写控制台中获取的 APIKey 信息

imageunderstanding_url = "wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image"  #云端环境的服务地址
answer = ""

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, imageunderstanding_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(imageunderstanding_url).netloc
        self.path = urlparse(imageunderstanding_url).path
        self.ImageUnderstanding_url = imageunderstanding_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.ImageUnderstanding_url + '?' + urlencode(v)
        #print(url)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, one, two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    #print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        print(content, end="")
        global answer
        answer += content
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, question):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid
        },
        "parameter": {
            "chat": {
                "domain": "image",
                "temperature": 0.5,
                "top_k": 4,
                "max_tokens": 2028,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }

    return data


def main(appid, api_key, api_secret, imageunderstanding_url, question):
    wsParam = Ws_Param(appid, api_key, api_secret, imageunderstanding_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    #ws.imagedata = imagedata
    ws.question = question
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def getText(role, content, picture):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    image = Image.fromarray(picture)
    byte_io = io.BytesIO()
    image.save(byte_io, format='PNG')
    image_bytes = byte_io.getvalue()
    # 进行 Base64 编码
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    text = [{"role": "user", "content": encoded_image, "content_type": "image"}, jsoncon]
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    #print("text-content-tokens:", getlength(text[1:]))
    while (getlength(text[1:]) > 8000):
        del text[1]
    return text


def generate_outfit_advice(user_name, height, weight, waist, chest, hip, shoulder_width, leg_length, arm_length, gender,
                           body_type, skin_color, style_preference, lifestyle_requirements, special_requirements,
                           feedback, user_pic):
    content = (f"""
                       你是一位专业的民族服饰搭配大师，你需要充分了解中华民族的所有民族服饰的相关知识，包括不同民族服饰适合什么样的人群等。
                       你需要对用户的照片和他们的输入信息作出评价，需要分析的因素包括以下内容： 
                       1、用户上传的照片，分析种族、民族、脸型、五官比例、身材比例、肤色肤质。 
                       2、用户基本信息：性别，年龄，身高，体重；
                       3、身体数据：胸围，腰围，臀围，肩宽，腿长，臂长； 
                       4、体型与身材特征：体型分类：如苹果型、梨型、矩形、沙漏型等；身材特征：如长腿、短腿、宽肩、窄肩等。 
                       5、肤色与发色：肤色分类：如冷色调、暖色调、中性色调等；发色与发型：目前的发色和发型。 
                       6、穿衣风格偏好：日常偏好的风格（例如休闲、正式、运动、复古等），喜欢的颜色和不喜欢的颜色，喜爱的服装品牌，特别喜欢的服装单品（例如裙子、裤子、衬衫等） 
                       7、生活方式和场合需求：工作环境（例如：办公室、户外、创意行业等），主要的社交活动类型（例如：商务会议、派对、休闲聚会等），平常的活动类型和频率（例如：健身、旅行、家庭活动等） 
                       8、季节和气候：所在地的气候情况（例如：四季分明、热带、寒冷地区等），需要的季节性服装（例如：冬季大衣、夏季连衣裙等） 
                       9、个人偏好和特殊需求：对于面料的偏好（例如：棉、麻、丝、羊毛等）；是否有过敏或不适宜穿戴的材质；是否有特定的宗教或文化穿衣要求；是否有特殊身体条件需要考虑（例如：孕妇、残障人士等）
                       输出要求：
                       一、要求输出一段用户的人物画像，包含具体的服饰穿搭建议。 每种体型的合适服装和不合适服装都具有一定的潜在服装特征。例如，草莓形的人更适合穿
                       宽领或深领的衣服，而梨形的人则更适合穿伞形下摆的衣服而不是紧身的衣服。 
                       二、将穿搭建议转化为具体的服饰特征，建立用户特征与服饰提示词的对应。 例如场合对应衣服的干练程度，更喜欢通勤场合的会倾向于推荐小袖口的民族服饰； 
                       根据体型推荐相关服饰，略显肥胖的人会推荐汉服齐腰儒裙等； 男性按身高与袖口来分辨哪种服饰。
                       根据用户信息，用户名为{user_name}，身高为{height}，体重为{weight}，腰围为{waist}，胸围为{chest}，臀围为{hip}，
                       肩宽为{shoulder_width}，腿长为{leg_length}，臂长为{arm_length}，性别为{gender}，体型分类为{body_type}，肤色为{skin_color}，
                       穿衣风格偏好为{style_preference}，生活方式和场景需求为{lifestyle_requirements}，其他特殊需求为{special_requirements},{feedback}。
                       请给出穿搭建议。
                       """)
    global answer
    answer = ""
    question = checklen(getText("user", content, user_pic))
    main(appid, api_key, api_secret, imageunderstanding_url, question)
    getText("assistant", answer, user_pic)
    return answer

