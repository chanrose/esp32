import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
import random
gc.collect()

ssid = 'ELIJAH-WIFI'
password = ''
mqtt_server = '172.21.3.184'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = b'zone-response'
topic_pub = b'zones'
current_time = 0
last_message = 0
message_interval = 1
counter = 0
zones = ["Z00", "Z15"]

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

c = 0
while station.isconnected() == False:
    print('Trying to connect {}'.format(c))
    c += 1
    time.sleep(0.5)
    pass

print('Connection successful')
print(station.ifconfig())
######################################

def sub_cb(topic, msg):
    print((topic, msg))
    green_light = msg.decode("utf-8")
    green_light = green_light.split("|")
    found_z00 = green_light[0].find(zones[0], 0)
    found_z15 = green_light[0].find(zones[1], 0)
    # print("Z00 finding:", found_z00, "Z15 finding: ", found_z15)
    is_z00_green_light = found_z00 > 0
    is_z15_green_light = found_z15 > 0
    if is_z00_green_light:
        remaining = green_light[0][found_z00 + 3: green_light[0].find(' sec')]
        print("Z00 Green Light is on", remaining)
    else:
        print("Z00 is Red Light")
    if is_z15_green_light:
        remaining = green_light[0][found_z15 + 3: green_light[0].find(' sec')]
        print("Z15 Green Light is on", remaining)
    else:
        print("Z15 is Red Light")
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to {} MQTT broker, subscribed to {} topic'.format(mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            msg = "#{}".format(counter)
            msg = b'Z00: V1 L0 | Z15: V0 LF'
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()

