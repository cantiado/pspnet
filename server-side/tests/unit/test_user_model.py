from app import User
from flask_bcrypt import Bcrypt
import pytest

@pytest.fixture(scope='module')
def user_data():
  newUser = {
    'email' : 'andrewramirez@unr.edu',
    'password' : '1041131',
    'firstname' : 'andrew',
    'lastname' : 'ramirez'
  }
  user = User(**newUser)
  return user
#test that the user model works and data is created successfully 
def test_user_model(user_data):

  bcrypt = Bcrypt()

  assert user_data.email == 'andrewramirez@unr.edu'
  assert user_data.password != '1041131'
  assert user_data.firstname == 'andrew'
  assert user_data.lastname == 'ramirez'
  assert bcrypt.check_password_hash(user_data.password, '1041131')
  