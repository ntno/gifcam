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

led_1 = 10 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
buttonLed = GPIO.PWM(led_1, 10)
buttonLed.start(0)

led_2 = 12 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)
statusLed = GPIO.PWM(led_2, 12)
statusLed.start(0)

def turnOnButtonLight():
    buttonLed.ChangeDutyCycle(50)

def turnOffButtonLight():
    buttonLed.ChangeDutyCycle(0)

def turnOnStatusLight():
    statusLed.ChangeDutyCycle(50)

def turnOffStatusLight():
    statusLed.ChangeDutyCycle(0)

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    turnOnButtonLight()
    turnOnStatusLight()
    cleanup()
