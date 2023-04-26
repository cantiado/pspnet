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

from base64 import encodebytes
import datetime
import io
import jwt
import PIL.Image as pimg
import os
import zipfile


app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "pspnetcs426@gmail.com"
app.config['MAIL_PASSWORD'] = ""
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
  saved_ds_ids = db.Column(db.Text, nullable=True)

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
  dataset_name = db.Column(db.String[20], nullable=False)

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
  num_images = db.Column(db.Integer, default=0)
  num_uploads = db.Column(db.Integer, default=0)
  size = db.Column(db.Float, default=0.0)
  project_ids = db.Column(db.Text, nullable=True)
  
  
  def __init__(self, dataset_name, dataset_description=None, location=None, visibility='public',
               num_images=0, num_uploads=0, size=0.0) -> None:
    self.name = dataset_name
    self.description = dataset_description
    self.location = location
    self.visibility = visibility
    self.num_images = num_images
    self.num_uploads = num_uploads
    self.size = size

class Upload(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uploader_id = db.Column(db.Integer, nullable=False)
  dataset_name = db.Column(db.String[40], nullable=False)
  upload_notes = db.Column(db.Text, nullable=True)
  verified = db.Column(db.Boolean, default=False)

  def __init__(self, uploader_id, dataset_name, notes) -> None:
    self.uploader_id = uploader_id
    self.dataset_name = dataset_name
    self.upload_notes = notes

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

class Project(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True)
  dataset_ids = db.Column(db.Text, nullable=True)
  owner_id = db.Column(db.Integer, nullable=False)
  shared_user_ids = db.Column(db.Text, nullable=True)

  def __init__(self, project_name, owner_id) -> None:
    self.name = project_name
    self.owner_id = owner_id

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
    img_labels = []
    result = db.session.query(Image.path, Image.label).filter_by(upload_id=unique_upload_id[0]).all()
    for path in result:
      upload_img_paths.append(img_from_path(path[0]))
      img_labels.append(path[1])

    response_data[str(unique_upload_id[0])] = {
      'paths': upload_img_paths,
      'labels': img_labels,
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
  visible_count = []

  # retrieve data where the last contribution to the dataset was public
  for dataset in unique_ds:
    query_data = db.session.query(Dataset.description, Dataset.location, 
                                  Dataset.visibility, Dataset.num_images). \
                                  filter(Dataset.name==dataset[0]
                                        ).order_by(Dataset.id.desc()).first()
    if query_data[2] == 'public':
      unique_visible.append(dataset[0])
      visibile_descr.append(query_data[0])
      visiblie_location.append(query_data[1])
      visible_count.append(query_data[3])
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
    img_count = visible_count[index]
    response_data['ds_info'][str(dataset)] = {'count': img_count,
                                              'paths': encoded_imgs,
                                              'description': visibile_descr[index],
                                              'location': visiblie_location[index],
                                              'show' : True}
  return jsonify(response_data), 200

@app.route('/explore/<dsName>/save/', methods=['POST'])
# @token_requireds
def save_dataset(dsName):
  user_id = request.get_json()['id']
  new_save_id = db.session.query(Dataset.id).filter(Dataset.name==dsName).first()[0]
  saved_ds = db.session.query(User.saved_ds_ids).filter(User.id==user_id).first()[0]
  if saved_ds is None: dataset_IDs = [str(new_save_id)]
  else: 
    print(f"Saved[0] has: {(saved_ds[0].split(',')).append('test')}")
    dataset_IDs = saved_ds[0].split(',') + [str(new_save_id)]
    print(f"in else with : {dataset_IDs}")
  print(dataset_IDs)
  joined_ids = ','.join(dataset_IDs)
  db.session.query(User).filter(User.id==user_id)\
    .update({User.saved_ds_ids : joined_ids},synchronize_session=False)
  db.session.commit()
  return jsonify("Success!"), 201

@app.route('/datasets/', methods = ['GET', 'POST'])
def dataset_prev_data():
  ds_name = request.get_json()
  paths = []
  img_paths = db.session.query(Image.path).filter_by(dataset_name = ds_name['ds_name'])
  for img_path in img_paths:
    paths.append(img_path[0].replace('/src/assets/',''))
  return jsonify(paths), 201

@app.route('/datasetview/<dsName>/', methods = ['GET'])
def dataset_view_data(dsName):
  ds_data = db.session.query(Dataset.num_images, Dataset.size, Dataset.visibility). \
    filter_by(name = dsName).order_by(Dataset.id.desc()).first()
  if ds_data[2] != 'public':
    return jsonify(dict({'status': "Private dataset"})), 401
  combined_data = {}
  combined_upload_data = []
  ds_upload_list = db.session.query \
    (Upload.id, Upload.uploader_id, Upload.upload_notes, Upload.verified)\
      .filter_by(dataset_name = dsName)
  for upload in ds_upload_list:
    upload_data = {}
    uploader_name = db.session.query(User.firstname, User.lastname).filter_by(id = upload[1]).all()
    parsed_name = uploader_name[0][0] + ' ' + uploader_name[0][1][0:1] + '.'
    upload_data['user'] = parsed_name
    paths = []
    labels = []
    img_data = db.session.query(Image.path, Image.label).filter_by(upload_id = upload[0])
    upload_data['count'] = img_data.count()
    for img_datum in img_data:
      paths.append(img_from_path(img_datum[0]))
      labels.append(img_datum[1])
    upload_data['images'] = paths
    upload_data['labels'] = labels
    upload_data['notes'] = upload[2]
    upload_data['verified'] = upload[3]
    upload_data['id'] = upload[0]
    combined_upload_data.append(upload_data)
  combined_data['upload_data'] = combined_upload_data
  combined_data['num_images'] = ds_data[0]
  combined_data['ds_size'] = ds_data[1]
  combined_data['status'] = "Success"
  return jsonify(combined_data), 200

@app.route('/datasetview/<dsName>/<uploadID>', methods = ['GET'])
@token_required
def update_verified_upload(dsName, uploadID):
  db.session.query(Upload).filter(Upload.id == uploadID)\
    .update({Upload.verified: True}, synchronize_session = False)
  db.session.commit()
  return jsonify("Success!"), 200

@app.route('/datasetview/<dsName>/download/', methods=['GET'])
def download_dataset(dsName):
  upload_ids = db.session.query(Upload.id)\
    .filter(Upload.dataset_name == dsName).all()
  dir = os.getcwd()
  image_file = io.BytesIO()
  with zipfile.ZipFile(image_file, 'w') as zf:
    for upload in upload_ids:
      upload_path = os.path.join(dir, "images", str(upload[0]))
      for root, dirs, file_paths in os.walk(upload_path):
        for file_path in file_paths:
          zf.write(os.path.join(upload_path, file_path),
                   arcname=os.path.join("Upload "+str(upload[0]), file_path), 
                   compress_type=zipfile.ZIP_DEFLATED)
  image_file.seek(0)
  return send_file(image_file, download_name=f"{dsName}.zip", as_attachment=True), 200

# function adapted from:
# https://stackoverflow.com/questions/64065587/how-to-return-multiple-images-with-flask
def img_from_path(image_path):
  pillow_img = pimg.open(image_path, mode='r')
  byte_array = io.BytesIO()
  pillow_img.save(byte_array, format='JPEG')
  encoded_img = encodebytes(byte_array.getvalue()).decode('ascii')
  return encoded_img

@app.route('/collections/affiliates/', methods=['POST'])
def get_affiliates():
  '''get set of all researchers/users a User is associated with'''
  frontend_data = request.get_json()
  user_id = frontend_data['id']
  user_ids_in_projects = db.session.query(Project.owner_id, Project.shared_user_ids).all()
  u_ID_list = []
  for u_IDs in user_ids_in_projects:
    if u_IDs[0] != user_id:
      u_ID_list.append(str(u_IDs[0]))
    if u_IDs[1] is not None: u_ID_list += u_IDs[1].split(',')
  print(u_ID_list)
  unique_IDs = set(u_ID_list)
  unique_IDs -= {str(user_id)}
  
  user_data = []
  for unique in unique_IDs:
    user_info = db.session.query(User.firstname, User.lastname, User.email, User.role)\
    .filter(User.id==int(unique)).first()
    name = " ".join([user_info[0], user_info[1]])
    structured_info = {'name' : name,
                       'email' : user_info[2],
                       'role' : user_info[3]}
    user_data.append(structured_info)
  return jsonify({'affiliates' : user_data}), 201

@app.route('/collections/<projectName>/', methods=['GET', 'POST'])
def view_project(projectName):
  if request.method == 'GET': 
    '''gets single-image preview for datasets in a project'''
    response_data = {}
    # response_data['project_dataests'] = {}
    project_id = db.session.query(Project.id).filter(Project.name==projectName).first()[0]
    datasets = db.session.query(Dataset.id, Dataset.name, Dataset.project_ids, Dataset.visibility).all()
    public_datasets = []
    # project_datasets = []
    for dataset_info in datasets:
      if dataset_info[3]=='public': public_datasets.append(dataset_info[1])
      if dataset_info[2] is None : continue # skip if dataset is not a part of any project
      project_ids = dataset_info[2].split(',')
      if str(project_id) in project_ids: # check if dataset is associated with a project
        dataset_name = dataset_info[1]
        # project_datasets.append(dataset_name)
        preview_img = db.session.query(Image.path).filter(Image.dataset_name==dataset_name).first()[0]
        img = img_from_path(preview_img) # gets byte string for preview image
        response_data[dataset_name] = img
        # response_data['project_dataests'][dataset_name] = img
    # public_outside_project = list(set(public_datasets)-set(project_datasets))
    # response_data['available_datasets'] = public_outside_project
    return response_data, 200
  
  if request.method == 'POST': # handle add/remove
    project_id = db.session.query(Project.id).filter(Project.name==projectName).first()[0]
    data = request.form.to_dict(flat=False)
    operation = data['operation'][0] # add or remove operation
    
    user_emails = data['emails']
    ids_from_emails = []
    for email in user_emails: # queries for the email associated with each user
      ids_from_emails.append(db.session.query(User.id).filter(User.email==email).first()[0])
    saved_ids = db.session.query(Project.shared_user_ids).filter(Project.name==projectName).first()[0]
    existing_ids = []
    if saved_ids is not None: # check for any already-shared users
      saved_ids = saved_ids.split(',')
      existing_ids = set([str(id) for id in saved_ids]) # set of already-added IDs
      saved_ids += ids_from_emails
    else: saved_ids = ids_from_emails
    saved_ids = [str(id) for id in saved_ids]
    saved_ids = list(set(saved_ids))
    new_ids = list(set(saved_ids)-existing_ids) # set of newly-added IDs
    for new_id in new_ids:
      new_email = db.session.query(User.email).filter(User.id==int(new_id)).first()[0]
      print(new_email)
      # send email to newly-invited researcher(s)
    shared_user_ids = ",".join(saved_ids) # converts field back to DB format
    if operation == "add":
      '''adds the newly given IDs to the project'''
      db.session.query(Project).filter(Project.id==project_id)\
        .update({Project.shared_user_ids:shared_user_ids}, synchronize_session=False)
      db.session.commit()
    if operation == "remove":
      pass
    return jsonify(success=True), 200

@app.route('/collections/shared', methods=['POST'])
# token required
def get_shared():
  frontend_data = request.get_json()
  return_data = {}
  projects = []
  user_id = frontend_data['id']
  user_projects = db.session.query(Project.name, Project.shared_user_ids) \
    .filter(Project.owner_id.contains(str(user_id))).all()
  for project_info in user_projects:
    if project_info[1] is None: continue
    elif str(user_id) in project_info[1].split(','):
      projects.append(project_info[0])
  return_data['projects'] = projects
  return jsonify(return_data), 201

@app.route('/collections/', methods=['POST'])
# @token_required
def get_collections():
  # param: user_id
  # return: dictionary {projects: [list,of,projects], 
                      # datasets: [{dataset-name : one byte-string image},
                      #            {etc:etc},...],
                      # public_datasets: [dataset_names]}
  
  form_info = request.get_json()
  if 'project_name' in form_info: # checks for type of POST request
    '''POST request to create a new project'''
    print(form_info)
    project_name = form_info['project_name']
    owner = form_info['user_id']
    project_exists = db.session.query(Project).filter(Project.name==project_name).first() is not None
    if project_exists:
      return jsonify({"success":False, "message": "Project name already exists"}), 400
    new_project = Project(project_name, owner)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"success": True}), 201
  '''POST request to receive the list of user-owned projects'''
  if 'id' in form_info:
    return_data = {}
    projects = []
    saved_datasets = {}
    user_id = form_info['id']
    saved_ds = db.session.query(User.saved_ds_ids).filter(User.id==user_id).first()[0]
    if saved_ds is not None: dataset_IDs = saved_ds.split(',')
    else: dataset_IDs = []
    for saved_id in dataset_IDs:
      saved_ds_name = db.session.query(Dataset.name).filter(Dataset.id==int(saved_id)).first()[0]
      saved_ds_img = db.session.query(Image.path).filter(Image.dataset_name==saved_ds_name).first()[0]
      saved_datasets[saved_ds_name] = img_from_path(saved_ds_img)
    public_datasets = db.session.query(Dataset.name).filter(Dataset.visibility=='public').all()
    public_datasets = list(set([dataset[0] for dataset in public_datasets]))
    user_projects = db.session.query(Project.name).filter(Project.owner_id==user_id).all()
    for project in user_projects:
      projects.append(project[0])
    return_data['projects'] = projects
    return_data['datasets'] = saved_datasets
    return_data['public_datasets'] = public_datasets
    return jsonify(return_data), 201
  if 'datasets' in form_info:
      '''Add list of datasets to a project'''
      # param: list of dataset names, project name
      datasets_to_add = form_info['datasets']
      project_name = form_info['project']
      project_id = db.session.query(Project.id).filter(Project.name==project_name).first()[0]
      dataset_query = db.session.query(Dataset.project_ids)
      for dataset_name in datasets_to_add:
        p_ids = dataset_query.filter(Dataset.name==dataset_name).first()[0]
        if p_ids is None: p_ids = [str(project_id)]
        else:
          p_ids = p_ids.split(',')
          if str(project_id) not in p_ids: p_ids.append(str(project_id))
        joined_p_ids = ','.join(p_ids)
        db.session.query(Dataset).filter(Dataset.name==dataset_name)\
          .update({Dataset.project_ids : joined_p_ids }, synchronize_session=False)
      db.session.commit()

      return jsonify("something"), 201

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
  
@app.route('/download/<job_id>', methods = ['GET'])
def download(job_id):
  
    path = os.path.join(app.root_path, app.config['DOWNLOAD'], job_id ,'predictions{}.csv'.format(job_id))
    return send_file(path, as_attachment=True)
  

if __name__ == "__main__":
  app.run(debug=True)