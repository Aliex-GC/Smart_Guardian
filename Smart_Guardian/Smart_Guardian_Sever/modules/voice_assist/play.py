from gtts import gTTS
import time
import pygame


tts = gTTS("今天的天气非常晴朗，天空湛蓝无云，微风拂面，令人感到心旷神怡。这种美好的天气让人忍不住想出去散步，享受大自然的宁静与美好。无论是在公园里漫步，还是在街道上行走，都能感受到阳光的温暖和空气的清新。这样的日子，正是放松心情、远离喧嚣的好时光。", lang="zh")
tts.save("output.mp3")
# 初始化 pygame 的音频模块
pygame.mixer.init()
pygame.mixer.music.load("output.mp3")
pygame.mixer.music.play()
# 等待音频播放完毕
while pygame.mixer.music.get_busy():
    time.sleep(0.5)
pygame.mixer.quit()