import cv2 as cv
import numpy as np

def calibrate_camera(video_file, board_pattern, board_cellsize):
    video = cv.VideoCapture(video_file)

    objp = np.zeros((board_pattern[0] * board_pattern[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:board_pattern[0], 0:board_pattern[1]].T.reshape(-1, 2)

    objpoints = []
    imgpoints = [] 

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    out = cv.VideoWriter('calibration_process.avi', cv.VideoWriter_fourcc(*'XVID'),5, (frame_width, frame_height))

    capture_photo = False
    while True:
        ret, frame = video.read()
        if not ret:
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        ret, corners = cv.findChessboardCorners(gray, board_pattern, None)
        if ret:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            cv.drawChessboardCorners(frame, board_pattern, corners2, ret)
            out.write(frame)

            if video.get(cv.CAP_PROP_POS_MSEC) >= 2000 and not capture_photo:
                cv.imwrite('sample_image.jpg', frame)
                capture_photo = True

    video.release()
    cv.destroyAllWindows()
    out.release()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error
    rmse = np.sqrt(mean_error / len(objpoints))

    return mtx, dist, rmse

def undistort_image(image, K, dist_coeff):
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(K, dist_coeff, (w, h), 1, (w, h))
    undistorted_image = cv.undistort(image, K, dist_coeff, None, new_camera_matrix)
    x, y, w, h = roi
    undistorted_image = undistorted_image[y:y+h, x:x+w]
    return undistorted_image

video_file = 'input.avi'
board_pattern = (9, 6) 
board_cellsize = 1.0 

K, dist_coeff, rmse = calibrate_camera(video_file, board_pattern, board_cellsize)

print("Camera matrix (K):")
print("fx:", K[0, 0])
print("fy:", K[1, 1])
print("cx:", K[0, 2])
print("cy:", K[1, 2])
print("RMSE:", rmse)

undistorted_image_file = 'undistorted_image.jpg'

image = cv.imread('sample_image.jpg')

undistorted_image = undistort_image(image, K, dist_coeff)

cv.imwrite(undistorted_image_file, undistorted_image)

print("Undistorted image saved as", undistorted_image_file)
