# sample-video-analyzer

## Build

```
sudo docker build -t videoanalyzer -f Dockerfile .
sudo docker tag videoanalyzer <your-container-registry>/videoanalyzer:1.0
sudo docker login -u <username> -p <password> <your-container-registry>
sudo docker push <your-container-registry>/videoanalyzer:1.0
```

## Deploy

### Container Create Options
```
{
    "HostConfig": {
        "Privileged": true,
        "Devices": [
            {
                "PathOnHost": "/dev/video0",
                "PathInContainer": "/dev/video0",
                "CgroupPermissions": "mrw"
            }
        ]
    }
}
```

### Module Twin Settings
With desired properties, we can change the behavior:
- `predictionUrl`, the prediction url - Default 'http://xxxx/image'
- `predictionInterval`, the prediction interval in seconds - Default 10

```
{
    "predictionUrl": "http://xxxx/image",
    "predictionInterval": 10
}
```