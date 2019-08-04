#see ~/aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging, time, json, os



IOT_HOST = os.getenv("IOT_HOST")
ROOTCAPATH = os.getenv("ROOTCAPATH")
CERTIFICATEPATH = os.getenv("CERTIFICATEPATH")
PRIVATEKEYPATH = os.getenv("PRIVATEKEYPATH")
IOT_PORT = int(os.getenv("IOT_PORT"))
IOT_CLIENT_ID = os.getenv("IOT_CLIENT_ID")
IOT_PUBLISH_TOPIC = os.getenv("IOT_PUBLISH_TOPIC")
IOT_SUBSCRIBE_TOPIC = os.getenv("IOT_SUBSCRIBE_TOPIC")

DEBUG=False
if(DEBUG):
    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

def createAwsIotMqttClient():
    # Init AWSIoTMQTTClient
    client = None
    client = AWSIoTMQTTClient(IOT_CLIENT_ID)
    client.configureEndpoint(IOT_HOST, IOT_PORT)
    client.configureCredentials(ROOTCAPATH, PRIVATEKEYPATH, CERTIFICATEPATH)

    # AWSIoTMQTTClient connection configuration
    client.configureAutoReconnectBackoffTime(1, 32, 20)
    client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    client.configureDrainingFrequency(2)  # Draining: 2 Hz
    client.configureConnectDisconnectTimeout(10)  # 10 sec
    client.configureMQTTOperationTimeout(5)  # 5 sec
    return client

def initializeClient(client):
    client.connect()

def addSubscription(topic, callback, client, qos=1):
    client.subscribe(topic, qos, callback)
    time.sleep(2)

# Custom MQTT message callback
def printMessageCallback(client, userdata, message):
    print("Received a new message: ")
    print("ts:")
    print(message.timestamp)
    print("payload:")
    print(message.payload)
    print("topic:")
    print(message.topic)
    print("--------------\n\n")


if __name__ == "__main__":
    awsIoTMQTTClient = createAwsIotMqttClient()
    initializeClient(awsIoTMQTTClient)
    addSubscription(IOT_SUBSCRIBE_TOPIC, printMessageCallback, awsIoTMQTTClient)

    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        message = {}
        message['message'] = "hello from {}".format(IOT_CLIENT_ID)
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        awsIoTMQTTClient.publish(IOT_PUBLISH_TOPIC, messageJson, 1)
        print('Published topic %s: %s\n' % (IOT_PUBLISH_TOPIC, messageJson))
        loopCount += 1
        time.sleep(1)
