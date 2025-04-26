import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import json
import random as rand
import argparse
import subprocess

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Clock frequency server with glitching.")
    parser.add_argument("-b", "--binary", type=bool, default=False, help="Clean binary clock signal.")
    parser.add_argument("-f", "--float", type=bool, default=False, help="Jittery floating point clock signal.")
    parser.add_argument("-g", "--glitch", type=bool, default=False, help="Introduce a clock glitch.")
    parser.add_argument("-gf", "--glitchframe", type=int, default=500, help="Frame to introduce glitch.")
    parser.add_argument("-fft", "--fftanalysis", type=bool, default=False, help="Perform FFT analysis.")
    return parser.parse_args()


# Setup the socket server
def setup_socket():
    HOST, PORT = 'localhost', 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, _ = sock.accept()  # Wait for a connection
    return sock, conn


# Generate binary clock signal
def generate_binary_signal(frame):
    return 1 if (frame % 10) < 5 else 0


# Generate a floating point signal with jitter
def generate_float_signal(frame):
    if (frame % 10) < 5:
        return rand.uniform(3.2, 3.4)
    else:
        return rand.uniform(-0.1, 0.1)


# Apply a glitch to the signal
def apply_glitch(state, glitch_performed, frame):
    # if rand.random() < 0.01: # uncomment for randomization
    state = 1 - state
    glitch_performed = True
    print("GLITCH PERFORMED at time: ", frame)
    return state, glitch_performed


# Start the observer program as a subprocess
def start_observer(binary, float):
    observer_script = "./clock_observer.py"
    try:
        if binary:
            subprocess.Popen(["python", observer_script, "-b True"])
        elif float:
            subprocess.Popen(["python", observer_script, "-f True"])
        print(f"Observer program '{observer_script}' started.")
    except Exception as e:
        print(f"Failed to start observer program: {e}")


# Start the FFT observer program as a subprocess
def start_observer_fft():
    """Start the observer program as a subprocess."""
    observer_script = "./FFTdata_observer.py"
    try:
        subprocess.Popen(["python", observer_script])
        print(f"Observer program '{observer_script}' started.")
    except Exception as e:
        print(f"Failed to start observer program: {e}")


def main():
    args = parse_arguments()
    
    if not args:
        print("No arguments provided. Example usage: python clock_freq_server.py -j True -g True -gf 500")
        return

    print("Arguments received:")
    print(f"Binary: {args.binary}, Float: {args.float}, Glitch: {args.glitch}, Glitch Frame: {args.glitchframe}")
    # Start the observer program
    if args.fftanalysis:
        start_observer_fft()
    else:
        start_observer(args.binary, args.float)

    sock, conn = setup_socket()

    frame = 0
    glitch_performed = False

    while conn:
        if args.binary:
            state = generate_binary_signal(frame)
        elif args.float:
            state = generate_float_signal(frame)
        else:
            state = 0  # Default state if no flag is set

        if args.glitch and args.glitchframe < frame and not glitch_performed:
            state, glitch_performed = apply_glitch(state, glitch_performed, frame)

        data = json.dumps(state)
        conn.sendall((f'{data}\n').encode())

        frame += 1

    sock.close()


if __name__ == "__main__":
    main()