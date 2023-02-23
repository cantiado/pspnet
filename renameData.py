#Nathaniel Leslie-Rivas
#CS 426
#Purpose: Rename entire dataset with correlating plant species and retrain using yolo

import os
import json

def main():
	#need to open plant species json file.
	with open(r"C:\Users\mineo\Capstone\plantnet_300K\plantnet300K_species_id_2_name.json") as json_file:
		data = json.load(json_file)
	json_file.close()
	
	object_id = []
	species_id = []

#specify folder and directory of test, valid, and train directories and keep running it.
	folder = r"C:\Users\mineo\Capstone\plantnet_300K\images\valid"
	os.chdir(r'C:\Users\mineo\Capstone\plantnet_300K\images\valid')
	for count, filename in enumerate(os.listdir(folder)):
		for key, value in data.items():
			if filename == key:
				os.rename(filename, value)
	
if __name__ == '__main__':
	main()
