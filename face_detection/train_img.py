import os
import cv2
import numpy as np

PATH = os.getcwd()

cascade_filename = "cascade\\haarcascade_frontalface_default.xml"
cascade_filepath = os.path.join(PATH, cascade_filename)
# print(f'cascade_filepath:{cascade_filepath}')
if os.path.exists(cascade_filepath):
    # print("yes exist")
    cascade = cv2.CascadeClassifier(cascade_filepath)
else :
    print("cascade file not exist!!")
"""
얼굴을 찾아 이미지를 가져온다.
"""
def detect_face(img):
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None
    
    #under the assumption that there will be only one face,
    #extract the face area
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]

"""
화면에 사각형을 표시한다.
"""
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #let's detect multiscale (some images may be closer to camera than others) images
    #result is a list of faces
    faces = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    
    if faces is():
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (400,500))
    (x, y, w, h) = faces[0]
    
    #return only the face part of the image
    return img,roi

def prepare_training_data(data_folder_path):
    #--STEP-1--
    # get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)
    
    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []
    print(1)
    #let's go through each directory and read images within it
    for dir_name in dirs:
        print(2, "/", dir_name)
        # our subject directories start with letter 's' so
        #ignore any non-relevant directories if any
        if not dir_name.startswith('s'):
            print("2-1")
            continue
        
        #--STEP-2--
        #extract label number of subject from dir_name
        #format of dir name = slabel
        #, so removing letter 's' from dir_name will give us label
        label = int(dir_name.replace("s", ""))
        
        #build path of directory contain images for current subject
        #sample subject_dir_path = "training_data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name
        
        # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        
        #--STEP-3--
        #go through each image name, read image,
        #detect face and add face to list of faces
        for image_name in subject_images_names:
            #print("3")
            #ignore system files like .DS_Store
            if image_name.startswith("."):
                #print("3-1")
                continue
            
            #build image path
            #sample image path=training_data/s1/user_1.jpg
            image_path = subject_dir_path + "/" + image_name
            
            #read image
            image = cv2.imread(image_path)
            
            #display an image window to show the image
            cv2.imshow("Training on image ..", cv2.resize(image, (400, 500)))
            cv2.waitKey(100)
            
            #detect face
            face, rect = detect_face(image)
            
            #--STEP-4--
            # for the purpose of this tutorial
            # we will ignore faces that are not detected
            if face is not None:
                # add face to list of faces
                faces.append(face)
                labels.append(label)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels

model = cv2.face.LBPHFaceRecognizer_create()

faces, labels = prepare_training_data(os.path.join(PATH, "training_data"))
print("############labels###############")
print(labels)
print("#################################")
model.train(faces, np.array(labels))
print("train is completed!!")
#카메라 열기
cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()
    
    #얼굴 검출해내기
    image, unknownface = face_detector(frame)
    
    try:
        # 검출된 사진을 흑백으로 전환
        unknownface = cv2.cvtColor(unknownface, cv2.COLOR_BGR2GRAY)
        result = model.predict(unknownface)
        
        if result[1] < 500:            
            confidence = int(100 * (1-(result[1])/300))
            display_string = str(confidence)+'% Confidence it is ' + str(result[0])
        cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)
        
        if confidence > 70:
            
            cv2.putText(image, "Hi Member!", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Face Cropper", image)
        else :
            
            cv2.putText(image, "Not Member!", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Face Cropper", image)
    except :
        
        #print(RuntimeError)
        cv2.putText(image, "Face Not Found!", (400, 500), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Face Cropper", image)
        pass
    
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()

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