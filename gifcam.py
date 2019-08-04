import os, random, string
from time import sleep
from pinConfig import isButtonPressed, turnOffButtonLight, turnOnButtonLight, turnOffStatusLight, turnOnStatusLight, flashButtonLight, flashStatusLight, cleanup
from cameraConfig import createGif, captureFrames, copyFramesForRebound

########################
#
# Behaviour Variables
#
########################
REBOUND = False      # Create a video that loops start <=> end
UPLOAD = True       # uploads the GIF to S3 after capturing


# Indicate ready status
turnOnStatusLight()

print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def uploadToS3():
    pass

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
            filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
            createGif(filename)
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
