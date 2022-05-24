import cv2
import requests
import time
from datetime import datetime
from azure.iot.device import IoTHubModuleClient

# Global variable
PREDICTION_URL = 'http://xxxx/image'
PREDICTION_INTERVAL = 10
IS_RECORDING = True
RECORDING_LENGTH = 60

def log_msg(msg):
    print("{}: {}".format(datetime.now(), msg))

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received twin patches
    def receive_twin_patch_handler(twin_patch):
        global PREDICTION_URL
        global PREDICTION_INTERVAL
        print("Twin Patch received")
        print("     {}".format(twin_patch))
        if "predictionUrl" in twin_patch:
            PREDICTION_URL = twin_patch["predictionUrl"]
        if "predictionInterval" in twin_patch:
            PREDICTION_INTERVAL = twin_patch["predictionInterval"]

    try:
        # Set handler on the client
        client.on_twin_desired_properties_patch_received = receive_twin_patch_handler

    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client

def predict(client):

    client.connect()

    capture = cv2.VideoCapture(0) # /dev/video*

    fps = int(capture.get(cv2.CAP_PROP_FPS)) 
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))        
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') 

    while True:
        start_recording = time.time()
        start_prediction = time.time()
        now = datetime.now()
        video_filename = now.strftime('%Y%m%d_%H%M%S') + '.mp4'
        writer = cv2.VideoWriter(video_filename, fourcc, fps, (w, h))

        while(capture.isOpened()): # open
            retval, frame = capture.read() # capture
            if retval is False:
                raise IOError

            if time.time() - start_prediction > PREDICTION_INTERVAL:
                ret, encoded = cv2.imencode('.jpg', frame)
                file = {'imageData': encoded.tobytes()}

                res = requests.post(PREDICTION_URL, files=file)
                log_msg(res.json())
                start_prediction = time.time()

            if IS_RECORDING:
                writer.write(frame)
                if time.time() - start_recording > RECORDING_LENGTH:
                    log_msg("recorded clips of video as mp4 files")
                    writer.release()
                    break

    #        elapsed_time  = time.time() - start
    #        if(elapsed_time < PREDICTION_INTERVAL):
    #            time.sleep(PREDICTION_INTERVAL - elapsed_time)
    #    capture.release()


def main():
    print ( "IoT Hub Client for Python" )

    client = create_client()

    try:
        predict(client)
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        client.shutdown()


if __name__ == "__main__":
    main()
