import json
from utils import directory
from camera.camera import Camera
import os

def main():

    path = directory()
    config_path = '/'.join([path, 'config', 'config.json'])
    path_cam_l = '/'.join([path, 'camera', 'data', 'left'])

    camera = Camera(True, path_cam_l, 'img_l')
    json_file = open(config_path)
    data = json.load(json_file)
    left_camera = data['waveshare_camera']['left']
    api_enum = data['waveshare_camera']['apiEnum']
    camera.captureImage(left_camera, api_enum, num_img=3)


if __name__ == '__main__':

    main()
