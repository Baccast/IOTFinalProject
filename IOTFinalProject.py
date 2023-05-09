import RPi.GPIO as GPIO
import time

# RGB LED pins
PIN_R = 5
PIN_G = 6
PIN_B = 13

# Traffic light pins
LIGHT_GREEN_PIN = 15
LIGHT_YELLOW_PIN = 16
LIGHT_RED_PIN = 18

# RGB LED colors
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

# Traffic light durations (in seconds)
GREEN_DURATION = 5
YELLOW_DURATION = 2
RED_DURATION = 5

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)

# Set up RGB LED pins
GPIO.setup(PIN_R, GPIO.OUT)
GPIO.setup(PIN_G, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)
GPIO.output(PIN_R, GPIO.HIGH)
GPIO.output(PIN_G, GPIO.HIGH)
GPIO.output(PIN_B, GPIO.HIGH)

# Set up traffic light pins
GPIO.setup(LIGHT_GREEN_PIN, GPIO.OUT)
GPIO.setup(LIGHT_YELLOW_PIN, GPIO.OUT)
GPIO.setup(LIGHT_RED_PIN, GPIO.OUT)


def set_rgb_color(color):
    # Since LED is common anode, use inverted logic
    GPIO.output(PIN_R, not color[0])
    GPIO.output(PIN_G, not color[1])
    GPIO.output(PIN_B, not color[2])


def set_traffic_light(color):
    GPIO.output(LIGHT_GREEN_PIN, GPIO.LOW)
    GPIO.output(LIGHT_YELLOW_PIN, GPIO.LOW)
    GPIO.output(LIGHT_RED_PIN, GPIO.LOW)

    if color == 'green':
        GPIO.output(LIGHT_GREEN_PIN, GPIO.HIGH)
    elif color == 'yellow':
        GPIO.output(LIGHT_YELLOW_PIN, GPIO.HIGH)
    elif color == 'red':
        GPIO.output(LIGHT_RED_PIN, GPIO.HIGH)


try:
    while True:
        # Set traffic light to green
        set_traffic_light('green')
        set_rgb_color(COLOR_GREEN)
        time.sleep(GREEN_DURATION)

        # Set traffic light to yellow
        set_traffic_light('yellow')
        set_rgb_color(COLOR_YELLOW)
        time.sleep(YELLOW_DURATION)

        # Set traffic light to red
        set_traffic_light('red')
        set_rgb_color(COLOR_RED)
        time.sleep(RED_DURATION)

except KeyboardInterrupt:
    GPIO.cleanup()
