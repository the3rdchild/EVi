import os

EVi = os.path.dirname(os.path.abspath(__file__))

result_dir = os.path.join(EVi, 'Result')
image_dir = os.path.join(result_dir, 'Image')

result_path = os.path.join(result_dir, 'Result.txt')
final_result_path = os.path.join(result_dir, 'Fresult.txt')
result_dir = os.path.join(EVi, 'Result')
image_dir = os.path.join(result_dir, 'Image')
model_path = os.path.join(EVi, 'Model', 'EVi.pt') #yolo8 - yolo11