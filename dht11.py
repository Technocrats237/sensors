#!/usr/bin/python
import Adafruit_DHT as DHT
import time
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt

sensor = DHT.DHT11
gpio = 4

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("$SYS/#")
    client.subscribe('technocrat/max_temp')
    client.subscribe('technocrat/max_humid')
    client.subscribe('technocrat/min_temp')
    client.subscribe('technocrat/min_humid')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("raspberrypi", 1883, 60)
client.loop_start()



try:
    last_temp, last_humid = 0, 0
    while True:
        start = time.time()
        humid, temp = DHT.read_retry(sensor, gpio, 1)
        end = time.time()
        if (temp and humid) is not None:
            last_temp, last_humid = temp, humid
            print("Temp: {0:.1f}*C \t Humid: {1:.1f}% in {2:.2f}s" .format(temp, humid, (end-start)))

            # sending the data to the server
            client.publish("technocrat/temp", temp)
            client.publish("technocrat/humid", humid)
        else:
            print("Failed to get reading. Please try again")
            client.publish("technocrat/temp", last_temp)
            client.publish("technocrat/humid", last_humid)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exit status received")
