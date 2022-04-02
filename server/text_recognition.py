import keras_ocr
import cv2
import numpy as np

pipeline = keras_ocr.pipeline.Pipeline()

def only_alphabet(text: str):
    output_text = ''
    for char in text:
        if char.isalpha():
            output_text += char
    return output_text

def extract_words_and_result_image(img):
    words = {}
    boxes = []
    prediction_groups = pipeline.recognize([img])
    word_box_list = prediction_groups[0]
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