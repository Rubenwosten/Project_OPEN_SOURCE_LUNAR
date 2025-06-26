import subprocess
import os
import time
import pyautogui
import shutil

wsl_path = '/home/ruben/eda_tools/xschem/projects/'

class AUTOMATE():
    def __init__(self, project_name, project_path, shared):
        self.block_data= None
        self.beheviour = None
        self.constrainst = None
        self.spice_path = None
        self.name = None
        self.type = None
        self.spice_filename= None
        self.config_file = None
        self.project_name = project_name
        self.project_path = project_path
        self.shared = shared


    def automation(self, block_data):
        self.block_data = block_data
        self.name = self.block_data.get('name')
        self.beheviour = self.block_data.get('beheviour')
        self.config_file = self.block_data.get('config')
        print("is hier gekomen")
        self.constrainst = self.block_data.get('constrainst')
        self.type = self.block_data.get('type')
        self.folder_structure()
        if self.type == "analog":
            self.get_spice()
            self.get_sp()
            self.get_gds()
            self.drc()
        elif self.type == "digital":
            self.Openlane()

    
    def folder_structure(self):
        cato = ['analog','digital','mixed']
        sub = [['schematics','netlists','flatten_netlist','simulation_results','layouts', 'other'],
               ['designs','testbenches','simulation_results','layouts','other'],
               ['python_files','symbol_files','simulation_results','layout','other']]
        for i in range(3):
            catog = cato[i]
            sub_folders = sub[i]
            cato_folder = os.path.join(self.shared,catog)
            os.makedirs(cato_folder,exist_ok=True)
            for j in range(len(sub_folders)):
                sub_path = os.path.join(cato_folder,sub_folders[j])
                os.makedirs(sub_path,exist_ok=True)


    def get_spice(self):
        filename = os.path.basename(self.beheviour)
        shared_sch_path = os.path.join(self.shared, f'analog/schematics/{filename}')

        # Step 1: Copy schematic to Docker shared folder
        try:
            os.makedirs(os.path.dirname(shared_sch_path), exist_ok=True)
            shutil.copy(self.beheviour, shared_sch_path)
        except Exception as e:

            return
        spice_filename = f'{self.name}.spice'

        # Step 2: Start Docker Compose
        try:
            cmd = (
                f"xschem -n /workspace/analog/schematics/{filename} -b -q && "
                f"cp /root/.xschem/simulations/{spice_filename} /workspace/analog/netlists/"
            )

            subprocess.run([
                'docker-compose', 'run', '--rm', 'analog', 'sh', '-c', cmd
            ], check=True, cwd=self.project_path)

        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return
   
        time.sleep(2)  # Wait to ensure SPICE file is written

        # Step 5: Copy from shared to project path
        netlist_shared = os.path.join(self.shared, f'analog/netlists/{spice_filename}')
        netlist_shared = netlist_shared.replace('\\', '/')
        print(netlist_shared)
        dest_dir = os.path.join(self.project_path, f'analog/simulation_file/')
        dest_dir = dest_dir.replace('\\', '/')
        print (dest_dir)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, spice_filename)

        try:
            shutil.copy(netlist_shared, dest_path)
        except Exception as e:
            return
        
    def get_sp(self):
        filename = os.path.basename(self.beheviour)
        
        shared_sch_path = os.path.join(self.shared, f'analog/schematics/{filename}')

        # Step 1: Copy schematic to Docker shared folder
        try:
            os.makedirs(os.path.dirname(shared_sch_path), exist_ok=True)
            shutil.copy(self.beheviour, shared_sch_path)
        except Exception as e:

            return
        self.spice_filename = f'{self.name}.spice'

        # Step 2: Start Docker Compose
        try:
            cmd = (
                f"xschem -f -n /workspace/analog/schematics/{filename} -b -q && "
                f"cp /root/.xschem/simulations/{self.spice_filename} /workspace/analog/flatten_netlist/"
            )

            subprocess.run([
                'docker-compose', 'run', '--rm', 'analog', 'sh', '-c', cmd
            ], check=True, cwd=self.project_path)

        except subprocess.CalledProcessError as e:
            print("Error:", e)
            return
   
        time.sleep(2)  # Wait to ensure SPICE file is written


        # Step 5: Copy from shared to project path
        netlist_shared = os.path.join(self.shared, f'analog/flatten_netlist/{self.spice_filename}')
        dest_dir = os.path.join(self.project_path, f'/analog/flatten_netlist')
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, self.spice_filename)

        try:
            shutil.copy(netlist_shared, dest_path)
        except Exception as e:
            return

    def get_gds(self):
        print ("maakt gds")
        try:
            cmd = (
                f"schematic2layout.py /workspace/analog/flatten_netlist/ -p $PDK_ROOT/SKY130_PDK/"
            )

            subprocess.run([
                'docker-compose', 'run', '--rm', 'align', 'sh', '-c', cmd
            ], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print("Command failed:", e)
       
    def drc(self):
        print('Running DRC using Magic in Docker')

        design = self.name
        gds_filename = f"{design}.gds"
        drc_report = f"{design}_drc.txt"

        # Step 1: Copy .gds file to Docker shared folder
        local_gds = os.path.join(self.project_path, f"analog/{self.name}/layouts/{gds_filename}")
        local_gds = local_gds.replace("\\","/")
        print(local_gds)
        shared_gds = os.path.join(self.shared, f"analog/layouts/{gds_filename}")
        shared_gds = shared_gds.replace("\\","/")
        shutil.copy(local_gds, shared_gds)

        # Step 2: Magic DRC command inside Docker
        cmd = f"""
magic -dnull -noconsole << EOF
tech load sky130A
cif *hierarchical yes
gds read /workspace/analog/layouts/{gds_filename}
load {design}
drc euclidean on
drc check
drc catchup
drc listall why > /workspace/analog/drc/{drc_report}
quit
EOF
"""

        try:
            subprocess.run([
                "docker-compose", "run", "--rm", "analog", "sh", "-c", cmd
            ], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print("DRC Error:", e)
            return

        # Step 3: Copy result back from shared
        shared_report = os.path.join(self.shared, f"analog/drc/{drc_report}")
        local_report = os.path.join(self.project_path, f"analog/drc/{drc_report}")
        os.makedirs(os.path.dirname(local_report), exist_ok=True)

        try:
            shutil.copy(shared_report, local_report)
            with open(local_report, 'r') as f:
                print("Magic DRC Output:")
                print(f.read())
        except Exception as e:
            print("Error copying DRC output:", e)

        return
    def pex():
                # Start Magic in headless batch mode
        commands_xschem_1 = ['docker-compose', 'run', 'analog']
        subprocess.Popen(commands_xschem_1)        
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
        commands_xschem_1 = ['docker-compose', 'run', 'analog']
        subprocess.Popen(commands_xschem_1)
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
        commands_xschem_1 = ['docker-compose', 'run', 'analog']
        subprocess.Popen(commands_xschem_1)
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

    def Openlane(self):
        filename = os.path.basename(self.beheviour)
        shared_sch_path = os.path.join(self.shared, f'digital/designs/{self.name}/src')
        os.makedirs(os.path.dirname(shared_sch_path), exist_ok=True)
        shared_sch_path = os.path.join(shared_sch_path, filename)
        # Step 1: Copy schematic to Docker shared folder
        try:
            shutil.copy(self.beheviour, shared_sch_path)
        except Exception as e:
            return
        
        filename = os.path.basename(self.config_file)
        shared_sch_path = os.path.join(self.shared, f'digital/designs/{self.name}')
        os.makedirs(os.path.dirname(shared_sch_path), exist_ok=True)
        shared_sch_path = os.path.join(shared_sch_path, filename)
        # Step 1: Copy schematic to Docker shared folder
        try:
            shutil.copy(self.config_file, shared_sch_path)
        except Exception as e:
            return
        
        filename = os.path.basename(self.constrainst)
        shared_sch_path = os.path.join(self.shared, f'digital/designs/{self.name}')
        os.makedirs(os.path.dirname(shared_sch_path), exist_ok=True)
        shared_sch_path = os.path.join(shared_sch_path, filename)
        # Step 1: Copy schematic to Docker shared folder
        try:
            shutil.copy(self.constrainst, shared_sch_path)
        except Exception as e:
            return
        try:
            cmd = (
                f"flow.tcl -design /workspace/digital/designs/{self.name}/"
            )

            subprocess.run([
                'docker-compose', 'run', '--rm', 'openlane', 'sh', '-c', cmd
            ], check=True, cwd=self.project_path)
        except subprocess.CalledProcessError as e:
            print("Command failed:", e)
       



        commands_openlane_1 = ['docker-compose', 'up', '-d']
        subprocess.Popen(commands_openlane_1)
        commands_openlane_2 = ['docker', 'exec', '-it','Openlane','bash']
        subprocess.Popen(commands_openlane_2)
        commands_openlane_3 = ['flow.tcl', '-design', f'workspace/{self.name}/digital/designs']
        subprocess.Popen(commands_openlane_3)