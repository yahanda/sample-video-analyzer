import sys
import signal
import threading
import cv2
import requests
import time
from datetime import datetime
from azure.iot.device import IoTHubModuleClient

# Event indicating client stop
stop_event = threading.Event()

def log_msg(msg):
    print("{}: {}".format(datetime.now(), msg))

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received twin patches
    async def receive_twin_patch_handler(twin_patch):
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

def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    try:
        capture = cv2.VideoCapture(0) # /dev/video*
        while(capture.isOpened()): # open
            start = time.time()
            log_msg("predict start")
            retval, frame = capture.read() # capture
            if retval is False:
                raise IOError

            ret, encoded = cv2.imencode('.jpg', frame)
            file = {'file': encoded.tobytes()}

            res = requests.post(PREDICTION_URL, files=file)
            log_msg(res.json())

            elapsed_time  = time.time() - start
            if(elapsed_time < PREDICTION_INTERVAL):
                time.sleep(PREDICTION_INTERVAL - elapsed_time)

    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    
    finally:
        print("Shutting down IoT Hub Client...")
        capture.release()

if __name__ == '__main__':
    main()