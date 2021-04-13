import camera.stereo as stereo
import camera.calibrate as calibrate
from camera.camera import captureImage
import utils
import cv2
from matplotlib import pyplot as plt
from matplotlib import patches
import argparse


def main():

    parser = argparse.ArgumentParser()
    # file path argument
    parser.add_argument("--img_dir", type=str, default='data/images/IMX219-83',
                        help="directory of images")
    parser.add_argument("--take_img", type=str, default='False',
                        help="Take depth images")
    parser.add_argument("--img_ext", type=str, default='.jpg',
                        help="Images extention")
    parser.add_argument("--show_plt", type=str, default='False',
                        help="Show plots")

    # create argument object
    args = parser.parse_args()

    camera_data = utils.read_json('config/jetson/config.json')

    left_pipeline = camera_data['waveshare_camera']['left']
    right_pipeline = camera_data['waveshare_camera']['right']
    api = camera_data['waveshare_camera']['apiEnum']

    utils.check_directory(args.img_dir)
    if args.take_img == 'True':
        captureImage(left_pipeline, api=api,  save_dir=args.img_dir,
                     img_name='img_l', show_img=False)
        captureImage(right_pipeline, api=api, save_dir=args.img_dir,
                     img_name='img_r', show_img=False)

    # Read the stereo-pair of images
    images = utils.files_in_dir(args.img_dir, args.img_ext)
    assert len(images) == 2
    img_left = cv2.cvtColor(cv2.imread(images[0]), cv2.COLOR_RGB2BGR)
    img_right = cv2.cvtColor(cv2.imread(images[1]), cv2.COLOR_RGB2BGR)

    if args.show_plt == 'True':
        # Large plot of the left image
        plt.figure(figsize=(10, 10), dpi=100)
        plt.imshow(img_left)
        plt.show()

    disp_left = stereo.compute_left_disparity_map(img_left, img_right)

    if args.show_plt == 'True':
        # Show the left disparity map
        plt.figure(figsize=(10, 10))
        plt.imshow(disp_left)
        plt.show()

    # Read the calibration
    # p_left, p_right = files_management.get_projection_matrices()

    # print("p_left \n", p_left)
    # print("\np_right \n", p_right)

    # # Decompose each matrix
    # k_left, r_left, t_left = stereo.decompose_projection_matrix(p_left)
    # k_right, r_right, t_right = stereo.decompose_projection_matrix(p_right)

    # # Display the matrices
    # print("k_left \n", k_left)
    # print("\nr_left \n", r_left)
    # print("\nt_left \n", t_left)
    # print("\nk_right \n", k_right)
    # print("\nr_right \n", r_right)
    # print("\nt_right \n", t_right)

    # Get the depth map by calling the above function
    # depth_map_left = stereo.calc_depth_map(disp_left, k_left, t_left, t_right)

    # # Display the depth map
    # plt.figure(figsize=(8, 8), dpi=100)
    # plt.imshow(depth_map_left, cmap='flag')
    # plt.show()

    # # Get the image of the obstacle
    # obstacle_image = files_management.get_obstacle_image()

    # # Show the obstacle image
    # plt.figure(figsize=(4, 4))
    # plt.imshow(obstacle_image)
    # plt.show()

    # # Gather the cross correlation map and the obstacle location in the image
    # cross_corr_map, obstacle_location = stereo.locate_obstacle_in_image(
    #     img_left, obstacle_image)

    # # Display the cross correlation heatmap
    # plt.figure(figsize=(10, 10))
    # plt.imshow(cross_corr_map)
    # plt.show()

    # # Print the obstacle location
    # print("obstacle_location \n", obstacle_location)

    # # Use the developed nearest point function to get the closest point depth and obstacle bounding box
    # closest_point_depth, obstacle_bbox = stereo.calculate_nearest_point(
    #     depth_map_left, obstacle_location, obstacle_image)

    # # Display the image with the bounding box displayed
    # fig, ax = plt.subplots(1, figsize=(10, 10))
    # ax.imshow(img_left)
    # ax.add_patch(obstacle_bbox)
    # plt.show()

    # # Print the depth of the nearest point
    # print("closest_point_depth {0:0.3f}".format(closest_point_depth))


if __name__ == '__main__':
    main()
