import cv2

def videoDetector(cam, cascade):
    while True:
        ret, img = cam.read()
        #print(img.shape())
        img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        results = cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(20, 20))

        for box in results:
            x,y,w,h = box
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255), thickness=2)
            
        cv2.imshow('facenet', img)
        if cv2.waitKey(1) > 0:
            break
        
def imgDetector(img, cascade):
    img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
cascade_filename = "haarcascade_frontalface_alt.xml"

cascade = cv2.CascadeClassifier(cascade_filename)

cam = cv2.VideoCapture("./sample.mp4")

# img = cv2.imread("sample.jpg")

videoDetector(cam, cascade)