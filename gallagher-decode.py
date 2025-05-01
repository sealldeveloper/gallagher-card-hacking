# Script created by sealldev / sealldeveloper
# Research from https://github.com/megabug/gallagher-research
import sys
import readline
import argparse
import pexpect
import time
from math import floor


def bitwise_inverse(hex_string):
    hex_string = hex_string.replace(" ", "").upper()
    num = int(hex_string, 16)
    inverted = ~num & 0xFFFFFFFFFFFFFFFF
    return format(inverted, '016X')

def read_from_proxmark(block_number, key):
    data=""
    command_read = f"hf mf rdsc -s {floor(block_number/4)} -k {key}"
    
    child = pexpect.spawn('pm3 -p /dev/tty.usbmodemiceman1', encoding='latin-1')
    child.logfile = sys.stdout

    def send_command(cmd, expect_prompt=True):
        child.sendline(cmd)
        if expect_prompt:
            child.expect('pm3 -->', timeout=10)

    try:
        # Wait for initial prompt
        child.expect('pm3 -->', timeout=10)
        send_command(command_read)
        data = child.before.split(f'{block_number} | ')[1].split(' | ')[0].replace(' ','')

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
    
    data_part1 = data[:16]
    data_part2 = data[16:]

    if bitwise_inverse(data_part1) == data_part2:
        return data_part1
    else:
        print('The data is not a valid Gallagher block!')
        return None
    return None

def hex_to_binary(hex_string):
    return ''.join(format(int(char, 16), '08b') for char in hex_string.split())

def create_inverse_sbox():
    original_sbox = [
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
    
    inverse_sbox = {value: index for index, value in enumerate(original_sbox)}
    return inverse_sbox

def inverse_lookup(hex_string):
    inverse_sbox = create_inverse_sbox()
    
    hex_string = hex_string.replace(" ", "").upper()
    hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    
    result = []
    for pair in hex_pairs:
        value = int(pair, 16)
        inverse_value = inverse_sbox[value]
        result.append(f"{inverse_value:02X}")
    
    return " ".join(result)

def parse_hex_string(hex_string):
    binary = hex_to_binary(hex_string)
    
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
    
    for key in structure:
        structure[key][0] = structure[key][0][::-1]

    results = {}
    
    for field, bit_lists in structure.items():
        value = 0
        bit_count = sum(len(bit_list) for bit_list in bit_lists)
        for bit_list in bit_lists:
            for bit in bit_list:
                value = (value << 1) | int(binary[bit])
        results[field] = (value, bit_count)
    
    if 'RC' in results:
        rc_value, rc_bits = results['RC']
        if 0 <= rc_value <= 15:
            if rc_value == 0:
                results['RC'] = (rc_value, 'A', rc_bits)
            else:
                results['RC'] = (rc_value, chr(rc_value + (ord('A'))), rc_bits)
        else:
            results['RC'] = ('Invalid', 'Invalid', rc_bits)
    
    return results

def process_input(user_input):
    inverse_result = inverse_lookup(user_input)
    print(f"Substitution Decoded: {inverse_result.replace(' ','')}")
    
    parsed_values = parse_hex_string(inverse_result)

    for key, value in parsed_values.items():
        if key == 'RC':
            numeric_value, letter_value, bit_count = value
            print(f"{key}: {numeric_value} ({letter_value}) (Binary: {bin(numeric_value)[2:].zfill(bit_count)})")
        else:
            numeric_value, bit_count = value
            print(f"{key}: {numeric_value} (Binary: {bin(numeric_value)[2:].zfill(bit_count)})")
    print()

def main():
    parser = argparse.ArgumentParser(description="Gallagher Decoder by sealldev")
    parser.add_argument('--read-proxmark',action='store_true',help='Read from proxmark card')
    parser.add_argument('-b', '--block',type=int,help='Read from proxmark card block')
    parser.add_argument('-k', '--key',help='Read from proxmark card key')
    parser.add_argument('hex_strings', nargs='*', help='Hex strings to process')
    
    args = parser.parse_args()

    print(" -- Gallagher Decoder by sealldev -- ")
    if args.hex_strings:
        # Process command-line arguments
        for arg in args.hex_strings:
            print(f"Processing input: {arg}")
            process_input(arg)
    if args.read_proxmark:
        block = 60
        key = "A0A1A2A3A4A5"
        if args.key:
            key = args.key
        if args.block:
            block = int(args.block)
        hex_string = read_from_proxmark(block, key)
        if hex_string == None:
            return
        process_input(hex_string)
    else:
        # Interactive mode
        print("Enter hex strings (or 'q' to quit):")
        while True:
            user_input = input("> ")
            if user_input.lower() == 'q':
                break
            if user_input:
                process_input(user_input)

if __name__ == "__main__":
    main()
