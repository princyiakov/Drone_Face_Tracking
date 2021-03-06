from djitellopy import Tello
import cv2
import numpy as np
import face_recognition


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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(img)

        face_list = []
        face_area = []
        print(faces)
        for (top, right, bottom, left) in faces:
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.rectangle(img, (h, x), (y, w), (0, 255, 2), 2)
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 2), 2)
            w = right - left
            h = bottom - top
            cx = left + w // 2
            cy = top + h // 2
            area = w * h
            face_list.append([cx, cy])
            face_area.append(area)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if len(face_area) != 0:
            i = face_area.index(max(face_area))

            return img, [face_list[i], face_area[i]]

        else:
            return img, [[0, 0], 0]

    def track_face(self, info, w, h, pid, p_error, p_up_dwn_error, p_for_back_error):
        error_yaw = info[0][0] - w // 2
        error_up_dwn = 0
        error_for_back = 0
        speed_yaw = pid[0] * error_yaw + pid[2] * (error_yaw - p_error)
        speed_yaw = int(np.clip(speed_yaw, -50, 50))

        error_up_dwn = info[0][1] - h // 2
        speed_up_dwn = pid[0] * error_up_dwn + pid[2] * (error_up_dwn - p_up_dwn_error)
        speed_up_dwn = int(np.clip(speed_up_dwn, -10, 5))

        """error_for_back = info[1] - 9000
        speed_for_back = pid[0] * error_for_back + pid[2] * (error_for_back - p_for_back_error)
        speed_for_back = int(np.clip(speed_for_back, -10, 5))"""

        if info[0][0] != 0:
            self.yaw_velocity = speed_yaw
            self.up_down_velocity = - speed_up_dwn
            if info[1] > 10000:
                self.move('back', 20)
                print('Area is ', info[1], 'Moving Back')
            elif info[1] < 7000 :
                self.move('forward', 20)
                print('Area is ', info[1], 'Moving Forward')


        else:
            self.for_back_velocity = 0
            self.left_right_velocity = 0
            self.up_down_velocity = 0
            self.yaw_velocity = 0

        if self.send_rc_control:
            self.send_rc_control(self.left_right_velocity,
                                 self.for_back_velocity,
                                 self.up_down_velocity,
                                 self.yaw_velocity)

        return error_yaw, error_up_dwn, error_for_back
