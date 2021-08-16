
import cv2 as cv
import dlib
import threading
import time
import math
import face_recognition
from datetime import datetime
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
print("Keep your face in front of the webcam for the first 20 seconds until it activates")
timer = 0
No_face = 0
More_faces = 0
Frame_Count = 0
count1 = 0
count2 = 0
count3 = 0
count4 = 0
unregistered = 0
doubtful = 0
clean = 0
def timer():
    global time_count
    time_count = 60
    for i in range(60):
        time_count = time_count - 1
        print(time_count)
        time.sleep(1)
countdown_thread = threading.Thread(target = timer)
countdown_thread.start()

encodearr = []
flag = True
video_capture = cv.VideoCapture(0)
def distance(x1, y1, x2, y2):
    part1 = math.pow((x1-x2), 2)
    part2 = math.pow((y1-y2), 2)
    dist = math.pow((part1 + part2) , 0.5)
    return dist
def detect_faces(image):
    
    global encodearr
    global flag
    global count
    global encodes
    count = 0
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    RGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    haar_cascade = cv.CascadeClassifier('haar_face.xml')
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3)
    
    faces = face_recognition.face_locations(RGB)
    print("Number of faces found =", len(faces))
    if(len(faces)== 1 and flag==True):
        
        encodes = face_recognition.face_encodings(RGB)[0]
        count = count + 1
        flag = False

    
    for(x,y,w,h) in faces_rect:
        cv.rectangle(image, (x,y), (x+w, y+h), (0,255,0), thickness=2)
        
    cv.imshow("Your face", image)
while True:
    _, img = video_capture.read()
    
    detect_faces(img)
    
    if(cv.waitKey(1) and time_count==0):
        break


encodearrbest = [encodes]

cv.destroyAllWindows()
    
    

print("Exam starts...")
def check(mouth):
    count1 = mouth.count("closed")
    count2 = mouth.count("open")
    if(count1==8):
        print("Mouth Closed")
        print(mouth)
    elif(count2==8):
        print("Mouth open")
        print(mouth)
    elif(count2 != count1 and (count1==1 or count2==1)):
        print("Talking suspected")
        print(mouth)
    elif(count2 != count1 and (count1 > 1 or count2 > 1)):
        print("Talking confirmed")
        print(mouth)
mouth_Stats = []
fc = 0
def timer_count():
    global timer
    while (1<2):
        timer = timer + 1
        time.sleep(1)
    
countdown_thread = threading.Thread(target = timer_count)
countdown_thread.start()
    
def Exam_detector(image):
    global No_face
    global More_faces
    global Frame_Count
    global count1
    global count2
    global count3
    global count4
    global doubtful
    global clean
    global unregistered
    
    global mouth_Stats
    global fc
    
    
    Frame_Count = Frame_Count + 1
    
    
    global encodearrbest
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    RGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    
    
    faces = face_recognition.face_locations(RGB)
    encodeCur = face_recognition.face_encodings(RGB, faces)
    
    
    
    if len(faces)==0 :
        No_face = No_face + 1
        count1 = count1 + 1
        count3 = 0
        count4 = 0
        
        
        if(count1%10==0):
            print("Warning: No face detected for 10 continuous frames")
            count1 = 0
        count2 = 0
        
        
    if(len(faces)>1):
        More_faces = More_faces + 1
        count2 = count2 + 1
        if(count2%10==0):
            print("Warning: Multiple face detected for 10 continuous frames")
            count2 = 0
        count1 = 0
        
    if(len(faces)==1):
        count1 = 0
        count2 = 0
        
   
    for(top, right, bottom, left), enc in zip(faces, encodeCur):
        matches = face_recognition.compare_faces(encodearrbest, enc)
        
        face_distances = face_recognition.face_distance(encodearrbest, enc)
        
        if(face_distances <= 0.4):
            cv.rectangle(image, (left, top), (right, bottom), (0,255,0), thickness=2)
            if(len(faces)== 1):
                count3 = 0
                count4 = 0
                clean = clean + 1
                
                faces = detector(gray)
                for face in faces:
                    
                    landmarks = predictor(gray, face)
                    for n in range(48,68):
                        
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        cv.circle(image, (x,y), 4, (255,0,0), -1)
                if(len(faces)==1):
                    left_x1 = landmarks.part(61).x
                    left_x2 = landmarks.part(67).x
                    left_y1 = landmarks.part(61).y
                    left_y2 = landmarks.part(67).y
                    mid_x1 = landmarks.part(62).x
                    mid_x2 = landmarks.part(66).x
                    mid_y1 = landmarks.part(62).y
                    mid_y2 = landmarks.part(66).y
                    right_x1 = landmarks.part(63).x
                    right_x2 = landmarks.part(65).x
                    right_y1 = landmarks.part(63).y
                    right_y2 = landmarks.part(65).y
                    dist1 = distance(left_x1,left_y1,left_x2,left_y2)
                    dist2 = distance(mid_x1,mid_y1,mid_x2,mid_y2)
                    dist3 = distance(right_x1,right_y1,right_x2,right_y2)
                    if(dist1<=10 and dist2<=10 and dist3<=10 and fc<=8):
                        fc = fc + 1
                        mouth_Stats.append("closed")
                    elif(dist1>10 and dist2>10 and dist3>10 and fc<=8):
                        fc = fc + 1
                        mouth_Stats.append("open")
                    if(fc==8):
                        check(mouth_Stats)
                        mouth_Stats = []
                        fc = 0
                
        elif(face_distances>0.4 and face_distances<=0.5):
            cv.rectangle(image, (left, top), (right, bottom), (255,0,0), thickness=2)
            count3 = count3 + 1
            
            if(len(faces)==1):
                doubtful = doubtful + 1
                count4 = 0
        elif(face_distances > 0.5):
            cv.rectangle(image, (left, top), (right, bottom), (0,0,255), thickness=2)
            count4 = count4 + 1
            
            if(len(faces)==1):
                unregistered = unregistered + 1
                count3 = 0
    if(count3==4):
        print("Suspicious activity detected for 4 continuous frames!")
        count3 = 0
    if(count4==4):
        print("Unregistered face detected for 4 continuous frames!")
        count4 = 0

        
        
            
    cv.imshow("Your face", image)
        
now = datetime.now()

current_time = now.strftime("%H:%M:%S")        
while True:
    _, frame = video_capture.read()
    Exam_detector(frame)
    
        
    
    
    
    if(cv.waitKey(1) & 0xFF == ord('q')):
        time = timer
        now1 = datetime.now()
        current_time1 = now.strftime("%H:%M:%S")
        break



print("Exam starting time:", current_time)
print("Exam ending time:", current_time1)
print("Total no of frames=", Frame_Count)
print("Total no of no face frames=", No_face)
print("Total no of multi face frames(includes unregistered multifaces)=", More_faces)
print("Total no of single unregistered frames=", unregistered)
print("Total no of suspicious frames(single)=", doubtful)
print("Total no of clean frames=", clean)
video_capture.release()
cv.destroyAllWindows()
    
        
    
        
