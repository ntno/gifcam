fork of [nickbrewer/gifcam](https://github.com/nickbrewer/gifcam)

* updated to upload gifs to AWS S3 instead of Twitter
* lambda function triggered on file upload posts to Twitter 

## Hardware WIP photos
see [hardware/](https://github.com/ntno/gifcam/tree/master/hardware)

## How To Use the Camera
- Power on the camera.
- The red status light will illuminate when the camera is ready to make a GIF.
- When you press the button, the status LED will strobe to indicate that the camera is recording.
- When recording finishes, the status LED will switch off.
- The button LED will blink while the GIF is being processed
- When processing is finished, the camera will return to the READY state, and the status LED will illuminate.


## TODOs
* add logging permission to lambda function
* figure out how to include pip dependency (twython)
* set up authentication with AWS IoT
* refactor scripts so i can take out default params
* add resource tags 
* investigate whether i need kms on the environment variables