from paddleocr import PaddleOCR, draw_ocr
import flask
import numpy as np
import cv2
from flask import request, send_file
from flask_cors import CORS, cross_origin
from PIL import Image
import requests
import sys
import os

# server url : https://visaitazsamongkol.herokuapp.com/

def predict():
    img_path = './tmp.jpeg'
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(img_path, cls=True)
    res = []
    for line in result:
        res.append(str(line))
        obj = eval(str(line))
        word = obj[1][0]
        confidence = obj[1][1]
        box = obj[0]
    return res

app = flask.Flask(__name__)
app.config["DEBUG"] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Computer Vision Server</h1>'''

@app.route('/image', methods=['POST'])
@cross_origin()
def receiveImageAndPredict():
    image = request.files['image']
    if (image.filename == ""):
        return '''<h1>No Image Received</h1>''', 500
    image = image.read()
    image_numpy = np.fromstring(image, np.uint8)
    img = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)
    cv2.imwrite('./tmp.jpeg', img)
    # return {'result': predict()}
    # processing here
    #
    return send_file('./tmp.jpeg', mimetype='image/jpeg')

@app.route('/image/url', methods=['POST'])
def receiveImageFromURLAndPredict():
    data = request.get_json()
    image_url = data['image_url']
    image = Image.open(requests.get(image_url, stream=True).raw)
    image.save('./tmp.jpeg')
    return {'result': predict()}

@app.route('/image/annotate', methods=['POST'])
def receiveImageAndAnnotate():
    image = request.files['image']
    data = request.get_json()
    boxes = data['boxes']
    if (image.filename == ""):
        return '''<h1>No Image Received</h1>''', 500
    image = image.read()
    image_numpy = np.fromstring(image, np.uint8)
    img = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)
    cv2.imwrite('./tmp.jpeg', img)
    # do annotation
    return send_file('./tmp.jpeg', mimetype='image/jpeg')

@app.route('/load_models', methods=['GET'])
def load_models():
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    return {'result': 'ok'}, 200

port = int(os.environ.get("PORT", 5000))

app.run(debug=True,host='0.0.0.0',port=port)