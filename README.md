# Drone_Face_Tracking

## How the face will be detected ?
Face detection is performed using Haar-Cascade . Here is a interesting read https://medium.com/dataseries/face-recognition-with-opencv-haar-cascade-a289b6ff042a#:~:text=Haar%20Cascade%20is%20a%20machine,of%20Simple%20Features%E2%80%9D%20in%202001.

## What is Face Tracking ?

Face Tracking Technology detects and tracks the presence of a human face in a digital video frame. This technology can be incorporated into computer and mobile applications, and can even be used in robotics.

## Drone used 
https://www.ryzerobotics.com/fr/tello

## For smooth Drone movements PID has been implemented
Watch this video to understand the concept of PID better https://www.youtube.com/watch?v=wkfEZmsQqiA&t=432s

## Logic behind the drone movements 
The centre of the face detected has to be alligned to the centre of the frame . Face tracking and drone movements are primarily based on this logic . 

## How to run the code ?
1. `pip install -r requirements_pip.txt`
2. Connect the tello drone from your system 
3. `python main.py`
