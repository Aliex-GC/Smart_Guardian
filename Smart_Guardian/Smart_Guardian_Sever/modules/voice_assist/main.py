import base64
import urllib
import requests
import json
import pyaudio
import wave
import numpy as np
import os
import pygame
from gtts import gTTS
import time 
import json
import Smart_Guardian_Sever.modules.voice_assist.ollama.client as client
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage,SystemMessage, HumanMessage
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import (
    ChatPromptTemplate
)

API_KEY = "mLtKHSgI0Kl9WBDoH91JRejY"
SECRET_KEY = "1Fohw23E3goFtd0LLmyatEQfSJYtSBDd"

# 定义录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAV_OUTPUT_FILENAME = "output_auto.wav"
SILENCE_THRESHOLD = 500  # 静音阈值
MAX_SILENCE_DURATION = 2  # 最大静音时间，单位秒

def record():
    # 初始化 PyAudio
    audio = pyaudio.PyAudio()
    # 打开流
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("开始录音...")

    frames = []
    silent_chunks = 0
    max_silent_chunks = int(MAX_SILENCE_DURATION * RATE / CHUNK)

    # 录制音频，检测音量是否保持静音
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # 将音频数据转换为 NumPy 数组
        audio_data = np.frombuffer(data, dtype=np.int16)

        # 计算音量的均方根（RMS），用于判断声音大小
        volume = np.sqrt(np.mean(np.square(audio_data)))

        if volume < SILENCE_THRESHOLD:
            silent_chunks += 1
        else:
            silent_chunks = 0

        # 如果静音时间超过设定的阈值，停止录音
        if silent_chunks > max_silent_chunks:
            print("检测到静音，录音结束。")
            break

    # 停止和关闭流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 保存为 .wav 文件
    wf = wave.open(WAV_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"音频已保存为 {WAV_OUTPUT_FILENAME}")


