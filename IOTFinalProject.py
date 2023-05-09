#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

# GPIO channel numbers for RGB LED pins
PIN_R = 11
PIN_G = 6
PIN_B = 13

# Colors in RGB format
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_R, GPIO.OUT)
GPIO.setup(PIN_G, GPIO.OUT)
GPIO.setup(PIN_B, GPIO.OUT)

# Initialize PWM instances for each pin
p_R = GPIO.PWM(PIN_R, 2000)  # Frequency: 2KHz
p_G = GPIO.PWM(PIN_G, 2000)
p_B = GPIO.PWM(PIN_B, 2000)

# Start with all LEDs off
p_R.start(0)
p_G.start(0)
p_B.start(0)


def set_color(color):
    # Set the RGB LED color
    r, g, b = color

    # Map color values from 0-255 to 0-100 (duty cycle)
    r = map_value(r, 0, 255, 0, 100)
    g = map_value(g, 0, 255, 0, 100)
    b = map_value(b, 0, 255, 0, 100)

    # Set duty cycle for each pin
    p_R.ChangeDutyCycle(r)
    p_G.ChangeDutyCycle(g)
    p_B.ChangeDutyCycle(b)


def map_value(x, in_min, in_max, out_min, out_max):
    # Map a value from one range to another
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


try:
    while True:
        # Set the RGB LED color based on the road light state
        road_light_state = input("Enter road light state (red/yellow/green): ")
        if road_light_state == "red":
            set_color(COLOR_RED)
        elif road_light_state == "yellow":
            set_color(COLOR_YELLOW)
        elif road_light_state == "green":
            set_color(COLOR_GREEN)
        else:
            print("Invalid road light state. Please enter red, yellow, or green.")

        time.sleep(1)

except KeyboardInterrupt:
    # Cleanup GPIO and stop PWM
    p_R.stop()
    p_G.stop()
    p_B.stop()
    GPIO.cleanup()
