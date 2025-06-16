import numpy as np

def get_output_type():
    return "analog"

def simulate(analog_input , digital_input):
    Vref = 0.5       # Reference voltage
    n_bits = 3
    max_code = 2**n_bits - 1

    input_data = np.asarray(digital_input)
    time = input_data[:, 0]
    bits = input_data[:, 1:4].astype(int)

    # Convert bits to integer value: (bit2 << 2) | (bit1 << 1) | (bit0)
    digital_code = bits[:, 2] << 2 | bits[:, 1] << 1 | bits[:, 0]

    # Convert to analog voltage
    analog_output = (digital_code / max_code) * Vref * 2 - Vref

    return np.column_stack((time, analog_output))
