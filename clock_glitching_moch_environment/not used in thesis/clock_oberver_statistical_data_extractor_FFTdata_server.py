import socket
import json
import threading
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



# Convert raw string of 1s and 0s into segments
def parse_signal(signal: float):
    # Check if signal is successfully received - Do this at earlier stage
    if not signal:
        return []
    
    # Initialize the variables
    parsed_data: list = []
    current_value: float = signal
    count: int = 1
    
    # print(f'Current value: {current_value}')
    
    # Count consecutive values
    if abs(signal - current_value) < 0.2: # Jittery floating point signal
        count += 1
    # If new bit is different, append the current segment and start a new one
    else:
        parsed_data.append([current_value, count]) # Jittery floating point signal
        current_value = signal
        count = 1
    
    # Append the last segment
    parsed_data.append([current_value, count])
    return parsed_data




# Measure pulse width (Duration of the cycle)
def measure_pulse_width(parsed_data):
    # Total time
    total_time = sum(duration for _, duration in parsed_data)
    # Total time signal is high
    high_time = sum(duration for value, duration in parsed_data if value == 1)
    # Return % of time signal is high
    return (high_time / total_time) * 100 if total_time > 0 else 0




# Frequency analysis (using Fast Fourier Transform)
def frequency_analysis(signal):
    # Convert from from to array
    binary_signal = np.array([bit for bit in signal])
    
    # Perform the FFT
    # np.fft.fft: This is a function from the NumPy library that computes the one-dimensional discrete Fourier Transform (DFT) using the Fast Fourier Transform (FFT) algorithm. The FFT is an efficient way to compute the DFT, which transforms a sequence of complex numbers into another sequence of complex numbers.
    # binary_signal: This is the input array to the fft function. It represents the signal data in the time domain that you want to transform into the frequency domain. The signal can be real or complex.
    # freq_spectrum: This is the variable that stores the result of the FFT. The result is an array of complex numbers representing the frequency spectrum of the input signal. Each element in this array corresponds to a specific frequency component of the input signal.
    freq_spectrum = np.fft.fft(binary_signal)
    
    # len(freq_spectrum): --> This part of the code calculates the length of the freq_spectrum array. The len() function returns the number of elements in the array.
    # np.fft.fftfreq(): --> This is a function from the NumPy library that computes the Discrete Fourier Transform (DFT) sample frequencies. It generates an array of frequency bin centers in cycles per unit of the sample spacing.
    # np.fft.fftfreq(len(freq_spectrum)): --> Here, np.fft.fftfreq() is called with the length of the freq_spectrum array as its argument. This means it will generate the frequency bins for a DFT of the same length as freq_spectrum.
    # freqs =: --> The result of np.fft.fftfreq(len(freq_spectrum)) is assigned to the variable freqs. This variable will now hold an array of frequency bin centers corresponding to the DFT of freq_spectrum.
    freqs = np.fft.fftfreq(len(freq_spectrum))
    
    # Return only the positive frequencies and their corresponding amplitudes (FFT is symmetric)
    half_index = len(freqs) // 2
    return freqs[:half_index], np.abs(freq_spectrum)[:half_index]
    
    # Return positive frequencies and their corresponding amplitudes
    # freqs[:len(freqs)//2: This part of the code extracts the first half of the freqs array. The freqs array contains the frequency bin centers for the DFT of the input signal. The DFT is symmetric, so the second half of the array is a mirror image of the first half. By taking only the first half of the array, the code is effectively extracting the positive frequencies.
    # np.abs(freq_spectrum)[:len(freqs)//2]: This part of the code extracts the first half of the absolute values of the freq_spectrum array. The freq_spectrum array contains the complex values representing the frequency spectrum of the input signal. The absolute values of these complex numbers represent the amplitudes of the frequency components. By taking only the first half of the array, the code is effectively extracting the amplitudes corresponding to the positive frequencies.
    # return freqs[:len(freqs)//2, np.abs(freq_spectrum)[:len(freqs)//2]]
    



if __name__ == '__main__':
    # Connect to the clock_freq_server.py
    HOST, PORT = 'localhost', 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))


    # Set up the socket server (for sending a "kill switch" signal)
    KILL_HOST, KILL_PORT = 'localhost', 7777
    kill_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kill_sock.bind((KILL_HOST, KILL_PORT))
    kill_sock.listen(1)
    # kill_conn, _ = kill_sock.accept() # Wait for a connection


    # Store client connection status
    kill_client_connection = None


    # Accept the connection in a seperate thread
    def accept_connection():
        global kill_client_connection
        while True:
            kill_connect, _ = kill_sock.accept()
            kill_client_connection = kill_connect
            print('Kill Client connected')


    # Start the connection accepting thread
    threading.Thread(target=accept_connection, daemon=True).start()

    # Create a figure and axis
    fig, ax = plt.subplots()
    x_data, y_data = [], []
    line, = ax.plot([], [], 'r-', label='Frequency Domain Fourier Transform')
    
    
    entire_signal = []
    # Receive the clock frequency from the server
    while True:
        try:
            data = sock.recv(1024).decode().strip()
            # print(f'Recieved data: {data}')
            if data:
                packet = json.loads(data)
                entire_signal.append(packet)
                
                # Analyze the signal
                parsed_data = parse_signal(packet)
                # print(f'Parsed signal durations: {parsed_data}')
                
                # Measure pulse width (Duration of the cycle)
                pulse_width = measure_pulse_width(parsed_data)
                # print(f'Pulse width: {pulse_width}')
                
                # Count the number of transitions (Edge detection)
                transitions = len(parsed_data) - 1
                # print(f'Number of transitions: {transitions}')
                
                # Perform frequency analysis
                freqs, amplitudes = frequency_analysis(entire_signal)
                # print(f'Frequencies: {freqs}')
                # print(f'Amplitudes: {amplitudes}')
                
                if kill_client_connection:
                    try:
                        # Send the Fourier Transform data to the client
                        processed_data = json.dumps({"frequency": freqs.tolist(), "amplitude": amplitudes.tolist()})
                        kill_client_connection.sendall((processed_data + "\n").encode())
                    except:
                        # Handle disconnection
                        kill_client_connection = None
                        print('Kill Client disconnected')
            
            if not data:
                break
        except Exception as e:
            print(f'Error: {e}')
            break
        
        
    
    # Close the connection
    sock.close()
    
    print(f'Total datapoint: {len(entire_signal)}')

    # # Plot the frequency spectrum
    plt.plot(freqs, amplitudes)
    plt.figtext(.67, .8, f'Data points = {len(entire_signal)}')
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.show()

    

    
    
    
    




