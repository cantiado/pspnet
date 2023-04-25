<template>
  <h1 class="text-3xl mb-5">
    Machine Learning Model:
    <a
      class="text-blue-500 underline"
      href="https://docs.ultralytics.com/yolov5/"
      >YOLOv5</a
    >
  </h1>
  <h2 class="text-lg font-bold">
    How to setup and install YOLOv5 to run PSPNet
  </h2>
  <p class="mb-5">
    Clone repo and install requirements.txt in a Python environment, including
    PyTorch. Models and datasets download automatically from the latest YOLOv5
    release with the following commands:
  </p>
  <div class="flex flex-col mb-5 bg-gray-100 px-2 py-1 rounded-md">
    <code class="truncate"
      >git clone https://github.com/ultralytics/yolov5 #clone</code
    >
    <code>cd yolov5</code>
    <code>pip install -r requirements.txt #install</code>
  </div>
  <p class="mb-5">
    Now, download our trained weight:
    <a
      class="text-blue-500 underline"
      href="https://drive.google.com/file/d/1GzaauTlnI9veRKHsFRiC1zMqqwWtCofC/view?usp=sharing"
      >PSPNet Trained Weight.</a
    >
  </p>
  <p class="mb-5">
    To run a prediction, execute the following commands:
  </p>
    <code class="mb-5 bg-gray-100 px-2 py-1 rounded-md"
      >python classify/predict.py --weights best.onnx --img 640 --source "path
      to image file or directory of images" --save-txt
    </code>
</template>
