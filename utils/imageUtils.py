import cv2 as cv
import numpy as np
from PIL import Image

# Bounding box constants
boundingBoxColor = (165, 214, 167)
boundingBoxBorderSize = 2
maskColor = (145, 255, 117)

# Id text constants
font = cv.FONT_HERSHEY_SIMPLEX
fontSize = 0.5
fontColor = (0, 255, 0)
lineType = 2


def deinterlaceImages(images, numpy=True):
    deinterlaced = []
    for image in images:
        if numpy:
            image = Image.fromarray(image).convert('RGB')
        size = list(image.size)
        image = image.resize([size[0], int(size[1] / 2)], Image.NEAREST)
        if numpy:
            image = np.array(image.resize(size))
        deinterlaced.append(np.array(image))
    return deinterlaced


def deinterlaceImagesDuplicate(images):
    deinterlaced = []
    for img in images:
        img[1::2] = img[::2]
        deinterlaced.append(img)
    return deinterlaced


def drawBoundingBox(frame, boundingBox, color=boundingBoxColor):
    cv.rectangle(frame,
                 (boundingBox.origin.x, boundingBox.origin.y),
                 (boundingBox.end.x, boundingBox.end.y),
                 color,
                 boundingBoxBorderSize)
    return frame


def drawMask(frame, mask):
    for c in range(3):
        frame[:, :, c] = np.where(mask == 1,
                                  frame[:, :, c] * 0.5 + 0.5 * maskColor[c] * 255,
                                  frame[:, :, c])
    return frame


def drawId(frame, id, box):
    return cv.putText(frame,
                      "Id: %d" % id,
                      (box.origin.x, box.origin.y - 16),
                      font,
                      fontSize,
                      fontColor,
                      lineType)
