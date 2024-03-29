# opencv_camera_calibration_and_distortion_correction


### 🖥 About project
- This project uses opencv to calibrate checkered images and alleviate camera curvature.

### 🕰 ️develop period
- 24/03/29   ~   24/03/29

### ⚙️ Development environment
- `python 3.11.5`
- **IDE** : Spyder

### 📋 Before exqution
 1. install OpenCV
-install opencv using your IDE's terminal
    ```python
    pip install opencv-python
    ```


### 📌 How to use

1. name the video ‘input.mp4’ and place it in the same location as the Python file.
2. run 'calibration.py'
3. a video will be created with the name 'calibration_process.avi', 'sample image', 'undistorted_image'.

### 💬camera calibration results
- fx: 220.4537306693774
- fy: 215.2506283623212
- cx: 189.38590665093488
- cy: 485.6445089225087
- RMSE: 0.23069927309910718

### 😄example image of distortion correction
- before
 
![sample_image](https://github.com/ywoolee/opencv_camera_calibration_and_distortion_correction/assets/68912105/6820ccb3-9b02-4d0d-9b45-3dbfc23a7dfa)

- after

![undistorted_image](https://github.com/ywoolee/opencv_camera_calibration_and_distortion_correction/assets/68912105/76cae424-fe5b-4e02-bd54-7f9b2e7954cb)
