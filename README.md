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
* set up authentication with AWS IoT
* refactor scripts so i can take out default params
* add resource tags 
* investigate whether i need kms on the environment variables
  * can encrypt in transit using CMK but that is $1 per month which seems like it might be overkill
  * environment variables are encrypted at rest by default
  * ssm-secure looks interesting but isn't available for all resource types
    * ssm + default at rest encryption ?
    * then the tokens are only inside AWS after initial set?

## Resources
* [how to create a python lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)
* [ssm-secure](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html) looks useful but is only supported on certain resource types

