import cv2
import numpy as np
import os

HOME = os.getcwd()
UPLOAD_PATH = os.path.join(HOME, 'uploads/')

def save(file, path) -> str:
    """Save an image by filepath"""
    new_path = os.path.join(UPLOAD_PATH, path)
    file.save(new_path)
    return new_path

def read_image(file) -> cv2.typing.MatLike:
    filestr = file.read()
    file_bytes = np.fromstring(filestr, np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)