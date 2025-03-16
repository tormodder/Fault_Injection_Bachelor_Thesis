import socket
import json
import matplotlib.pyplot as plt
import collections


# Connect to the clock_freq_server.py
HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


# Initialize the data storage
x_data = collections.deque(maxlen=50)
y_data = collections.deque(maxlen=50)


# Set up a real-time plot
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='Observed Clock Frequency')
ax.set_ylim(-1, 2)
ax.set_xlim(0, 50)
ax.set_xlabel('Time (updates)')
ax.set_ylabel('Frequency')
ax.legend()

def update(frame):
    global x_data, y_data
    ax.clear()
    ax.plot(x_data, y_data, 'b-', label='Observed Clock Frequency')
    ax.set_ylim(-1, 2)
    ax.set_xlim(max(0, x_data[0] if x_data else 0), max(x_data) + 1)
    ax.legend()
    plt.pause(0.05)
    

# Receive the clock frequency from the server
while True:
    try:
        data = sock.recv(1024).decode().strip()
        if not data:
            break
        for line in data.split('\n'):
            packet = json.loads(line)
            x_data.append(packet['frame'])
            y_data.append(packet['frequency'])
            update(packet['frame'])
    except (json.JSONDecodeError, ConnectionError):
        break


sock.close()
plt.show()