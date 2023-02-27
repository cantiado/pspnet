from flask import Flask, request

app = Flask(__name__)

image_folder = "images"
import os
import csv
import sys
from pathlib import Path

@app.route("/")
def hello_world():
  return "<h1>Hello world<h1>"

@app.route("/identify", methods=["POST"])
def identify():
  print("here!")
  files = request.files.to_dict(flat=False)["image-input"]
  for i, file in enumerate(files):
    file.save(os.path.join(image_folder, file.filename))

  #commands here give global environment path to project for deployment on any machine
  FILE = Path(__file__).resolve()
  path = FILE.parents[0]
  os.chdir(path)
  cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/ --img 640'
  os.system(cmd)

  #Declare string variables, append with new information from inference txt, print out
  confidenceInterval = []
  object_id = []
  species_id = []

  #this command is used to concatenate all txt files in the labels directory after prediciton is made
  os.chdir("labels")
  cmd2 = r"cat *.txt > predictions.txt"
  os.system(cmd2)
  os.chdir(path)
  
  os.remove(r'labels/*txt')

  return "success"
#2/27/2023 - Convert text files in predict class to csv...

"""
  with open(r'\predict\predict.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Confidence Interval", "Object ID", "Species"])
     writer.writerow([confidenceInterval[0], object_id[0], species_id[0]])
     writer.writerow([confidenceInterval[1], object_id[1], species_id[1]])
     writer.writerow([confidenceInterval[2], object_id[2], species_id[2]])
     writer.writerow([confidenceInterval[3], object_id[3], species_id[3]])
     writer.writerow([confidenceInterval[4], object_id[4], species_id[4]])
"""