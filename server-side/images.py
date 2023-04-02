import os
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
#2/27/2023 - Convert text files in predict class to csv...

if __name__ == "__main__":
  app.run(port=5001, debug=True, host='0.0.0.0')