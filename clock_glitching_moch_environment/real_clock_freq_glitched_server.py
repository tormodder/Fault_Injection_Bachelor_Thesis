# Live plot code
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import json
import csv

# Set up the socket server (for observation)
HOST, PORT = 'localhost', 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, _ = sock.accept() # Wait for a connection


# Broadcast the real clock frequency data
# with open('./real_clock_data/exported_clock.csv', 'r') as real_clock_data:
with open('./real_clock_data/exported_clock_glitched.csv', 'r') as real_clock_data:
    csv_reader = csv.reader(real_clock_data)
    # print(csv_reader)
    for line in csv_reader:
        print(float(line[0]))
        # Send the signal to (FFTdata_obsever.py) for analysis
        data = json.dumps(float(line[0]))
        # REMOVE newline character since realworld ain't that perfect
        conn.sendall((f'{data}\n').encode())
    


# Animation of real clock from datadump
# with open('exported_clock.csv', 'r') as real_clock_data:
#     csv_reader = csv.reader(real_clock_data)
    
#     fig, ax = plt.subplots()
    
#     line, = ax.plot([], [], 'r-', label='Clock Frequency')
#     x_data, y_data = [], []

#     def update(frame):
#         global x_data, y_data
#         try:
#             row = next(csv_reader)
#             x_data.append(frame)
#             y_data.append(float(row[0]))
#             # print(f'Frame: {frame}, Data: {row[0]}')
#             data = json.dumps(float(row[0]))
#             # REMOVE newline character since realworld ain't that perfect
#             conn.sendall((f'{data}\n').encode())  
#         except StopIteration:
#             pass
        
#         x_data = x_data[-50:]
#         y_data = y_data[-50:]
        
#         ax.clear()
#         ax.plot(x_data, y_data, 'r-', label='Clock Frequency')
#         ax.set_ylim(min(y_data) - 1, max(y_data) + 1)
#         ax.set_xlim(max(0, x_data[0] if x_data else 0), x_data[-1] if x_data else 1)
#         ax.set_xlabel('Time (updates)')
#         ax.set_ylabel('Frequency')
#         ax.legend()
#         ax.set_title('Clock Frequency')
        
#     ani = animation.FuncAnimation(fig, update, interval=1)
#     plt.show()




# Close the connection
conn.close()
