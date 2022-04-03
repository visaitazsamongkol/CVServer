import numpy as np
import cv2

class Detector_utils():
  def __init__(self):
    pass

  def compute_input(self, image):
    # should be RGB order
    image = image.astype("float32")
    mean = np.array([0.485, 0.456, 0.406])
    variance = np.array([0.229, 0.224, 0.225])

    image -= mean * 255
    image /= variance * 255
    return image
  
  def getBoxes(
      self,
      y_pred,
      detection_threshold=0.7,
      text_threshold=0.4,
      link_threshold=0.4,
      size_threshold=10,
  ):
      box_groups = []
      for y_pred_cur in y_pred:
          # Prepare data
          textmap = y_pred_cur[..., 0][0].copy()
          linkmap = y_pred_cur[..., 1][0].copy()
          img_h, img_w = textmap.shape


          _, text_score = cv2.threshold(
              textmap, thresh=text_threshold, maxval=1, type=cv2.THRESH_BINARY
          )
          _, link_score = cv2.threshold(
              linkmap, thresh=link_threshold, maxval=1, type=cv2.THRESH_BINARY
          )

          n_components, labels, stats, _ = cv2.connectedComponentsWithStats(
              np.clip(text_score + link_score, 0, 1).astype("uint8"), connectivity=4
          )
          boxes = []
          for component_id in range(1, n_components):
              # Filter by size
              size = stats[component_id, cv2.CC_STAT_AREA]

              if size < size_threshold:
                  continue

              # If the maximum value within this connected component is less than
              # text threshold, we skip it.
              if np.max(textmap[labels == component_id]) < detection_threshold:
                  continue

              # Make segmentation map. It is 255 where we find text, 0 otherwise.
              segmap = np.zeros_like(textmap)
              segmap[labels == component_id] = 255
              segmap[np.logical_and(link_score, text_score)] = 0
              x, y, w, h = [
                  stats[component_id, key]
                  for key in [
                      cv2.CC_STAT_LEFT,
                      cv2.CC_STAT_TOP,
                      cv2.CC_STAT_WIDTH,
                      cv2.CC_STAT_HEIGHT,
                  ]
              ]

              # Expand the elements of the segmentation map
              niter = int(np.sqrt(size * min(w, h) / (w * h)) * 2)
              sx, sy = max(x - niter, 0), max(y - niter, 0)
              ex, ey = min(x + w + niter + 1, img_w), min(y + h + niter + 1, img_h)
              segmap[sy:ey, sx:ex] = cv2.dilate(
                  segmap[sy:ey, sx:ex],
                  cv2.getStructuringElement(cv2.MORPH_RECT, (1 + niter, 1 + niter)),
              )

              # Make rotated box from contour
              contours = cv2.findContours(
                  segmap.astype("uint8"),
                  mode=cv2.RETR_TREE,
                  method=cv2.CHAIN_APPROX_SIMPLE,
              )[-2]
              contour = contours[0]
              box = cv2.boxPoints(cv2.minAreaRect(contour))

              # Check to see if we have a diamond
              w, h = np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2])
              box_ratio = max(w, h) / (min(w, h) + 1e-5)
              if abs(1 - box_ratio) <= 0.1:
                  l, r = contour[:, 0, 0].min(), contour[:, 0, 0].max()
                  t, b = contour[:, 0, 1].min(), contour[:, 0, 1].max()
                  box = np.array([[l, t], [r, t], [r, b], [l, b]], dtype=np.float32)
              else:
                  # Make clock-wise order
                  box = np.array(np.roll(box, 4 - box.sum(axis=1).argmin(), 0))
              boxes.append(2 * box)
          box_groups.append(np.array(boxes))
      return box_groups 