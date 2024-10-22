import os
import cv2
from ultralytics import YOLO

home_directory = os.path.expanduser('D:/Download/perkuliahan/EVi/test')
result_dir = os.path.join(home_directory, 'result')
image_dir = os.path.join(result_dir, 'image')
os.makedirs(image_dir, exist_ok=True)
result_path = os.path.join(result_dir, 'result.txt')
final_result_path = os.path.join(result_dir, 'fresult.txt')

model_path = os.path.join(home_directory, 'model', 'rgd.pt')
model = YOLO(model_path)

class_names = {"Glass": 0, "Metal": 0, "Plastic": 0}
total_counts = {name: 0 for name in class_names}

cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # fallback to 30 fps if unknown
frame_count = 0
detect_interval = 2  # seconds

try:
    with open(result_path, "w") as deteksi_txt:
        deteksi_txt.write(f"Detection interval: {detect_interval} seconds\n")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            current_time = frame_count / fps

            if current_time % detect_interval < 1.0 / fps:
                results = model(frame)  # detect
                class_counts = {name: 0 for name in class_names}

                for result in results:
                    for cls in result.boxes.cls:
                        cls_name = model.names[int(cls)]
                        if cls_name in class_counts:
                            class_counts[cls_name] += 1

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
    print(f"Detection finished. Results saved in {result_dir}.")
