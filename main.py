import cv2
import time
from ultralytics import YOLO
import os

# Set up paths
home_directory = os.path.expanduser('~/EVi')
model_path = os.path.join(home_directory, 'Model', 'best.pt')
result_path = os.path.join(home_directory, 'Result', 'Result.txt')
image_save_path = os.path.join(home_directory, 'Result')

# Initialize the YOLO model
model = YOLO(model_path)

# Open the camera (default camera index is 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Prepare to write detection results
deteksi_txt = open(result_path, "w")
total_counts = {"Glass": 0, "Metal": 0, "Plastic": 0}

# Start processing frames from the camera
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for consistent processing
    frame = cv2.resize(frame, (1920, 1080))

    # Perform detection on the current frame
    results = model(frame)
    class_counts = {}

    # Iterate over detected objects
    for result in results:
        for cls in result.boxes.cls:
            cls_name = model.names[int(cls)]
            if cls_name in class_counts:
                class_counts[cls_name] += 1
            else:
                class_counts[cls_name] = 1

    # If any objects detected, save the image and record the details
    if class_counts:
        # Save the frame where detections occurred
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"detected_{timestamp}.jpg"
        cv2.imwrite(os.path.join(image_save_path, image_filename), frame)

        # Write detection details to the result file
        deteksi_txt.write(f"Time: {timestamp} - Detected objects: ")
        for cls_name, count in class_counts.items():
            deteksi_txt.write(f"{cls_name}: {count} ")
            if cls_name in total_counts:
                total_counts[cls_name] += count
        deteksi_txt.write("\n")

# Release the camera and close the file
cap.release()
deteksi_txt.close()

# Write final detection totals
final_result_path = os.path.join(home_directory, 'Result', 'Final_Result.txt')
with open(final_result_path, "w") as final_result_txt:
    for cls_name, total in total_counts.items():
        final_result_txt.write(f"{cls_name}: {total}\n")

print("Detections finished. Results are saved in the Result folder.")
