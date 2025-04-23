# Live plot code
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as rand
import socket
import json


# Set up the socket server (for observation)
HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, _ = sock.accept() # Wait for a connection


# Create a firgure and axis
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'r-', label='Clock Frequency')
glitch_performed = False

def update(frame):
    global x_data, y_data
    
    # Create a fake clock frequency based on animation frame number
    if (frame % 10) < 5:
        freq = 1
    else:
        freq = 0
        
    # Introduce random glitches
    if not glitch_performed:
        if rand.random() < 0.03:
            freq = 1 - freq
            glitch_performed = True
    
    
    ############ Uncomment for animation ############
    x_data.append(frame)
    y_data.append(freq)
    
    # 50 reading sliding window
    x_data = x_data[-50:]
    y_data = y_data[-50:]
    
    ax.clear()
    ax.plot(x_data, y_data, 'r-', label='Clock Frequency')
    ax.set_ylim(-1, 2)
    ax.set_xlim(max(0, frame - 50), frame +1)
    ax.set_xlabel(' Time (updates)')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.set_title('Moch Clock Frequency')
    ######################################################
    
    # Send the signal to (FFTdata_obsever.py) for analysis
    data = json.dumps(freq)
    # REMOVE newline character since realworld ain't that perfect
    conn.sendall((f'{data}\n').encode())   


ani = animation.FuncAnimation(fig, update, interval=60)
plt.show()
conn.close()