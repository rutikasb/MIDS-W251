#!/usr/bin/env python

import os, sys
import paho.mqtt.client as mqtt
import ibm_boto3
import time
import traceback
import cv2
from io import BytesIO
from PIL import Image
from ibm_botocore.client import Config

MQTT_BROKER = "broker"
MQTT_TOPIC = "faces"
BUCKET_NAME = "rutika-hw03"
Connected = False

# Boto S3 client configuration
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us.cloud-object-storage.appdomain.cloud'

creds = {"apikey": "<api-key>",
  "cos_hmac_keys": {
    "access_key_id": "<access-key-id>",
    "secret_access_key": "<secret-access-key>"
  },
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "iam_apikey_description": "Auto-generated for key bcecf662-88c6-48af-bbbd-d3d6c8489452",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/37d593cd072c45d790ab0474d61bb350::serviceid:ServiceId-3679517e-28b6-4607-b542-c6d6b6cfb1f2",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/37d593cd072c45d790ab0474d61bb350:b65eb2aa-38a0-455d-b0d6-543d259c7a6c::"
}

auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us.cloud-object-storage.appdomain.cloud'
resource = ibm_boto3.resource('s3', ibm_api_key_id=creds['apikey'], ibm_service_instance_id=creds['resource_instance_id'], ibm_auth_endpoint=auth_endpoint, config=Config(signature_version='oauth'), endpoint_url=service_endpoint)

# resource.meta.client.upload_file("/Users/rutika/Desktop/iam.JPG", "rutika-hw03", "iam.JPG")

def on_message(client, userdata, message):
    print("Message received")
    try:
        # convert the byte array to jpg image and upload to object storage
        key = str(time.time()) + ".jpg"
        img_path = "/home/" + key
        img = Image.open(BytesIO(message.payload))
        img.save(img_path)
        resource.meta.client.upload_file(img_path, "rutika-hw03", key)
        os.remove(img_path)
        print("--------------")
    except:
        print("Exception")
        os.remove(img_path)
        traceback.print_exc(file=sys.stdout)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = true
    else:
        print("Connection to broker failed")

# create mqtt client for subscribing
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(MQTT_BROKER, port=1883)
mqttc.subscribe(MQTT_TOPIC)

mqttc.loop_start()

# while Connected != True:
#     time.sleep(0.1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
    mqttc.disconnect()
    mqttc.loop_stop()
