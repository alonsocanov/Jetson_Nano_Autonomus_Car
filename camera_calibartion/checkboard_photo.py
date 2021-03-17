from camera import Camera


def main():

    camera = Camera(True, 'data/left', 'img')
    GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink'
    camera.captureImage(0, 1)


if __name__ == '__main__':

    main()
