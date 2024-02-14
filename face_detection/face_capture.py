import cv2
import numpy as np
import os

PATH = os.getcwd()

cascade_filename = "cascade\\haarcascade_frontalface_default.xml"

def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    face = cascade.detectMultiScale(gray, 1.3, 5)
    if len(face) == 0:
        return None
    else:
        for box in face:
            x,y,w,h = box
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 255), thickness=2)
            img_face = img[y:y+h, x:x+w]
        return img_face

cascade_filepath = os.path.join(PATH, cascade_filename)
# print(f'cascade_filepath:{cascade_filepath}')
if os.path.exists(cascade_filepath):
    # print("yes exist")
    cascade = cv2.CascadeClassifier(cascade_filepath)
else :
    print("cascade file not exist!!")

cap = cv2.VideoCapture(0)
n = 1
m = 1
cur_folder = f"training_data\\s{n}"
folder_path = os.path.join(PATH, cur_folder)
file_list = os.listdir(folder_path)
m = len(file_list)
while True:
    ret, frame = cap.read()
    img_face = face_extractor(frame)
    if img_face is not None :
        face = cv2.resize(img_face, (200, 200))
        if cv2.waitKey(1) > 0:
            m = m + 1            
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = os.path.join(folder_path , f'user_{m}.jpg')
            cv2.imwrite(file_name_path, face)            
            conv_img = cv2.imencode(".jpg", img_face)[1]
            
            data_encode = np.array(conv_img)
            img_data = data_encode.tobytes()
            # print(img_data)
        cv2.putText(frame, f"cur files list len:{m}" ,(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)            
        cv2.imshow("frame", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()