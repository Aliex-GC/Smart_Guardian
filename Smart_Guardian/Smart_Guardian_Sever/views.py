from django.shortcuts import render
from django.http import JsonResponse
from Smart_Guardian_Sever.modules.voice_assist import main 
import os,pyaudio,threading
import cv2
import os
import time
# Create your views here.



conversation_history = []
# 定义录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAV_OUTPUT_FILENAME = "output_auto.wav"
SILENCE_THRESHOLD = 500  # 静音阈值
MAX_SILENCE_DURATION = 3  # 最大静音时间，单位秒

# 创建一个LBPH人脸识别器
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./model/trainer.yml')
current_recognized_name = None
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
    print(f"检测到的人脸数量: {len(faces)}")  # 调试输出s
    recognized_name = None
    for x, y, w, h in faces:
        ids, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        print(f"ID: {ids}, Confidence: {confidence}")  # 调试输出
        if confidence <= 100:
            recognized_name = str(names[ids - 1])
            break
    return recognized_name

def capture_image():
    print("尝试打开摄像头...")  # 调试输出
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("无法打开摄像头")  # 调试输出
        return None
    ret, frame = cap.read()
    
    cap.release()
    
    if ret:
        print("图像捕获成功")  # 调试输出
        return frame
    else:
        print("无法捕获图像")  # 调试输出
        return None



# 直接在后端调用摄像头并进行识别
def recognition_thread():
    global current_recognized_name
    print("识别线程启动...")  # 调试输出
    while True:
        img = capture_image()
        if img is not None:
            current_recognized_name = face_detect_demo(img)
            print(f"识别到的名字: {current_recognized_name}")  # 调试输出
        time.sleep(20)  # 每两秒执行一次



def index(request):
    if request.method == "POST":
        main.record()
        if(os.path.exists("./output_auto.wav")):
            try:
                user_message=main.gettext()
                
                print("检测到录音如下：\n",user_message)
                if("天气" in user_message):
                    print("wheather:")
                    bot_response=main.output_weather()
                else:
                    print("AI回答如下：")
                    bot_response=main.TYgraphPrompt(user_message)
                    print(bot_response)
                response=JsonResponse({
                    'user_message': user_message,
                    'bot_message': bot_response
                })
                threading.Thread(target=main.output, args=(bot_response,)).start()
            except:
                audio = pyaudio.PyAudio()
                stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
                main.play_audio(stream, "./error.wav")
                stream.stop_stream()
                stream.close()
                audio.terminate()
        else:
            print("没有找到录音文件！")

        # 返回用户输入和机器人的回复
        # return JsonResponse({
        #     'user_message': user_message,
        #     'bot_message': bot_response
        # })
        return response


    global current_recognized_name
    print("进入 index 视图...")  # 调试输出
    if current_recognized_name is None:  # 仅在第一次访问时启动线程
        print("准备启动识别线程...")  # 调试输出
        get_names()
        threading.Thread(target=recognition_thread, daemon=True).start()
        print("识别线程启动中...")  # 调试输出
    context = {
        'recognized_name': current_recognized_name
    }
    return render(request, 'index.html', context)

def get_recognized_name(request):
    global current_recognized_name
    print(current_recognized_name)
    return JsonResponse({'recognized_name': current_recognized_name})