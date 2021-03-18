from camera import Camera
import json


def main():

    camera = Camera(True, 'data/left', 'img')
    json_file = open('../config/config.json')
    data = json.load(json_file)
    left_camera = data['waveshare_camera']['left']
    api_enum = data['waveshare_camera']['apiEnum']
    camera.captureImage(left_camera, api_enum, num_img=3)


if __name__ == '__main__':

    main()
