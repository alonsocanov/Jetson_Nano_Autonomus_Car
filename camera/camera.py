import os
import cv2
import sys
import glob
import numpy as np


class Camera:
    def __init__(self, pipeline = 0, api = None) -> None:

        self.pipeline = pipeline
        self.api = api


    def save_img(image, path):
        cv2.imwrite(filename=path, img=frame)


    def check_webcam_avalability(self, webcam: cv2.VideoCapture) -> None:
        if not webcam.isOpened():
            print("Error opening webcam")
            webcam.release()
            sys.exit(1)

    def check(self, char:str='q') -> bool:
        if cv2.waitKey(1) & 0xFF == ord(char):
            return True
        return False

    def capture_video(self, fps) -> None:
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
                    if self.check:
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

    def capture_image(self, num_img: int = 1, fps: int = 1, save_dir: str = '', img_name: str = '', file_type: str = '.jpg') -> None:
        if not self.api:
            webcam = cv2.VideoCapture(self.pipeline)
        else:
            webcam = cv2.VideoCapture(self.pipeline, self.api)
        self.check_webcam_avalability(webcam)
        # photo counter
        i = 1
        while i <= num_img:
            try:
                ret, frame = webcam.read()
                if not ret:
                    print('Could not get feed')
                    sys.exit(1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if np.mean(gray) < 90:
                    print('The image too dark, it will not be saved')

                elif save_dir and img_name:
                    img_name = ''.join([img_name, '_', str(i), file_type])
                    path = '/'.join([save_dir, img_name])
                    cv2.imwrite(filename=path, img=frame)
                    i += 1
                    print(path)
                # see image for fps * seconds
                cv2.waitKey(int(fps * 1000))

                if self.check:
                    break
            except KeyboardInterrupt:
                print("Interrupted")
                break
        webcam.release()
        cv2.destroyAllWindows()
