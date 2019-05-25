#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time

MQTT_LOCAL_BROKER = "broker"
MQTT_LOCAL_TOPIC = "faces"
MQTT_REMOTE_BROKER = "169.53.0.105"
MQTT_REMOTE_TOPIC = "faces"
Connected = False

# create mqtt client for remote broker
remote_client = mqtt.Client()
remote_client.connect(MQTT_REMOTE_BROKER, port=1883)

def on_message(client, userdata, message):
    print("Message received")
    remote_client.publish(MQTT_REMOTE_TOPIC, payload=message.payload, qos=0, retain=False)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = true
    else:
        print("Connection to broker failed")

# create local mqtt client for subscribing
local_client = mqtt.Client()
local_client.on_connect = on_connect
local_client.on_message = on_message
local_client.connect(MQTT_LOCAL_BROKER, port=1883)
local_client.subscribe(MQTT_LOCAL_TOPIC)

local_client.loop_start()

# while Connected != True:
#     time.sleep(0.1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting")
    local_client.disconnect()
    local_client.loop_stop()
