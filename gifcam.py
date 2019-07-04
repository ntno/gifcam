import picamera, os, random, string
from time import sleep
from pinConfig import isButtonPressed, turnOffButtonLight, turnOnButtonLight, turnOffStatusLight, turnOnStatusLight, flashButtonLight, flashStatusLight, cleanup


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
turnOnStatusLight()

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
        if isButtonPressed():
            ### TAKING PICTURES ###
            print('Capture Started')
            turnOffStatusLight()
            flashButtonLight()
            captureFrames()
            turnOffButtonLight()

            ### PROCESSING GIF ###
            print('Processing Gif')
            flashStatusLight()
            if rebound == True: # make copy of images in reverse order
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
