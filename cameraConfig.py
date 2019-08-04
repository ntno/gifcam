import picamera, os

num_frame = 8       # Number of frames in Gif
gif_delay = 15      # Frame delay [ms]

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

def captureFrames(numFrames=num_frame):
    print("Capturing {} Frames".format(numFrames))
    for i in range(numFrames):
        camera.capture('{0:04d}.jpg'.format(i))

def copyFramesForRebound(numFrames=num_frame):
    print("Copying captures for rebound")
    for i in range(numFrames - 1):
        source = '{}.jpg'.format(str(numFrames - i - 1))
        source = source.zfill(8) # pad with zeros

        dest = '{}.jpg'.format(str(numFrames + i))
        dest = dest.zfill(8) # pad with zeros

        copyCommand = 'cp {} {}'.format(source, dest)
        print("\t" + copyCommand)
        os.system(copyCommand)

def createGif(filename, delay=gif_delay, removeFrames=True):
    print('Creating Gif, delay={}'.format(delay))
    graphicsmagickCommand =  'gm convert -delay {} *.jpg {}.gif'.format(str(delay), filename)
    os.system(graphicsmagickCommand)
    if(removeFrames):
        os.system("rm ./*.jpg") # cleanup source images
