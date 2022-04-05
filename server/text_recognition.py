import cv2
import numpy as np
from keras_ocr_onnx import Onnx_keras_ocr
import os
    
detector_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './detector/detector.onnx')
recognizer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './recognizer/recognizer.onnx')

onnx_keras_ocr = Onnx_keras_ocr(detector_path,recognizer_path)

def get_words(text: str):
    words = []
    word = ''
    for char in text:
        if char.isalpha():
            word += char
        else:
            if len(word)>1: words.append(word)
            word = ''
    if len(word)>1: words.append(word)
    return words

def extract_words_and_result_image(img):
    word_dict = {}
    boxes = []
    prediction_groups = onnx_keras_ocr.run([img])
    word_box_list = prediction_groups
    for text, box in word_box_list:
        words = get_words(text)
        if len(words)==0: continue
        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
        boxes.append(box)

    bounding_box_img = img.copy()
    cv2.polylines(bounding_box_img, pts=np.int32(boxes), isClosed=True, color=(0,0,255), thickness=2)
    return word_dict, bounding_box_img