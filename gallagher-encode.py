# Script created by sealldev / sealldeveloper
# Research from https://github.com/megabug/gallagher-research
import sys
import readline
import argparse
import subprocess
import time
import pexpect
from math import floor

def bitwise_inverse(hex_string):
    hex_string = hex_string.replace(" ", "").upper()
    num = int(hex_string, 16)
    inverted = ~num & 0xFFFFFFFFFFFFFFFF
    return format(inverted, '016X')

def write_to_proxmark(hex_data, block_number, key):
    command_read = f"hf mf rdsc -s {floor(block_number/4)} -k {key}"
    command_write = f"hf mf csetblk --blk {block_number} -d {hex_data}{bitwise_inverse(hex_data)}"
    
    child = pexpect.spawn('pm3 -p /dev/tty.usbmodemiceman1', encoding='utf-8')
    child.logfile = sys.stdout

    def send_command(cmd, expect_prompt=True):
        child.sendline(cmd)
        if expect_prompt:
            child.expect('pm3 -->', timeout=10)

    try:
        # Wait for initial prompt
        child.expect('pm3 -->', timeout=10)
        send_command(command_read)
        send_command(command_write)
        send_command(command_read)

    except pexpect.TIMEOUT:
        print("Command timed out. Proxmark3 might not be responding.")
    except pexpect.EOF:
        print("Proxmark3 client closed unexpectedly.")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        # Ensure we exit the simulation mode and close the client
        child.sendline("exit")
        child.close()

def emulate_to_proxmark(hex_data, block_number):
    command_load = "hf mf eload -f base-dump.json"
    command_write = f"hf mf esetblk --blk {block_number} -d {hex_data}{bitwise_inverse(hex_data)}"
    command_sim = f"hf mf sim --1k"

    child = pexpect.spawn('pm3 -p /dev/tty.usbmodemiceman1', encoding='utf-8')
    child.logfile = sys.stdout

    def send_command(cmd, expect_prompt=True):
        child.sendline(cmd)
        if expect_prompt:
            child.expect('pm3 -->', timeout=10)

    try:
        # Wait for initial prompt
        child.expect('pm3 -->', timeout=10)
        send_command(command_load)
        send_command(command_write)
        send_command(command_sim, expect_prompt=False)

        # Wait for "Emulator stopped" message
        child.expect('Emulator stopped', timeout=None)

    except pexpect.TIMEOUT:
        print("Command timed out. Proxmark3 might not be responding.")
    except pexpect.EOF:
        print("Proxmark3 client closed unexpectedly.")
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    finally:
        # Ensure we exit the simulation mode and close the client
        child.sendline("exit")
        child.close()

def create_sbox():
    return [
        0xA3, 0xB0, 0x80, 0xC6, 0xB2, 0xF4, 0x5C, 0x6C, 0x81, 0xF1, 0xBB, 0xEB, 0x55, 0x67, 0x3C, 0x05,
        0x1A, 0x0E, 0x61, 0xF6, 0x22, 0xCE, 0xAA, 0x8F, 0xBD, 0x3B, 0x1F, 0x5E, 0x44, 0x04, 0x51, 0x2E,
        0x4D, 0x9A, 0x84, 0xEA, 0xF8, 0x66, 0x74, 0x29, 0x7F, 0x70, 0xD8, 0x31, 0x7A, 0x6D, 0xA4, 0x00,
        0x82, 0xB9, 0x5F, 0xB4, 0x16, 0xAB, 0xFF, 0xC2, 0x39, 0xDC, 0x19, 0x65, 0x57, 0x7C, 0x20, 0xFA,
        0x5A, 0x49, 0x13, 0xD0, 0xFB, 0xA8, 0x91, 0x73, 0xB1, 0x33, 0x18, 0xBE, 0x21, 0x72, 0x48, 0xB6,
        0xDB, 0xA0, 0x5D, 0xCC, 0xE6, 0x17, 0x27, 0xE5, 0xD4, 0x53, 0x42, 0xF3, 0xDD, 0x7B, 0x24, 0xAC,
        0x2B, 0x58, 0x1E, 0xA7, 0xE7, 0x86, 0x40, 0xD3, 0x98, 0x97, 0x71, 0xCB, 0x3A, 0x0F, 0x01, 0x9B,
        0x6E, 0x1B, 0xFC, 0x34, 0xA6, 0xDA, 0x07, 0x0C, 0xAE, 0x37, 0xCA, 0x54, 0xFD, 0x26, 0xFE, 0x0A,
        0x45, 0xA2, 0x2A, 0xC4, 0x12, 0x0D, 0xF5, 0x4F, 0x69, 0xE0, 0x8A, 0x77, 0x60, 0x3F, 0x99, 0x95,
        0xD2, 0x38, 0x36, 0x62, 0xB7, 0x32, 0x7E, 0x79, 0xC0, 0x46, 0x93, 0x2F, 0xA5, 0xBA, 0x5B, 0xAF,
        0x52, 0x1D, 0xC3, 0x75, 0xCF, 0xD6, 0x4C, 0x83, 0xE8, 0x3D, 0x30, 0x4E, 0xBC, 0x08, 0x2D, 0x09,
        0x06, 0xD9, 0x25, 0x9E, 0x89, 0xF2, 0x96, 0x88, 0xC1, 0x8C, 0x94, 0x0B, 0x28, 0xF0, 0x47, 0x63,
        0xD5, 0xB3, 0x68, 0x56, 0x9C, 0xF9, 0x6F, 0x41, 0x50, 0x85, 0x8B, 0x9D, 0x59, 0xBF, 0x9F, 0xE2,
        0x8E, 0x6A, 0x11, 0x23, 0xA1, 0xCD, 0xB5, 0x7D, 0xC7, 0xA9, 0xC8, 0xEF, 0xDF, 0x02, 0xB8, 0x03,
        0x6B, 0x35, 0x3E, 0x2C, 0x76, 0xC9, 0xDE, 0x1C, 0x4B, 0xD1, 0xED, 0x14, 0xC5, 0xAD, 0xE9, 0x64,
        0x4A, 0xEC, 0x8D, 0xF7, 0x10, 0x43, 0x78, 0x15, 0x87, 0xE4, 0xD7, 0x92, 0xE1, 0xEE, 0xE3, 0x90
    ]

