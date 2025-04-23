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
with open('./real_clock_data/exported_clock.csv', 'r') as real_clock_data:
    csv_reader = csv.reader(real_clock_data)
    # print(csv_reader)
    for line in csv_reader:
        print(float(line[0]))
        # Send the signal to (FFTdata_obsever.py) for analysis
        data = json.dumps(float(line[0]))
        # REMOVE newline character since realworld ain't that perfect
        conn.sendall((f'{data}\n').encode())

# Close the connection
conn.close()
