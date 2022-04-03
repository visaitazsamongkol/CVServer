# FROM registry.baidubce.com/paddlepaddle/paddle:2.1.2
FROM python:3.7.13-slim-buster

WORKDIR /app

#RUN pip install paddleocr flask_cors
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-python==4.1.2.30 flask flask_cors pillow requests
RUN pip install onnxruntime


COPY . .

EXPOSE 5000

EXPOSE $PORT

ENTRYPOINT ["python"]
CMD ["app.py"]