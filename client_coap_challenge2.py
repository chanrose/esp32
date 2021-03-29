# Paula Andreas Broset
# COAP Challenge 2
import network
import machine
import microcoapy
from time import sleep
from machine import Pin

btn = Pin(27, Pin.IN, Pin.PULL_UP)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

_MY_SSID = 'AIU-WIFI'
_MY_PASS = ''
_SERVER_IP = '10.0.13.59'
# I am connecting to Andreas Server node here, for now we jus wanna see can we turn on the led or not
_SERVER_PORT = 5683  # default CoAP port
_COAP_POST_URL = 'dht/getValue'


def connectToWiFi():
    nets = wlan.scan()
    for net in nets:
        ssid = net[0].decode("utf-8")
        if ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(ssid, _MY_PASS)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting
            print('WLAN connection succeeded!')
            break

    return wlan.isconnected()


def sendPostRequest(client, message):
     # About to post message...
     
    messageId = client.post(_SERVER_IP, _SERVER_PORT, _COAP_POST_URL, "test",
                                    None, microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN)
    print("[POST] Message Id: ", messageId)

     # wait for response to our request for 2 seconds
    client.poll(10000)

# def sendPutRequest(client):
#     # About to post message...
#     messageId = client.put(_SERVER_IP, _SERVER_PORT, "led/turnOn", "test",
#                                    "authorization=1234567",
#                                    microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN)
#     print("[PUT] Message Id: ", messageId)
#
#     # wait for response to our request for 2 seconds
#     client.poll(10000)

def getDHT(packet, senderIp, senderPort):
    d.measure()
    temp = str(d.temperature()) + " deg celsius"
    hum = str(d.humidity()) + "g.kg^-1"
    message = temp + ", " + hum
    client.sendResponse(senderIp, senderPort, packet.messageid, message, microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT, microcoapy.COAP_CONTENT_FORMAT.COAP_NONE,
                        
def sendGetRequest(client):
    # About to post message...
    messageId = client.get(_SERVER_IP, _SERVER_PORT, _COAP_POST_URL)
    print("[GET] Message Id: ", messageId, 'Sending URL...', _COAP_POST_URL)

    # wait for response to our request for 2 seconds
    if client.poll(10000):
        print("Request received")
    else:
        print("no message received")

    if client.poll(10000):
        print("message received 2")
    else:
        print("no message received 2")

    # if client.state == self.TRANSMISSION_STATE.STATE_SEPARATE_ACK_RECEIVED_WAITING_DATA:
    #     client.state = self.TRANSMISSION_STATE.STATE_IDLE
    #     client.sendResponse(_SERVER_IP, _SERVER_PORT, packet.messageid,
    #                     None, macros.COAP_TYPE.COAP_ACK,
    #                     macros.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)

def receivedMessageCallback(packet, sender):
    print('Message received:', packet.toString(), ', from: ', sender)
    
    
connectToWiFi()

client = microcoapy.Coap()
client.discardRetransmissions = True
#client.debug = False
# setup callback for incoming response to a request
client.responseCallback = receivedMessageCallback

# Starting CoAP...
client.start()

# sendPostRequest(client)
# sendPutRequest(client)


while True:
    sleep(1)
    sendPostRequest(client)
   
    
# stop CoAP
client.stop()
