import cv2
import time
import os

# 创建目录
os.makedirs('./Smart_Guardian/data', exist_ok=True)

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

for i in range(1, 21):
    ret, frame = cap.read()  # 读取摄像头画面
    if not ret:
        print("无法读取摄像头画面")
        break

    # 生成文件名
    filename = f"./Smart_Guardian/data/{i:03d}.gc.jpg"
    
    # 保存图片
    cv2.imwrite(filename, frame)
    print(f"已保存: {filename}")

    # 等待一秒
    time.sleep(1)

# 释放摄像头
cap.release()
cv2.destroyAllWindows()
