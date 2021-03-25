import os
import cv2
import sys
import glob
import numpy as np
import time


class Camera:
    def __init__(self, pipeline=0, api=None, scale: float = 1.0) -> None:
        print('hi')

        self.pipeline = pipeline
        self.api = api
        self.scale = scale

    def check_webcam_avalability(self, webcam: cv2.VideoCapture) -> None:
        if not webcam.isOpened():
            print("Error opening webcam")
            webcam.release()
            sys.exit(1)

    def check(self, char: str = 'q') -> bool:
        if cv2.waitKey(1) & 0xFF == ord(char):
            return True
        return False

    def set_scale(self, scale: float = 1.0):
        self.scale = scale

    def resize_dim(self, dim: tuple):
        if not isinstance(dim, tuple) or len(dim) != 2:
            print('Dimension must be a tuple and of lenght 2')
            sys.exit(1)
        return (int(dim[0] * self.scale), int(dim[1] * self.scale))

    def captureVideo(self, fps, save_dir: str = '', video_name: str = 'video', show_frame: bool = False, time: float = None) -> None:
        if not self.api:
            webcam = cv2.VideoCapture(self.pipeline)
        else:
            webcam = cv2.VideoCapture(self.pipeline, self.api)
        self.check_webcam_avalability(webcam)

        width, height = self.resize_dim(
            (int(webcam.get(3)), int(webcam.get(4))))

        if save_dir:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            vid_name = ''.join([video_name, '.avi'])
            path = '/'.join([save_dir, vid_name])
            out = cv2.VideoWriter(path, fourcc, fps, (width, height))
        while True:
            try:
                # capture each frame
                ret, frame = webcam.read()
                if not ret:
                    print('Could not get frame')
                    sys.exit(1)
                frame = cv2.resize(frame, (width, height))
                # display frame
                if show_frame:
                    cv2.imshow('Frame', frame)
                if save_dir:
                    out.write(frame)
                if self.check():
                    break
            except KeyboardInterrupt:
                print('Interrupted')
                break
        # After the loop release the video and out object
        webcam.release()
        if save_dir:
            out.release()
        # Destroy all windows
        cv2.destroyAllWindows()

    def captureImage(self, num_img: int = 1, fps: int = 1, save_dir='', img_name='img', file_type='.jpg', show_img=False) -> None:
        if not self.api:
            webcam = cv2.VideoCapture(self.pipeline)
        else:
            webcam = cv2.VideoCapture(self.pipeline, self.api)
        self.check_webcam_avalability(webcam)
        if show_img:
            time.sleep(fps)
        for i in range(num_img):
            try:
                ret, frame = webcam.read()
                if not ret:
                    print('Unable to get image')
                    sys.exit(1)
                if save_dir:
                    image_name = ''.join([img_name, '_', str(i), file_type])
                    path = '/'.join([save_dir, image_name])
                    cv2.imwrite(filename=path, img=frame)
                if show_img:
                    cv2.imshow("Captured Image", frame)
                    cv2.waitKey(int(fps * 1000))
                if self.check():
                    break
            except KeyboardInterrupt:
                print("Interrupted")
                break
        webcam.release()
        cv2.destroyAllWindows()
