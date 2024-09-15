import cv2 as cv
import numpy as np
from ultralytics import YOLO
import mysql.connector
import os

# Connect to the database
db_connection = mysql.connector.connect(
    host="host",
    user="user",
    password="password",
    database="database"
)

cursor = db_connection.cursor()

# Global variables for drawing rectangle
start_line = [0, 0]
end_line = [0, 0]
draw = False
roi_defined = False  # To check if ROI is defined

# Mouse callback function for drawing the rectangle
def draw_rectangle(event, x, y, flags, param):
    global start_line, end_line, draw, frame, roi_defined
    if event == cv.EVENT_LBUTTONDOWN:
        draw = True
        start_line[0], start_line[1] = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if draw:
            frame_copy = frame.copy()  # Make a copy of the frame
            cv.rectangle(frame_copy, tuple(start_line), (x, y), (255, 255, 4), 3)
            cv.imshow("Detection", frame_copy)

    elif event == cv.EVENT_LBUTTONUP:
        draw = False
        end_line[0], end_line[1] = x, y
        roi_defined = True  # Set the flag to indicate ROI is defined
        cv.rectangle(frame, tuple(start_line), (x, y), (255, 255, 4), 3)  # Draw final rectangle

def save_detected_object( image_path):
    insert_query = """INSERT INTO image (cropped_object) VALUES ( %s)"""
    data = ( image_path,)
    cursor.execute(insert_query, data)
    db_connection.commit()

def video_process(video_path, output_dir, model):
    global frame
    frame_count = 0
    saved_objects = set()
    cap = cv.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Draw the ROI if defined
        if roi_defined:
            cv.rectangle(frame, tuple(start_line), tuple(end_line), (255, 255, 4), 3)

        # Perform object detection and tracking
        results = model.track(source=frame, persist=True)

        if results is not None:
            boxes = results[0].boxes.xyxy.cpu().tolist()
            ids = results[0].boxes.id.numpy()
            class_names = results[0].names

            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = map(int, box)
                obj_id = ids[i]

                # Check if the detected object is inside the ROI
                if roi_defined and is_inside_roi(x1, y1, x2, y2):
                    # Check if this object ID has already been saved
                    if obj_id not in saved_objects:
                        # Draw the bounding box on the frame
                        cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 250), 3)

                        # Crop the detected object
                        cropped_object = frame[y1:y2, x1:x2]

                        # Save the cropped object as an image
                        crop_filename = os.path.join(output_dir, f"frame_{frame_count}_obj_{obj_id}.png")
                        cv.imwrite(crop_filename, cropped_object)

                        # Save the object details to the database
                        save_detected_object(crop_filename)

                        # Add the object ID to the set of saved objects
                        saved_objects.add(obj_id)

        # Display the frame with detections
        cv.imshow("Detection", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Increment the frame count
        frame_count += 1

    # Release resources
    cap.release()
    cv.destroyAllWindows()

def is_inside_roi(x1, y1, x2, y2):
    """Check if the bounding box of the detected object is inside the defined ROI."""
    roi_x1, roi_y1 = start_line
    roi_x2, roi_y2 = end_line
    return (x1 > roi_x1 and y1 > roi_y1 and x2 < roi_x2 and y2 < roi_y2)

# Set video path and output directory
video_path = "video path"
output_dir = "Output die"

# Load the YOLO model once before the loop
model = YOLO("model path")

# Create a named window for drawing the rectangle
cv.namedWindow("Detection")
cv.setMouseCallback("Detection", draw_rectangle)

# Start video processing
video_process(video_path, output_dir, model)

# Close the database connection
cursor.close()
db_connection.close()


