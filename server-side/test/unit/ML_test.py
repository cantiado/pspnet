import os
from pathlib import Path


def test_model():
    FILE = Path(__file__).resolve()
    path = FILE.parents[2] #gets operating directory and all directories above it.
    print(path)
    os.chdir(path) #changes to operating directory

    path = Path(r'images\example.jpg') #for testing checks if image is available.

    if path.is_file():
        test = r"python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/ --img 640"
        os.system(test)
            
        #executes command for python script testing of images.py... for image prediction
        label = Path(r'labels\example.txt')
        if label.is_file():
            print("Test successfully inferenced image and created a text file with predictions.")

if __name__ == "__main__":
    test_model()