import numpy as np
import cv2
import flask
from flask import request, send_file, jsonify, make_response
from flask_cors import CORS, cross_origin
from PIL import Image
import requests
import os
import base64
from text_recognition import extract_words_and_result_image, onnx_keras_ocr
from dict_search import search_dictionary, search_thesaurus

# server url : https://visaitazsamongkol.herokuapp.com/
tmp_filename = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), 'tmp.jpg')

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Computer Vision Server</h1>'''


@app.route('/ocr', methods=['POST'])
@cross_origin()
def receiveImageAndOCR():
    file = request.files['image']
    if (file.filename == ""):
        return '''<h1>No Image Received</h1>''', 500
    byte_arr = file.read()
    img_numpy = np.frombuffer(byte_arr, np.uint8)
    imgBGR = cv2.imdecode(img_numpy, cv2.IMREAD_COLOR)
    # Text Recognition
    words, bounding_box_img = extract_words_and_result_image(imgBGR)
    # Convert img to byte_string
    _, bounding_box_img_numpy = cv2.imencode('.jpg', bounding_box_img)
    # numpy array => byte array => base64 string
    output_base64_str = base64.b64encode(bounding_box_img_numpy).decode()

    return jsonify({'words': list(words.keys()), 'base64_string': output_base64_str})


@app.route('/search/dictionary', methods=['POST'])
@cross_origin()
def receiveWordListAndSearchDictionary():
    words = request.get_json()
    # Dictionary Search
    dictionary = {}
    for word in words:
        dictionary[word] = search_dictionary(word)

    return jsonify(dictionary)


@app.route('/search/thesaurus', methods=['POST'])
@cross_origin()
def receiveWordListAndSearchThesaurus():
    words = request.get_json()
    # Thesaurus Search
    thesaurus = {}
    for word in words:
        thesaurus[word] = search_thesaurus(word)

    return jsonify(thesaurus)


@app.route('/image/url', methods=['POST'])
def receiveImageFromURLAndPredict():
    data = request.get_json()
    image_url = data['image_url']
    image = Image.open(requests.get(image_url, stream=True).raw)
    image.save(tmp_filename)
    return send_file(tmp_filename, mimetype='image/jpeg')


@app.route('/test', methods=['GET'])
def test():
    test_img_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'test.png')
    img = Image.open(test_img_path)
    res = onnx_keras_ocr.run([img])
    return {"result": [[text, box.tolist()] for text, box in res]}


port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host='0.0.0.0', port=port)
