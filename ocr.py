import cv2
import numpy as np
from PIL import Image
import pytesseract
from pytesseract import Output
import os
import io
from flask import Response

word_path = '/Users/imspiedy/Desktop/ML/OCR/static/word_updated/'
char_path = '/Users/imspiedy/Desktop/ML/OCR/static/char_updated/'

def ImagetoText(filename):
    """ Takes image as input and return's text extracted from the given image"""

    pil_img = Image.open(filename)
    opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    text = pytesseract.image_to_string(opencvImage)

    return text


def ImagetoCharBoxes(filename):
    pil_img = Image.open(filename)
    opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    boxes = pytesseract.image_to_boxes(opencvImage)
    h, w, c = opencvImage.shape

    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(opencvImage, (int(b[1]), h - int(b[2])), \
            (int(b[3]), h - int(b[3])),\
                (0, 255,0), 2)
    img = Image.fromarray(img, 'RGB')
    img.save(char_path+filename.filename)
    

    return filename.filename

def ImagetoWordBoxes(filename):
    # img = cv2.imread(filename)
    pil_img = Image.open(filename)
    
    opencvImage = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    d = pytesseract.image_to_data(opencvImage, output_type=Output.DICT)
    n_boxes = len(d['text'])

    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['width'][i])
            img = cv2.rectangle(opencvImage, (x, y), (x+w, y+h), (0, 255, 0), 2)

    img = Image.fromarray(img, 'RGB')
    img.save(word_path+filename.filename)

    return filename.filename 
