from djitellopy import Tello
import cv2


class MyDrone(Tello):
    def __init__(self):
        super().__init__()
        self.my_drone = Tello()
        self.my_drone.connect()
        self.my_drone.for_back_velocity = 0
        self.my_drone.left_right_velocity = 0
        self.my_drone.up_down_velocity = 0
        self.my_drone.yawn_velocity = 0
        self.my_drone.speed = 0
        self.my_drone.streamoff()
        self.my_drone.streamon()
        print(self.my_drone.get_battery())

    def get_fame(self):
        frame = self.my_drone.get_frame_read()
        frame = frame.frame
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resizing both axes by 1/4

        return frame
