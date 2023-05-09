import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
TRANSMITTER_PIN = 17
RECEIVER_PIN = 27
GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)
GPIO.setup(RECEIVER_PIN, GPIO.IN)


def toggle_lights(lane1, lane2):
    # Toggle the lights in each lane
    lane1.toggle()
    lane2.toggle()


def laserSetup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)
    GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
    GPIO.setup(RECEIVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def run_traffic_simulation():
    # Initialize the lane objects
    lane1 = TrafficLane('Lane 1')
    lane2 = TrafficLane('Lane 2')

    while True:
        # Check if car is detected in Lane 2
        car_detected = detect_car()

        # Set Lane 1 green and Lane 2 red
        lane1.set_green()
        lane2.set_red()
        print_lights(lane1, lane2)
        time.sleep(5)

        # Set Lane 1 yellow and Lane 2 red
        lane1.set_yellow()
        print_lights(lane1, lane2)
        time.sleep(2)

        # Set Lane 1 red and Lane 2 green if car is detected
        if car_detected:
            lane1.set_red()
            lane2.set_green()
            print_lights(lane1, lane2)
            time.sleep(5)
        else:
            print("No car detected in Lane 2")

        # Set Lane 1 red and Lane 2 yellow
        lane1.set_red()
        lane2.set_yellow()
        print_lights(lane1, lane2)
        time.sleep(2)


def detect_car():
    # Simulated car detection mechanism using laser interruption
    # Replace this with your actual laser sensor detection logic
    if GPIO.input(RECEIVER_PIN) == GPIO.HIGH:
        return True
    else:
        return False


def print_lights(lane1, lane2):
    # Print the status of the lights in each lane
    print(f'{lane1.name}: {lane1.light_color}')
    print(f'{lane2.name}: {lane2.light_color}')
    print('---')


class TrafficLane:
    def __init__(self, name):
        self.name = name
        self.light_color = 'Red'

    def toggle(self):
        # Toggle the light color
        if self.light_color == 'Red':
            self.light_color = 'Green'
        else:
            self.light_color = 'Red'

    def set_red(self):
        # Set the light color to red
        self.light_color = 'Red'

    def set_green(self):
        # Set the light color to green
        self.light_color = 'Green'

    def set_yellow(self):
        # Set the light color to yellow
        self.light_color = 'Yellow'


if __name__ == "__main__":
    # Set up the laser sensor
    laserSetup()

    # Run the traffic simulation
    try:
        run_traffic_simulation()
    except KeyboardInterrupt:
        GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
        GPIO.cleanup()
