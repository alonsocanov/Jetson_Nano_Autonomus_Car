import os
import cv2
import sys
import glob
import numpy as np
from camera import Camera


class Calibrate:
    def __init__(self, save: bool = False, path: str = '', file_name: str = '') -> None:
        self._save = save
        self._file_name = file_name
        self._path = path
        self._cur_dir = os.path.abspath(os.path.dirname(__file__))
        if path:
            path = [self._cur_dir, self._path, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir, self._path]
            self._dir_path = '/'.join(path)
        else:
            path = [self._cur_dir, self._file_name]
            self._file_path = '/'.join(path)
            path = [self._cur_dir]
            self._dir_path = '/'.join(path)

        self._mtx_file = 'camera_matrix.txt'
        self._new_mtx_file = 'new_camera_matrix.txt'
        self._dist_file = 'camera_distortion.txt'
        self._roi_file = 'region_of_interest.txt'

    @property
    def check_Q(self) -> bool:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    @property
    def directoy_path(self) -> None:
        return self._dir_path

    @property
    def file_path(self) -> None:
        return self._file_path

    @property
    def current_directory(self) -> None:
        return self._cur_dir

    @property
    def mtx(self):
        mtx_path = '/'.join([self.directoy_path, self._mtx_file])
        try:
            mtx = np.loadtxt(mtx_path, dtype=np.float32, delimiter=',')
        except:
            mtx = np.eye(3)
        return mtx

    @property
    def new_mtx(self):
        new_mtx_path = '/'.join([self.directoy_path, self._new_mtx_file])
        try:
            new_mtx = np.loadtxt(new_mtx_path, dtype=np.float32, delimiter=',')
        except:
            new_mtx = np.eye(3)
        return new_mtx

    @property
    def dist(self):
        dist_path = '/'.join([self.directoy_path, self._dist_file])
        try:
            dist = np.loadtxt(dist_path, dtype=np.float32, delimiter=',')
        except:
            dist = np.zeros((1, 4))
        return dist

    @property
    def roi(self):
        roi_path = '/'.join([self.directoy_path, self._roi_file])
        try:
            roi = np.loadtxt(roi_path, dtype=np.float32, delimiter=',')
        except:
            roi = np.array([0, 0, 0, 0])
        return roi

    def distortion_mean(self, obj_pts, img_pts, rvecs, tvecs, mtx, dist) -> None:
        mean_error = 0
        for i in range(len(obj_pts)):
            img_pts2, _ = cv2.projectPoints(
                obj_pts[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(img_pts[i], img_pts2, cv2.NORM_L2) / len(img_pts2)
            mean_error += error
        return mean_error / len(obj_pts)

    def saveData(self, mtx: np.array = None, new_mtx: np.array = None, dist: np.array = None, roi: np.array = None) -> None:

        if mtx is not None:
            cam_mtx = '/'.join([self._dir_path, self._mtx_file])
            np.savetxt(cam_mtx, mtx, delimiter=',')
        if new_mtx is not None:
            new_cam_mtx = '/'.join([self._dir_path, self._new_mtx_file])
            np.savetxt(new_cam_mtx, new_mtx, delimiter=',')
        if dist is not None:
            cam_dist = '/'.join([self._dir_path, self._dist_file])
            np.savetxt(cam_dist, dist, delimiter=',')
        if roi is not None:
            reg_interest = '/'.join([self._dir_path, self._roi_file])
            np.savetxt(reg_interest, roi, delimiter=',')

    def crop(self, img: np.array, x: int, y: int, w: int, h: int):
        w, h, _ = img.shape
        img = img[y:h, x:w, :]
        # Resize the image
        img = cv2.resize(img, (h, w))
        return img

    def calibrate(self, fish_eye=False, num_rows: int = 9, num_cols: int = 6, dimension: int = 30, extension: str = 'jpg', show_img: bool = False) -> None:
        mtx, new_mtx, dist, roi = None, None, None, None
        path = ''.join([self._dir_path, '/*.', extension])
        images = glob.glob(path)
        flag_img = False
        # chessboard grid
        grid = (num_cols, num_rows)
        # filter size
        filt = (5, 5)
        # prepare object points
        objp = np.zeros((1, num_cols * num_rows, 3), np.float32)
        objp[0, :, :2] = np.mgrid[0:num_cols, 0:num_rows].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        # 3d point in real world space
        obj_pts = []
        # 2d points in image plane.
        img_pts = []
        # number of imges
        print('Provided images: ', len(images))
        if len(images) < 9:
            print('Not enough images, at least 9 images must be given')
            sys.exit()

        for image in images:
            # termination criteria
            criteria = (cv2.TERM_CRITERIA_EPS +
                        cv2.TERM_CRITERIA_MAX_ITER, dimension, .1)
            # Read Image
            img = cv2.imread(image)
            # convert to gray scale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(
                gray, grid, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            # If found, add object points, image points (after refining them)
            if ret:
                obj_pts.append(objp)
                corners2 = cv2.cornerSubPix(
                    gray, corners, filt, (-1, -1), criteria)
                img_pts.append(corners2)
                # Draw and display the corners
                if show_img:
                    img = cv2.drawChessboardCorners(img, grid, corners2, ret)
                    cv2.imshow('img', img)
                    cv2.waitKey(500)
            else:
                pass

        cv2.destroyAllWindows()

        print('Useful images: ', len(obj_pts))
        print('Image dimensions: ', img.shape)

        h, w, _ = img.shape
        num_obj_pts = len(obj_pts)

        if num_obj_pts > 1:
            flag_img = True
            if not fish_eye:
                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
                    obj_pts, img_pts, (w, h), None, None)
                new_mtx, roi = cv2.getOptimalNewCameraMatrix(
                    mtx, dist, (w, h), 1, (w, h))

            elif fish_eye:
                calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC + \
                    cv2.fisheye.CALIB_CHECK_COND + cv2.fisheye.CALIB_FIX_SKEW
                criteria = (cv2.TERM_CRITERIA_EPS +
                            cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)

                mtx = np.zeros((3, 3))
                dist = np.zeros((4, 1))
                new_mtx = np.eye(3)
                rvecs = [np.zeros((1, 1, 3), dtype=np.float64)
                         for i in range(num_obj_pts)]
                tvecs = [np.zeros((1, 1, 3), dtype=np.float64)
                         for i in range(num_obj_pts)]
                rms, _, _, _, _ = cv2.fisheye.calibrate(
                    obj_pts, img_pts, (w, h), mtx, dist, rvecs, tvecs, calibration_flags, criteria)
                dist = np.transpose(dist)
        else:
            print('Not enough images')
            mtx, new_mtx = np.eye(3), np.eye(3)
            dist = np.zeros((1, 4))
            roi = (0, 0, w, h)

        print('Calibration Matrix: ')
        print(mtx)
        print('Disortion: ')
        print(dist)
        # Distortion Error
        if flag_img:
            error = self.distortion_mean(
                obj_pts, img_pts, rvecs, tvecs, mtx, dist)
            print('Total error: ', error)
            # save resuts in a .txt file
            self.saveData(mtx, new_mtx, dist, roi)

    def undisort(self, img: np.array, mtx: np.array, new_mtx: np.array, dist: np.array, roi: np.array = None, fish_eye: bool = False) -> np.array:
        h, w, _ = img.shape
        if not fish_eye:
            undisorted_img = cv2.undistort(img, mtx, dist, None, new_mtx)
            # Crop image (region of interesest)
            if roi[0]:
                x, y, w, h = roi.astype(int)
                undisorted_img = self.crop(undisorted_img, x, y, w, h)
        if fish_eye:
            balance = 1
            dim1 = img.shape[:2][::-1]
            dim2 = (int(dim1[0] / 1.1), int(dim1[1] / 1.1))
            dim3 = (int(dim1[0] / 1), int(dim1[1] / 1))

            if dim2 is None:
                dim2 = dim1
            if dim3 is None:
                dim3 = dim1

            scaled_mtx = mtx * dim1[0] / w
            scaled_mtx[2][2] = 1

            new_mtx = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(
                scaled_mtx, dist, dim2, np.eye(3), balance=balance)
            mapx, mapy = cv2.fisheye.initUndistortRectifyMap(
                scaled_mtx, dist, np.eye(3), new_mtx, dim3, cv2.CV_16SC2)
            undisorted_img = cv2.remap(
                img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undisorted_img
