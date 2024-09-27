import snowboydecoder


    
detector = snowboydecoder.HotwordDetector("smart_guardian.pmdl", sensitivity=0.5)

def detected_callback():
    print("已被唤醒")

def interrupt_callback():
    global interrupted
    return interrupted


def main():

    while True:
        print("Start Listen!")
        try:
            detector.start(detected_callback=detected_callback,
                           interrupt_check=interrupt_callback,
                           sleep_time=0.03)
        finally:
            detector.terminate()
