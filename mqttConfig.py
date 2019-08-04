#see ~/aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging, time, json, os

AllowedActions = ['both', 'publish', 'subscribe']

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print("client: ")
    print(client)
    print("userdata:")
    print(userdata)
    print("message:")
    print(message.keys())
    print("message payload:")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


host = os.getenv("IOT_HOST")
rootCAPath = os.getenv("ROOTCAPATH")
certificatePath = os.getenv("CERTIFICATEPATH")
privateKeyPath = os.getenv("PRIVATEKEYPATH")
port = int(os.getenv("IOT_PORT"))
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

def createAwsIotMqttClient():
    # Init AWSIoTMQTTClient
    client = None
    client = AWSIoTMQTTClient(clientId)
    client.configureEndpoint(host, port)
    client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

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


if __name__ == "__main__":
    awsIoTMQTTClient = createAwsIotMqttClient()
    initializeClient(awsIoTMQTTClient)
    addSubscription(subscribeTopic, customCallback, awsIoTMQTTClient)

    # Publish to the same topic in a loop forever
    loopCount = 0
    while True:
        message = {}
        message['message'] = "hello from {}".format(clientId)
        message['sequence'] = loopCount
        messageJson = json.dumps(message)
        awsIoTMQTTClient.publish(publishTopic, messageJson, 1)
        print('Published topic %s: %s\n' % (publishTopic, messageJson))
        loopCount += 1
        time.sleep(1)
