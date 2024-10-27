import os
import cv2
from ultralytics import YOLO

home_directory = os.path.expanduser('~/EVi')
result_dir = os.path.join(home_directory, 'result')
image_dir = os.path.join(result_dir, 'image')
os.makedirs(image_dir, exist_ok=True)
result_path = os.path.join(result_dir, 'result.txt')
final_result_path = os.path.join(result_dir, 'fresult.txt')

model_path = os.path.join(home_directory, 'model', 'EVi.pt') #yolo8 - yolo11
model = YOLO(model_path)

class_names = {"Handphone": 0, "Memberi contekan": 0, "Menengok": 0, "Menunduk": 0}
total_counts = {name: 0 for name in class_names}

cap = cv2.VideoCapture(0)

# default = 640 x 480
# the result is depend on the camera spec
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 720p = 1280 × 720
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # 1080p = 1920 × 1080

fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # fallback to 30 fps if unknown
frame_count = 0
detect_interval = 0.033  # seconds | 1s / FPS = interval
conf_thres = 0.85 # confidence threshold 

try:
    with open(result_path, "w") as deteksi_txt:
        deteksi_txt.write(f"Deteksi interval: {detect_interval} seconds\n")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            current_time = frame_count / fps

            if current_time % detect_interval < 1.0 / fps:
                results = model(frame, conf=conf_thres)  # detect
                class_counts = {name: 0 for name in class_names}
                
                for result in results:
                    for cls in result.boxes.cls:
                        cls_name = model.names[int(cls)]
                        if cls_name in class_counts:
                            class_counts[cls_name] += 1

                # uncomment to preview the camera
                #     for box in result.boxes:
                #         x1, y1, x2, y2 = map(int, box.xyxy[0])
                #         conf = box.conf[0]  
                #         cls = int(box.cls[0]) 
                #         class_name = model.names[cls]
                #         cv2.rectangle(frame, (x1, y1), (x2, y2), (230, 230, 230), 1)
                #         label = f"{class_name} {conf:.2f}"
                #         cv2.putText(frame, label, (x1, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1)
                
                # cv2.imshow('Preview', frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

                # timestamp
                minutes = int(current_time // 60)
                seconds = int(current_time % 60)
                deteksi_txt.write(f"Time: {minutes}m:{seconds}s: ")

                # representative image and log
                for cls_name, count in class_counts.items():
                    if count > 0:
                        deteksi_txt.write(f"{cls_name}: {count} ")
                        total_counts[cls_name] += count

                        # save with box
                        output_img_path = os.path.join(image_dir, f"frame_{minutes}m{seconds}s_{cls_name}.jpg")
                        boxed_frame = result.plot()
                        cv2.imwrite(output_img_path, boxed_frame)
                deteksi_txt.write("\n")
            
            # total counts
            with open(final_result_path, "w") as final_result_txt:
                for cls_name, total in total_counts.items():
                    final_result_txt.write("{}: {}\n".format(cls_name, total))
finally:
    cap.release()
    print(f"Hasil disimpan di {result_dir}.")
