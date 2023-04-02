from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail, Message
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from email_validator import validate_email, EmailNotValidError
from threading import Thread

import jwt
import datetime

import io
from base64 import encodebytes
import PIL.Image as pimg

import os


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "pspnetcs426@gmail.com"
app.config['MAIL_PASSWORD'] = "waiccpkrmgjpescr"
app.config['TESTING'] = False

app.config['DOWNLOAD'] = 'images'


CORS(app, resources={r"/*":{'origins':"*"}})

bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

db.init_app(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(20), nullable=False)
  lastname = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  role = db.Column(db.String(20), default = "researcher")
  #NOTE user role is set by an administrator. 

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.password = bcrypt.generate_password_hash(password, 10)

class Image(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  path = db.Column(db.String[40], nullable=False)
  uploader_id = db.Column(db.Integer, nullable=False)
  label = db.Column(db.String[30], nullable=True)
  access = db.Column(db.Integer, nullable=False)
  location = db.Column(db.String[30], nullable=True)
  verifier_id = db.Column(db.Integer, nullable=True)
  upload_id = db.Column(db.Integer, nullable=False)
  dataset_name = db.Column(db.String[20], nullable=True)

  def __init__(self, path, uploader_id, upload_id, dataset_name,
               verifier_id=None, label=None, location=None, access=0):
    self.path = path
    self.uploader_id = uploader_id
    self.label = label
    self.access = access
    self.location = location
    self.verifier_id = verifier_id
    self.upload_id = upload_id
    self.dataset_name = dataset_name


class Dataset(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String[30], nullable=False)
  description = db.Column(db.String[40], nullable=True)
  location = db.Column(db.String[50], nullable=True)
  visibility = db.Column(db.String[10], default='public')
  
  
  def __init__(self, dataset_name, dataset_description=None, location=None, visibility='public') -> None:
    self.name = dataset_name
    self.description = dataset_description
    self.location = location
    self.visibility = visibility

class Upload(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uploader_id = db.Column(db.Integer, nullable=False)

  def __init__(self, uploader_id) -> None:
    self.uploader_id = uploader_id

class JobRegistry(db.Model):
  job_id = db.Column(db.Integer, primary_key=True)
  uploader_id = db.Column(db.Integer, nullable=False)
  dataset = db.Column(db.String(20), nullable=False)
  uploadNote = db.Column(db.String(80), nullable=True)
  geolocation = db.Column(db.String(20), nullable=True)
  model = db.Column(db.String(20), nullable=False)
  numimages = db.Column(db.Integer, nullable=False)
  starttime = db.Column(db.String(20), nullable=False)
  finishtime = db.Column(db.String(20), nullable=True)
  
  def __init__(self, job_id, uploader_id, dataset, uploadNote, geolocation, model, numimages, startime):
    self.job_id = job_id
    self.uploader_id = uploader_id
    self.dataset = dataset
    self.uploadNote = uploadNote
    self.geolocation = geolocation
    self.model = model
    self.numimages = numimages
    self.starttime = startime



#creates wrapper function for routes that require authorized tokens. 
#code adapted from blog post https://stackabuse.com/single-page-apps-with-vue-js-and-flask-jwt-authentication/
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
      return jsonify(invalid_msg), 401
    
  return authorize

#code adapted form https://dev.to/paurakhsharma/flask-rest-api-part-5-password-reset-2f2e
def new_thread_email(msg, app):
  with app.app_context():
    try:
      mail.send(msg)
    except ConnectionRefusedError:
      print("Mail Servers are not working")

#sends recovery email for forgot password
def send_email(subject, sender, recipients, text, html):
  msg = Message()
  msg.subject = subject
  msg.sender = sender
  msg.recipients = recipients
  msg.body = text
  msg.html = html

  Thread(target=new_thread_email, args=[msg, app]).start()


@app.route('/login/', methods = ['POST'])
def login():
  invalid_msg = {'message' : 'Invalid login credentials'}
  if request.method == 'POST':
    login_credentials=request.get_json()
    password = login_credentials.get('password')
    email = login_credentials.get('email')

    #validate email address
    try:
      validation = validate_email(email, check_deliverability=False)
      email = validation.email
    except EmailNotValidError as err:
      return jsonify({'message' : str(err)}), 401

    testUser = User.query.filter_by(email = email).first()

    if not testUser:
      return jsonify(invalid_msg), 401
    else:
      if not bcrypt.check_password_hash(testUser.password, password):
        return jsonify(invalid_msg), 401
      else:
        token = jwt.encode({
          'sub' : testUser.id,
          'iat' : datetime.datetime.utcnow(),
          'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
          app.config['SECRET_KEY'])
        response_login = {
          'token' : token
        }
        return jsonify(response_login), 200

@app.route('/register/', methods = ['POST'])
def register():
  if request.method == 'POST':
    user_data = request.get_json()

    #validate the user email
    try:
      email = user_data.get('email')
      validation = validate_email(email, check_deliverability=True)
      user_data['email'] = validation.email
    except EmailNotValidError as err:
      return jsonify({'message' : str(err)}), 401

    newUser = User(**user_data)
    if User.query.filter_by(email = newUser.email).first() is not None:
      return jsonify({'message': 'Email Already in Use.'}), 401
    db.session.add(newUser)
    db.session.commit()
    return {'message': 'success'} , 201

#testing protected route that requires jwt
@app.route('/userdata/', methods = ['GET'])
@token_required
def userdata(user):
  return {
    'name' : user.firstname + " " + user.lastname,
    'email' : user.email,
    'role' : user.role,
    'id' : user.id,
  }, 201

#route to update information from account settings page
@app.route('/settings/', methods = ['PUT'])
@token_required
def updateUser(user):
  user_data = request.get_json()
  user.email = user_data.get('email')
  user.firstname = user_data.get('firstname')
  user.lastname = user_data.get('lastname')
  db.session.commit()
  return { 'status' : 'good' } , 201

@app.route('/profile/', methods = ['GET', 'POST'])
def profile():
  response_data = {}
  user_id = request.get_json()['id']

  user_uploads = db.session.query(Upload.id).filter_by(uploader_id=user_id).all()

  for unique_upload_id in user_uploads:
    upload_img_paths = []
    result = db.session.query(Image.path).filter_by(upload_id=unique_upload_id[0]).all()
    for path in result:
      upload_img_paths.append(img_from_path(path[0]))

    response_data[str(unique_upload_id[0])] = {
      'paths': upload_img_paths,
      'count': len(upload_img_paths)
    }
  return jsonify(response_data), 201

@app.route('/explore/', methods=['GET'])
def explore_data():
  unique_ds = db.session.query(Dataset.name).filter(Dataset.visibility==
                                                    'public').distinct().all()
  unique_visible = []
  visibile_descr = []
  visiblie_location = []

  # retrieve data where the last contribution to the dataset was public
  for dataset in unique_ds:
    query_data = db.session.query(Dataset.description, Dataset.location, 
                                  Dataset.visibility).filter(Dataset.name==dataset[0]
                                                             ).order_by(Dataset.id.desc()).first()
    if query_data[2] == 'public':
      unique_visible.append(dataset[0])
      visibile_descr.append(query_data[0])
      visiblie_location.append(query_data[1])
  response_data = {}
  combined_encoded = []
  response_data['ds_info'] = {}
  for index, dataset in enumerate(unique_visible):
    encoded_imgs = []
    images = db.session.query(Image.path).filter_by(dataset_name = dataset)
    paths = images[0:4]
    for img_path in paths:
      encoded_imgs.append(img_from_path(img_path[0]))
    combined_encoded.append(encoded_imgs)
    img_count = images.count()
    response_data['ds_info'][str(dataset)] = {'count': img_count,
                                              'paths': encoded_imgs,
                                              'description': visibile_descr[index],
                                              'location': visiblie_location[index],
                                              'show' : True}
    response_data['images'] = combined_encoded
  return jsonify(response_data), 201

@app.route('/datasets/', methods = ['GET', 'POST'])
def dataset_prev_data():
  ds_name = request.get_json()
  paths = []
  img_paths = db.session.query(Image.path).filter_by(dataset_name = ds_name['ds_name'])
  for img_path in img_paths:
    paths.append(img_path[0].replace('/src/assets/',''))
  return jsonify(paths), 201

@app.route('/datasetview/', methods = ['GET', 'POST'])
def dataset_view_data():
  ds_name = request.get_json()
  response_data = {}
  paths = []
  labels = []
  img_paths = db.session.query(Image.path, Image.label).filter_by(dataset_name = ds_name['ds_name'])
  for img_path in img_paths:
    paths.append(img_from_path(img_path[0]))
    labels.append(img_path[1])
  response_data['images'] = paths
  response_data['labels'] = labels
  return jsonify(response_data), 201

# function adapted from:
# https://stackoverflow.com/questions/64065587/how-to-return-multiple-images-with-flask
def img_from_path(image_path):
  pillow_img = pimg.open(image_path, mode='r')
  byte_array = io.BytesIO()
  pillow_img.save(byte_array, format='JPEG')
  encoded_img = encodebytes(byte_array.getvalue()).decode('ascii')
  return encoded_img


#route responsible for forgot password
@app.route('/forgotpass/', methods = ['POST'])
def forgot_pass():
  user_data = request.get_json()
  email = user_data['email']
  url = 'http://localhost:8080/reset/'

  #validate email and check if in database
  try:
    validation = validate_email(email, check_deliverability=False)
    email = validation.email
  except EmailNotValidError as err:
    return jsonify({'message' : str(err)}), 401
  user = User.query.filter_by(email = email).first()
  if not user:
    return jsonify({'message' : 'No user found with email'}), 401

  #create token for reset password
  token = jwt.encode({
    'sub' : user.id,
    'iat' : datetime.datetime.utcnow(),
    'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
    app.config['SECRET_KEY'])

  send_email('PSPNet Password Reset',
             sender= app.config['MAIL_USERNAME'],
             recipients= [user.email], 
             text=render_template('reset_password.txt', url= url + token),
             html=render_template('reset_password.html', url= url + token))
  return { 'message' : 'success'}, 201

#user with reset token can reset the password
@app.route('/changePass/', methods = ['POST'])
@token_required
def changePass(user):
  data = request.get_json()
  new_password = data.get('new_password')
  new_hashed = bcrypt.generate_password_hash(new_password, 10)
  user.password = new_hashed 
  db.session.commit()

  send_email('PSPNet Password Reset',
             sender= app.config['MAIL_USERNAME'],
             recipients= [user.email], 
             text=render_template('success_password.txt'),
             html=render_template('success_password.html'))
  

  return {'message' : 'success'}, 201

@app.route('/getCurrentJobs/', methods = ['GET'])
@token_required
def getCurrentJobs(user):
  current_jobs = JobRegistry.query.filter_by(finishtime = None).filter_by(uploader_id=user.id).all()
  jobs_data = [{
    'id' : job.job_id,
    'datasetName' : job.dataset,
    'datasetNotes' : job.uploadNote,
    'datasetGeoloc' : job.geolocation,
    'visibility' : 'yes',
    'model' : job.model,
    'numImages' : job.numimages,
    'start' : job.starttime,
    'eta' : job.finishtime
  } for job in current_jobs]
  return jsonify(jobs_data), 201
  
@app.route('/getFinishedJobs/', methods = ['GET'])
@token_required
def getFinishedJobs(user):
  all_user_jobs = JobRegistry.query.filter_by(uploader_id=user.id).all()
  finished_jobs = []
  for job in all_user_jobs:
    if job.finishtime != None:
      finished_jobs.append(job)

  jobs_data = [{
    'id' : job.job_id,
    'datasetName' : job.dataset,
    'datasetNotes' : job.uploadNote,
    'datasetGeoloc' : job.geolocation,
    'visibility' : 'yes',
    'model' : job.model,
    'numImages' : job.numimages,
    'start' : job.starttime,
    'end' : job.finishtime
  } for job in finished_jobs]
  return jsonify(jobs_data), 201
  
# @token_required
@app.route('/download', methods = ['GET'])
def download():
  path = os.path.join(app.root_path, app.config['DOWNLOAD'], '1','predictions.csv')
  return send_file(path, as_attachment=True)

if __name__ == "__main__":
  app.run(debug=True)