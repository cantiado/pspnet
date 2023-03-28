import os
import shutil

def bookKeeping(job_id, path, job_folder):
  os.system(r'python yolov5/classify/predict.py --weights yolov5/best.onnx --save-txt --source images/' + str(job_id) + r' --img 640')

  os.chdir("labels")
  cmd2 = r"cat *.txt > predictions.txt"
  os.system(cmd2)

  #changes back to pspnet/server-side folder to append predictions.txt to csv file.
  os.chdir(path)
  
  #saves csv prediction labels folder...
  read_file = pd.read_csv (r'labels/predictions.txt')
  read_file.to_csv(r"labels/predictions.csv", index = None)


  #move csv prediction to newly created jobs folder... and deletes labels folder to remove previous job
  shutil.move("labels/predictions.csv", job_folder)
  shutil.rmtree(r"labels")