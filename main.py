from drone import MyDrone, cv2


def main():

    drone = MyDrone()

    while True:
        img = drone.get_fame()
        cv2.imshow('Drone Output', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break


if __name__ == '__main__':
    main()
