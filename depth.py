import camera.stereo as stereo
import camera.calibrate as calibrate
import files_management
from matplotlib import pyplot as plt
from matplotlib import patches

# Use regular numpy notation instead of scientific one
np.set_printoptions(suppress=True)

# Read the stereo-pair of images
img_left = files_management.read_left_image()
img_right = files_management.read_right_image()


# Large plot of the left image
plt.figure(figsize=(16, 12), dpi=100)
plt.imshow(img_left)

# Read the calibration
p_left, p_right = files_management.get_projection_matrices()

print("p_left \n", p_left)
print("\np_right \n", p_right)


disp_left = stereo.compute_left_disparity_map(img_left, img_right)

# Show the left disparity map
plt.figure(figsize=(10, 10))
plt.imshow(disp_left)
plt.show()

# Decompose each matrix
k_left, r_left, t_left = stereo.decompose_projection_matrix(p_left)
k_right, r_right, t_right = stereo.decompose_projection_matrix(p_right)

# Display the matrices
print("k_left \n", k_left)
print("\nr_left \n", r_left)
print("\nt_left \n", t_left)
print("\nk_right \n", k_right)
print("\nr_right \n", r_right)
print("\nt_right \n", t_right)


# Get the depth map by calling the above function
depth_map_left = stereo.calc_depth_map(disp_left, k_left, t_left, t_right)


# Display the depth map
plt.figure(figsize=(8, 8), dpi=100)
plt.imshow(depth_map_left, cmap='flag')
plt.show()

# Get the image of the obstacle
obstacle_image = files_management.get_obstacle_image()

# Show the obstacle image
plt.figure(figsize=(4, 4))
plt.imshow(obstacle_image)
plt.show()


# Gather the cross correlation map and the obstacle location in the image
cross_corr_map, obstacle_location = stereo.locate_obstacle_in_image(
    img_left, obstacle_image)

# Display the cross correlation heatmap
plt.figure(figsize=(10, 10))
plt.imshow(cross_corr_map)
plt.show()

# Print the obstacle location
print("obstacle_location \n", obstacle_location)


# Use the developed nearest point function to get the closest point depth and obstacle bounding box
closest_point_depth, obstacle_bbox = stereo.calculate_nearest_point(
    depth_map_left, obstacle_location, obstacle_image)

# Display the image with the bounding box displayed
fig, ax = plt.subplots(1, figsize=(10, 10))
ax.imshow(img_left)
ax.add_patch(obstacle_bbox)
plt.show()

# Print the depth of the nearest point
print("closest_point_depth {0:0.3f}".format(closest_point_depth))
