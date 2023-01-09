from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
CORS(app, resources={r"/*":{'origins':"*"}})
db = SQLAlchemy(app)

db.init_app(app)

class User(db.Model):
  userID = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(20), nullable=True)
  lastname = db.Column(db.String(20), nullable=True)
  email = db.Column(db.String(20), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)

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
    testUser = User.query.filter_by(password = password, email = email).first()
    if testUser is None:
      response_login = {'status':'failure'}
    
  return jsonify(response_login)

if __name__ == "__main__":
  app.run(debug=True)
    
    


  