import collections
import socket
import json
import threading
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from scipy import stats

mean_amplitudes = 0

class SignalAnalyzer:
    def __init__(self):
        # Data storage
        self.signal_window = collections.deque(maxlen=50) # last 50 signals
        self.time_window = collections.deque(maxlen=50) # last 50 time points
        self.entire_signal = collections.deque(maxlen=1000) # for FFT analysis
        self.fft_freqs = np.array([])
        self.fft_amplitudes = np.array([])
        self.counter = 0
        
        # Set up the socket server (for observation)
        self.sock = None
        self.connected = False
        self.data_buffer = ''
        
        # Set up the live plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        # self.fig, (self.ax2) = plt.subplots(1, 1, figsize=(10, 8))
        self.fig.tight_layout(pad=4.0)
        
        # Raw signal plot
        self.line1, = self.ax1.plot([], [], 'r-', label='Raw Signal')
        self.ax1.set_ylim(-1, 4)
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_title('Clock Signal')
        self.ax1.legend()
        self.ax1.grid(True)
        
        # Frequency domain plot
        self.line2, = self.ax2.plot([], [], 'b-', label='FFT Analysis')
        self.ax2.set_xlabel('Frequency')
        self.ax2.set_ylabel('Amplitude')
        self.ax2.set_title('Frequency Domain Analysis')
        self.ax2.legend()
        self.ax2.grid(True)
        
        # Status text
        self.status_text = self.fig.text(0.02, 0.02, '', fontsize=8)
        
        # Start the signal thread receiver
        self.receiver_thread = None
    
    
    # Connect to the signal broadcaster
    def connect_to_broadcast(self, host='localhost', port=9999):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.connected = True
            print(f'Connected to signal broadcaster at {host}:{port}')
        
            # Start the signal receiver thread
            self.receiver_thread = threading.Thread(target=self.receive_data, 
                                                    daemon=True)
            self.receiver_thread.start()
            
            return True
        except Exception as e:
            print(f'Error connecting to signal broadcaster: {e}')
            self.connected = False
            return False
    
    
    # Thread function to receive data from broadcaster
    def receive_data(self):
        while self.connected:
            try:
                data = self.sock.recv(4096).decode()
                if not data:
                    print('Connection closed')
                    self.connected = False
                    break    
                
                # Add to buffer and process
                self.data_buffer += data
                # REMOVE newline character since realworld is not that perfect
                lines = self.data_buffer.split('\n')
            
                # Last line might be incomplete, so don't process it
                self.data_buffer = lines.pop() if lines else ''
                
                # Process the complete lines
                for line in lines:
                    try:
                        signal = json.loads(line)
                        self.process_signal(signal)
                    except json.JSONDecodeError as e:
                        print(f'Error decoding JSON: {e}')
                        
            except Exception as e:
                print(f'Error receiving data: {e}')
                self.connected = False
                break
            
            
    # Process the signal
    def process_signal(self, signal):
        # Store the signal
        self.counter += 1
        self.time_window.append(self.counter)
        
        self.signal_window.append(signal)
        self.entire_signal.append(signal)
        
        # Perform FFT analysis given enough data
        if len(self.entire_signal) > 10:
            self.perform_fft()
            
            
    # Perform FFT analysis
    def perform_fft(self):
        signal_array = np.array(self.entire_signal)
        
        # Perform FFT
        freq_spectrum = np.fft.fft(signal_array)
        freqs = np.fft.fftfreq(len(signal_array))
        
        # Get positive frequencies
        half_index = len(freqs) // 2
        self.fft_freqs = freqs[:half_index]
        self.fft_amplitudes = np.abs(freq_spectrum)[:half_index]
        
        # Find the frequency to monitor
        self.trigger(self.fft_amplitudes)
        
    
    # Trigger function to determine if a glitch occurred
    def trigger(self, fft_amplitudes):
        global mean_amplitudes
        
        # Ignore the first 1000 frames for analysis stablisation
        if self.counter > 1000 and np.mean(fft_amplitudes) - mean_amplitudes > 2.0:
            print(f'Determined glitch at frame: {self.counter}')
            
            print(f'Mean amplitude(frame {self.counter - 1}): {mean_amplitudes}')
            print(f'Mean amplitude(frame {self.counter}): {np.mean(fft_amplitudes)}')
        
        mean_amplitudes = np.mean(fft_amplitudes)
        
        
    # Update the plot
    def update_plot(self, frame):
        # Update the raw signal plot
        self.ax1.clear()
        if self.time_window and self.signal_window:
            time_array = np.array(self.time_window)
            signal_array = np.array(self.signal_window)
            self.ax1.plot(time_array, signal_array, 'r-', label='Raw Signal')
            self.ax1.set_ylim(min(-1, np.min(signal_array) - 0.1), 
                              max(3.5, np.max(signal_array) + 0.1))
            self.ax1.set_xlabel('Time')
            self.ax1.set_ylabel('Amplitude')
            self.ax1.set_title('Clock Signal')
            self.ax1.legend()
            self.ax1.grid(True)
        
        # Update the FFT plot
        self.ax2.clear()
        if len(self.fft_freqs) > 0 and len(self.fft_amplitudes) > 0:
            self.ax2.plot(self.fft_freqs, 
                          self.fft_amplitudes, 
                          'b-', 
                          label='FFT Analysis')
            
            # Find and mark dominant frequency
            if len(self.fft_freqs) > 1 and len(self.fft_amplitudes) > 1:
                peak_idx = np.argmax(self.fft_amplitudes[1:])
                if peak_idx < len(self.fft_freqs):
                    peak_freq = self.fft_freqs[peak_idx]
                    peak_amp = self.fft_amplitudes[peak_idx]
                    self.ax2.plot(peak_freq, peak_amp, 'ro')
                    self.ax2.annotate(f'{peak_freq:.2f}', 
                                      (peak_freq, peak_amp), 
                                      textcoords="offset points", 
                                      xytext=(5,5))
            
            # Set reasonable limits
            if len(self.fft_amplitudes) > 0:
                max_amp = np.max(self.fft_amplitudes)  
            else: max_amp = 0
            
            self.ax2.set_xlim(0, 0.5) # Nyquist limit
            self.ax2.set_ylim(0, max_amp) # comment out for zoomed in view
            # self.ax2.set_ylim(0, 10) # uncomment for zoomed in view
            
            self.ax2.set_xlabel('Frequency')
            self.ax2.set_ylabel('Amplitude')
            self.ax2.set_title('Frequency Domain Analysis')
            self.ax2.legend()
            self.ax2.grid(True)
            
        # Update the status text
        status = f'Connected: {self.connected} | Signal Length: {self.counter}'
        self.status_text.set_text(status)
        
        # Adjust layout
        self.fig.tight_layout(pad=4.0, rect=[0, 0.03, 1, 0.97])
        
        # return self.line1, self.line2, self.status_text
        return self.line2, self.status_text
    
    
    # Run the analyzer
    def run(self):
        # Connect to the broadcaster
        if not self.connect_to_broadcast():
            print('Error connecting to broadcaster. Exiting...')
            return
        
        # Set up the animation
        ani = animation.FuncAnimation(self.fig, 
                                      self.update_plot, 
                                      interval=1/1000, 
                                      blit=False)
        plt.show()
        
        # Close the connection
        if self.sock:
            self.sock.close()
        
        print('Signal analyzer shut down')
    

if __name__ == '__main__':
    analyzer = SignalAnalyzer()
    analyzer.run()