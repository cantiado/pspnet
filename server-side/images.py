from flask import Flask, request

app = Flask(__name__)

image_folder = "images"
import os
import json
import csv

@app.route("/")
def hello_world():
  return "<h1>Hello world<h1>"

@app.route("/identify", methods=["POST"])
def identify():
  print("here!")
  files = request.files.to_dict(flat=False)["dropzone-file"]
  for i, file in enumerate(files):
    file.save(os.path.join(image_folder, file.filename))

  cmd = r'python \yolov5\classify\predict.py --weights \yolov5\best.onnx --save-txt --source \images --img 640'
  os.system(cmd)
  
  #opens and saves json file data format to variable
  with open(r"plantnet300K_species_id_2_name.json") as json_file:
    data = json.load(json_file)
  json_file.close()

  #Declare string variables, append with new information from inference txt, print out
  confidenceInterval = []
  object_id = []
  species_id = []
  
  #After predicting images, need list of txt outputs... uses single hard coded output for testing
  with open(r'\yolov5\runs\predict-cls\exp\labels\65e9dc873ad002330d91abbae2d5dd2d7b41d8be.txt','r') as f:
    for line in f:
        for word in line.split():
            temp = word
            temp = float(temp)
            if temp <= 1:
                confidenceInterval.append(word)
            for key, value in data.items():
                if word == key:
                    object_id.append(word)
                    species_id.append(value)
  f.close()

#prediction saved to \prediction\predict.csv
#need to append txt file outputs to one save file and interate through it
  with open(r'\predict\predict.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Confidence Interval", "Object ID", "Species"])
     writer.writerow([confidenceInterval[0], object_id[0], species_id[0]])
     writer.writerow([confidenceInterval[1], object_id[1], species_id[1]])
     writer.writerow([confidenceInterval[2], object_id[2], species_id[2]])
     writer.writerow([confidenceInterval[3], object_id[3], species_id[3]])
     writer.writerow([confidenceInterval[4], object_id[4], species_id[4]])

  return "success"