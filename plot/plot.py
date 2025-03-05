import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

filename = "test_data.csv"

file = os.path.join(os.path.dirname(__file__), filename)
data = pd.read_csv(file, header=None)

# Flatten data to 1D numPy array
bitstream = data.values.flatten()

start_idx = np.where(bitstream == 0)[0][0]  # First occurrence of zero
bitstream = bitstream[start_idx:]  # Trim leading ones

# ensure num bits is multiple of 16
num_bits = len(bitstream)
if num_bits % 16 != 0:
    bitstream = bitstream[:-(num_bits % 16)]

# make 16-bit chunks
bit_chunks = bitstream.reshape(-1, 16)

# Convert each chunk to an int (LSB)
#counter_values = np.array([int("".join(map(str, bits[::-1])), 2) for bits in bit_chunks])
counter_values = np.array([int("".join(map(str, bits)), 2) for bits in bit_chunks])
corrected_values = [counter_values[0]] 

# Filter to remove consecutive max values
max_value = 65535  # 16-bit max value
filtered_values = [counter_values[0]]
for i in range(1, len(counter_values)):
    if not (counter_values[i] == max_value and counter_values[i-1] == max_value):
        filtered_values.append(counter_values[i])

filtered_values = np.array(filtered_values)
plt.figure(figsize=(25,5))
plt.plot(filtered_values, marker="o", linestyle="-", markersize=3, markevery=10)
plt.xlabel("μs")
plt.ylabel("number")
plt.title("Values over time")
plt.grid(True)
plt.savefig("plot.png")
