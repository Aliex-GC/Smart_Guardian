import os
import cv2
from PIL import Image
import numpy as np


def getImageAndLabels(path):
    faceSamples = []
    ids = []
    # 获取图像目录中所有以指定扩展名结尾的图像文件路径
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if
                  f.lower().endswith(('.png', '1.jpg', '.jpeg', '.gif', '.bmp'))]

    # 加载人脸检测器（Haar级联分类器）
    face_detector = cv2.CascadeClassifier(
        './haar/haarcascade_frontalface_alt.xml')

    for imagePath in imagePaths:
        # 使用PIL库打开图像并转换为灰度图
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # 使用Haar级联分类器检测图像中的人脸
        faces = face_detector.detectMultiScale(img_numpy)

        # 从图像文件名中提取人物ID
        id = int(os.path.split(imagePath)[1].split('.')[0])

        # 遍历检测到的人脸并保存样本
        for x, y, w, h in faces:
            ids.append(id)
            faceSamples.append(img_numpy[y:y + h, x:x + w])

    # 打印最后一个图像文件的ID、以及所有收集到的人脸样本
    print('id', id)
    print('fs', faceSamples)

    return faceSamples, ids


if __name__ == '__main__':
    # 打印OpenCV版本信息
    print(cv2.__version__)

    # 设置图像目录路径
    path = './data/'

    # 获取人脸样本和对应的ID
    faces, ids = getImageAndLabels(path)

    # 创建LBPH人脸识别器
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # 训练人脸识别器
    recognizer.train(faces, np.array(ids))

    # 将训练好的模型保存为YML文件
    recognizer.write("./model/trainer.yml")