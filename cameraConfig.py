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
    for i in range(numFrames):
        camera.capture('{0:04d}.jpg'.format(i))

def copyFramesForRebound(numFrames=num_frame):
    print("Copying captures for rebound")
    for i in range(numFrames - 1):
        source = str(numFrames - i - 1) + ".jpg"
        source = source.zfill(8) # pad with zeros
        dest = str(numFrames + i) + ".jpg"
        dest = dest.zfill(8) # pad with zeros
        copyCommand = "cp " + source + " " + dest
        os.system(copyCommand)

def createGif(filename, delay=gif_delay, removeFrames=False):
    print('Creating Gif')
    graphicsmagickCommand = "gm convert -delay " + str(delay) + " " + "*.jpg " + filename + ".gif"
    os.system(graphicsmagickCommand)
    if(removeFrames):
        os.system("rm ./*.jpg") # cleanup source images
