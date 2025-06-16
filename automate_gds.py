import subprocess
import os
import time
import pyautogui

wsl_path = '/home/ruben/eda_tools/xschem/projects/'

class AUTOMATE_ANALOG():
    def __init__(self, project_name):
        self.block_data= None
        self.schematic = None
        self.constrainst = None
        self.spice_path = None
        self.name = None
        self.project_name = project_name


    def automation(self, block_data):
        self.block_data = block_data
        self.name = self.block_data.get('name')
        self.schematic = self.block_data.get('schematic')
        print("is hier gekomen")
        self.constrainst = self.block_data.get('constrainst')
        self.folder_structure()
        self.get_spice()
        self.get_sp()
        print("is hier gekomen")
    
    def folder_structure(self):
        tools = ["xschem-src","ALIGN-public","magic","ngspice_git"]  # your array of tools
        
        base_path = "/home/ruben/eda_tools"
        for tool in tools:
            folder_path = f"{base_path}/{tool}/projects/{self.name}"
            try:
                subprocess.run(["wsl", "mkdir", "-p", folder_path], check=True)
                print(f"Directory ensured in WSL: {folder_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create directory in WSL: {folder_path}")
                print(e)
    
    def get_spice(self):
        if self.schematic is None or self.schematic == '':
            command = ["wsl", "xschem"]
            subprocess.Popen(command)
            self.schematic = f"/home/ruben/eda_tools/xschem-src/projects/{self.name}/{self.name}.sch"
        else:   
            
            command = ["wsl", "xschem", "-n", self.schematic, "-q"]
            subprocess.Popen(command)
            time.sleep(4)
            command_copy = ["wsl", "cp", f"/home/ruben/.xschem/simulations/{self.name}.spice",f"/mnt/c/Users/Ruben/Project_lunar/Project_OPEN_SOURCE_LUNAR/Projecten/{self.project_name}/Simulations/Analog/" ]
            subprocess.Popen(command_copy)

    
    def get_sp(self):
        print("komt hier 2")
        if self.schematic is None or self.schematic == '':
            command = ["wsl", "xschem"]
            subprocess.Popen(command)
            self.schematic = f"/home/ruben/eda_tools/xschem-src/projects/{self.name}/{self.name}.sch"
        else:   
            print(self.project_name)
            command = ["wsl", "xschem","-f", "-n", self.schematic, "-q"]
            subprocess.Popen(command)
            time.sleep(4)
            command_copy = ["wsl", "cp", f"/home/ruben/.xschem/simulations/{self.name}.spice",f"/mnt/c/Users/Ruben/Project_lunar/Project_OPEN_SOURCE_LUNAR/Projecten/{self.project_name}/Layouts/Analog/" ]
            subprocess.Popen(command_copy)

    def get_gds(self):
        # Ensure the SPICE file exists
        check_cmd = ["wsl", "test", "-f", self.spice_path]
        result = subprocess.run(check_cmd)
        if result.returncode != 0:
            raise FileNotFoundError("SPICE file not found. Generate it first.")

        print("SPICE file found. Running ALIGN...")

        # Run schematic2layout.py via WSL
        align_cmd = [
            "wsl", "schematic2layout.py", self.netlist_dir,
            "-p", self.pdk_dir,
            "-c"
        ]
        subprocess.run(align_cmd, check=True)
        
        print("ALIGN run complete.")

        # Check if GDS was created
        gds_check_cmd = ["wsl", "test", "-f", self.gds_path]
        gds_result = subprocess.run(gds_check_cmd)
        if gds_result.returncode != 0:
            raise FileNotFoundError("GDS file not created.")

        print(f"GDS file created: {self.gds_path}")
        return self.gds_path
    def drc(self):
    # Start magic in batch mode
        proc = subprocess.Popen(
            ["magic", "-dnull", "-noconsole"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Send individual Tcl commands
        commands = [
            "load sky130.tech",
            "gds read mylayout.gds",
            "load my_top_cell",
            "drc euclidean on",
            "drc check",
            "drc count",
            "drc listall stdout",
            "exit"
        ]

        # Join and send commands
        stdout, stderr = proc.communicate("\n".join(commands))

        print("Magic DRC Output:")
        print(stdout)

        if stderr:
            print("Errors:")
            print(stderr)

        return
    def pex():
                # Start Magic in headless batch mode
        proc = subprocess.Popen(
            ["magic", "-dnull", "-noconsole"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Input layout and cell name
        gds_path = "mylayout.gds"
        top_cell = "my_top_cell"
        spice_output = "extracted.spice"

        # Commands for PEX
        commands = [
            "load sky130.tech",                  # Load your tech file
            f"gds read {gds_path}",              # Load the GDS
            f"load {top_cell}",                  # Load top cell
            "extract all",                       # Do full layout extraction
            f"ext2spice lvs",                    # Optional: enable LVS-compatible netlist
            f"ext2spice {spice_output}",         # Output netlist file
            "exit"
        ]

        # Send the commands
        stdout, stderr = proc.communicate("\n".join(commands))

        # Print results
        print("Magic PEX Output:")
        print(stdout)
        if stderr:
            print("Errors:")
            print(stderr)
        return
    
    def extract_with_magic(gds_path, top_cell, spice_output):
        commands = [
            "load sky130.tech",
            f"gds read {gds_path}",
            f"load {top_cell}",
            "extract all",
            "ext2spice lvs",
            f"ext2spice {spice_output}",
            "exit"
        ]

        proc = subprocess.Popen(
            ["magic", "-dnull", "-noconsole"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proc.communicate("\n".join(commands))
        print("PEX Output:\n", stdout)
        if stderr:
            print("PEX Errors:\n", stderr)

    def run_lvs(layout_netlist, schematic_netlist, top_cell, setup_file="sky130A_setup.tcl", lvs_report="lvs_report.txt"):
        lvs_command = [
            "netgen", "-batch", "lvs",
            f"{layout_netlist} {top_cell}",
            f"{schematic_netlist} {top_cell}",
            setup_file,
            lvs_report
        ]

        result = subprocess.run(
            lvs_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("LVS Output:\n", result.stdout)
        if result.stderr:
            print("LVS Errors:\n", result.stderr)




#class AUTOMATE_DIGITAL():
    #def __init__():