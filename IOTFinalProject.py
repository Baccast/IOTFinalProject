import time
import RPi.GPIO as GPIO
import tkinter as tk

# Set up GPIO pins
TRANSMITTER_PIN = 17
RECEIVER_PIN = 27
BUTTON_PIN = 22

# GUI settings


class TrafficLightGUI:
    def __init__(self, root):
        self.root = root
        self.lane1_light = tk.Label(
            root, text='Lane 1: Red', font=('Arial', 16), fg='red')
        self.lane2_light = tk.Label(
            root, text='Lane 2: Red', font=('Arial', 16), fg='red')
        self.lane1_light.pack()
        self.lane2_light.pack()

    # Update the traffic light colors
    def update_lights(self, lane1_color, lane2_color):
        self.lane1_light.config(
            text=f'Lane 1: {lane1_color}', fg='green' if lane1_color == 'Green' else 'red')
        self.lane2_light.config(
            text=f'Lane 2: {lane2_color}', fg='green' if lane2_color == 'Green' else 'red')
        self.root.update()

# Toggle the lights in each lane


def toggle_lights(lane1, lane2):
    # Toggle the lights in each lane
    lane1.toggle()
    lane2.toggle()

# Set up the laser sensor


def laserSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering for GPIO pins
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)  # Set pin mode as output
    GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
    GPIO.setup(RECEIVER_PIN, GPIO.IN)
    # Set LaserRecvPin's mode as input, and pull up to high level(3.3V)
    GPIO.setup(RECEIVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Run the traffic simulation


def run_traffic_simulation(gui):
    # Initialize the lane objects
    lane1 = TrafficLane('Lane 1')
    lane2 = TrafficLane('Lane 2')

    car_detected = False
    car_previous_state = False

    while True:
        # Check if car is detected in Lane 2
        car_detected = detect_car()
        button_detected = detect_button()

        # If button pressed print "Button Pressed"
        if button_detected:
            print("Button Pressed")

        if car_detected and not car_previous_state:
            print("Car detected in Lane 2")
            time.sleep(2)
            lane1.set_yellow()
            time.sleep(2)
            lane1.set_red()
            lane2.set_green()
            gui.update_lights(lane1.light_color, lane2.light_color)
            time.sleep(5)

        # Set Lane 1 green and Lane 2 red
        lane1.set_green()
        lane2.set_red()
        gui.update_lights(lane1.light_color, lane2.light_color)
        time.sleep(5)

        car_previous_state = car_detected

# Simulate the car detection mechanism


def detect_button():
    # Check whether the button is pressed or not.
    button_state = GPIO.input(BUTTON_PIN)
    if button_state == GPIO.LOW:
        # Wait for button release
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        return True
    else:
        return False


def detect_car():
    # Simulated car detection mechanism using laser interruption
    # Replace this with your actual laser sensor detection logic
    if GPIO.input(RECEIVER_PIN) == GPIO.LOW:
        return True
    else:
        return False
    time.sleep(0.1)

# Traffic lane class


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
        self.light_color = 'Red'

    def set_green(self):
        self.light_color = 'Green'

    def set_yellow(self):
        self.light_color = 'Yellow'


# Main function
if __name__ == '__main__':
    laserSetup()
    root = tk.Tk()
    root.title('Traffic Light Simulation')
    root.geometry('400x200')
    gui = TrafficLightGUI(root)
    run_traffic_simulation(gui)
