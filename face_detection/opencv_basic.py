import cv2
import os
PATH = os.getcwd()

cascade_filename = "cascade\\haarcascade_frontalface_default.xml"
cascade_filepath = os.path.join(PATH, cascade_filename)
if os.path.exists(cascade_filepath):
    # print("yes exist")
    cascade = cv2.CascadeClassifier(cascade_filepath)
    
image_path = "sample.jpg"
image = cv2.imread(image_path)

if image is not None:
    print('이미지가 성공적으로 로드되었습니다.')
else :
    print("이미지를 로드할 수 없습니다.")

pixel_value = image[200, 100]
print('특정 픽셀의 색상 값: ', pixel_value)

image[0:200, 0:100] = [0, 0, 255] # BGR 형식

cv2.putText(
            img = image, 
            text = 'Hello, OpenCV',
            org = (50, 50),
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 1,
            color = (255, 255, 255),
            thickness = 1
            )
faces = cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)
for (x,y,w,h) in faces:
    cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0, 0), 2)
# blurred_image = cv2.medianBlur(image, 5)
cv2.imshow('blurred_image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()