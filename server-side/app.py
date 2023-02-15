from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
import datetime



app = Flask(__name__)
app.app_context().push()
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'
CORS(app, resources={r"/*":{'origins':"*"}})
db = SQLAlchemy(app)

db.init_app(app)
db.create_all()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(20), nullable=False)
  lastname = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.password = bcrypt.generate_password_hash(password, 10)

#The following code was used to add a single test element to the user DB
#testUser = User(userID=2, firstname="Andrew", lastname="Ramirez", email="andrewramirez@unr.edu", password="1041131")
#with app.app_context():
#  db.session.add(testUser)
#  db.session.commit()


class Image(db.Model):
  image_id = db.Column(db.String[20], primary_key=True)
  path = db.Column(db.String[40], nullable=False)
  uploader_id = db.Column(db.Integer, nullable=False)
  label = db.Column(db.String[30], nullable=True)
  access = db.Column(db.Integer, nullable=False)
  location = db.Column(db.String[30], nullable=True)
  verifier_id = db.Column(db.Integer, nullable=True)
  upload_id = db.Column(db.Integer, nullable=False)
  dataset_name = db.Column(db.String[20], nullable=True)

  def __init__(self, image_id, path, uploader_id, upload_id, dataset_name,
               verifier_id=None, label=None, location=None, access=0):
    self.image_id = image_id
    self.path = path
    self.uploader_id = uploader_id
    self.label = label
    self.access = access
    self.location = location
    self.verifier_id = verifier_id
    self.upload_id = upload_id
    self.dataset_name = dataset_name
  # insert into image values ("test-image-id", "/src/assets/user_images/sage.jpg",0,NULL,0,NULL, NULL, 0, "test")
  # test_image = Image('test-image-id4', '/src/assets/user_images/sage.jpg', upload_id=0, uploader_id=0,
  #     dataset_name="test", verifier_id=None, label=None,location=None,access=0)
  # db.session.add(test_image)
  # db.session.commit()

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
      user = User.query.filter_by(email=data['sub']).first()
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
          'sub' : testUser.email,
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
  }, 201

@app.route('/profile/', methods = ['GET'])
@token_required
def profile():
  all_img = Image.query.get("image_id")
  return jsonify(all_img), 201

if __name__ == "__main__":
  app.run(debug=True)
    