<template>
  <h1 class="text-3xl mb-5">Machine Learning Model: <a class="text-blue-500 underline" href="https://docs.ultralytics.com/yolov5/"
      >YOLOv5</a
    ></h1>
  <h2>
    <b>How to setup and install YOLOv5 to run PSPNet</b>
  </h2>
  <p>
    Clone repo and install requirements.txt in a Python environment, 
    including PyTorch. Models and datasets
    download automatically from the latest YOLOv5 release with the following commands:
  </p>
  <p style="border-width:4px; border-style:solid; border-color:#000000; padding: 1em;">
  git clone https://github.com/ultralytics/yolov5      #clone
  <br>cd yolov5
  <br>pip install -r requirements.txt  #install
  </p>
  <p>
    <br>Now, download our trained weight: <a class="text-blue-500 underline" href="https://drive.google.com/file/d/1GzaauTlnI9veRKHsFRiC1zMqqwWtCofC/view?usp=sharing"
      >PSPNet Trained Weight.</a><br>
  </p>
  <p>
    <br>To run a prediction, execute the following commands:
    <p style="border-width:4px; border-style:solid; border-color:#000000; padding: 1em;">
      python classify/predict.py --weights best.onnx --img 640 --source "path to image file or directory of images" --save-txt

  </p>

  </p>
</template>