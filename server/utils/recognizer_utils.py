import numpy as np
import cv2
from PIL import Image
class Recognizer_utils():
  def __init__(self):
    self.alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    self.blank_label_idx = len(self.alphabet)
  
  def read_and_fit(
    self,
    image,
    width: int,
    height: int,
    cval: int = 255,
    mode="letterbox",
  ):
    
    image = self.fit(image=image, width=width, height=height, cval=cval, mode=mode)
    return image

  def fit(
    self,
    image,
    width: int,
    height: int,
    cval: int = 255,
    mode="letterbox",
    return_scale=False,
  ):
    fitted = None
    x_scale = width / image.shape[1]
    y_scale = height / image.shape[0]
    if x_scale == 1 and y_scale == 1:
        fitted = image
        scale = 1
    elif (x_scale <= y_scale and mode == "letterbox") or (
        x_scale >= y_scale and mode == "crop"
    ):
        scale = width / image.shape[1]
        resize_width = width
        resize_height = (width / image.shape[1]) * image.shape[0]
    else:
        scale = height / image.shape[0]
        resize_height = height
        resize_width = scale * image.shape[1]
    if fitted is None:
        resize_width, resize_height = map(int, [resize_width, resize_height])
        if mode == "letterbox":
            fitted = np.zeros((height, width, 3), dtype="uint8") + cval
            image = cv2.resize(image, dsize=(resize_width, resize_height))
            fitted[: image.shape[0], : image.shape[1]] = image[:height, :width]
        elif mode == "crop":
            image = cv2.resize(image, dsize=(resize_width, resize_height))
            fitted = image[:height, :width]
        else:
            raise NotImplementedError(f"Unsupported mode: {mode}")
    if not return_scale:
        return fitted
    return fitted, scale 

  def crop_images(self, images, boxes):
    if type(images[0]) == np.ndarray:
        images =  [Image.fromarray(image) for image in images]
    cropped_images = []
    for idx, image in enumerate(images):
      cropped_text_images = []
      for box in boxes[0]:
          position = self.getPositionOfBox(box)
          cropped_image = image.crop(position)
          cropped_text_images.append(np.array(cropped_image))
      cropped_images.append(cropped_text_images)
    return cropped_images
  
  def getPositionOfBox(self, box):
      minX, maxX = int(round(np.min(box[:,0]))), int(round(np.max(box[:,0])))
      minY, maxY = int(round(np.min(box[:,1]))), int(round(np.max(box[:,1])))
      return (minX, minY, maxX, maxY)
