import time
import RPi.GPIO as GPIO
import tkinter as tk
import threading

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
        lane1_text = f'Lane 1: {lane1_color}'
        lane2_text = f'Lane 2: {lane2_color}'
        lane1_fg_color = 'green' if lane1_color == 'Green' else 'red'
        lane2_fg_color = 'green' if lane2_color == 'Green' else 'red'

        if lane1_color == 'Yellow':
            lane1_text += ' (Caution!)'
            lane1_fg_color = 'yellow'

        if lane2_color == 'Yellow':
            lane2_text += ' (Caution!)'
            lane2_fg_color = 'yellow'

        self.lane1_light.config(text=lane1_text, fg=lane1_fg_color)
        self.lane2_light.config(text=lane2_text, fg=lane2_fg_color)
        self.root.update()


# Set up the laser sensor


def laserSetup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering for GPIO pins
    GPIO.setup(TRANSMITTER_PIN, GPIO.OUT)  # Set pin mode as output
    GPIO.output(TRANSMITTER_PIN, GPIO.HIGH)
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

        if car_detected and not car_previous_state:
            print("Car detected in Lane 2")
            time.sleep(2)
            lane1.set_yellow()
            time.sleep(2)
            lane1.set_red()
            lane2.set_green()
            gui.update_lights(lane1.light_color, lane2.light_color)
            time.sleep(5)
            car_previous_state = car_detected

        # Set Lane 1 green and Lane 2 red
        lane1.set_green()
        lane2.set_red()
        gui.update_lights(lane1.light_color, lane2.light_color)
        time.sleep(5)

        car_previous_state = car_detected

# Simulate the car detection mechanism

# Check for button input


def button_check():
    while True:
        button_detected = detect_button()
        if button_detected:
            print("Button Pressed")
            crossWalk()


def detect_button():
    # Check whether the button is pressed or not.
    button_state = GPIO.input(BUTTON_PIN)
    if button_state == GPIO.LOW:
        time.sleep(1)
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

# Traffic lane class


def crossWalk():
    lane1 = TrafficLane('Lane 1')
    lane2 = TrafficLane('Lane 2')

    time.sleep(3)
    lane1.set_yellow()
    lane2.set_yellow()
    gui.update_lights(lane1.light_color, lane2.light_color)
    time.sleep(2)
    # For 10 seconds force both lights to stay red
    endTime = time.time() + 10
    while time.time() < endTime:
        lane1.set_red()
        lane2.set_red()
        gui.update_lights(lane1.light_color, lane2.light_color)
        time.sleep(0.1)


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

    simulation_thread = threading.Thread(
        target=run_traffic_simulation, args=(gui,))
    button_thread = threading.Thread(target=button_check)

    simulation_thread.start()
    button_thread.start()

    root.mainloop()  # Start the GUI event loop

    # Wait for threads to finish
    simulation_thread.join()
    button_thread.join()
