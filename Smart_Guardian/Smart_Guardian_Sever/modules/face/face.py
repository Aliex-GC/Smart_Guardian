import cv2
import os
import numpy as np

# 创建一个LBPH人脸识别器
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./model/trainer.yml')

names = []

def get_names():
    path = './data/'
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    for imagePath in imagePaths:
        name = str(os.path.splitext(os.path.basename(imagePath))[0])
        names.append(name)

def face_detect_demo(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier('./haar/haarcascade_frontalface_alt.xml')
    faces = face_detector.detectMultiScale(gray, 1.1, 5)

    recognized_name = None
    for x, y, w, h in faces:
        ids, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        if confidence <= 100:
            recognized_name = str(names[ids - 1])
            break
    return recognized_name

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        return frame
    else:
        return None

# 准备模型和名称列表
get_names()

# 直接在后端调用摄像头并进行识别
def recognize_face_from_camera():
    img = capture_image()
    if img is not None:
        recognized_name = face_detect_demo(img)
        return recognized_name
    return None
print(recognize_face_from_camera())
