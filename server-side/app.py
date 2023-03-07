from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
import datetime

import io
from base64 import encodebytes
import PIL.Image as pimg



app = Flask(__name__)
app.app_context().push()
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'
CORS(app, resources={r"/*":{'origins':"*"}})
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
      print(e)
      return jsonify(invalid_msg), 401
    
  return authorize

@app.route('/login/', methods = ['POST'])
def login():
  invalid_msg = {'message' : 'Invalid login credentials'}
  if request.method == 'POST':
    login_credentials=request.get_json()
    password = login_credentials.get('password')
    email = login_credentials.get('email')
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
  all_img = db.session.query(Image.upload_id).filter_by(uploader_id=user_id)
  unique_upload = all_img.distinct().all()
  img_data = {}
  for unique_upload_id in unique_upload:
    result = (db.session.query(Image.path).filter_by(upload_id=unique_upload_id[0]).all())  
    for path in result:
      adjusted_path = str(path[0].replace('/src/assets/',''))
    img_data[str(unique_upload_id[0])] = adjusted_path
  response_data['img_count'] = all_img.count()
  response_data['img_data'] = img_data
  return jsonify(response_data), 201

@app.route('/explore/', methods=['GET'])
def explore_data():
  unique_ds = db.session.query(Dataset.name).filter(Dataset.visibility=='public').distinct().all()
  # unique_ds = db.session.query(Dataset.name, Dataset.description, 
  #                              Dataset.location).filter(Dataset.visibility=='public')
  # test_names = unique_ds.filter

  unique_visible = []
  visibile_descr = []
  visiblie_location = []

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
    cleaned_paths = []
    encoded_imgs = []
    images = db.session.query(Image.path).filter_by(dataset_name = dataset)
    paths = images[0:4]
    for img_path in paths:
      encoded_imgs.append(img_from_path(img_path[0]))
      cleaned_paths.append(img_path[0].replace('/src/assets/',''))
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
  paths = []
  img_paths = db.session.query(Image.path).filter_by(dataset_name = ds_name['ds_name'])
  for img_path in img_paths:
    paths.append(img_path[0].replace('/src/assets/',''))
  return jsonify(paths), 201

# function adapted from:
# https://stackoverflow.com/questions/64065587/how-to-return-multiple-images-with-flask
def img_from_path(image_path):
  pillow_img = pimg.open(image_path, mode='r')
  byte_array = io.BytesIO()
  pillow_img.save(byte_array, format='JPEG')
  encoded_img = encodebytes(byte_array.getvalue()).decode('ascii')
  return encoded_img

if __name__ == "__main__":
  app.run(debug=True)