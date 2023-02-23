#Nathaniel Leslie-Rivas
#CS 426
#JSON2Python Dictionary
#Create CSV file for readibility
#Need to find way to exectute code on set of image txt files, only one works for now...
#2.13.23 - Use command line to get txt file path

import json
import csv
import os

### Executes yolov5 command to predict an image and save the text output...
cmd = r'python C:\Users\mineo\Downloads\yolov5\classify\predict.py --weights C:\Users\mineo\Downloads\yolov5\best.onnx --save-txt --source C:\Users\mineo\Downloads\plantnet_300K\images\train\1355920 --img 640'
os.system(cmd)

# Opening JSON file
with open(r"C:\Users\mineo\Downloads\plantnet_300K\plantnet300K_species_id_2_name.json") as json_file:
	data = json.load(json_file)
json_file.close()

#Declare string variables, append with new information from inference txt, print out
confidenceInterval = []
object_id = []
species_id = []

#create dictionary from json file then referencing the data to the text file.
#save data to strings then print using for loop showing confidence interval and top 5 results.


#rename text file in folder or fix image uploads to something like img[].jpg for file naming, improve batch system
with open(r'C:\Users\mineo\Downloads\yolov5\runs\predict-cls\exp\labels\65e9dc873ad002330d91abbae2d5dd2d7b41d8be.txt','r') as f:
    for line in f:
        for word in line.split():
            temp = '5'
            temp = word
            temp = float(temp)
            if temp <= 1:
                confidenceInterval.append(word)
            for key, value in data.items():
                if word == key:
                    object_id.append(word)
                    species_id.append(value)
f.close()

#Create csv file with prediciton information
#Save CSV file where needed

with open(r'C:\Users\mineo\Downloads\predict\predict.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Confidence Interval", "Object ID", "Species"])
     writer.writerow([confidenceInterval[0], object_id[0], species_id[0]])
     writer.writerow([confidenceInterval[1], object_id[1], species_id[1]])
     writer.writerow([confidenceInterval[2], object_id[2], species_id[2]])
     writer.writerow([confidenceInterval[3], object_id[3], species_id[3]])
     writer.writerow([confidenceInterval[4], object_id[4], species_id[4]])
