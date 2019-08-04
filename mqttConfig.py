#see ~/aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging, time, json, os

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


host = os.getenv("IOT_HOST")
rootCAPath = os.getenv("ROOTCAPATH")
certificatePath = os.getenv("CERTIFICATEPATH")
privateKeyPath = os.getenv("PRIVATEKEYPATH")
port = os.getenv("IOT_PORT")
clientId = os.getenv("IOT_CLIENT_ID")
publishTopic = os.getenv("IOT_PUBLISH_TOPIC")
subscribeTopic = os.getenv("IOT_SUBSCRIBE_TOPIC")
# logLevel = os.getenv("LOG_LEVEL")


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(subscribeTopic, 1, customCallback)
time.sleep(2)

if __name__ == "__main__":
    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        message = {}
        message['message'] = "hello from {}".format(clientId)
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        myAWSIoTMQTTClient.publish(publishTopic, messageJson, 1)
        print('Published topic %s: %s\n' % (publishTopic, messageJson))
        loopCount += 1
        time.sleep(1)
