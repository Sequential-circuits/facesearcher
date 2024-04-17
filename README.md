# Robotic Arm Project

This is a project of a robotic arm which uses 2 cameras to search for a face and once it finds it locks on to it. I showed this at a presentation at the Bletchley Park AI user group. There is a demo video in this repo to get an idea of how it is made and works.

It uses both a camera and a 3D sensor of a Kinect. When the Kinect finds my face, it proceeds to move the arm until it is able to find it again using a camera at the tip of the arm. Once this 2nd camera finds my face, it locks on my face and stops searching.

It employs an Nvidia Jetson Nano 4 Gb attached to a PCA9685 board controlling 6 servos. I developed the software using Python and the libraries Adafruit ServoKit for the servos, OpenCV for the camera, and Freenect for the Kinect.

The system works by recognizing faces using the Xbox 360 camera. Once it finds it, it moves the robotic arm until the 2nd camera attached to the tip of the robot arm finds it too. Once that happens, it stops. The AI face recognition is a cheesy Haar Cascade (yup, that stuff is still around lol), but you can't ask much more from a humble Jetson :D

## Hardware Required:

- Nvidia Jetson Nano
- SSD card with Ubuntu 20.4 Focal installed that comes with Jetpack 4.6. Do NOT install any other Ubuntu as the camera will not work!
- Robotic Arm kit with 6 axis
- 6 servos
- PCA9685 controller
- Xbox Kinect 360 (NOT the Kinect One)
- Camera IMX219 with a long flat cable

You will have to install the libraries Adafruit ServoKit, OpenCV, and Freenect V1. There are excellent guides at [this link](https://naman5.wordpress.com/2014/06/24/experimenting-with-kinect-using-opencv-python-and-open-kinect-libfreenect/) for the Kinect and [this link](https://github.com/AnbuKumar-maker/AI-on-Jetson-Nano/blob/master/Installing%20PCA9685%20Motor%20Driver%20in%20Jetson%20Nano) for the controller and servos.

## TO DO:

1. Make the other axis work, as now it only works with 1.
2. Use the Kinect's depth sensor to measure the distance of the face and move the axis accordingly.
3. Recode this in C++ or Rust in order to make it faster.
