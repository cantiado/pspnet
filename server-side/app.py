from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from functools import wraps
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import jwt
import datetime



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SECRET_KEY'] = '95fd1e474cbc4b49a3286dc09cba7510'
CORS(app, resources={r"/*":{'origins':"*"}})
db = SQLAlchemy(app)

db.init_app(app)

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

#creates wrapper function for routes that require authorized tokens. 
def token_required(f):
  @wraps(f)
  def authorize(*args, **kwargs):
    token = request.headers.get('token')

    invalid_msg = {
      'message' : 'Invalid token. Re-authroization requried',
      'authenticated' : False
    }
    expired_msg = {
      'message' : 'Expired token. Re-authorization required',
      'authenticated' : False
    }
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      user = User.query.filter_by(email=data['sub']).first()
      if not user:
        raise RuntimeError('User not found')
      return f(user, *args, **kwargs)
    except ExpiredSignatureError:
      return jsonify(expired_msg), 401
    except InvalidTokenError:
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
    return 201

#testing protected route that requires jwt
@app.route('/protected', methods = ['POST'])
@token_required
def protected(user):
  return jsonify({'name' : user.firstname})

if __name__ == "__main__":
  app.run(debug=True)
    