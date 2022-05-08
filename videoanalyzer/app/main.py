import cv2
import requests
import io
from PIL import Image
from datetime import datetime
import asyncio

prediction_url = "https://japaneast.api.cognitive.microsoft.com/customvision/v3.0/Prediction/xxxxxxxxxxxxxxxxxxxxxx/detect/iterations/Iteration1/image"
prediction_interval_msec = 1000

def log_msg(msg):
    print("{}: {}".format(datetime.now(), msg))

def cv2pil(image):
    img = image.copy()
    if img.ndim == 2:
        pass
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif pilImage.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    pilImage = Image.fromarray(img)
    return pilImage

if __name__ == '__main__':
    try:
        capture = cv2.VideoCapture(0) # /dev/video*
        while(capture.isOpened()): # open
            retval, frame = capture.read() # capture
            if retval is False:
                raise IOError

            pilimg = cv2pil(frame)
            imageData = io.BytesIO()
            pilimg.save(imageData,'JPEG')
            imageData = imageData.getvalue()

            file = {'file': imageData}
            payload = {'Prediction-Key': 'xxxxxxxxxxxxxxxxxxxxx'}
            res = requests.post(prediction_url, params=payload, files=file)
            #res = requests.post(prediction_url, files=file)
            log_msg(res.json())

            asyncio.sleep(prediction_interval_msec / 1000)

    finally:
        capture.release () # VideoCaptureのClose
