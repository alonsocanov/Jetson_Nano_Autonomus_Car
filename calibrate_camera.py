import json
from utils import directory
from camera.camera import Camera
from camera.calibrate import Calibrate
import os
import time
import argparse

def main():
    path = directory()
    config_path = '/'.join([path, 'config', 'config.json'])
    path_cam_l = '/'.join([path, 'camera', 'waveshare', 'left'])
    path_cam_r = '/'.join([path, 'camera', 'waveshare', 'right'])

    json_file = open(config_path)
    data = json.load(json_file)

    parser = argparse.ArgumentParser(description='Camera Calibration')
    parser.add_argument('--calibrate', type=str, default='None',
                        help='Chose how many pictures to take')
    parser.add_argument('--camera', type=str, default='None',
                        help='Chose camera to calibrate (left, right or both)')
    parser.add_argument('--num_images', type=int, default=0,
                        help='Chose how many pictures to take')
    args = parser.parse_args()



    if args.camera == 'left' or args.camera == 'both' and args.num_images:
        time.sleep(5)
        camera = Camera(True, path_cam_l, 'img_l')
        left_camera = data['waveshare_camera']['left']
        api_enum = data['waveshare_camera']['apiEnum']
        camera.captureImage(left_camera, api_enum, num_img=args.num_images)

    if args.camera == 'right' or args.camera == 'both' and args.num_images:
        time.sleep(5)
        camera = Camera(True, path_cam_r, 'img_r')
        left_camera = data['waveshare_camera']['right']
        api_enum = data['waveshare_camera']['apiEnum']
        camera.captureImage(left_camera, api_enum, num_img=args.num_images)

    if args.calibrate == 'left':
        left_img = Calibrate(True, path_cam_l)
        left_img.calibrate(fish_eye=False, num_rows=9, num_cols=6, dimension=30)









if __name__ == '__main__':

    main()
