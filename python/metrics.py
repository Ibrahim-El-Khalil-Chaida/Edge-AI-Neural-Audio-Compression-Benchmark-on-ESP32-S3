import numpy as np

def calculate_mse(original, reconstructed):
    """Calculates Mean Squared Error between two audio arrays."""
    return np.mean((original - reconstructed) ** 2)

def calculate_snr(original, reconstructed):
    """Calculates Signal-to-Noise Ratio (SNR) in dB."""
    noise = original - reconstructed
    signal_power = np.mean(original ** 2)
    noise_power = np.mean(noise ** 2)
    
    if noise_power == 0:
        return float('inf')
        
    return 10 * np.log10(signal_power / noise_power)