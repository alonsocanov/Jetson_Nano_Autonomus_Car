import os
import cv2
import sys
import glob
import numpy as np


class Camera:
    def __init__(self, save: bool = False, save_path: str = '', file_name: str = '') -> None:

        self._save = save
        self._file_name = file_name
        self._save_path = save_path
        self._cur_dir = os.path.abspath(os.path.dirname(__file__))
        if save_path:
            path = [self._cur_dir, self._save_path, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir, self._save_path]
            self._dir_path = '/'.join(path)
        else:
            path = [self._cur_dir, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir]
            self._dir_path = '/'.join(path)

    def check_webcam_avalability(self, webcam: cv2.VideoCapture) -> None:
        if not webcam.isOpened():
            print("Error opening webcam")
            sys.exit(1)

    @property
    def check_Q(self) -> bool:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    def captureVideo(self, fps) -> None:
        webcam = cv2.VideoCapture(0)
        width = int(webcam.get(3))
        height = int(webcam.get(4))

        self.check_webcam_avalability(webcam)
        if self._save:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            save_path = ''.join([self._file_path, '.avi'])
            out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))
        while True:
            try:
                # capture each frame
                ret, frame = webcam.read()
                if ret:
                    # display frame
                    cv2.imshow('Frame', frame)
                    if self._save:
                        out.write(frame)
                    if self.check_Q:
                        break
                else:
                    break
            except KeyboardInterrupt:
                print('Interrupted')
                break
        # After the loop release the video and out object
        webcam.release()
        if self._save:
            out.release()
        # Destroy all windows
        cv2.destroyAllWindows()

    def captureImage(self, pipeline, api = None, num_img: int = 1, fps: int = 1) -> None:
        # webcam = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)20/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)
        if not api:
            webcam = cv2.VideoCapture(pipeline)
        else:
            webcam = cv2.VideoCapture(pipeline, api)

        self.check_webcam_avalability(webcam)
        # number of photos to take
        cv2.waitKey(3000)
        for i in range(num_img):
            try:
                ret, frame = webcam.read()
                if not ret:
                    print('Could not get feed')
                    sys.exit(1)

                # cv2.imshow("Captured Image", frame)
                if self._save:
                    print('Saving image...')
                    path = ''.join([self._file_path, '_', str(i), '.jpg'])
                    print(path)
                    cv2.imwrite(filename=path, img=frame)
                # see image for 2 seconds
                # cv2.waitKey(int(fps * 1000))
                if self.check_Q:
                    break
            except KeyboardInterrupt:
                print("Interrupted")
                break
        webcam.release()
        cv2.destroyAllWindows()
