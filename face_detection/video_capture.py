import cv2
import timeit
import time
video = cv2.VideoCapture("sample.mp4")
prev_time = 0
FPS = 10
current_time = 0

while True:
    ret, frame = video.read()
    
    current_time = time.time() - prev_time
    
    if (ret is True) and (current_time > 1./FPS):
        cv2.imshow('video', frame)
        start_t = timeit.default_timer()
        """ 알고리즘 연산 """
        
        
        prev_time = time.time()
        cv2.imshow('video', frame)    
        """ 알고리즘 연산 """
        
        # 알고리즘 종료 시점
        terminate_t = timeit.default_timer()
        
        FPS = int(1./(terminate_t - start_t))
        
        print(FPS)
        if cv2.waitKey(1) > 0:
            break
        