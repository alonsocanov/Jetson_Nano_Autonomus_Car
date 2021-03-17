from camera import Camera


def main():

    camera = Camera(True, 'data/left', 'img')
    camera.captureImage(0, 1)


if __name__ == '__main__':

    main()
