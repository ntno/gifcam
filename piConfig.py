import RPi.GPIO as GPIO

########################
#
# Define GPIO
#
########################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button_pin = 19 #Button GPIO Pin
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

status_led_pin = 10 
GPIO.setup(status_led_pin, GPIO.OUT)
statusLed = GPIO.PWM(status_led_pin, 2)
statusLed.start(0)

button_led_pin = 12
GPIO.setup(button_led_pin, GPIO.OUT)
buttonLed = GPIO.PWM(button_led_pin, 2)
buttonLed.start(0)

def isButtonPressed():
    return GPIO.input(button_pin) == False

def turnOnButtonLight():
    buttonLed.ChangeDutyCycle(100)

def flashButtonLight():
    buttonLed.ChangeDutyCycle(50)

def turnOffButtonLight():
    buttonLed.ChangeDutyCycle(0)

def turnOnStatusLight():
    statusLed.ChangeDutyCycle(100)

def flashStatusLight():
    statusLed.ChangeDutyCycle(50)

def turnOffStatusLight():
    statusLed.ChangeDutyCycle(0)

def cleanup():
    buttonLed.stop()
    statusLed.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    turnOnButtonLight()
    turnOnStatusLight()
    cleanup()
