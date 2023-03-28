import os
import sys
import shutil
import pandas as pd
from pathlib import Path
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

from redis import Redis
from rq import Queue

from app import Image
from app import Dataset
from app import Upload

from api import bookKeeping

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
db = SQLAlchemy(app)
db.init_app(app)

r = Redis(host='redis', port=6379)
queue = Queue(connection=r)


image_folder = "images"


  

@app.route("/identify", methods=["POST"])
def identify():

  uploadTime = datetime.datetime.utcnow() 

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
                        dataset_location, visibility, uploadTime)
  new_upload = Upload(user_id)
  db.session.add(new_upload)

  job_id = db.session.query(Upload.id).order_by(Upload.id.desc()).first()[0]
  
  # form_info["dataset-name"]: dataset name
  # form_info["dataset-notes"]: dataset notes
  # form_info["dataset-geoloc"]: dataset geolocation
  # form_info["visibility"]: {"public", "shared", "private"}
  # form_info["user-id"]: user id
  # return jsonify(message="Successfully uploaded images!")
  

  job_folder = os.path.join(image_folder, str(job_id)) 
  os.makedirs(job_folder)
  numImages = 0
  for i, file in enumerate(files):
    file.save(os.path.join(job_folder, file.filename))
    new_image = Image(os.path.join(job_folder, file.filename), user_id, 
                      job_id, dataset_name, location=dataset_location)
    db.session.add(new_image)
    db.session.commit()
    
    numImages = numImages + 1
    # save file paths to image database

  new_dataset.numimages = numImages

  #commands here give global environment path to project for deployment on any machine
  FILE = Path(__file__).resolve()
  path = FILE.parents[0]
  os.chdir(path)

  print("Predicting...")
  new_job = queue.enqueue(bookKeeping, args=(job_id, path, job_folder))

  '''
  os.system(r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640')
  
  #cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640'
  #os.system(cmd)

  #Declare string variables, append with new information from inference txt, print out
  confidenceInterval = []
  species_id = []

  #this command is used to concatenate all txt files in the labels directory after prediciton is made
  
  os.chdir("labels")
  cmd2 = r"cat *.txt > predictions.txt"
  os.system(cmd2)

  #changes back to pspnet/server-side folder to append predictions.txt to csv file.
  os.chdir(path)
  
  #saves csv prediction labels folder...
  read_file = pd.read_csv (r'labels/predictions.txt')
  read_file.to_csv(r"labels/predictions.csv", index = None)


  #move csv prediction to newly created jobs folder... and deletes labels folder to remove previous job
  shutil.move("labels/predictions.csv", job_folder)
  shutil.rmtree(r"labels")'''

  finishTime = datetime.datetime.utcnow()

  new_dataset.finishtime = finishTime
  new_dataset.numimages = numImages
  db.session.add(new_dataset)
  db.session.commit()

  return "Success!"
#2/27/2023 - Convert text files in predict class to csv...

if __name__ == "__main__":
  app.run(port=5001, debug=True, host='0.0.0.0')