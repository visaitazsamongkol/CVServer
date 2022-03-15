import flask
import numpy as np
import cv2
from flask import request, send_file
from flask_cors import CORS, cross_origin
from PIL import Image
import io
import base64

app = flask.Flask(__name__)
app.config["DEBUG"] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Computer Vision Server</h1>'''

@app.route('/image', methods=['POST'])
@cross_origin()
def receiveImage():
    image = request.files['image']
    if (image.filename == ""):
        return '''<h1>No Image Received</h1>''', 500
    image = image.read()
    image_numpy = np.fromstring(image, np.uint8)
    img = cv2.imdecode(image_numpy, cv2.IMREAD_COLOR)
    #cv2.imwrite('./image.jpg', img)

    # processing here
    #

    return "image received", 200
    
@app.route('/image', methods=['GET'])
@cross_origin()
def getImage():
    filename = "./image.jpg"
    # img = Image.open('./image.jpg')
    # rawBytes = io.BytesIO()
    # img.save(rawBytes, "JPEG")
    # rawBytes.seek(0)
    # img_bytes = base64.b64encode(rawBytes.read())
    return send_file(filename, mimetype='image/jpeg')
    # return {'image': str(img_bytes)}, 200

app.run(host='192.168.1.105', port=5000)