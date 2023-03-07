import os
import sys
import pandas as pd
from pathlib import Path
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import Image
from app import Dataset
from app import Upload

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
db = SQLAlchemy(app)
db.init_app(app)


image_folder = "images"

@app.route("/identify", methods=["POST"])
def identify():
  # files = request.files.to_dict(flat=False)["image-input"]
  files = request.files.to_dict(flat=False)["images"]
  form_info = request.form.to_dict()
  user_id = form_info['user-id']
  dataset_name = form_info['dataset-name']
  dataset_description = form_info['dataset-notes']
  dataset_description = None if dataset_description == "" else dataset_description
  dataset_location = form_info['dataset-geoloc']
  dataset_location = None if dataset_location == "" else dataset_location
  visibility = form_info['visibility']
  new_dataset = Dataset(dataset_name, dataset_description, 
                        dataset_location, visibility)
  db.session.add(new_dataset)
  new_upload = Upload(user_id)
  db.session.add(new_upload)
  db.session.commit()
  job_id = db.session.query(Upload.id).order_by(Upload.id.desc()).first()[0]
  
  # form_info["dataset-name"]: dataset name
  # form_info["dataset-notes"]: dataset notes
  # form_info["dataset-geoloc"]: dataset geolocation
  # form_info["visibility"]: {"public", "shared", "private"}
  # form_info["user-id"]: user id
  # return jsonify(message="Successfully uploaded images!")

  job_folder = os.path.join(image_folder, str(job_id)) 
  os.makedirs(job_folder)
  for i, file in enumerate(files):
    file.save(os.path.join(job_folder, file.filename))
    new_image = Image(os.path.join(job_folder, file.filename), user_id, 
                      job_id, dataset_name, location=dataset_location)
    db.session.add(new_image)
    db.session.commit()
    # save file paths to image database

  #commands here give global environment path to project for deployment on any machine
  FILE = Path(__file__).resolve()
  path = FILE.parents[0]
  os.chdir(path)
  print("Predicting...")
  cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640'
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