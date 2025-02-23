import tkinter as tk
from tkinter import ttk
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MarsTimeMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Mars Time Machine - SpaceBrah Extreme")
        self.root.geometry("450x600")
        
        self.pilot = "SpaceBrah"
        self.current_year = 2025
        self.earth_semi_major = 1.0  # AU
        self.mars_semi_major = 1.524  # AU
        self.mu_sun = 1.327e20  # Sun's gravitational parameter (m^3/s^2)
        self.speed_of_light = 299_792  # km/s
        self.fuel = 100.0  # Starting fuel %

        # GUI Setup
        self.label = tk.Label(root, text=f"{self.pilot}, rig your Mars ride:", font=("Arial", 14))
        self.label.pack(pady=10)

        tk.Label(root, text="Target Year:").pack()
        self.year_var = tk.IntVar(value=2075)
        self.year_entry = tk.Entry(root, textvariable=self.year_var)
        self.year_entry.pack()

        tk.Label(root, text="Mars Era:").pack()
        self.era_var = tk.StringVar(value="Future")
        eras = ["Past (1976)", "Present (2025)", "Future (2075+)"]
        self.era_menu = ttk.Combobox(root, textvariable=self.era_var, values=eras)
        self.era_menu.pack()

        tk.Label(root, text="Fuel Burn Rate (1-10):").pack()
        self.burn_var = tk.DoubleVar(value=5.0)
        self.burn_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.burn_var)
        self.burn_scale.pack()

        self.launch_btn = tk.Button(root, text="Launch to Mars!", command=self.launch_sequence)
        self.launch_btn.pack(pady=20)

        self.log = tk.Text(root, height=20, width=50)
        self.log.pack(pady=10)

    def log_message(self, message):
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.root.update()

    def hohmann_transfer(self):
        """Calculate delta-V and travel time for Hohmann transfer to Mars."""
        a_transfer = (self.earth_semi_major + self.mars_semi_major) / 2  # Semi-major axis of transfer orbit
        transfer_time = math.pi * math.sqrt(a_transfer**3 / self.mu_sun)  # Half-orbit time (seconds)
        delta_v1 = math.sqrt(self.mu_sun / self.earth_semi_major) * (math.sqrt(2 * self.mars_semi_major / (self.earth_semi_major + self.mars_semi_major)) - 1)
        delta_v2 = math.sqrt(self.mu_sun / self.mars_semi_major) * (1 - math.sqrt(2 * self.earth_semi_major / (self.earth_semi_major + self.mars_semi_major)))
        total_delta_v = (delta_v1 + delta_v2) * 1000  # Convert to m/s
        return total_delta_v, transfer_time / (24 * 3600)  # Days

    def calculate_time_warp(self, target_year):
        """Add a sci-fi time jump to the orbital transfer."""
        time_shift = abs(target_year - self.current_year)
        base_travel = self.hohmann_transfer()[1]  # Days from Hohmann
        warp_factor = time_shift * 0.05  # Arbitrary warp per year
        return base_travel + warp_factor

    def plot_landing(self, success):
        """Show a simple 3D Mars landing plot using NumPy."""
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title("Mars Landing - SpaceBrah")

        # Mars surface (sphere)
        u, v = np.meshgrid(np.radians(range(0, 360, 10)), np.radians(range(0, 180, 10)))
        x = 3389.5 * np.cos(u) * np.sin(v)
        y = 3389.5 * np.sin(u) * np.sin(v)
        z = 3389.5 * np.cos(v)
        ax.plot_surface(x, y, z, color='red', alpha=0.5)

        # Landing trajectory
        t = np.linspace(0, 1, 50)
        traj_x = np.zeros(50)
        traj_y = t * 500 if success else t * 1000
        traj_z = 3389.5 - (t * 500 if success else t * 1000)
        ax.plot(traj_x, traj_y, traj_z, color='blue' if success else 'black', label="Safe Landing" if success else "Crash")

        ax.set_xlabel("X (km)")
        ax.set_ylabel("Y (km)")
        ax.set_zlabel("Z (km)")
        plt.legend()
        plt.show()

    def launch_sequence(self):
        self.fuel = 100.0
        self.launch_btn.config(state="disabled")
        self.log.delete(1.0, tk.END)

        target_year = self.year_var.get()
        era = self.era_var.get()
        burn_rate = self.burn_var.get()
        delta_v, hohmann_days = self.hohmann_transfer()

        self.log_message(f"Target: Mars, {target_year} ({era})")
        self.log_message(f"Hohmann Transfer: {hohmann_days:.1f} days | Delta-V: {delta_v:.1f} m/s")
        travel_time = self.calculate_time_warp(target_year)
        self.log_message(f"Warping... Total time: {travel_time:.1f} days")

        self.root.after(1000, self.perform_launch)

    def perform_launch(self):
        self.log_message("Launch in 3... 2... 1...")

        stages = ["Earth orbit escape", "Mid-course correction", "Mars orbit insertion"]
        self.execute_stages(stages, 0)

    def execute_stages(self, stages, index):
        if index >= len(stages):
            self.log_message("\nLanded on Mars!")
            target_year = self.year_var.get()
            era = self.era_var.get()

            if "Past" in era:
                self.log_message("1976 - Viking 1 terrain ahead!")
            elif "Present" in era:
                self.log_message("2025 - Modern rovers nearby!")
            else:
                self.log_message("2075+ - Future colonies looming?")

            self.plot_landing(True)
            self.launch_btn.config(state="normal")
            return

        stage = stages[index]
        fuel_cost = self.burn_var.get() * random.uniform(0.8, 1.2)
        self.fuel -= fuel_cost

        if self.fuel <= 0:
            self.log_message(f"{stage}: Fuel gone! Crashing...")
            self.plot_landing(False)
            self.launch_btn.config(state="normal")
            return

        event = random.choice(["Solar flare dodged", "Engine boost", "Time dilation hit"])
        self.log_message(f"{stage}: {event} | Fuel: {self.fuel:.1f}%")

        self.root.after(1000, lambda: self.execute_stages(stages, index + 1))

# Launch the GUI
root = tk.Tk()
app = MarsTimeMachine(root)
root.mainloop()
