import threading
from time import sleep
import sys
import numpy as np
import freenect
import cv2 
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
print ("Reseting servo 0")
kit.servo[0].angle=180
print ("Reseting servo 1")
kit.servo[1].angle=153
print ("Reseting servo 2")
kit.servo[2].angle=180
print ("Reseting servo 3")
kit.servo[3].angle=70
print ("Reseting servo 4")
kit.servo[4].angle=100
print ("Reseting servo 5")
kit.servo[5].angle=0

framekinectv1=None
depth=None
framecamera=None
framekinectv2=None
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
face_cascade_name = "/root/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier()
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print("Error loading xml file for face")
    exit(0)
else:
    print("Loaded xml file for face")

print("Loading camera")
sourcecamera = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=180, height=180, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=2  ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
if not sourcecamera.isOpened():
  print("Error: Could not open camera.")
  exit()
print("Loading Kinect V2")
disablekinectv2=0
sourcekinectv2 = cv2.VideoCapture(1)
if not sourcekinectv2.isOpened():
  print("Error: Could not open kinect v2, will disable it")
  disablekinectv2=1
  
def get_depth_data():
  depth, _ = freenect.sync_get_depth()
  depth = depth.astype(np.uint16)  # Ensure data type is correct
  depth >>= 3  # Remove the 3 lowest bits (might differ based on hardware)
  depth = depth.astype(np.uint8)  # Convert to uint8 for OpenCV visualization
  return depth

def moveservos(servo,angle):
    #move2=(150-xkinect+wkinect/2)
    #if move2<0:
    #  move2=0
    #if move2>180:
    #  move2=180
    #kit.servo[2].angle=move2 

    #move4=(180-ykinect+hkinect/2)
    #print ("move4=",move4)
    #if move4<0:
    #  move4=0
    #if move4>180:
    #  move4=180
    #print('Move4 [%d%%]\r'%move4, end="")
    #kit.servo[4].angle=100 
    
    #move5=(90-(xkinect+ykinect/2))
    #if move5<0:
    #  move5=0
    #if move5>180:
    #  move5=180
    #print('Move5 [%d%%]\r'%move5, end="")
    #kit.servo[5].angle=move5
    
    
    kit.servo[5].angle=angle
    print("\r>> Advancing servo 5 at angle ",angle, end='')
    kit.servo[4].angle=100

def display_video():
  angle=0
  while(True): 
    boxcamera=None
    boxkinectv1=None
    xkinect=None
    ykinect=None
    wkinect=None
    hkinect=None
    xcamera=None
    ycamera=None
    wcamera=None
    hcamera=None
    
    retcamera, framecamera = sourcecamera.read() 
    framecamera = cv2.resize(framecamera, (180,180))
    framecamera = cv2.flip(framecamera, 0)
    graycamera=cv2.cvtColor(framecamera,cv2.COLOR_BGR2GRAY)
    facescamera=face_cascade.detectMultiScale(graycamera,1.2,5)
    for (xcamera,ycamera,wcamera,hcamera) in facescamera:
       cv2.rectangle(framecamera,(xcamera,ycamera),(xcamera+wcamera,ycamera+hcamera),(0,0,255),4)
       boxcamera = (xcamera, ycamera, wcamera, hcamera)
    
    framekinectv1 = get_video()
    framekinectv1 = cv2.resize(framekinectv1, (180,180))
    graykinectv1=cv2.cvtColor(framekinectv1,cv2.COLOR_BGR2GRAY)
    faceskinectv1=face_cascade.detectMultiScale(graykinectv1,1.2,5)
    for (xkinect,ykinect,wkinect,hkinect) in faceskinectv1:
      cv2.rectangle(framekinectv1,(xkinect,ykinect),(xkinect+wkinect,ykinect+hkinect),(100,100,100),4)
      boxkinectv1 = (xkinect, ykinect, wkinect, hkinect)

    text=str(xkinect)+" "+str(ykinect)+" "+str(wkinect)+" "+str(hkinect)
    cv2.putText(framekinectv1, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow('Camera', framecamera)
    cv2.moveWindow('Camera', 100, 200)

    cv2.imshow('Camera Kinect V1', framekinectv1)
    cv2.moveWindow('Camera Kinect V1', 300, 200)
    
    #depth = get_depth()
    depth = get_depth_data()
    for depth_frame in get_depth_data():
      frame_blur = cv2.GaussianBlur(depth_frame, (5, 5), 0)
      ret, thresh = cv2.threshold(frame_blur, 100, 255, cv2.THRESH_BINARY)
      contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      if contours:
        max_contour = max(contours, key=cv2.contourArea)
        distance_mm = depth_frame[np.where(cv2.drawContours(np.zeros_like(depth_frame), [max_contour], 0, (255, 255, 255), thickness=cv2.FILLED))].mean()
        #print('Distance to closest object: ',distance_mm," mm\r", end="")
        #print('Distance to closest object: ',distance_mm)
    frame_contours = cv2.drawContours(depth_frame.copy(), [max_contour], -1, (0, 255, 0), 3)
    depth = cv2.resize(depth, (180,180))
    cv2.imshow('Depth kinect V1',depth)
    cv2.moveWindow('Depth kinect V1', 600, 200)
    
    if xcamera==None:
      print("Searching...")
      if xkinect!=None:
        moveservos(5,angle)
        angle=angle+3
        if angle>180:
          angle=0
    else:
      print("Found! :")
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
      vid.release() 
      cv2.destroyAllWindows() 
      break

servo_thread = threading.Thread(target=moveservos)
video_thread = threading.Thread(target=display_video)

servo_thread.start()
video_thread.start()

servo_thread.join()
video_thread.join()
