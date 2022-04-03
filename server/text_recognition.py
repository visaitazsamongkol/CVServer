import cv2
import numpy as np
from keras_ocr_onnx import Onnx_keras_ocr
import os
    
detector_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './detector/detector.onnx')
recognizer_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), './recognizer/recognizer.onnx')

onnx_keras_ocr = Onnx_keras_ocr(detector_path,recognizer_path)

def only_alphabet(text: str):
    output_text = ''
    for char in text:
        if char.isalpha():
            output_text += char
    return output_text

def extract_words_and_result_image(img):
    words = {}
    boxes = []
    prediction_groups = onnx_keras_ocr.run([img])
    word_box_list = prediction_groups
    for word, box in word_box_list:
        word = only_alphabet(word)
        if len(word)<=1: continue
        if word not in words:
            words[word] = 1
        else:
            words[word] += 1
        boxes.append(box)

    bounding_box_img = img.copy()
    cv2.polylines(bounding_box_img, pts=np.int32(boxes), isClosed=True, color=(0,0,255), thickness=2)
    return words, bounding_box_img