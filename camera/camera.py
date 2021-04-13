import os
import cv2
import sys
import glob
import numpy as np
import time
from utils import sys_exit
import time


def checkDevice(source, api=None):
    if not api:
        cap = cv2.VideoCapture(source)
    else:
        cap = cv2.VideoCapture(source, api)
    if cap is None or not cap.isOpened():
        cap.release()
        message = 'Could not open video feed'
        sys_exit(message)
    return cap


def check_webcam_avalability(webcam: cv2.VideoCapture) -> None:
    if not webcam.isOpened():
        webcam.release()
        sys_exit(message)


def check_key(char: str = 'q') -> bool:
    if cv2.waitKey(1) & 0xFF == ord(char):
        return True
    return False


def scale(dim: tuple, scale: float = 1):
    if not isinstance(dim, tuple) or len(dim) != 2:
        message = ' '.join(['Dimension must be a tuple and of lenght 2:', dim])
        sys_exit(message)
    return(int(dim[0] * scale), int(dim[1] * scale))


def resize(img: np.ndarray, dim: tuple):
    if not isinstance(dim, tuple) or len(dim) != 2:
        message = ' '.join(['Dimension must be a tuple and of lenght 2:', dim])
        sys_exit(message)
    return cv2.resize(img, dim)


def save_video(file_path, dim, fps=24):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(file_path, fourcc, fps, (dim[0], dim[1]))
    return out


def captureVideo(pipeline, api=None, fps=24, path: str = '', show_frame: bool = True, vid_lenght: float = None):
    if not api:
        webcam = cv2.VideoCapture(pipeline)
    else:
        webcam = cv2.VideoCapture(pipeline, api)
    check_webcam_avalability(webcam)

    width, height = scale((int(webcam.get(3)), int(webcam.get(4))))

    if path:
        if not path.endswith('.avi'):
            path = ''.join(path, '.avi')
        out = save_video(path, (width, height), fps=24)
    if vid_lenght:
        t = time.time()
    while True:

        try:
            # capture each frame
            ret, frame = webcam.read()
            if not ret:
                message = 'Could not get frame'
                sys_exit(message)
            frame = resize(frame, (width, height))
            # display frame
            if show_frame:
                cv2.imshow('Frame', frame)
            if path:
                out.write(frame)
            if check_key():
                break
            if vid_lenght:
                if time.time() - t >= vid_lenght:
                    break

        except KeyboardInterrupt:
            print('Interrupted')
            break
    # After the loop release the video and out object
    webcam.release()
    if path:
        out.release()
    # Destroy all windows
    cv2.destroyAllWindows()


def captureImage(pipeline, api=None, num_img: int = 1, fps: int = 1, save_dir='', img_name: str = 'img', file_type: str = '.jpg', show_img: bool = True):
    flag_stetero = isinstance(pipeline, tuple) or isinstance(pipeline, list)
    flag_mono = isinstance(pipeline, str) or isinstance(pipeline, int)
    if not api:
        webcam = cv2.VideoCapture(pipeline)
    else:
        webcam = cv2.VideoCapture(pipeline, api)
    check_webcam_avalability(webcam)
    if show_img:
        time.sleep(fps)
    for i in range(num_img):
        try:
            ret, frame = webcam.read()
            if not ret:
                message = 'Unable to get image'
                sys_exit(message)

            if save_dir:
                image_name = ''.join([img_name, '_', str(i), file_type])
                path = '/'.join([save_dir, image_name])
                cv2.imwrite(filename=path, img=frame)
            if show_img:
                cv2.imshow("Captured Image", frame)
                cv2.waitKey(int(fps * 1000))
            if check_key():
                break
        except KeyboardInterrupt:
            print("Interrupted")
            break
    webcam.release()
    cv2.destroyAllWindows()


def stereoCapture(pipeline, api=None, num_img: int = 1, fps: int = 1, save_dir='', img_name='img', file_type='.jpg', show_img=True):
    if not api:
        webcam_1 = cv2.VideoCapture(pipeline[0])
        webcam_2 = cv2.VideoCapture(pipeline[1])
    else:
        webcam_1 = cv2.VideoCapture(pipeline[0], api)
        webcam_2 = cv2.VideoCapture(pipeline[1], api)
    check_webcam_avalability(webcam_1)
    check_webcam_avalability(webcam_2)
    if show_img:
        time.sleep(fps)
    for i in range(num_img):
        try:
            ret_1, frame_1 = webcam_1.read()
            ret_2, frame_2 = webcam_2.read()
            if not ret_1 or not ret_2:
                message = 'Unable to get image'
                sys_exit(message)

            if save_dir:
                image_name = ''.join([img_name, '_', str(i), file_type])
                path_1 = '/'.join([save_dir[0], image_name])
                path_2 = '/'.join([save_dir[1], image_name])
                cv2.imwrite(filename=path_1, img=frame)
                cv2.imwrite(filename=path_2, img=frame)
            if show_img:
                cv2.imshow("Captured Image", frame_1)
                cv2.waitKey(int(fps * 1000))
            if check_key():
                break
        except KeyboardInterrupt:
            print("Interrupted")
            break
    webcam_1.release()
    webcam_2.release()
    cv2.destroyAllWindows()
