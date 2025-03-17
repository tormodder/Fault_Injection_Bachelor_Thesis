# Live plot code
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import json
import random

# Set up the socket server (for observation)
HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print(f'Broadcasting Clock Signal on {HOST}:{PORT}')

# Wait for a connection
conn, addr = sock.accept() 
print(f'Connected to FFT analyzer at {addr}')



try:
    # Send simulated signal to the client
    counter = 0
    while True:
        # Create a fake clock frequency
        if (counter % 10) < 5:
            freq = random.uniform(0.9, 1.0)
        else:
            freq = random.uniform(0.0, 0.1)
        
        # Introduce random glitches
        if random.random() < 0.03:
            freq = 1 - freq
    

        # Send the signal
        data = json.dumps(freq)
        conn.sendall((f'{data}\n').encode())   # REMOVE newline character here and in analyzer
        
        #Increament the counter and sleep
        counter += 1
        time.sleep(0.05)
except (BrokenPipeError, ConnectionResetError):
    print('Client disconnected')
finally:
    conn.close()
    sock.close()
    print('Broadcasting stopped')
