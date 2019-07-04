import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string

########################
#
# Behaviour Variables
#
########################
num_frame = 8       # Number of frames in Gif
gif_delay = 15      # Frame delay [ms]
rebound = True      # Create a video that loops start <=> end
UPLOAD = True       # uploads the GIF to S3 after capturing


########################
#
# Define GPIO
#
########################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 19 #Button GPIO Pin
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led_1 = 10 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
buttonLed = GPIO.PWM(led_1, 10)
led_2 = 12 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)
statusLed = GPIO.PWM(led_2, 2)


########################
#
# Camera
#
########################
camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
##GPIO.output(led_2, 1)

# Indicate ready status
buttonLed.start(100)
statusLed.start(0)

print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def uploadToS3():
    pass
    # try:
    #     print('Posting to Twitter')
    #     photo = open(filename + ".gif", 'rb')
    #     response = twitter.upload_media(media=photo)
    #     twitter.update_status(status='Taken with #PIX-E Gif Camera', media_ids=[response['media_id']])
    # except:
    #     # Display error with long status light
    #     statusLed.ChangeDutyCycle(100)
    #     buttonLed.ChangeDutyCycle(0)
    #     sleep(2)

def captureFrames(numFrames=num_frame):
    for i in range(numFrames):
        camera.capture('{0:04d}.jpg'.format(i))

def copyFramesForRebound(numFrames=num_frame):
    for i in range(numFrames - 1):
        source = str(numFrames - i - 1) + ".jpg"
        source = source.zfill(8) # pad with zeros
        dest = str(numFrames + i) + ".jpg"
        dest = dest.zfill(8) # pad with zeros
        copyCommand = "cp " + source + " " + dest
        os.system(copyCommand)

def createGif(filename, delay=gif_delay):
    print('Processing')
    graphicsmagickCommand = "gm convert -delay " + str(delay) + " " + "*.jpg " + filename + ".gif"
    os.system(graphicsmagickCommand)
    os.system("rm ./*.jpg") # cleanup source images

try:
    while True:
        if GPIO.input(button) == False: # Button Pressed

            ### TAKING PICTURES ###
            print('Gif Started')
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(50)

            randomstring = random_generator()
            captureFrames()

            ### PROCESSING GIF ###
            statusLed.ChangeDutyCycle(50)
            buttonLed.ChangeDutyCycle(0)
            if rebound == True: # make copy of images in reverse order
                copyFramesForRebound()
                
            filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
            createGif(filename)

            ### UPLOAD TO AWS ###
            if(UPLOAD):
                statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                uploadToS3()

            print('Done')
            print('System Ready')

        else : # Button NOT pressed
            ### READY TO MAKE GIF ###
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(100)
            sleep(0.05)

except:
    GPIO.cleanup()
