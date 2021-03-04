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

    @staticmethod
    def detect_face(img):
        face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(img_grey, 1.2, 4)
        face_list = []
        face_area = []

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cx = x + w // 2
            cy = y + h // 2
            area = w * h
            face_list.append([cx, cy])
            face_area.append(area)
        if len(face_area) != 0:
            i = face_area.index(max(face_area))

            return img, [face_list[i], face_area[i]]

        else:
            return img, [[0, 0], 0]
