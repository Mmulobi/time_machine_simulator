# Improved Time machine simulation with tkinter GUI

import tkinter as tk
from tkinter import ttk
import time
import random

# create class for time machine
class TimeMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mars Time Machine - SpaceBrah Edition")
        self.root.geometry("400x500")

        # Create pilot setup
        self.pilot = "SpaceBrah"
        self.current_year = 2025 # set the current year as today 23 feb 2025
        self.mars_distance = 225_000_000 # distance from Earth to Mars in km
        self.speed = 299_792 # speed of light in km/s
        self.fuel = 100 # fuel in percentage


        # GUI Elements
        self.label = tk.Label(root, text=f"Welcome, {self.pilot}: set your Mars trip:", font=("Arial", 14))
        self.label.pack(pady=10)

        # lets create a year selection
        tk.Label(root, text="Pick a year:").pack()
        self.year_var = tk.IntVar(value=2075)
        self.year_entry = tk.Entry(root, textvariable=self.year_var)
        self.year_entry.pack()

        # Mars mission vibes
        tk.Label(root, text="Mars Era:").pack()
        self.era_var = tk.StringVar(value="Future")
        eras = ["Past (1976 - Viking 1)", "Present (2025 - Today)", "Future (2075+)"]
        self.era_menu = ttk.Combobox(root, textvariable=self.era_var, values=eras)
        self.era_menu.pack()


        # lets create a launch button
        self.launch_btn = tk.Button(root, text="Launch to Mars", command=self.launch_sequence)
        self.launch_btn.pack(pady=20)


        # Output log
        self.log = tk.Text(root, height=15, width=50)
        self.log.pack(pady=10)


    def log_message(self, message):
        """
        Add messages to the text log
        """
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.root.update()

    def calculate_travel_time(self, target_year):
        """
        Simple calculation with orbital window flavor

        """
        time_shift = abs(target_year - self.current_year)
        distance_time = self.mars_distance / self.speed
        launch_window_penalty = random.uniform(0, 5) if time_shift % 2 == 0 else 0
        total_time = distance_time + (time_shift * 0.1) + launch_window_penalty
        return total_time

    def launch_sequence(self):
        """
        Run the trip with GUI updates
        """
        self.fuel = 100 # reset fuel
        self.launch_btn.config(state="disabled")
        self.log.delete(1.0, tk.END) # clear log

        target_year = self.year_var.get()
        era = self.era_var.get()
        self.log_message(f"Launching to Mars in {era} era, target year: {target_year}")

        self.log_message("Initilizing Time Machine...")
        time.sleep(2)
        self.log_message(f"Engines hot....fuel: {self.fuel}%")
        time.sleep(2)
        self.log_message("Blast off in 3...2...1.....")
        time.sleep(2)


        travel_time = self.calculate_travel_time(target_year)
        self.log_message(f"Warping....ETA: {travel_time:.2f} seconds")


        for _ in range(3):
            time.sleep(2)
            self.fuel -= random.randint(10, 25)
            if self.fuel <= 0:
                self.log_message("Fuel out! Crashed on Deimos, Better luck next time!")
                self.launch_btn.config(state="normal")
                return
            event = random.choice(["Wormhole jumped", "Dust storm avoided", "Time flux smoothed"])
            self.log_message(f"Status: {event} - Fuel: {self.fuel}%")

        self.log_message(f"\nLanded! Welcome to Mars, {self.pilot}, year {target_year}!")
        if "Past" in era:
            self.log_message("Viking 1 vibes-hope you like retro rovers!")
        elif "Present" in era:
            self.log_message("Perserverence says hi-watch for drones!")
        else:
            self.log_message("Future Mars-terraforming in progress, watch for green!")

        self.launch_btn.config(state="normal")

# Lets fire this baby up
root = tk.Tk()
app = TimeMachineGUI(root)
root.mainloop()