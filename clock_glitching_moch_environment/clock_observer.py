import socket
import json
import matplotlib.pyplot as plt
import collections
import sys
import argparse

# Initialize the data storage
x_data = collections.deque(maxlen=50)
y_data = collections.deque(maxlen=50)
frame = 0



def parse_arguments():
    parser = argparse.ArgumentParser(description="Clock frequency server with glitching.")
    parser.add_argument("-b", "--binary", type=bool, default=False, help="Clean binary clock signal.")
    parser.add_argument("-f", "--float", type=bool, default=False, help="Jittery floating point clock signal.")
    return parser.parse_args()



def connect_to_server():
    """Connect to the clock frequency server."""
    HOST, PORT = 'localhost', 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


    
def main():
    global x_data, y_data, frame
    
    args = parse_arguments()
    print("Arguments received:")
    print(f"Binary: {args.binary}, Float: {args.float}")
   
    # Connect to the server
    sock = connect_to_server()
    if not sock:
        print("Failed to connect to the server.")
        return


    


    # Set up a real-time plot
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b-', label='Observed Clock Frequency')
    
    if args.binary:
        ax.set_ylim(-0.2, 1.2)
    elif args.float:
        ax.set_ylim(-0.2, 3.5)
    
    ax.set_xlim(0, 50)
    ax.set_xlabel('Time (updates)')
    ax.set_ylabel('Frequency')
    ax.legend()

    def update(frame):
        ax.clear()
        ax.plot(x_data, y_data, 'b-', label='Observed Clock Frequency')
        if args.binary:
            ax.set_ylim(-0.2, 1.2)
        elif args.float:
            ax.set_ylim(-0.2, 3.5)  
        ax.set_xlim(max(0, x_data[0] if x_data else 0), max(x_data) + 1)
        ax.legend()
        plt.pause(0.01)  # Pause to allow the plot to update


    # Close program gracefully on plot close
    def on_close(event):
        print("Plot window closed. Closing socket...")
        sock.close()
        sys.exit()  # Exit the program
        

    # Connect the close event to the on_close function
    fig.canvas.mpl_connect('close_event', on_close)

    # Receive the clock frequency from the server
    while sock:
        try:
            data = sock.recv(1024).decode().strip()
            if not data:
                break
            for line in data.split('\n'):
                frame += 1
                packet = json.loads(line)
                
                x_data.append(frame)
                y_data.append(packet)
                print(f"Received: {packet}")
                update(frame)
        except (json.JSONDecodeError, ConnectionError):
            break

    plt.show()

if __name__ == "__main__":
    main()