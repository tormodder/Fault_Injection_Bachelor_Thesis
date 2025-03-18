# Live plot code
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import json


# Set up the socket server (for observation)
HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, _ = sock.accept() # Wait for a connection

counter = 0

# Quick send
while conn:
    # Create a fake clock frequency based on animation frame number
    if (counter % 4) < 2:
        freq = random.uniform(0.9, 1.0)
    else:
        freq = random.uniform(0.0, 0.1)





    # Send the clock frequency to the client as "bitstream"
    data = json.dumps(freq)
    # REMOVE newline character since realworld ain't that perfect
    conn.sendall((f'{data}\n').encode()) 
    counter += 1


conn.close()


# Create a firgure and axis
# fig, ax = plt.subplots()
# x_data, y_data = [], []
# line, = ax.plot([], [], 'r-', label='Clock Frequency')

# def update(frame):
#     global x_data, y_data
    
#     # Create a fake clock frequency based on animation frame number
#     if (frame % 10) < 5:
#         freq = random.uniform(0.8, 1.0)
#     else:
#         freq = random.uniform(0.0, 0.2)
#     x_data.append(frame)
#     y_data.append(freq)
    
#     # 50 reading sliding window
#     x_data = x_data[-50:]
#     y_data = y_data[-50:]
    
#     ax.clear()
#     ax.plot(x_data, y_data, 'r-', label='Clock Frequency')
#     ax.set_ylim(-1, 2)
#     ax.set_xlim(max(0, frame - 50), frame +1)
#     ax.set_xlabel(' Time (updates)')
#     ax.set_ylabel('Frequency')
#     ax.legend()
#     ax.set_title('Moch Clock Frequency')
    
#     # Send the clock frequency to the client as "bitstream"
#     # data = json.dumps(freq)
#     # print(data)
#     # conn.sendall((data).encode())
    
#     data = json.dumps(freq)
#     # REMOVE newline character since realworld ain't that perfect
#     conn.sendall((f'{data}\n').encode()) 
    
# ani = animation.FuncAnimation(fig, update, interval=60)
# plt.show()
# conn.close()