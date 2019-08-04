import os, random, string, json
from time import sleep
from pathlib import Path
from pinConfig import isButtonPressed, turnOffButtonLight, turnOnButtonLight, turnOffStatusLight, turnOnStatusLight, flashButtonLight, flashStatusLight, cleanup
from cameraConfig import createGif, captureFrames, copyFramesForRebound, moveFramesToFolder
from mqttConfig import createAwsIotMqttClient, initializeClient, addSubscription, printMessageCallback, IOT_PUBLISH_TOPIC, IOT_SUBSCRIBE_TOPIC
from lambdas.generateUrl.generateUrl import postToPresignedUrl

########################
#
# Behaviour Variables
#
########################
REBOUND = False      # Create a video that loops start <=> end
UPLOAD = True       # uploads the GIF to S3 after capturing

def uploadFramesToS3(presignedUrlResponse):
    pathToFrames = presignedUrlResponse['info']['frames']
    lsCommand = "ls -tr {} | awk '{print $0}'".format(pathToFrames)
    lsResult = subprocess.check_output(lsCommand, shell=True)
    lsResult = str(lsResult, "utf-8").rstrip().split('\n')
    
    numFrames = len(lsResult) + 1
    frames = []
    for i in range(0, numFrames):
        pathToFrame = os.path.join(pathToFrames, lsResult[i])
        frames.append(Path(pathToFrame))

    for p in frames:
        response = postToPresignedUrl(presignedUrlResponse, p)
        print(p, response.status_code)

def requestPresignedUrl(client, fileName, info=None):
    message = {}
    message['fileName'] = fileName
    message['info'] = info
    messageJson = json.dumps(message)
    client.publish(IOT_PUBLISH_TOPIC, messageJson, 1)

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def presignedUrlResponseCallBack(client, userdata, message):
    print("\n\n--------------")
    print("Received a new message: ")
    print("ts:")
    print(message.timestamp)
    print("payload:")
    print(message.payload)
    print("topic:")
    print(message.topic)
    bytesPayload = message.payload
    payloadAsStr = str(bytesPayload, "utf-8")
    payload = json.loads(payloadAsStr)
    uploadFramesToS3(payload)
    print("--------------\n\n")


if __name__ == "__main__":
    if(UPLOAD):
        print("Intializing AWS MQTT Client")
        awsClient = createAwsIotMqttClient()
        initializeClient(awsClient)
        addSubscription(IOT_SUBSCRIBE_TOPIC, printMessageCallback, awsClient)
        print("Done initializing AWS MQTT Client")


    # Indicate ready status
    turnOnStatusLight()

    print("System Ready")

    try:
        while True:
            if isButtonPressed():
                ### TAKING PICTURES ###
                print('Capture Started')
                turnOffStatusLight()
                flashButtonLight()
                captureFrames()
                turnOffButtonLight()

                ### PROCESSING GIF ###
                print('Processing')
                flashStatusLight()
                if(REBOUND): # make copy of images in reverse order
                    copyFramesForRebound()

                randomstring = random_generator()
                folderName = '/home/pi/gifcam/jpgs/{}'.format(randomstring)  
                moveFramesToFolder(Path(folderName))
                if(UPLOAD):
                    info = {}
                    uploadFileName = "{}.jpg".format(randomstring)
                    info['uploadFileName'] = uploadFileName
                    info['frames'] = folderName
                    requestPresignedUrl(awsClient, uploadFileName, info)

                turnOffStatusLight()

                ### UPLOAD TO AWS ###
                if(UPLOAD):
                    flashButtonLight()
                    uploadToS3()
                    turnOffButtonLight()

                print('Done')
                print('System Ready')

            else : # Button NOT pressed
                ### READY TO MAKE GIF ###
                turnOnStatusLight()
                sleep(0.05)

    except:
        cleanup()