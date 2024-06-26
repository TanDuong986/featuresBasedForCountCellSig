import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os 

# Example series of voltage values (replace with your actual data)

data = pd.read_csv(os.path.join("E:/UET Office/MEMS/CountCell/featuresBasedForCountCellSig/Label_GUI/All files labelling/file900.txt"), delim_whitespace=True, header=None, names=['Time', 'Value'])
# print(data.head())

series = data["Value"]  # Example series of 1000 voltage values

# # Plot the time-domain signal (series)
# plt.figure(figsize=(10, 4))
# plt.subplot(2, 1, 1)
# plt.plot(series)
# plt.title('Time Domain Signal (Series)')
# plt.xlabel('Sample')
# plt.ylabel('Amplitude')

# # Perform Fourier Transform (FFT)
# n = len(series)  # Length of the signal
# Y = np.fft.fft(series) / n  # FFT computing and normalization
# frq = np.fft.fftfreq(n)  # Frequency range

# # Plot the frequency-domain signal
# plt.subplot(2, 1, 2)
# plt.plot(frq, np.abs(Y))
# plt.title('Frequency Domain Signal')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')

# plt.tight_layout()
# plt.show()

time = data['Time']
values = data['Value']

# Plot the time-domain signal
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(time, values)
plt.title('Original Time Domain Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Perform Fourier Transform (FFT)
n = len(values)  # Length of the signal
sampling_interval = time[1] - time[0]  # Calculate the time interval between samples
Y = np.fft.fft(values)  # FFT computing
frq = np.fft.fftfreq(n, d=sampling_interval)

# Extract positive frequencies
positive_frequencies = frq[:n//2]
positive_Y = Y[:n//2]

# Plot the frequency-domain signal (positive frequencies only)
plt.subplot(3, 1, 2)
plt.plot(positive_frequencies, np.abs(positive_Y))
plt.title('Frequency Domain Signal (Positive Frequencies Only)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

# Reconstruct the time-domain signal using only positive frequencies
# Create an array with zeros for the negative frequencies
Y_filtered = np.zeros_like(Y, dtype=complex)

# Copy the positive frequency components
Y_filtered[:n//2] = positive_Y
# Mirror the positive frequencies to the negative side (to maintain symmetry)
Y_filtered[-(n//2)+1:] = np.conj(positive_Y[1:][::-1])

# Perform the inverse FFT (IFFT)
reconstructed_signal = np.fft.ifft(Y_filtered).real

# Plot the reconstructed time-domain signal
plt.subplot(3, 1, 3)
plt.plot(time, reconstructed_signal)
plt.title('Reconstructed Time Domain Signal (From Positive Frequencies)')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
