from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
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

@app.route('/login', methods = ['POST'])
def login():
  response_login = {'status':'success'}
  if request.method == 'POST':
    login_credentials=request.get_json()
    password = login_credentials.get('password')
    email = login_credentials.get('email')
    testUser = User.query.filter_by(email = email).first()
    if testUser is None:
      response_login = {'status' : 'failure'}
    else:
      if not bcrypt.check_password_hash(testUser.password, password):
        response_login = {'status' : 'failure'}

  return jsonify(response_login)

@app.route('/register', methods = ['POST'])
def register():
  response_create = {'status':''}
  if request.method == 'POST':
    user_data = request.get_json()
    newUser = User(**user_data)
    if User.query.filter_by(email = newUser.email).first() is not None:
      return jsonify({'status': 'Email Already in Use.'})
    db.session.add(newUser)
    db.session.commit()

  return jsonify(response_create)

if __name__ == "__main__":
  app.run(debug=True)
    
    


  