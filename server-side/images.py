import os
import sys
import pandas as pd
from pathlib import Path
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import Image

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
db = SQLAlchemy(app)
db.init_app(app)


image_folder = "images"

@app.route("/identify", methods=["POST"])
def identify():
  files = request.files.to_dict(flat=False)["image-input"]
  for i, file in enumerate(files):
    file.save(os.path.join(image_folder, file.filename))
    new_image = Image(os.path.join(image_folder, file.filename), 0, 0, "test")
    db.session.add(new_image)
    db.session.commit()
    # save file paths to image database

  #commands here give global environment path to project for deployment on any machine
  FILE = Path(__file__).resolve()
  path = FILE.parents[0]
  os.chdir(path)
  print("Predicting...")
  cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/ --img 640'
  os.system(cmd)

  #Declare string variables, append with new information from inference txt, print out
  confidenceInterval = []
  species_id = []

  #this command is used to concatenate all txt files in the labels directory after prediciton is made
  os.chdir("labels")
  cmd2 = r"cat *.txt > predictions.txt"
  os.system(cmd2)

  #changes back to pspnet/server-side folder to append predictions.txt to csv file.
  os.chdir(path)
  read_file = pd.read_csv (r'labels/predictions.txt')
  read_file.to_csv (r'labels/predictions.csv', index=None)
  
  return open(r"labels/predictions.csv", mode='r')
#2/27/2023 - Convert text files in predict class to csv...

if __name__ == "__main__":
  app.run(port=5001, debug=True)