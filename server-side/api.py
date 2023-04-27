import os, glob
import shutil
import pandas as pd

from flask import Flask, render_template

from app import app, db, mail
from app import JobRegistry
from app import User, Image
from flask_mail import Mail, Message
from threading import Thread


#YOLOv5 predictions folder
def YOLOv5(path, job_id):
  #executes yolo prediction model on images/jobs folder...
  os.chdir(path)
  directory = 'images/' +str(job_id)

  #type checks each file in directory to verify if user uploaded images, if not error is returned and function terminates
  for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if f.lower().endswith(('bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm')):
        print("")
    else:
      print("Error, Prediction Failed.\nUser Uploaded Incorrect File Type.")
      return 0

  print("Predicting...")
  cmd = r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640'
  os.system(cmd)
  return 1

def shutilFunction(job_id, job_folder, path):
  #changes back to pspnet/server-side folder to append predictions.txt to csv file.
  os.chdir(path)
  prediction_ID = "labels/predictions" + str(job_id) + ".csv" #creates unique string for shutil
  shutil.move(prediction_ID, job_folder)
  shutil.rmtree(r"labels/")

def csvCreation(job_id):
  os.chdir("labels")
  #lists here are used when parsing through text files in the label directory after prediciton
  listOne = []
  listTwo = []
  split = []

  #looks for each file with the .txt extension in the labels directory
  for filename in glob.glob('*.txt'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # opens text file in readonly mode
      textLine = f.readlines() #gets each line from an individual text file
      for x in range(5): #reads through top five predictions in each text line
        split = textLine[x].split(" ", 1) #splits the confidence interval from species classification
        predictionNumber = filename + " prediction: " + str(x) #creates new string to indicate classification order
        listOne = [split[0], split[1], predictionNumber] #adds each id to a list
        listTwo.append(listOne) #appends the list into one larger list
        if x == 1:
          print("update label...")
          updateLabel(filename, job_id, split[1])
    db.session.commit()
  
  #creates a new csv data frame containing top 5 classifications for each image
  prediction = pd.DataFrame(listTwo, columns=['CONFIDENCE_INTERVAL', 'SPECIES', 'PICTURE_ID'])  
  prediction.insert(3, "MODEL: YOLOv5", " ")
  prediction_ID = "predictions" + str(job_id) + ".csv" 
  prediction.to_csv(prediction_ID) #converts the dataframe to a csv

def updateLabel(filename, job_id, label):
  '''Updates the label for a given file'''
  # creates the Image.path, .txt is replaced with % for the LIKE query
  img_path = os.path.join('images',str(job_id), filename.replace('.txt','%'))
  db.session.query(Image).filter(Image.path.like(img_path)).update({Image.label: label}, synchronize_session = False)

def bookKeeping(job_id, path, job_folder):
  #calls to yolov5 function to prediction images in jobs folder
  failCheck = YOLOv5(path, job_id)

  #if yolov5 function call fails due to user error, the fail check bellow will execute and prevent further execution.
  
  #calls to function which creates detailed csv for images...
  csvCreation(job_id)

  #calls to shutil function to move prediction file job_folder then removes the labels directory
  shutilFunction(job_id, job_folder, path)



def job_callback(job, connection, result, *args, **kwargs):
  #first thing is to get the associated job registry object
  with app.app_context():
    finished_job = JobRegistry.query.filter_by(job_id = job.id).first()
    finished_job.finishtime = job.ended_at

    #next get user associated with job and send an email
    user = User.query.filter_by(id=finished_job.uploader_id).first()

    msg = Message()
    msg.subject = 'PSPNet Job Completed'
    msg.sender = "pspnetcs426@gmail.com" 
    msg.recipients = [user.email]
    msg.body = render_template('job_completed.txt', description=finished_job.uploadNote, name=finished_job.dataset)
    msg.html = render_template('job_completed.txt', description=finished_job.uploadNote, name=finished_job.dataset)

    mail.send(msg)


    ''' send_email('PSPNet Job Completed',
              sender= "pspnetcs426@gmail.com",
              recipients= [user.email], 
              text=render_template('job_completed.txt', description=finished_job.uploadNote, name=user.firstname),
              html=render_template('job_completed.html', description=finished_job.uploadNote, name=user.firstname ))
    '''


    db.session.commit()
  


if __name__ == "__main__":
  app.run(port=5002, debug=True)