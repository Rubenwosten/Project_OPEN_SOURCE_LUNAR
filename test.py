file_path = r"\\wsl$\Ubuntu\home\ruben\projects\test_xschem_sky130\top.sch" #file path for windows

try:
    with open(file_path, 'r') as f: #open file
        content = f.read() #read file
    print("File loaded successfully!") # gives check if succesfull
    print("Preview of content:\n", content[:200]) #with quick preview
except FileNotFoundError: # if not found
    print("File not found:", file_path)


import subprocess

# Define schematic file path in WSL
wsl_sch_path = "/home/ruben/projects/test_xschem_sky130/top.sch"

# Command to run in WSL
command = ["wsl", "xschem", wsl_sch_path]

try:
    subprocess.run(command, check=True)
    print("✅ Xschem launched with rc_circuit.sch")
except subprocess.CalledProcessError as e:
    print("❌ Failed to launch Xschem:", e)

from Datastructure import GDSBlock, Pin

block = GDSBlock(
    name="mux1",
    gds_path="mux1.gds",
    position=(200, 150),
    size=(100, 80),
    pins=[
        Pin(name="A", direction="input", position=(0, 40)),
        Pin(name="B", direction="input", position=(0, 60)),
        Pin(name="Y", direction="output", position=(100, 50)),
    ]
)

print(block)