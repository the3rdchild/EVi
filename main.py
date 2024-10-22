import cv2
import time
from ultralytics import YOLO
import os

home_directory = os.path.expanduser('D:/Download/perkuliahan/EVi/EVi')
model_path = os.path.join(home_directory, 'model', 'best.pt')
result_path = os.path.join(home_directory, 'result', 'result.txt')
image_save_path = os.path.join(home_directory, 'result', 'image')

model = YOLO(model_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

deteksi_txt = open(result_path, "w")
total_counts = {"Handphone": 0, "Memberi contekan": 0, "Menengok": 0, "Menunduk": 0}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1920, 1080))

    results = model(frame)
    class_counts = {}

    for result in results:
        for cls in result.boxes.cls:
            cls_name = model.names[int(cls)]
            if cls_name in class_counts:
                class_counts[cls_name] += 1
            else:
                class_counts[cls_name] = 1

## SAVE IMAGE DETECTED
    if class_counts:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_filename = f"detected_{timestamp}.jpg"
        cv2.imwrite(os.path.join(image_save_path, image_filename), frame)

        deteksi_txt.write(f"Time: {timestamp} - Detected objects: ")
        for cls_name, count in class_counts.items():
            deteksi_txt.write(f"{cls_name}: {count} ")
            if cls_name in total_counts:
                total_counts[cls_name] += count
        deteksi_txt.write("\n")

    cv2.imshow('Camera 1', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
deteksi_txt.close()

final_result_path = os.path.join(home_directory, 'result', 'fresult.txt')
with open(final_result_path, "w") as final_result_txt:
    for cls_name, total in total_counts.items():
        final_result_txt.write(f"{cls_name}: {total}\n")

print("Detections finished. Results are saved in the Result folder.")
