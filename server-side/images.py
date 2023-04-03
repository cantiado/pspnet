import os, glob
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
from app import JobRegistry

from api import bookKeeping
from api import job_callback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
db = SQLAlchemy(app)
db.init_app(app)

r = Redis(host='redis', port=6379)
queue = Queue(connection=r)


image_folder = "images"

def YOLOv5(path, job_id):
  #executes yolo prediction model on images/jobs folder...
  os.chdir(path)
  directory = 'images/' +str(job_id)

  #type checks each file in directory to verify if user uploaded images, if not error is returned and function terminates
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if f.lower().endswith(('bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm')):
        print("")
    else:
      print("Error, Prediction Failed.\nUser Uploaded Incorrect File Type.")
      return 0

  print("Predicting...")
  cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640'
  os.system(cmd)
  return 1

def shutilFunction(job_id, job_folder, path):
  #changes back to pspnet/server-side folder to append predictions.txt to csv file.
  os.chdir(path)
  prediction_ID = "labels/predictions" + str(job_id) + ".csv" #creates unique string for shutil
  shutil.move(prediction_ID, job_folder)
  shutil.rmtree(r"labels/")

def csvCreation(job_id):
  os.chdir("labels")
  #lists here are used when parsing through text files in the label directory after prediciton
  listOne = []
  listTwo = []
  split = []

  #looks for each file with the .txt extension in the labels directory
  for filename in glob.glob('*.txt'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # opens text file in readonly mode
      textLine = f.readlines() #gets each line from an individual text file
      for x in range(5): #reads through top five predictions in each text line
        split = textLine[x].split(" ", 1) #splits the confidence interval from species classification
        predictionNumber = filename + " prediction: " + str(x) #creates new string to indicate classification order
        listOne = [split[0], split[1], predictionNumber] #adds each id to a list
        listTwo.append(listOne) #appends the list into one larger list
  
  #creates a new csv data frame containing top 5 classifications for each image
  prediction = pd.DataFrame(listTwo, columns=['CONFIDENCE_INTERVAL', 'SPECIES', 'PICTURE_ID'])  
  prediction.insert(3, "MODEL: YOLOv5", " ")
  prediction_ID = "predictions" + str(job_id) + ".csv" 
  prediction.to_csv(prediction_ID) #converts the dataframe to a csv

@app.route("/identify", methods=["POST"])
def identify():


  # files = request.files.to_dict(flat=False)["image-input"]
  files = request.files.to_dict(flat=False)["images"]
  form_info = request.form.to_dict()
  user_id = form_info['user-id']
  dataset_name = form_info['dataset-name']
  dataset_description = form_info['dataset-notes']
  upload_notes = None if dataset_description == "" else dataset_description
  dataset_description = upload_notes # placeholder for dataset info
  dataset_location = form_info['dataset-geoloc']
  dataset_location = None if dataset_location == "" else dataset_location
  visibility = form_info['visibility']
  new_dataset = Dataset(dataset_name, dataset_description, 
                        dataset_location, visibility)
  new_upload = Upload(user_id, dataset_name, upload_notes)
  db.session.add(new_upload)
  db.session.add(new_dataset)
  db.session.commit()

  job_id = db.session.query(Upload.id).order_by(Upload.id.desc()).first()[0]
  
  # form_info["dataset-name"]: dataset name
  # form_info["dataset-notes"]: dataset notes
  # form_info["dataset-geoloc"]: dataset geolocation
  # form_info["visibility"]: {"public", "private"}
  # form_info["user-id"]: user id
  

  job_folder = os.path.join(image_folder, str(job_id)) 
  os.makedirs(job_folder)
  numImages = 0
  for i, file in enumerate(files):
    file.save(os.path.join(job_folder, file.filename))
    new_image = Image(os.path.join(job_folder, file.filename), user_id, 
                      job_id, dataset_name, location=dataset_location)
    db.session.add(new_image)
    
    numImages = numImages + 1
    # save file paths to image database
  db.session.commit()
  new_dataset.numimages = numImages
  #commands here give global environment path to project for deployment on any machine
  FILE = Path(__file__).resolve()
  path = FILE.parents[0]

  print("Predicting...")
  new_job = queue.enqueue(bookKeeping, args=(job_id, path, job_folder), job_id=str(job_id), on_success=job_callback)
  added_job = JobRegistry(new_job.id,
                          user_id,
                          dataset_name,
                          dataset_description,
                          dataset_location,
                          'Yolov5',
                          numImages,
                          new_job.enqueued_at)
  db.session.add(added_job)

  #fill in upload table using new_job attributes
  #the finishtime should be set to null


  db.session.add(new_dataset)
  db.session.commit()

  return "Success!"

if __name__ == "__main__":
  app.run(port=5001, debug=True, host='0.0.0.0')