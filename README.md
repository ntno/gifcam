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
