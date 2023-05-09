import time
import RPi.GPIO as GPIO
import tkinter as tk

# Set up GPIO pins
TRANSMITTER_PIN = 17
RECEIVER_PIN = 27
BUTTON_PIN = 22


class TrafficLightGUI:
    def __init__(self, root):
        self.root = root
        self.lane1_light = tk.Label(
            root, text='Lane 1: Red', font=('Arial', 16), fg='red')
        self.lane2_light = tk.Label(
            root, text='Lane 2: Red', font=('Arial', 16), fg='red')
        self.status_label = tk.Label(
            root, text='', font=('Arial', 16), fg='black')
        self.lane1_light.pack()
        self.lane2_light.pack()
        self.status_label.pack()

    def update_lights(self, lane1_color, lane2_color):
        self.lane1_light.config(
            text=f'Lane 1: {lane1_color}', fg='green' if lane1_color == 'Green' else 'red')
        self.lane2_light.config(
            text=f'Lane 2: {lane2_color}', fg='green' if lane2_color == 'Green' else 'red')
        self.root.update()

    def update_status(self, status):
        self.status_label.config(text=status)
        self.root.update()


def toggle_lights(lane1, lane2):
    # Toggle the lights in each lane
    lane1.toggle()
    lane2.toggle()


def laserSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering for GPIO pins
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)  # Set pin mode as output
    GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
    GPIO.setup(RECEIVER_PIN, GPIO.IN)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Set LaserRecvPin's mode as input, and pull up to high level(3.3V)
    GPIO.setup(RECEIVER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def run_traffic_simulation(gui):
    # Initialize the lane objects
    lane1 = TrafficLane('Lane 1')
    lane2 = TrafficLane('Lane 2')

    car_detected = False
    car_previous_state = False

    while True:
        # Check if car is detected in Lane 2
        car_detected = detect_car()

        if car_detected and not car_previous_state:
            print("Car detected in Lane 2")
            time.sleep(3)

        # Set Lane 1 green and Lane 2 red
        lane1.set_green()
        lane2.set_red()
        gui.update_lights(lane1.light_color, lane2.light_color)
        time.sleep(5)

        # Set Lane 1 red and Lane 2 green if car is detected
        if car_detected:
            lane1.set_yellow()
            time.sleep(2)
            lane1.set_red()
            lane2.set_green()
            gui.update_lights(lane1.light_color, lane2.light_color)
            time.sleep(5)
        else:
            print("No car detected in Lane 2")

        car_previous_state = car_detected


def detect_car():
    # Simulated car detection mechanism using laser interruption
    # Replace this with your actual laser sensor detection logic
    if GPIO.input(RECEIVER_PIN) == GPIO.LOW:
        return True
    else:
        return False
    time.sleep(0.1)


def handle_button_click(channel):
    # Handle button click event
    print("Button clicked")
    # Set Lane 1 and Lane 2 lights to red for 10 seconds
    lane1.set_red()
    lane2.set_red()
    gui.update_lights(lane1.light_color, lane2.light_color)
    gui.update_status("Someone is crossing the road")
    time.sleep(10)
    gui.update_status("")


def setup_button():
    # Set up button event detection
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
                          callback=handle_button_click, bouncetime=200)


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
    # Set up the laser sensor and button
    laserSetup()
    setup_button()

    # Create the GUI window
    root = tk.Tk()
    root.title("Traffic Light Simulation")

    # Create the GUI object
    gui = TrafficLightGUI(root)

    # Run the traffic simulation
    try:
        run_traffic_simulation(gui)
    except KeyboardInterrupt:
        GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
        GPIO.cleanup()
