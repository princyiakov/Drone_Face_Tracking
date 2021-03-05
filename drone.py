from djitellopy import Tello
import cv2
import numpy as np


class MyDrone(Tello):
    def __init__(self):
        super().__init__()
        self.connect()
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 0
        self.streamoff()
        self.streamon()
        print(self.get_battery())

    def get_fame(self, w, h):
        frame = self.get_frame_read()
        frame = frame.frame
        frame = cv2.resize(frame, (w, h))

        return frame

    @staticmethod
    def detect_face(img):
        face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(img_grey, 1.2, 3)
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

    def track_face(self, info, w, h, pid, p_error, p_up_dwn_error, p_for_back_error):
        error_yaw = info[0][0] - w // 2
        speed_yaw = pid[0] * error_yaw + pid[2] * (error_yaw - p_error)
        speed_yaw = int(np.clip(speed_yaw, -100, 100))

        error_up_dwn = info[0][1] - h // 2
        speed_up_dwn = pid[0] * error_up_dwn + pid[2] * (error_up_dwn - p_up_dwn_error)
        speed_up_dwn = int(np.clip(speed_up_dwn, -100, 100))

        error_for_back = info[1] - 5000
        speed_for_back = pid[0] * error_for_back + pid[2] * (error_for_back - p_for_back_error)
        speed_for_back = int(np.clip(speed_for_back, -100, 100))

        if info[0][0] != 0:
            self.yaw_velocity = speed_yaw
            self.up_down_velocity = - speed_up_dwn
            self.for_back_velocity = speed_for_back

        else:
            self.for_back_velocity = 0
            self.left_right_velocity = 0
            self.up_down_velocity = 0
            self.yaw_velocity = 0
            error_x = 0

        if self.send_rc_control:
            self.send_rc_control(self.left_right_velocity,
                                 self.for_back_velocity,
                                 self.up_down_velocity,
                                 self.yaw_velocity)

        return error_yaw, error_up_dwn, error_for_back
