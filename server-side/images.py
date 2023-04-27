import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS

from redis import Redis
from rq import Queue
from rq.job import Job

from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt



from app import Image
from app import Dataset
from app import Upload
from app import JobRegistry
from app import User

from app import token_required

from api import bookKeeping
from api import job_callback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "pspnetcs426@gmail.com"
app.config['MAIL_PASSWORD'] = ""
app.config['TESTING'] = False


from app import db
db.init_app(app)
#db = SQLAlchemy(app)
#db.init_app(app)

CORS(app, resources={r"/*":{'origins':"*"}})

r = Redis(host='redis', port=6379)
queue = Queue(connection=r)


image_folder = "images"

def token_required(f):
  @wraps(f)
  def authorize(*args, **kwargs):
    token = request.headers.get('token')

    invalid_msg = {
      'message' : 'Invalid token.',
      'authenticated' : False
    }
    expired_msg = {
      'message' : 'Expired token.',
      'authenticated' : False
    }
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
      user = User.query.filter_by(id=data['sub']).first()
      if not user:
        raise RuntimeError('User not found')
      return f(user, *args, **kwargs)
    except ExpiredSignatureError:
      return jsonify(expired_msg), 401
    except (InvalidTokenError, Exception) as e:
      print(str(e))
      #return jsonify(invalid_msg), 401
      return jsonify({'error' : str(e)}), 401
    
  return authorize

  

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

@app.route('/getCurrentJobs/', methods = ['GET'])
@token_required
def getCurrentJobs(user):
  
  current_jobs = JobRegistry.query.filter_by(finishtime = None).filter_by(uploader_id=user.id).all()
  jobs_data = []

  for job in current_jobs:
    redis_job = Job.fetch(str(job.job_id), connection=r)

    print(redis_job.get_position())

    single_data = {
      'id' : job.job_id,
      'datasetName' : job.dataset,
      'datasetNotes' : job.uploadNote,
      'datasetGeoloc' : job.geolocation,
      'visibility' : 'yes',
      'model' : job.model,
      'numImages' : job.numimages,
      'start' : job.starttime,
      'eta' : str('executing' if redis_job.get_position() == None else redis_job.get_position() + 1)
    }
    jobs_data.append(single_data)
  return jsonify(jobs_data), 200

if __name__ == "__main__":
  app.run(port=5001, debug=True, host='0.0.0.0')