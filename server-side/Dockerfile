FROM python:3.10.9
COPY . /server-side
WORKDIR /server-side
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
CMD ["python", "images.py"]