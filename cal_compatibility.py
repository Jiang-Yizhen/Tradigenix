import vgg16
import numpy as np


def cosine_similarity(vector1, vector2):
    # # 计算向量的点积
    # dot_product = np.dot(vector1, vector2)
    # # 计算向量的模长
    # magnitude_vector1 = np.linalg.norm(vector1)
    # magnitude_vector2 = np.linalg.norm(vector2)
    # # 计算余弦相似度
    # return dot_product / (magnitude_vector1 * magnitude_vector2)
    flat_vector1 = vector1.reshape(-1)
    flat_vector2 = vector2.reshape(-1)
    dot_product = np.dot(flat_vector1, flat_vector2)
    norm_vector1 = np.linalg.norm(flat_vector1)
    norm_vector2 = np.linalg.norm(flat_vector2)
    return dot_product / (norm_vector1 * norm_vector2)


def cal_compatibility():
    n = 4096
    access_feature = []
    cloth_feature = []
    for item_id in range(1, 9):
        access_feature.append(vgg16.extract_features('downloads/access_' + '%s.jpg' % item_id)[0])
    for item_id in range(1, 7):
        cloth_feature.append(vgg16.extract_features('downloads/cloth_' + '%s.jpeg' % item_id)[0])

    best_score = float('-inf')
    best_cloth = 0
    best_access = 0
    for i in range(1, 9):
        for j in range(1, 7):
            score = cosine_similarity(access_feature[i - 1], cloth_feature[j - 1])
            if score > best_score:
                best_score = score
                best_cloth = j
                best_access = i
    print(best_cloth, best_access)
    picture = [f"downloads/cloth_{best_cloth}.jpeg", f"downloads/access_{best_access}.jpg"]
    return picture