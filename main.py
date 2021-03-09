from drone_haarcascade import MyDrone, cv2
import calendar
import time


def main():
    drone = MyDrone()
    p_error = 0
    p_up_dwn_error = 0
    p_for_back_error = 0
    pid = [0.5, 0, 0.5]
    w, h = 360, 240
    start_flight = 0  # Set 1 to not take off
    gmt = time.gmtime()
    ts = calendar.timegm(gmt)
    filenm = str(ts) + '.avi'
    out = cv2.VideoWriter(filenm, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (w, h))

    while True:
        if start_flight == 0:
            drone.takeoff()
            start_flight = 1
            drone.move('up', 100)
        img = drone.get_fame(w, h)
        img, info = drone.detect_face(img)
        print (info)
        p_error, p_up_dwn_error, p_for_back_error = drone.track_face(info, w, h, pid, p_error,
                                                                     p_up_dwn_error,
                                                                     p_for_back_error)
        out.write(img)
        cv2.imshow('Drone Output', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break
    out.release()
    drone.land()


if __name__ == '__main__':
    main()
