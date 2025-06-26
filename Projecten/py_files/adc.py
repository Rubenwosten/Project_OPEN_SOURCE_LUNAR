import numpy as np

def get_output_type():
    return "digital"

def simulate(analog_input, digital_input=None):
    """
    Simulate an ideal 3-bit ADC and return the digital output bits with timestamps.

    Args:
        analog_input (np.ndarray): 2-column array [time, analog_value]
        digital_input (np.ndarray): unused

    Returns:
        np.ndarray: array of [time, MSB, Bit1, LSB]
    """
    Vref = 0.5       # Reference voltage
    n_bits = 3       # Resolution (MSB, Bit1, LSB)
    max_code = 2**n_bits - 1

    time = analog_input[:, 0]
    signal = analog_input[:, 1]

    # Clip to [0, Vref]
    clipped_signal = np.clip(signal, 0, Vref)

    # Convert to digital code
    codes = np.round((clipped_signal / Vref) * max_code).astype(int)

    # Extract individual bits (MSB to LSB)
    bits = [(codes >> i) & 1 for i in reversed(range(n_bits))]  # MSB first
    bits_array = np.column_stack(bits)  # Shape: (N, 3)

    # Combine with time
    output = np.column_stack((time, bits_array))  # Shape: (N, 4) -> [time, MSB, Bit1, LSB]

    return output
