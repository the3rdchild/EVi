## <div align="center">EVi - Exam Vision</div>
[EVi](https://github.com/the3rdchild/evi/) (Exam Vision) is a machine learning-based solution that detects cheating during online exams in real time. By leveraging the power of YOLOv8, this program identifies suspicious behaviors during exams, helping to maintain academic integrity on a large scale.
The system generates reports with timestamps of when cheating behaviors are detected, provides visualizations such as heatmaps to highlight suspicious activities, and can identify cheating patterns across multiple students. EVi can be an essential tool for educators and institutions looking to enhance exam monitoring and prevent academic misconduct efficiently.

## <div align="center">Documentation</div>
## Installation
### Windows
1. Clone the repository to your local machine:
```git
git clone https://github.com/yourusername/EVi.git
cd EVi
```
2. Set up a Python virtual environment (optional):
```
python -m venv venv
```

3. Activate the virtual environment (optioal):
```
venv\Scripts\activate
```

or you can run all the program using
included [run.bat](https://github.com/the3rdchild/EVi/blob/main/run.bat) file:
- Double-click the run.bat file, which contains simple code:
```
@echo off
python -u main.py
```

### Linux
1. Clone the repository to your local machine:
```git
git clone https://github.com/yourusername/EVi.git
cd EVi
```
2. Set up a Python virtual environment (optional):
```
python -m venv venv
```

3. Activate the virtual environment (optioal):
```
venv\Scripts\activate
```

4. Run the program:
```
python main.py
```

## <div align="center">Models</div>
EVi uses the YOLOv8 model, which is well-suited for real-time object detection tasks. The system is pre-trained with EVi.pt, a specialized model to recognize cheating behaviors based on various visual and behavioral cues.
To use the model:

1. Download the trained model [EVi.pt](https://github.com/the3rdchild/EVi/tree/main/model) and place it in the model directory.
2. Modify the configuration in [main.py](https://github.com/the3rdchild/EVi/blob/main/main.py) to point to the path of EVi.pt in your local machine.

You can also modify the classes detected by the model by editing the [main.py](https://github.com/the3rdchild/EVi/blob/main/main.py) file. In the model section, update the class_names dictionary to include your desired classes like this: 
```
some code ...

class_names = {"your": 0, "class": 0}.

some code ...
```
