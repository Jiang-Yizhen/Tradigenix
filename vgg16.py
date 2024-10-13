# from tensorflow.keras.applications.imagenet_utils import preprocess_input
# from tensorflow.keras.applications.vgg16 import VGG16
# from keras.models import Model
# from keras.preprocessing import image
# import numpy as np
# from PIL import ImageFile
#
# ImageFile.LOAD_TRUNCATED_IMAGES = True
#
# base_model = VGG16(weights='imagenet', include_top=True)
# model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)
#
#
# def extract_feature(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))  # 224×224
#
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     features = model.predict(x)  # fc2
#
#     return features
import keras
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
import numpy as np

# 加载预训练的 VGG16 模型，不包括全连接层
base_model = VGG16(weights='imagenet', include_top=False)


def extract_features(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = base_model.predict(x)
    # print(features.shape)
    return features

# image_path = "downloads/access_1.jpg"
# features = extract_features(image_path)
# print(features.shape)
