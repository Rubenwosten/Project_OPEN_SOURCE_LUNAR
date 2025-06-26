# Timing constraints

# Define the clock
create_clock -name clk -period 10.0 [get_ports clk]

# Define input and output delays
set_input_delay 2.0 -clock clk [all_inputs]
set_output_delay 2.0 -clock clk [all_outputs]
