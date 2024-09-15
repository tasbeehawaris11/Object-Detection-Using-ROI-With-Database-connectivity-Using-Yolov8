# Object-Detection-Using-ROI-With-Database-connectivity-Using-Yolov8

Object Detection and Cropping with ROI Selection
This project implements an object detection and cropping script using YOLOv8 and OpenCV. It allows you to define a Region of Interest (ROI) in a video and save detected objects within that region.
Functionality
Object Detection: The script utilizes YOLOv8 to detect objects in a video stream.
ROI Selection: Users can define a rectangular ROI by clicking and dragging on the video frame.
Object Cropping: Detected objects within the defined ROI are cropped and saved as separate images.
Database Storage: Information about the cropped objects (image path) can be stored in a MySQL database (optional).
Requirements
Python 3.x
OpenCV (cv2)
Ultralytics (for YOLOv8)
mysql-connector-python (for database connection - optional)
Installation
Install required libraries using pip:

Bash


pip install opencv-python ultralytics mysql-connector-python


Download a pre-trained YOLOv8 model (e.g., yolov8n.pt) from the Ultralytics repository: [invalid URL removed]
Usage
Update the script with your desired video path (video_path) and output directory (output_dir).
(Optional) If using a database, modify the database connection details (host, user, password, database) at the beginning of the script.
Run the script:

Bash


python your_script_name.py


How to Use ROI Selection:
Open the video window titled "Detection".
Click and drag your mouse to define a rectangular area as the ROI.
The script will show a live preview with the ROI highlighted.
Detected objects within the ROI will be saved as separate images.

