import os
import re
import subprocess

import matplotlib.pyplot as plt
import numpy as np
import shutil
import importlib.util
import time


class SimulatorManager:
    def __init__(self, linux_netlist_path, linux_project_dir, windows_project_path, project_name, parameter_file):
        self.linux_netlist_path = linux_netlist_path
        self.windows_netlist_path = os.path.join(windows_project_path, f"spice_files/{project_name}.spice")
        self.linux_project_dir = linux_project_dir
        self.windows_project_dir = windows_project_path
        self.windows_project_dir_ubt =  windows_project_path.replace("C:", "/mnt/c").replace("\\", "/")
        self.paramater_file = parameter_file

        self.project_name = project_name
        self.block_info = {}
        self.net_info = {}
        self.digital_input_events = {}
        self.analog_blocks= []
        self.analog_sim_placeholder = []
        self.analog_sim = []

        self.digital_sim_placeholder = []
        self.digital_sim = []
        self.digital_blocks = []
        self.mixed_blocks = []
        self.multiblock_simfile = []
        self.waveform_data = {} 

        self.initial_sim = True
        self.time_step = None
        self.sim_time_analog = None
        self.sim_time_digital = None

        self.offset = 0
        self.driver_signals = None
    
    def parse_netlist(self):
        if os.path.exists(self.windows_netlist_path):
            pass
        else:
            command_copy = ["wsl", "cp", self.linux_netlist_path, self.windows_project_dir_ubt] #copy command in ubuntu to retrieve netlist
            subprocess.run(command_copy, check=True) #run commands
        with open(self.windows_netlist_path, 'r') as f: #read netlist
            lines = f.readlines() #store netlist in lines

        in_top_subckt = False #Flag to start extracting
        instances = [] #blocks
        top_pins = [] #vdd signals and such gnd

        for line in lines: #for loop to get netlist information
            line = line.strip() #split line in array
            if not in_top_subckt: #First search starting point
                if line.startswith('**.subckt'):  #check if it is the starting point
                    in_top_subckt = True #now continue to get the blocks
                    tokens = line.split() #search for vdd and gnd
                    top_pins = tokens[2:] #get those pins
            elif line.startswith('X'): #line starts with x is block
                tokens = line.split() # split block line
                inst_name = tokens[0] # get the X as block
                nets = tokens[1:-1] # get all net connections of block
                block = tokens[-1] #get the block name 
                instances.append((inst_name, nets, block)) #append array
            elif line.startswith('**.ends'): #stop line for extraction
                break #stop loop

        for inst_name, nets, block in instances: #loop through blocks
            sym_filename = f"{block}.sym" #sim file is block name + .sym
            sym_path_windows = os.path.join(self.windows_project_dir,f'sym_files/{sym_filename}')
            sym_path_windows = sym_path_windows.replace("\\", "/")
            if os.path.exists(sym_path_windows):
                pass
            else:
                sym_path = os.path.join(self.linux_project_dir, sym_filename) #path in linux 
                
                command_copy = ["wsl", "cp", sym_path, f'{self.windows_project_dir_ubt}sym_files/'] #commands to get the .sym file
                subprocess.run(command_copy, check=True) #run it in ubuntu
                
                if not os.path.isfile(sym_path_windows): #if not exist
                    print(f"[Error] Missing .sym file for block: {block} at {sym_path}") #give error but go on
                    continue #go to next block

            with open(sym_path_windows, 'r') as f: # read lines
                sym_lines = f.readlines() # store sym file

            pins = [] #collect pins
            source_file = None #get the source file of .sch .v .py
            i = 0
            while i < len(sym_lines): #loop through lines
                line = sym_lines[i].strip() #get line as an array

                if line.startswith('B'): # if it starts with B it is a connection pin
                    full_line = line # B is spread of 2 lines so get the full line
                    if '{' in full_line and '}' not in full_line: #B is finished when } 
                        while '}' not in full_line and i + 1 < len(sym_lines): 
                            i += 1
                            full_line += ' ' + sym_lines[i].strip() #add line to full line
                    match = re.search(r'\{(.*?)\}', full_line) ########## Opzoeken wat betekent #############
                    if match: #get the mathc
                        metadata = match.group(1) #store what is in between {}
                        fields = metadata.split() #split what is in between {}
                        pin = {} #pin dict
                        for field in fields: # loop though line
                            if '=' in field: # search =
                                key, value = field.split('=', 1) #split the key=value for pin name and pin direction
                                pin[key] = value #store
                        if 'name' in pin and 'dir' in pin: #if both 
                            pins.append((pin['name'], pin['dir'])) #voeg totale pins toe

                elif line.startswith('K {'): #K stores the file type
                    content_lines = [] #stores lines in K
                    while not line.endswith('}'): #loop t/m }
                        content_lines.append(line) #voeg line toe
                        i += 1
                        if i < len(sym_lines): #check if it exist
                            line = sym_lines[i].strip() #make array of line
                    content_lines.append(line)
                    k_block = '\n'.join(content_lines) #make 1 big line
                    match = re.search(r'SYMATTR\s+File\s+([^\s]+)', k_block) #search file
                    if match: #if match then there is a .py or .v file
                        source_file = match.group(1) #get the source file
                    match_analog = re.search(r'type\s*=\s*subcircuit', k_block, re.IGNORECASE)
                    if match_analog:
                        source_file = os.path.join(self.windows_project_dir, f"spice_files/{block}.spice")
                        source_file = source_file.replace("\\", "/")
                i += 1

            inputs, outputs = [], [] #make input out puts pin
            pin_mapping = {} #make dictornary

            for (pin_name, direction), net in zip(pins, nets): 
                pin_mapping[pin_name] = net
                if direction == 'in':
                    inputs.append(net)
                else:
                    outputs.append(net)

                if net not in self.net_info:
                    self.net_info[net] = {'driver': None, 'receivers': []}

                if direction == 'in':
                    self.net_info[net]['receivers'].append({'block': inst_name, 'pin': pin_name})
                elif direction == 'out':
                    self.net_info[net]['driver'] = {'block': inst_name, 'pin': pin_name}

            self.block_info[inst_name] = {
                'block_type': block,
                'sym_path': sym_path_windows,
                'inputs': inputs,
                'outputs': outputs,
                'nets' : nets,
                'pin_to_net': pin_mapping,
                'source_file': source_file
            }


    def classify_blocks(self):
        for blk, data in self.block_info.items(): #loop trough blocks
            source = data.get('source_file', '') #collect source file if there is.
            if source.endswith('.v'): # if .v then block is digital
                data['category'] = 'digital' #store digital in dic
                self.digital_blocks.append(blk)
            elif source.endswith('.py'): #if .py then is block mixed signal
                data['category'] = 'mixed' #store mixed type in dic
                self.mixed_blocks.append(blk)
            elif source.endswith('.spice') or source is None: #if .sch is stored or it is none
                data['category'] = 'analog' #store analog type
                self.analog_blocks.append(blk) 
            else: #else type is unknown because convention is not met
                data['category'] = 'unknown' #

    def group_analog_blocks(self):
        combined = []
        remaining = list(self.analog_blocks)  # preserves order
        unvisited = set(remaining)            # for fast lookup

        while remaining:
            start_block = remaining.pop(0)
            if start_block not in unvisited:
                continue

            group = [start_block]
            queue = [start_block]
            unvisited.remove(start_block)

            while queue:
                current = queue.pop(0)
                current_info = self.block_info.get(current, {})
                outputs_nets = current_info.get('outputs', [])

                for net in outputs_nets:
                    net_data = self.net_info.get(net, {})
                    receivers = net_data.get('receivers', [])

                    for receiver in receivers:
                        neighbor = receiver.get('block')  # correct key
                        if neighbor in unvisited:
                            neighbor_info = self.block_info.get(neighbor, {})
                            if neighbor_info.get('category') == 'analog':
                                queue.append(neighbor)
                                group.append(neighbor)
                                unvisited.remove(neighbor)

            combined.append(group)

        self.analog_blocks = combined

    def process_netlist(self, block):
        info = self.block_info[block]
        name = info.get('block_type')
        spice_file = info.get('source_file')
        sub_lines = []

        with open(spice_file, 'r') as f:
            content = f.read()

        start_col = False
        for line in content.splitlines():
            line = line.strip()
            if not start_col:
                if line.startswith('**.subckt'):
                    start_col = True
                    # Replace '**.subckt' with '.subckt'
                    line = line.replace('**.subckt', '.subckt', 1)
                    sub_lines.append(line)
            elif line.startswith('**.ends'):
                sub_lines.append(f'.ends {name}')
                break
            else:
                sub_lines.append(line)

        return sub_lines
    
    def data_splitter(self,path_folder, net):
        path_data = os.path.join(path_folder, f'{net}.txt')
        data = np.loadtxt(path_data)
        return data
    
    def format_digital_time(self, value):
    # Convert time in seconds (e.g., 1e-09) to integer in nanoseconds
        return str(int(round(value * 1e9)))  # e.g., 1e-08 → "10"
    
    def format_digital_value(self, value):
        return str(int(round(value)))  # e.g., 1.0 or 0.0 → "1" or "0"
    
    def format_analog_value(self, value):
        abs_val = abs(value)
        suffix = ''
        scale = 1

        if 1e-12 <= abs_val < 1e-9:
            suffix = 'p'
            scale = 1e12
        elif 1e-9 <= abs_val < 1e-6:
            suffix = 'n'
            scale = 1e9
        elif 1e-6 <= abs_val < 1e-3:
            suffix = 'u'
            scale = 1e6
        elif 1e-3 <= abs_val < 1e-2:
            suffix = 'm'
            scale = 1e3
        elif 1e-2 <= abs_val <= 1e3:
            return f"{value:.4f}".rstrip('0').rstrip('.')
        else:
            return f"{value:.2e}"  # fallback for very large or very small

        scaled = value * scale
        return f"{scaled:.4f}{suffix}".rstrip('0').rstrip('.')

    def prepare_simulation_files(self):
        for idx, blk_group in enumerate(self.analog_blocks):
            file_name = os.path.join(self.windows_project_dir, f"spice_files/analog_group_{idx}.spice")
            file_name = file_name.replace("\\", "/")
            simulation_lines = []
            title = f"* Analog block group {idx} simulation"
            simulation_lines.append(title)

            blocks = []
            ic_lines = []
            vsource_lines = []
            wrdata_lines = []

            for blk in blk_group:
                blk_info = self.block_info[blk]
                lines = self.process_netlist(blk)
                simulation_lines.extend(lines)
                simulation_lines.append('')

                # Create instance line
                nets = " ".join(blk_info.get('nets', []))
                name = blk_info.get('block_type')
                block_instance_line = f"{blk} {nets} {name}"
                blocks.append(block_instance_line)

                # Handle input nets
                for net in blk_info.get('inputs', []):
                    driver = self.net_info.get(net, {}).get('driver')
                    if driver:
                        driver_blk = driver.get('block')
                        if driver_blk and driver_blk not in blk_group:
                            driver_info = self.block_info.get(driver_blk)
                            if driver_info:
                                category = driver_info.get('category')
                                if category == 'digital' or category == 'mixed':
                                    vsource_lines.append(f"V{net} {net} 0 PWL(0n 0 {net}_placeholder)")
                                elif category == 'analog':
                                    ic_lines.append(f".IC V({net})=0")
                    else:
                        # If net has no known driver, assume it's analog and give initial condition
                        ic_lines.append(f".IC V({net})=0")

                # Handle output nets
                for net in blk_info.get('outputs', []):
                    wrdata_lines.append(f"wrdata {net}.txt V({net})")

            # Final file structure
            simulation_lines.append('')
            simulation_lines.extend(vsource_lines)
            simulation_lines.extend(ic_lines)
            simulation_lines.append('')
            simulation_lines.extend(blocks)
            simulation_lines.append('')
            simulation_lines.append(".control")
            simulation_lines.append("   tran sim_step_placeholder sim_time_placeholder")
            simulation_lines.append("   .probe")
            simulation_lines.extend([f"   {line}" for line in wrdata_lines])
            simulation_lines.append(".endc")
            simulation_lines.append(".end")

            with open(file_name, 'w') as f:
                f.write("\n".join(simulation_lines))
            self.analog_sim_placeholder.append(file_name)    
        # TODO: Implement digital block testbench generation
        for blk in self.digital_blocks:
            test_bench_lines = []
            info = self.block_info.get(blk, {})  # use dict get to avoid errors if missing
            test_bench_lines.append("`timescale 1ns / 1ps")
            name = info.get('block_type', 'unknown')
            module_line = f"module {name}_tb;"

            filename = os.path.join(self.windows_project_dir, f"testbench_files/{name}_tb.v")
            filename = filename.replace("\\", "/")
            test_bench_lines.append(module_line)

            inputs = info.get('inputs', [])
            
            outputs = info.get('outputs', [])
            signals = []
            for input_pin in inputs:
                
                for receiver in self.net_info[input_pin]['receivers']:
                    if receiver['block'] == blk:
                        signal_pin = receiver['pin']
                        input_line = f"reg {signal_pin}_tb;"
                        test_bench_lines.append(input_line)

                
            for output_pin in outputs:
                driver = self.net_info[output_pin]['driver']
                out_signal = driver['pin']
                signals.append(out_signal)
                output_line = f"wire {out_signal}_tb;"
                test_bench_lines.append(output_line)

            instan_line = f"{name} dut ("
            test_bench_lines.append(instan_line)

            # Add port connections comma separated
            port_lines = []
            for input_pin in inputs:
                for receiver in self.net_info[input_pin]['receivers']:
                    if receiver['block'] == blk:
                        signal_pin = receiver['pin']
                        port_lines.append(f".{signal_pin}({signal_pin}_tb)")
            for output_pin in outputs:
                driver = self.net_info[output_pin]['driver']
                out_signal = driver['pin']
                port_lines.append(f".{out_signal}({out_signal}_tb)")

            # Join ports with commas and indent nicely
            port_connections = ",\n    ".join(port_lines)
            test_bench_lines.append("    " + port_connections)

            close_line = ");"
            test_bench_lines.append(close_line)

            test_bench_lines.append("initial begin")
            sim_file = f'$dumpfile("{name}_tb.vcd");'
            test_bench_lines.append(sim_file)
            data = f'$dumpvars(0, {name}_tb);'
            test_bench_lines.append(data)
            # Create format string for monitor (e.g., "a_tb=%b b_tb=%b ...")
            format_str = " ".join([f"{sig}_tb=%b" for sig in signals])

            # Create signal list with _tb suffix
            tb_signals = ", ".join([f"{sig}_tb" for sig in signals])

            # Final monitor line
            monitor_line = f'$monitor("%0t: {format_str}", $time, {tb_signals});'
            test_bench_lines.append(monitor_line)
            test_bench_lines.append('simulation_lines_placeholder')

            test_bench_lines.append("end")
            test_bench_lines.append("endmodule")
            with open(filename, 'w') as f:
                f.write("\n".join(test_bench_lines))
            self.digital_sim_placeholder.append(filename)

    def parse_si_value(self, value_str, context={}):
        si_multipliers = {
            'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3,
            'k': 1e3, 'M': 1e6, 'G': 1e9
        }
        value_str = value_str.strip()
        if value_str in context:
            return context[value_str]
        match = re.match(r'^([0-9.]+)([a-zA-Z]?)$', value_str)
        if match:
            num, suffix = match.groups()
            return float(num) * si_multipliers.get(suffix, 1)
        raise ValueError(f"Could not parse value: {value_str}")

    def generate_squarewave_transitions(self, period, duty, start, end, step):
        times = np.arange(start, end, step)
        signal = ((times % period) < (period * duty)).astype(float)

        # Detect changes and store [time, value]
        transitions = [[times[0], signal[0]]]
        for i in range(1, len(signal)):
            if signal[i] != signal[i - 1]:
                transitions.append([times[i], signal[i]])
        transitions = np.array(transitions)
        return transitions

    def parse_parameter_file(self):
        
        with open(self.paramater_file, 'r') as f:
            lines = f.readlines()

        context = {}

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            # Handle squarewave signal
            if value.startswith('squarewave('):
                value = value[len('squarewave('):-1]
                args = {}
                for part in value.split(','):
                    k, v = part.split('=')
                    args[k.strip()] = self.parse_si_value(v.strip(), context)

                clk_wave = self.generate_squarewave_transitions(
                    period=args['period'],
                    duty=args['duty'],
                    start=args['start'],
                    end=args['end'],
                    step=args['step']
                )
                self.clk = clk_wave
                self.net_info[key]['value'] = clk_wave

            else:
                parsed_val = self.parse_si_value(value, context)
                context[key] = parsed_val

                if key == 'time_step':
                    self.time_step = parsed_val
                elif key == 'sim_time_analog':
                    self.sim_time_analog = parsed_val
                elif key == 'sim_time_digital':
                    self.sim_time_digital = parsed_val
                elif key.startswith('net'):
                    self.net_info[key]['value'] = parsed_val

    def generate_sim_verilog(self, block):
        
        lines = []
        blk_info = self.block_info[block]
        inputs = blk_info.get('inputs', [])

        for signal_name in inputs:
            tb_signal = None
            for receiver in self.net_info[signal_name]['receivers']:
                if receiver['block'] == block:
                    tb_signal = f"{receiver['pin']}_tb"
                    pin_name = receiver['pin']
                    break

            if tb_signal is None:
                continue

            event_list = self.digital_input_events.get(block, {}).get(pin_name, [])

            if not event_list:
                lines.append(f"#0 {tb_signal} = 0; // No stimulus yet")
                continue

            # First assignment must be #0
            first_time, first_val = event_list[0]
            lines.append(f"#0 {tb_signal} = {first_val};")

            last_time = first_time
            for t, v in event_list[1:]:
                delta = float(round((t - last_time),2))
                lines.append(f"#{delta} {tb_signal} = {v};")
                last_time = t

        return lines
    
    def Replace_placeholders(self):
        for inx, blk_group in enumerate(self.analog_blocks):
            sim_file = os.path.join(self.windows_project_dir, f'spice_files/{inx}_run_sim.spice')
            sim_file = sim_file.replace("\\","/")
            file = self.analog_sim_placeholder[inx]
            with open(file,'r') as f:
                content = f.read()
            content = content.replace('sim_step_placeholder', f'{self.format_analog_value(self.time_step)}')
            content = content.replace('sim_time_placeholder', f'{self.format_analog_value(self.sim_time_analog)}')

            for net_name in self.net_info:
                placeholder = f"{net_name}_placeholder"
                net_value = self.net_info[net_name].get('value')
                if net_value is None:
                    print (f'Warning: {net_name} value not defined, could break simulation')
                    content = re.sub(
                        rf'V{net_name}\s+{net_name}\s+0\s+PWL\(0n 0\s+{placeholder}\)',
                        f'V{net_name} {net_name} 0 0',
                        content
                    )
                    continue
                if isinstance(net_value, (int, float)):
                    
                    formatted_val = self.format_analog_value(net_value)
                    content = content.replace(placeholder,formatted_val)
                elif isinstance(net_value, str):
                    content = content.replace(placeholder, net_value)
                elif isinstance(net_value, np.ndarray):
                    continue    
            with open(sim_file, 'w') as f:
                f.write(content)
            self.analog_sim.append(sim_file)
        for inx, blk in enumerate(self.digital_blocks):
            sim_file = os.path.join(self.windows_project_dir,f'testbench_files/{blk}_run_tb.v')
            sim_file = sim_file.replace("\\","/")
            file = self.digital_sim_placeholder[inx]
            with open(file,'r') as f:
                content = f.read()
            sim_lines = self.generate_sim_verilog(blk)
            content = content.replace('simulation_lines_placeholder', "\n".join(sim_lines))
            with open(sim_file, 'w') as f:
                f.write(content)
            self.digital_sim.append(sim_file)
    
    def load_simulation_module(self, module_name, directory):
        module_path = os.path.join(directory, f"{module_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    
    def mixed_output (self):
        for blk in self.mixed_blocks:
            component = self.block_info[blk]['block_type']
            blk_info = self.block_info[blk]
            mixed_signal_dir = os.path.join(self.windows_project_dir,'py_files/')
            mixed_signal_dir = mixed_signal_dir.replace('\\','/')
            sim_module = self.load_simulation_module(component, mixed_signal_dir)
            if 'output_type' not in blk_info:
                  # Check if module defines get_output_type()
                if hasattr(sim_module, "get_output_type"):
                    output_type = sim_module.get_output_type()
                    self.block_info[blk]['output_type'] = output_type
                else:
                    raise AttributeError(f"{blk} does not define get_output_type()")

    def load_net_data(self, net_dir, net):
        filepath = os.path.join(net_dir, f"{net}.txt")
        return np.loadtxt(filepath)       
   
    def build_signal_inputs(self, analog_inputs, digital_inputs, net_dir):
    
        analog_data_list = []
        digital_data_list = []

        # Handle analog signals
        if analog_inputs:
            for net in analog_inputs:
                data = self.load_net_data(net_dir,net)
                analog_data_list.append(data[:, 1])  # values only

            time = data[:, 0]  # assume same time for all
            analog_input = np.column_stack([time] + analog_data_list)
        else:
            analog_input = None

        # Handle digital signals
        if digital_inputs:
            digital_data_list = []
            max_len = 0
            reference_time = None

            # First pass: find the longest signal and load all
            loaded_signals = []

            for net in digital_inputs:
                data = self.load_net_data(net_dir, net)
                data = np.array(data)

                # Ensure it's 2D
                if data.ndim == 1:
                    if data.size == 2:
                        data = data.reshape(1, 2)
                    else:
                        raise ValueError(f"Invalid digital input shape: {data.shape}")

                # Track max length and time
                if data.shape[0] > max_len:
                    max_len = data.shape[0]
                    reference_time = data[:, 0]  # Time from the longest signal

                loaded_signals.append(data)

            # Second pass: pad values to max_len
            for data in loaded_signals:
                values = data[:, 1]
                current_len = len(values)

                if current_len < max_len:
                    pad_len = max_len - current_len
                    last_value = values[-1]
                    values = np.concatenate([values, np.full(pad_len, last_value)])

                digital_data_list.append(values)

            # Final stack
            digital_input = np.column_stack([reference_time] + digital_data_list)
        else:
            digital_input = None

        return analog_input, digital_input
    
    def store_digital_net(self, nets, data):
        data = np.array(data)
        if data.ndim == 1:
            data = data.reshape((1, -1))
        time = data[:, 0]  # First column is time
        for i, net_name in enumerate(nets):
            net_data = data[:, i + 1]  # i+1 because data[:,0] is time
            file_path = os.path.join(self.windows_project_dir, f'Output_data/Tussen_data/{net_name}.txt')
            with open(file_path, "w") as f:
                for t, v in zip(time, net_data):
                    f.write(f"{t} {v}\n")
    

    def synchronize_all_nets(self):
        eind_dir = os.path.join(self.windows_project_dir, "Output_data/Eind_data/")
        os.makedirs(eind_dir, exist_ok=True)

        time_step_interp = self.time_step if self.time_step else 1e-9
        sim_end = self.sim_time_analog
        time_array = np.arange(0, sim_end + time_step_interp / 2, time_step_interp)

        for net_name, net_data in self.net_info.items():
            driver = net_data.get("driver")
            if not driver:
                continue

            blk = driver['block']
            blk_info = self.block_info[blk]
            category = blk_info.get("category")
            output_type = blk_info.get("output_type", "analog")

            # Try _complete.txt first
            file_path = os.path.join(self.windows_project_dir, f"Output_data/Eind_data/{net_name}_complete.txt")
            if not os.path.exists(file_path):
                # Fallback to Tussen_data
                file_path = os.path.join(self.windows_project_dir, f"Output_data/Tussen_data/{net_name}.txt")
                if not os.path.exists(file_path):
                    print(f"[WARN] No data for {net_name} found")
                    continue

            raw = np.loadtxt(file_path)
            if raw.ndim == 1:
                raw = raw.reshape((1, -1))

            t_raw = raw[:, 0]
            v_raw = raw[:, 1]

            is_from_complete = "_complete.txt" in file_path

            if category == "analog" or (category == "mixed" and output_type == "analog"):
                # Analog — linear interpolation
                if is_from_complete:
                    t_raw = t_raw * 1e-9  # ns → s
                v_interp = np.interp(time_array, t_raw, v_raw)

            elif category == "digital" or (category == "mixed" and output_type == "digital"):
                # Digital — step-hold
                if is_from_complete:
                    t_raw = t_raw * 1e-9  # ns → s

                v_interp = np.zeros_like(time_array)
                j = 0
                last_val = int(v_raw[0])
                for i, t_now in enumerate(time_array):
                    while j + 1 < len(t_raw) and t_raw[j + 1] <= t_now:
                        j += 1
                    last_val = int(v_raw[j])
                    v_interp[i] = last_val

            else:
                continue  # unknown type

            synced = np.column_stack((time_array, v_interp))
            self.net_info[net_name]["value"] = synced

            # Save synced data
            eind_path = os.path.join(eind_dir, f"{net_name}.txt")
            np.savetxt(eind_path, synced, fmt="%.9e %.6f")
    def run_simulations(self):
        
        for sim in self.analog_sim:

            sim_file = os.path.basename(sim)
            sym_path = os.path.join(self.windows_project_dir_ubt, 'spice_files/')
            sym_path = sym_path.replace("\\", "/")
            wsl_file = os.path.join(sym_path, sim_file)
            subprocess.run(["wsl","ngspice", "-b", wsl_file])
            time.sleep(1)

        
        for i in range(len(self.digital_blocks)):
            
            blk = self.digital_blocks[i]
            verilog_file = self.block_info[blk]['source_file']
            
            info = self.block_info.get(blk)
            modname = self.block_info[blk]['block_type'].replace(".v", "")
            tb_file = self.digital_sim[i]
                # Directories
            tb_file = os.path.basename(tb_file)
            
            verilog_dir = os.path.join(self.windows_project_dir, "verilog_files")
            tb_dir = os.path.join(self.windows_project_dir, "testbench_files")
            base_dir = os.path.dirname(self.windows_project_dir)
            shared_dir = os.path.join(base_dir, "shared")

            os.makedirs(shared_dir, exist_ok=True)

            # Full paths
            verilog_src = os.path.join(verilog_dir, verilog_file)
            tb_src = os.path.join(tb_dir, tb_file)
            verilog_dst = os.path.join(shared_dir, verilog_file)
            tb_dst = os.path.join(shared_dir, tb_file)

            # Copy Verilog file if not present
            if not os.path.exists(verilog_dst):
                shutil.copy(verilog_src, verilog_dst)

            # Always copy (overwrite) testbench
            shutil.copy(tb_src, tb_dst)
            # Navigate to base_dir for docker-compose
            compose_cmd = ["cmd", "/c", f"cd /d {base_dir} && docker-compose up -d icarus"]
            subprocess.run(compose_cmd, shell=True)
            time.sleep(1)
            # Compose simulation command
            sim_output_name = modname + "_sim"
            docker_cmd = f"iverilog -o {sim_output_name} {verilog_file} {tb_file} && vvp {sim_output_name} > {sim_output_name}.txt"
            
            # Run docker exec
            exec_cmd = ["docker", "exec", "icarus", "sh", "-c", docker_cmd]
            subprocess.run(exec_cmd)
            time.sleep(1)
            sim_output_shared = os.path.join(shared_dir,f"{sim_output_name}.txt")
          
            sim_output = os.path.join(self.windows_project_dir, "Output_data/Tussen_data/") 
            
            shutil.copy(sim_output_shared,sim_output)
            dat = self.parse_digital_sim_output(os.path.join(sim_output, f'{sim_output_name}.txt'))
            output_nets = self.block_info[blk]['outputs']
            self.store_digital_net(output_nets, dat)
          
        self.synchronize_all_nets()
        for blk in self.mixed_blocks:
            component = self.block_info[blk]['block_type']

            inputs = self.block_info[blk]['inputs']
            
            mixed_signal_dir = os.path.join(self.windows_project_dir,'py_files/')
            mixed_signal_dir = mixed_signal_dir.replace('\\','/')
            sim_module = self.load_simulation_module(component, mixed_signal_dir)
          
            digital_inputs = []
            analog_inputs = []

            for input_p in inputs:
                
                input_block = self.net_info[input_p]['driver']['block']

                if self.block_info[input_block]['category'] == 'analog':
                    analog_inputs.append(input_p)
                elif self.block_info[input_block]['category'] == 'digital':
                    digital_inputs.append(input_p)
                elif self.block_info[input_block]['category'] == 'mixed':
                    if self.block_info[input_block]['output_type'] == 'digital':
                        digital_inputs.append(input_p)
                    elif self.block_info[input_block]['output_type'] == 'analog':
                        analog_inputs.append(input_p)

            net_dir = os.path.join(self.windows_project_dir, "Output_data/Tussen_data/")
            analog_input, digital_input = self.build_signal_inputs(analog_inputs,digital_inputs,net_dir)
            output = sim_module.simulate(analog_input,digital_input)
            print (output)
            output_nets = self.block_info[blk]['outputs']
            self.store_digital_net(output_nets,output)
  
    def parse_digital_sim_output(self, file_path):
        result = []

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()

                # Skip comment lines or lines with no ':'
                if ':' not in line or '=' not in line:
                    continue

                # Split time and signal parts
                time_part, signal_part = line.split(":", 1)
                try:
                    time_val = int(time_part.strip())
                except ValueError:
                    continue  # skip malformed time

                # Extract all signal=value pairs
                matches = re.findall(r'(\w+)\s*=\s*(\d+)', signal_part)
                if not matches:
                    continue  # skip if no valid signals found

                values = [time_val]
                for _, val in matches:
                    values.append(int(val))

                result.append(values)

        return result
    
    def Extract_value_event_analog(self,data):
        """
    Extracts events where the signal value changes and formats them into a string.

    Args:
        data (np.ndarray): Array of shape (N, 2), where [:, 0] = time, [:, 1] = value

    Returns:
        str: A string in the form "0n value 10n value ..."
    """
        event_found = False
        times = data[:, 0]
        values = data[:, 1]

        event_list = []
        offset = self.offset*1e9
        # Always add the first event
        last_value = values[0]
        time_ns = round(times[0] * 1e9)
        event_list.append(f"{time_ns}n {last_value}")

        for i in range(1, len(values)):
            if values[i] != last_value:
                time_ns = round(times[i] * 1e9,2)
                print (time_ns)
                event_list.append(f"{time_ns}n {values[i]}")
                last_value = values[i]
                if not event_found:
                    if time_ns>offset:
                        event_found = True
                        event_timestamp = time_ns
                        break
        print (event_list)
        return " ".join(event_list), event_timestamp

    def Extract_value_event_digital(self, data):
        events = []
        offset = self.offset * 1e9  # offset in ns
        event_stamp = None

        if data.ndim == 1:
            data = data.reshape((1, -1))

        # Adjust time to absolute
        time_ns = (data[0, 0] / 1000) + self.offset * 1e9
        last_value = data[0, 1]
        events.append((time_ns, last_value))

        if len(data) == 1:
            if time_ns > offset:
                event_stamp = time_ns
            return events, event_stamp

        for i in range(1, len(data)):
            current_time_ns = (data[i, 0] / 1000) + self.offset * 1e9
            current_value = data[i, 1]
            if current_value != last_value:
                events.append((current_time_ns, current_value))
                if event_stamp is None and current_time_ns > offset:
                    event_stamp = current_time_ns
                last_value = current_value
                break

        return events, event_stamp
    
    def Time_event(self):
        Time_event = None
        data_dir = os.path.join(self.windows_project_dir, 'Output_data/Tussen_data/')
        for net_name, net_info in self.net_info.items():
            driver = net_info.get('driver')
            if driver != None:
                blockdata = self.block_info.get(driver['block'])
                if blockdata['category'] == 'analog':
                    continue
                elif blockdata['category'] == 'mixed':
                    data = self.data_splitter(data_dir, net_name)
                    output, event_stamp = self.Extract_value_event_analog(data)
                    if event_stamp is None:
                        continue
                    elif Time_event is None:
                        Time_event = event_stamp
                    elif Time_event >= event_stamp:
                        Time_event = event_stamp
                    net_info['value'] = str(output)
                elif blockdata['category'] == 'digital':
                    data = self.data_splitter(data_dir, net_name)
                    output, event_stamp = self.Extract_value_event_digital(data)
                    if event_stamp is None:
                        continue
                    elif Time_event is None:
                        Time_event = event_stamp
                    elif Time_event > event_stamp:
                        Time_event = event_stamp
                    #self.check_event(net_name)
                else: pass
        return Time_event
            
        # TODO: Detect events from .sym or handle full-time simulation
        # TODO: Calculate time slices based on event timestamps

    def extract_netvalue(self, time_event):
        input_dir = os.path.join(self.windows_project_dir, 'Output_data/Tussen_data/')
        output_dir = os.path.join(self.windows_project_dir, 'Output_data/Eind_data/')
        os.makedirs(output_dir, exist_ok=True)
        print("[DEBUG] Net list in net_info:", list(self.net_info.keys()))
        for net_name, net_data in self.net_info.items():
            driver = net_data.get('driver')
            if not driver:
                continue

            blk = driver['block']
            blk_info = self.block_info.get(blk, {})
            if not blk_info:
                continue

            category = blk_info.get('category')
            file_path = os.path.join(input_dir, f"{net_name}.txt")
            out_path = os.path.join(output_dir, f"{net_name}_complete.txt")

            if not os.path.exists(file_path):
                continue

            data = np.loadtxt(file_path)
            if data.ndim == 1:
                data = data.reshape((1, -1))
            if data.shape[1] != 2:
                continue

            # Analog (mixed)
            elif category == 'mixed':
                times = data[:, 0] * 1e9  # seconds → ns
                values = data[:, 1]

                idx = times <= time_event
                cropped_times = times[idx]
                cropped_values = values[idx]

                if len(cropped_times) == 0:
                    continue

                # Extend to t_event if needed
                if cropped_times[-1] < time_event:
                    cropped_times = np.append(cropped_times, time_event)
                    cropped_values = np.append(cropped_values, cropped_values[-1])

                # Get output type: analog or digital
                output_type = blk_info.get('output_type', 'analog')

                if output_type == 'analog':
                    # → Store as PWL for analog receivers
                    pwl_str = " ".join([f"{float(round(t,2))}n {v}" for t, v in zip(cropped_times, cropped_values)])
                    self.net_info[net_name]['value'] = pwl_str

                    # Save to file
                    with open(out_path, 'w') as f:
                        for t, v in zip(cropped_times, cropped_values):
                            f.write(f"{float(round(t,2))} {v}\n")

                elif output_type == 'digital':
                    # → Store transitions for digital receivers
                    event_array = []
                    last_val = None
                    for t, v in zip(cropped_times, cropped_values):
                        t_int = float(round(t,2))
                        v_int = int(v)
                        if last_val is None or v_int != last_val:
                            event_array.append([t_int, v_int])
                            last_val = v_int

                    self.net_info[net_name]['value'] = event_array

                    # Push to digital receivers
                    receivers = net_data.get('receivers', [])
                    for rec in receivers:
                        blk = rec['block']
                        pin = rec['pin']

                        if self.block_info.get(blk, {}).get('category') != 'digital':
                            continue

                        if blk not in self.digital_input_events:
                            self.digital_input_events[blk] = {}
                        self.digital_input_events[blk][pin] = event_array

                        print(f"[✔ DIGITAL from MIXED] Stored {len(event_array)} events for {blk}.{pin} (from {net_name})")

                    # Save to file
                    with open(out_path, 'w') as f:
                        for t, v in event_array:
                            f.write(f"{t} {v}\n")

            elif category == 'digital':
                
                times = data[:, 0] / 1000  # convert from ps to ns
                values = data[:, 1]
                
                
                event_array = []
                seen_times = set()

                # Round initial time and add first event
                t0 = int(round(times[0]))
                v0 = int(values[0])
                event_array.append([t0, v0])
                seen_times.add(t0)
                last_val = v0

                for t, v in zip(times[1:], values[1:]):
                    t_int = float(round(t,2))
                    v_int = int(v)

                    if t_int in seen_times:
                        continue  # Skip duplicate time

                    if v_int != last_val:
                        event_array.append([t_int, v_int])
                        seen_times.add(t_int)
                        last_val = v_int

                # Store complete event list
                self.net_info[net_name]['value'] = np.array(event_array)

                # Propagate to each digital receiver
                receivers = net_data.get('receivers', [])
                for rec in receivers:
                    blk = rec['block']
                    pin = rec['pin']

                    if self.block_info[blk]['category'] != 'digital':
                        continue

                    if blk not in self.digital_input_events:
                        self.digital_input_events[blk] = {}
                    self.digital_input_events[blk][pin] = list(event_array)

                # Write to output file
                out_path = os.path.join(output_dir, f"{net_name}_complete.txt")
                with open(out_path, 'w') as f:
                    for t, v in event_array:
                        f.write(f"{t} {v}\n")
                            
    def main_loop(self):
        # INITIAL SETUP — RUN ONCE
        self.parse_netlist()
        self.classify_blocks()
        self.group_analog_blocks() 
        self.mixed_output()
        self.prepare_simulation_files()

        self.parse_parameter_file()

        # SIMULATION LOOP
        while self.offset < self.sim_time_analog:
            print(f"\n[SIM] Running simulation from t = {self.offset * 1e9:.0f} ns")
            
            self.Replace_placeholders()
            self.run_simulations()

            event = self.Time_event()
            if event is None or event <= self.offset * 1e9:
                print("[SIM] No new event or stuck at same time. Ending simulation.")
                break

            # ✅ Extract values BEFORE next Replace
            self.extract_netvalue(event)

            self.offset = event / 1e9  # Update simulation time



                    
    
if __name__ == "__main__":
    netlist_path = f"/home/ruben/.xschem/simulations/toplevel.spice"
    project_dir = f"/home/ruben/eda_tools/xschem-src/projects/test_sim/"
    project_name = "toplevel"
    projec_dir = "C:/Users/Ruben/Project_lunar/Project_OPEN_SOURCE_LUNAR/Projecten"
    para = "C:/Users/Ruben/Project_lunar/Project_OPEN_SOURCE_LUNAR/Projecten/Parameter_files/Parameters.txt"
    sim = SimulatorManager(netlist_path, project_dir,projec_dir,project_name, para)

    sim.main_loop()