def encode_with_sbox(binary_string):
    sbox = create_sbox()
    encoded_values = []
    
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        value = int(byte, 2)
        encoded_value = sbox[value]
        encoded_values.append(encoded_value)
    
    return ''.join(f"{value:02X}" for value in encoded_values)

def recreate_binary_string(parsed_values):
    structure = {
        'CN': [[26,25,24] + [23,22,21,20,19,18,17,16] + [39,38,37,36,35] + [7,6,5,4,3,2,1,0]],
        'FC': [[59,58,57,56] + [15,14,13,12,11,10,9,8] + [47,46,45,44]],
        'RC': [[30,29,28,27]],
        'UB': [[34,33,32,31]],
        'UE': [[43,42,41,40]],
        'UC': [[51,50,49,48]],
        'UD': [[55,54,53,52]],
        'IL': [[63,62,61,60]]
    }
    
    binary_string = ['0']*64
    for field, bits in structure.items():
        if field in parsed_values:
            value = parsed_values[field]
            binary_value = bin(value).replace('0b','').zfill(len(bits[0]))[::-1]
            i=0
            for b in bits[0]:
                binary_string[b] = binary_value[i]
                i+=1
    
    return "".join(binary_string)

def process_values(parsed_values):
    recreated_binary = recreate_binary_string(parsed_values)
    print(f"Recreated Binary String: {recreated_binary}")

    print(f"Unencoded Hex String {hex(int(recreated_binary,2)).replace('0x','').upper()}")

    encoded_hex = encode_with_sbox(recreated_binary)
    print(f"Encoded Hex String: {encoded_hex}")

    return encoded_hex

def interactive_mode():
    while True:
        parsed_values = {}
        for field in ['CN', 'FC', 'RC', 'UB', 'UE', 'UC', 'UD', 'IL']:
            value = input(f"Enter value for {field}: ")
            parsed_values[field] = int(value)

        process_values(parsed_values)

        continue_input = input("Do you want to enter another set of values? (y/n): ")
        if continue_input.lower() != 'y':
            break

def main():
    parser = argparse.ArgumentParser(description="Gallagher Encoder by sealldev")
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--write-proxmark', action='store_true', help='Write encoded data to Proxmark3')
    parser.add_argument('--emulate-proxmark', action='store_true', help='Emulate encoded data to Proxmark3')
    parser.add_argument('-b', '--block', type=int, help='Block to write or emulate to when using Proxmark3')
    parser.add_argument('-k', '--key', help='Key to read original data with using Proxmark3')
    parser.add_argument('--CN', type=int, help='Value for CN')
    parser.add_argument('--FC', type=int, help='Value for FC')
    parser.add_argument('--RC', type=int, help='Value for RC')
    parser.add_argument('--UB', type=int, help='Value for UB')
    parser.add_argument('--UE', type=int, help='Value for UE')
    parser.add_argument('--UC', type=int, help='Value for UC')
    parser.add_argument('--UD', type=int, help='Value for UD')
    parser.add_argument('--IL', type=int, help='Value for IL')

    args = parser.parse_args()

    print(" -- Gallagher Encoder by sealldev -- ")
    if args.interactive:
        interactive_mode()
    elif all(getattr(args, field) is not None for field in ['CN', 'FC', 'RC', 'UB', 'UE', 'UC', 'UD', 'IL']):
        parsed_values = {
            'CN': args.CN,
            'FC': args.FC,
            'RC': args.RC,
            'UB': args.UB,
            'UE': args.UE,
            'UC': args.UC,
            'UD': args.UD,
            'IL': args.IL
        }
        encoded_hex = process_values(parsed_values)
        block = 60
        key = "A0A1A2A3A4A5"
        if args.block:
            block = args.block
        if args.key:
            key = args.key
        if args.write_proxmark:
            write_to_proxmark(encoded_hex, block, key)
        if args.emulate_proxmark:
            emulate_to_proxmark(encoded_hex, block)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
