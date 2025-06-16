import os
import numpy as np
import matplotlib.pyplot as plt

def plot_signals(folder_path, file_names, analog_files, output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)

    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)

        # Load data
        try:
            data = np.loadtxt(file_path)
            if data.ndim != 2 or data.shape[1] != 2:
                print(f"Skipping {file_name}: expected 2 columns, got shape {data.shape}")
                continue
        except Exception as e:
            print(f"Error reading {file_name}: {e}")
            continue

        time = data[:, 0]
        values = data[:, 1]

        # Create plot
        plt.figure()
        if file_name in analog_files:
            plt.plot(time, values, label=file_name)  # Analog
        else:
            plt.step(time, values, where='post', label=file_name)  # Digital

        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.title(f"Plot of {file_name}")
        plt.legend()
        plt.grid(True)

        # Save plot
        safe_name = os.path.splitext(file_name)[0].replace(" ", "_")
        output_file = os.path.join(output_dir, f"{safe_name}.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Saved plot to {output_file}")

# === Usage ===
folder = r'C:/Users/Ruben/OneDrive/Bureaublad/Data_1ns'
file_names = [
    "Net1.txt", "Net2.txt", "net3_complete.txt", "Net4_complete.txt",
    "Net5_complete.txt", "Net6_complete.txt", "Net7_complete.txt", "VOUT.txt"
]

analog_files = ["Net1.txt", "Net2.txt", "Net7_complete.txt", "VOUT.txt"]

plot_signals(folder, file_names, analog_files)