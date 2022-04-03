import onnxruntime as rt
from PIL import Image
import numpy as np
import cv2
import os
from utils.detector_utils import Detector_utils
from utils.recognizer_utils import Recognizer_utils

class Onnx_keras_ocr():
  def __init__(self, detector_path, recognizer_path):
    self.detector_path = detector_path
    self.recognizer_path = recognizer_path

    self.detector_utils = Detector_utils()
    self.recognizer_utils = Recognizer_utils()

    self.detector = self.initialize_detector()
    self.recognizer = self.initialize_recognizer()
  
  def initialize_detector(self):
    sessOptions = rt.SessionOptions()
    sessOptions.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL 
    detector = rt.InferenceSession(self.detector_path, sessOptions)
    return detector

  def initialize_recognizer(self):
    sessOptions = rt.SessionOptions()
    sessOptions.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL 
    recognizer = rt.InferenceSession(self.recognizer_path, sessOptions)
    return recognizer

  def detect(self, images):
    images = [self.detector_utils.compute_input(np.array(image)) for image in images]
    k = self.detector.get_inputs()[0]
    detection_results = self.detector.run([], {k.name: np.array(images)})
    return self.detector_utils.getBoxes(detection_results)
  
  def recognize(self, images, boxes):
    cropped_images = np.array(self.recognizer_utils.crop_images(images, boxes))
    recognition_results = []
    for idx in range(len(images)):
      for image in cropped_images[idx]:
        image = self.recognizer_utils.read_and_fit(
                image,
                width=200,
                height=31,
                cval=0,
        )
        if image.shape[-1] == 3:
            # Convert color to grayscale
            image = cv2.cvtColor(image, code=cv2.COLOR_RGB2GRAY)[..., np.newaxis]
        image = image.astype("float32") / 255
        k = self.recognizer.get_inputs()[0]
        recognition_result = "".join(
              [
                  self.recognizer_utils.alphabet[idx]
                  for idx in self.recognizer.run([], {k.name: image[np.newaxis]})[0][0]
                  if idx not in [self.recognizer_utils.blank_label_idx, -1]
              ]
          )
        
        recognition_results.append(recognition_result)
    return recognition_results
    
  def run(self, images):
    boxes = self.detect(images)
    results = self.recognize(images, boxes)
    return [(text, box) for text, box in zip(results, boxes[0])]