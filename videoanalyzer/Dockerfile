FROM balenalib/raspberrypi4-64

RUN apt update && apt install -y python3 python3-pip git libgl1-mesa-glx libopencv-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD [ "python3", "-u", "./main.py" ]
