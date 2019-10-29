import os, random, string, json, subprocess
from time import sleep
from pathlib import Path
from pinConfig import isButtonPressed, turnOffButtonLight, turnOnButtonLight, turnOffStatusLight, turnOnStatusLight, flashButtonLight, flashStatusLight, cleanup
from cameraConfig import createGif, captureFrames, copyFramesForRebound, moveFramesToFolder
from mqttConfig import createAwsIotMqttClient, initializeClient, addSubscription, printMessageCallback, IOT_PUBLISH_TOPIC, IOT_SUBSCRIBE_TOPIC
from lambdas.generateUrl.generateUrl import postToPresignedUrl, deleteToPresignedUrl

########################
#
# Behaviour Variables
#
########################
REBOUND = False      # Create a video that loops start <=> end
UPLOAD = True       # uploads the GIF to S3 after capturing

def uploadFramesToS3(presignedUrlResponse):
    pathToFrames = presignedUrlResponse['info']['frames']
    lsCommand = "ls -tr {}".format(pathToFrames) 
    cleanedFileListing = lsCommand + "| awk '{print $0}'"
    lsResult = subprocess.check_output(cleanedFileListing, shell=True)
    lsResult = str(lsResult, "utf-8").rstrip().split('\n')
    
    numFrames = len(lsResult) + 1
    frames = []
    for i in range(0, numFrames):
        pathToFrame = os.path.join(pathToFrames, lsResult[i])
        frames.append(Path(pathToFrame))

    responseCodes = []
    for p in frames:
        response = postToPresignedUrl(presignedUrlResponse['post'], p)
        responseCodes.append(response.status_code)
    
    return responseCodes

def markFrameUploadComplete(presignedUrlResponse):
    deleteToPresignedUrl(presignedUrlResponse['delete'])

def requestPresignedUrl(client, fileName, info=None):
    flashButtonLight()
    message = {}
    message['fileName'] = fileName
    message['info'] = info
    messageJson = json.dumps(message)
    client.publish(IOT_PUBLISH_TOPIC, messageJson, 1)

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def postFramesToS3CallBack(client, userdata, message):
    bytesPayload = message.payload
    payloadAsStr = str(bytesPayload, "utf-8")
    payload = json.loads(payloadAsStr)
    responseCodes = uploadFramesToS3(payload)
    invalidResponses = [item for item in responseCodes if item != 204]
    if(len(invalidResponses) == 0):
        markFrameUploadComplete(payload) 
    turnOffButtonLight()

if __name__ == "__main__":
    if(UPLOAD):
        print("Intializing AWS MQTT Client")
        awsClient = createAwsIotMqttClient()
        initializeClient(awsClient)
        addSubscription(IOT_SUBSCRIBE_TOPIC, postFramesToS3CallBack, awsClient)
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
                print('Done')
                print('System Ready')

            else : # Button NOT pressed
                ### READY TO MAKE GIF ###
                turnOnStatusLight()
                sleep(0.05)

    except:
        cleanup()