def gettext():
    url = "https://vop.baidu.com/server_api"
    payload = json.dumps({
        "format": "wav",
        "rate": 16000,
        "channel": 1,
        "cuid": "uFq7OZ0O4UWIK3HeglRLlbjY9StNruq4",
        "speech": get_file_content_as_base64("./output_auto.wav",False),
        "len": len(open("./output_auto.wav", 'rb').read()),
        "token": get_access_token()
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # print(response.text)
    return response.json().get("result")[0]
    

def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode('utf8')
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

os.environ['OPENAI_API_BASE'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
DASHSCOPE_API_KEY= "sk-31ed7f23b2cc4ca9959e37bbf7259b64"
llm = chat_model = ChatOpenAI(model="qwen2-57b-a14b-instruct", api_key=DASHSCOPE_API_KEY,openai_api_base = os.environ['OPENAI_API_BASE'], max_tokens=2000)


conversation_history = []

def TYgraphPrompt(prompt: str, metadata={}, model="qwen2-57b-a14b-instruct"):
    # 系统提示词
    SYS_PROMPT = "你是一个提供中文简洁答案的助手。请尽量简短地回答以下问题："
    conversation_history.append(HumanMessage(content=prompt))
    # 定义聊天提示模板，包括对话历史的占位符
    prompt_template = ChatPromptTemplate(
        messages=[
            SystemMessage(content=SYS_PROMPT),
        ] + conversation_history  # 将对话历史传递给模板
    )


    # 创建一个运行序列（管道）
    chain = prompt_template | llm

    try:
        # 使用链条生成响应，并传递对话历史
        response = chain.invoke({"input": prompt})

        # 处理响应
        if isinstance(response, AIMessage):
            content = response.content
            conversation_history.append(AIMessage(content=content))  # 保存 AI 的回复到对话历史
            return content
        else:
            return None
    except Exception as e:
        print("\n\nERROR ### Here is the buggy response: ", e, "\n\n")
        return None

def LLMPrompt(prompt: str, metadata={}, model="zephyr:latest"):
    if model == None:
        model = "zephyr:latest"
    print("==  zephyr start  ==")
    # model_info = client.show(model_name=model)
    # print( chalk.blue(model_info))

    SYS_PROMPT = (
        "请用中文直接地、简洁地回答以下问题,回答中不要包含任何英文："
    )


    USER_PROMPT = f"问题如下： {prompt} "
    response, _ = client.generate(model_name=model, system=SYS_PROMPT, prompt=USER_PROMPT)

    return response

def output(cotent):
    tts = gTTS(cotent, lang="zh")
    tts.save("output.mp3")
    # 初始化 pygame 的音频模块
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    # 等待音频播放完毕
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    return 1

def play_audio(stream, filename):
    wf = wave.open(filename, 'rb')
    while True:
        data = wf.readframes(2048)
        if data == b"":
            break
        stream.write(data)
    time.sleep(0.01)
    wf.close()

def get_comprehensive_url():
    return (
        f"https://api.caiyunapp.com/v2.6/4Ol0FEX9i8oRvxaz/101.6656,39.2072/weather?"
        f"dailysteps=3&hourlysteps=48"
    )


def get_weather() -> dict | int:
    """
    :return: dict 天气查询结果 , int 天气查询失败后的代码
    """
    # old_weather = LocalStorage.get("weather")
    # if old_weather:
    #     old_data: dict = json.loads(old_weather)
    #     if old_data['server_time'] + 900 > datetime.datetime.now().timestamp():
    #         return old_data

    response = requests.get(get_comprehensive_url())
    if response.status_code == 200:
        resp_data = response.text
        # LocalStorage.set("weather", resp_data)
        return dict(json.loads(resp_data))
    print(response.status_code)
    return response.status_code
def output_weather():
    weather_map = {
        "CLEAR_DAY": "晴（白天）",
        "CLEAR_NIGHT": "晴（夜间）",
        "PARTLY_CLOUDY_DAY": "多云（白天）",
        "PARTLY_CLOUDY_NIGHT": "多云（夜间）",
        "CLOUDY": "阴",
        "LIGHT_HAZE": "轻度雾霾",
        "MODERATE_HAZE": "中度雾霾",
        "HEAVY_HAZE": "重度雾霾",
        "LIGHT_RAIN": "小雨",
        "MODERATE_RAIN": "中雨",
        "HEAVY_RAIN": "大雨",
        "STORM_RAIN": "暴雨",
        "FOG": "雾",
        "LIGHT_SNOW": "小雪",
        "MODERATE_SNOW": "中雪",
        "HEAVY_SNOW": "大雪",
        "STORM_SNOW": "暴雪",
        "DUST": "浮尘",
        "SAND": "沙尘",
        "WIND": "大风"
    }
    weather_info = get_weather()
    if isinstance(weather_info, dict):
        description = weather_map[weather_info['result']['realtime']['skycon']]
        temp = weather_info['result']['realtime']['temperature']
        humidity = weather_info['result']['realtime']['humidity'] * 100
        wind_speed = weather_info['result']['realtime']['wind']['speed']
        forcast = weather_info['result']['forecast_keypoint']
        answer = f"当前天气{description}，气温{temp}度，湿度{int(humidity)}%，风速是{wind_speed}米每秒。{forcast}"
    else:
        answer = "获取天气信息失败。"
    print(answer)
    return answer


def voice_assistant():
        record()
        if(os.path.exists("./output_auto.wav")):
            try:
                text=gettext()
                print("检测到录音如下：\n",text)
                print("AI回答如下：")
                answer=TYgraphPrompt(text)
                print(answer)
                output(answer)
            except:
                audio = pyaudio.PyAudio()
                stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
                play_audio(stream, "error.wav")
                stream.stop_stream()
                stream.close()
                audio.terminate()
        else:
            print("没有找到录音文件！")




        

        
