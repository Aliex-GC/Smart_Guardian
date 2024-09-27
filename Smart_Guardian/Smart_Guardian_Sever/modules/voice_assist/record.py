import pyaudio
import wave
import numpy as np
import time

# 定义录音参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAV_OUTPUT_FILENAME = "output_auto.wav"
SILENCE_THRESHOLD = 500  # 静音阈值
MAX_SILENCE_DURATION = 2  # 最大静音时间，单位秒

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
