import random
from typing import TextIO

MAX = (2**16) - 1

binary_list = [format(i, '016b') for i in range(MAX + 1)]

def generate_start() -> str:
    return "1" * random.randint(10, 50)


def generate_UART(s: str) -> str:
    return "0" + s + "0"

def write_in_format(bitpattern: str, f: TextIO):
    for bit in bitpattern:
        f.write(bit + "\n")

def main():

    f = open("test_data.csv", "w")
    start = generate_start()
    write_in_format(start, f)

    binary_list = [format(i, '016b') for i in range(MAX + 1)]
   
    for num in binary_list:
        num = generate_UART(num)
        write_in_format(num, f)
    f.close()
if __name__ == "__main__":
    main()
    
