# Homework 3 - Internet of Things 101

## Overall architecture/flow
![flow](hw03.png)

## Running containers on TX2

### Build the following images for
1. Face detector and publisher
2. MQTT Broker
3. MQTT message forwarder
```
docker build -t detector -f face_detector/Dockerfile .
docker build -t broker -f mqtt_broker/Dockerfile .
docker build -t forwarder -f mqtt_forwarder/Dockerfile .
```

### Launch the containers for the above images in a docker network
```
# create a bridge named hw03
docker network create --driver bridge hw03

# launch the detector container and run the python script to capture images
# from USB cam and publish it to the broker
xhost local:root
docker run --name detector -e DISPLAY=$DISPLAY --privileged --network hw03 -v /tmp:/tmp --device /dev/video1 -t detector
docker cp face_detector/detector.py detector:/home/detector.py
docker exec detector /bin/sh -c "python /home/detector.py"


# launch the MQTT broker container
docker run --name broker --network hw03 -p 1883:1883 -t broker


# launch the MQTT message forwarder and subscribe to the topic
docker run --name forwarder --network hw03 -ti forwarder
docker cp mqtt_forwarder/forwarder.py forwarder:/home/
docker exec forwarder /bin/sh -c "python /home/forwarder.py"
```


## Setting up cloud environment

1. For running the containers on the VMs, the VM setup in week 02 was used
2. An Object Storage was created via the IBM cloud console

Git clone this repository on the remote VM and build a docker network of 2 containers - mqtt broker and image saver/uploader

### Build images:
```
docker build -t broker -f mqtt_broker/Dockerfile .
docker build -t image_saver -f image_saver/Dockerfile .
```

### Launch conainers in a network
```
# create a bridge
docker network create --driver bridge hw03

# launch the MQTT broker container
docker run --name broker --network hw03 -p 1883:1883 -ti broker

# run the subscriber/image saver
docker run --name image_saver --network hw03 -t image_saver
docker cp image_saver/saver.py image_saver:/home/
docker exec image_saver /bin/sh -c "python /home/saver.py"
```


## Publishing

All the messages were published with qos=0 which publishes a message at most once. The recipient does not acknowledge receipt of the message and the message is not stored and re-transmitted. Since we're publishing images every second, it's okay if all messages are not delivered and we can afford to lose some data.
