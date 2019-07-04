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
* remove files from pi after successful upload to AWS

## Future Enhancements 
* (requires $) encrypt environment variables in transit via CMK
  * ssm-secure looks interesting but isn't available for all resource types
    * ssm + default at rest encryption ?
    * then the tokens are only inside AWS after initial set?
* handle no wifi connection

## Resources
* [how to create a python lambda deployment package](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)
* [ssm-secure](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html) looks useful but is only supported on certain resource types
* [iot lifecycle presentation](https://www.slideshare.net/AmazonWebServices/the-lifecycle-of-an-aws-iot-thing)
* [iot security white paper](https://d1.awsstatic.com/whitepapers/architecture/AWS-IoT-Lens.pdf)
* [simple aws iot setup](https://teenenggr.in/2018/10/11/how-to-setup-aws-iot-with-raspberrypi/)
* [aws iot architecture example](https://www.youtube.com/watch?v=gKMaf5E-z7Q&feature=youtu.be&t=2312)

## Extra Installation Steps for AWS integration
--see @nickbrewer install doc first: [README.md](https://github.com/nickbrewer/gifcam)--


[ssl module is not available error](https://stackoverflow.com/questions/44290926/pip-cannot-confirm-ssl-certificate-ssl-module-is-not-available)

hopefully if you run these commands first you won't have to reconfigure / remake later
* `sudo apt-get install build-essential checkinstall`
* `sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev`

[how to install python 3.6 on pi](https://raspberrypi.stackexchange.com/questions/59381/how-do-i-update-my-rpi3-to-python-3-6)
* `wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz`
* `tar xzvf Python-3.6.0.tgz`
* `cd Python-3.6.0/`
* `./configure`
* `make -j4`
* `sudo make install`

add local bin to PATH (set in .bashrc)

    #add user bin to path
    export PATH="$PATH:~/.local/bin"


install additional libraries (`pip3 install --user x`)
* awscli
* boto3
* AWSIoTPythonSDK
* RPi.GPIO
* picamera

