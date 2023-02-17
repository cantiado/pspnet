from flask import Flask, request
import os

app = Flask(__name__)

image_folder = "images"

@app.route("/")
def hello_world():
  return "<h1>Hello world<h1>"

@app.route("/identify", methods=["POST"])
def identify():
  print("here!")
  files = request.files.to_dict(flat=False)["image-input"]
  for i, file in enumerate(files):
    file.save(os.path.join(image_folder, file.filename))
  return "success"