import RPi.GPIO as GPIO


########################
#
# Define GPIO
#
########################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 19 #Button GPIO Pin
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_1 = 10 
GPIO.setup(led_1, GPIO.OUT)

led_2 = 12
GPIO.setup(led_2, GPIO.OUT)

buttonLed = GPIO.PWM(led_2, led_2)
buttonLed.start(0)

statusLed = GPIO.PWM(led_1, led_1)
statusLed.start(0)

FLASH_RATE=20
ON_RATE=100

def turnOnButtonLight(onRate=ON_RATE):
    buttonLed.ChangeDutyCycle(onRate)

def flashButtonLight(flashRate=FLASH_RATE):
    buttonLed.ChangeDutyCycle(flashRate)

def turnOffButtonLight():
    buttonLed.ChangeDutyCycle(0)

def turnOnStatusLight(onRate=ON_RATE):
    statusLed.ChangeDutyCycle(onRate)

def flashStatusLight(flashRate=FLASH_RATE):
    statusLed.ChangeDutyCycle(flashRate)

def turnOffStatusLight():
    statusLed.ChangeDutyCycle(0)

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    turnOnButtonLight()
    turnOnStatusLight()
    cleanup()
