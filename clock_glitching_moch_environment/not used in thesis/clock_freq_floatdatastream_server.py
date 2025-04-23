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
conn, addr = sock.accept() # Wait for a connection
print(f'Connected to signal receiver at {addr}')

frame = 0
glitch_performed = False # UNCOMMENT for glitching

while conn:
    # # Setting the state of the moch clock signal
    # if (frame % 10) < 5:
    #     state = random.uniform(0.9, 1.0)
    # else:
    #     state = random.uniform(0.0, 0.1)
    
    # Setting the state of the moch clock signal - Voltage levels
    if (frame % 10) < 5:
        state = random.uniform(3.1, 3.5)
    else:
        state = random.uniform(-0.2, 0.2)
        
    #############################################
    # UNCOMMENT for glitching
    #############################################
    # Introduce a single random glitch at a specific frame for analysis
    if frame > 500 and not glitch_performed:
        if random.random() < 0.01:
            state = 3.3 - state
            print("GLITCH PERFORMED at time: ", frame)
            glitch_performed = True
    #############################################

    # Send the clock frequency to the client as "bitstream"
    data = json.dumps(state)
    conn.sendall((f'{data}\n').encode())
    
    frame += 1

sock.close()