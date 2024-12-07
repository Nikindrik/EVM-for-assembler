import argparse
import struct
import csv

result_data = []
log_file_data = []

def parse_args():
    '''
    Parsing command line arguments
    :return: command line arguments
    '''
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")
    parser.add_argument("mode", choices=["assemble", "interpret"], help="Operation mode: 'assemble' or 'interpret'")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("output_file", help="Output file or result file")
    parser.add_argument("--log_file", help="Log file (CSV format) for assembler")
    parser.add_argument("--memory_range", help="Memory range for interpreter (start:end)", type=str)
    return parser.parse_args()

def read_input_file(input_file: str):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error! File {input_file} not found")
        exit(1)

def parse_instruction(instruction: str) -> dict:
    '''
    Parses a string with instructions for keys (A, B, C, D) and converts them into numeric values
    :param instruction: instruction
    :return: A dictionary of instruction parameters, where keys are strings and values are numbers
    '''
    parts = instruction.split(',')
    values = {}
    for part in parts:
        key, value = part.split('=')
        values[key.strip()] = int(value.strip())
    return values

def assemble_instruction(value: dict):
    '''
    Generates machine code (in bytes) based on the instruction parameters and adds it to the global list
    :param value: Dictionary with instruction parameters (keys A, B, C, D)
    :return:
    '''
    global result_data, log_file_data
    A = value['A']
    B = value['B']
    C = value['C']
    D = value.get('D', 0)

    if A == 198:
        command = A | (B << 8) | (C << 13)
        bytes_ = command.to_bytes(6, byteorder='little')
    elif A == 67:  # 4-byte command (read memory)
        command = A | (B << 8) | (C << 13) | (D << 25)
        bytes_ = command.to_bytes(4, byteorder='little')
    elif A in (244, 103):  # 3-byte command (write memory or subtract)
        command = A | (B << 8) | (C << 13) | (D << 18)
        bytes_ = command.to_bytes(3, byteorder='little')
    else:
        print(f"Unknown instruction A={A}")
        return

    result_data.extend(bytes_)
    log_file_data.append({
        "A": A, "B": B, "C": C, "D": D,
        "bytes": ",".join([f"0x{byte:02X}" for byte in bytes_])
    })

def write_log_file(log_file):
    with open(log_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["A", "B", "C", "D", "bytes"])
        writer.writeheader()
        writer.writerows(log_file_data)
    print(f"Log written to {log_file}")

def write_binary_file(output_file):
    with open(output_file, "wb") as file:
        file.write(bytearray(result_data))
    print(f"Binary written to {output_file}")

def read_binary_file(input_file):
    try:
        with open(input_file, "rb") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error! File {input_file} not found")
        exit(1)

def interpret_commands(binary_data: bytes, memory_range: str):
    '''
    Executes commands read from a binary file, modifying virtual memory, and returns a slice of it over a specified range
    :param binary_data: Byte data read from a binary file
    :param memory_range: Format string memory range
    :return: List of memory values
    '''
    memory = [0] * 256
    for i in range(0, len(binary_data), 6):
        if i + 6 > len(binary_data):
            break
        command = int.from_bytes(binary_data[i:i+6], byteorder='little')
        opcode = command & 0xFF
        arg1 = (command >> 8) & 0x1F
        arg2 = (command >> 13) & 0xFFFFF
        if opcode == 198:  # Load constant
            memory[arg1] = arg2
        elif opcode == 67:  # Read memory
            offset = arg2
            address = (command >> 25) & 0x1F
            memory[arg1] = memory[address] + offset
        elif opcode == 244:  # Write memory
            address = arg1
            value = memory[arg2]
            memory[address] = value
        elif opcode == 103:  # Subtract
            address1 = arg1
            address2 = arg2
            result_address = (command >> 18) & 0x1F
            memory[result_address] = memory[address1] - memory[address2]

    start, end = map(int, memory_range.split(":"))
    return memory[start:end]

def write_result_file(result_file, memory_slice):
    with open(result_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Address", "Value"])
        for address, value in enumerate(memory_slice):
            writer.writerow([address, value])
    print(f"Result written to {result_file}")

def main():
    args = parse_args()
    if args.mode == "assemble":
        if not args.log_file:
            print("Error! Log file is required for assembly.")
            exit(1)
        instructions = read_input_file(args.input_file)
        for line in instructions:
            if not line.strip():
                continue
            values = parse_instruction(line.strip())
            assemble_instruction(values)
        write_binary_file(args.output_file)
        write_log_file(args.log_file)
    elif args.mode == "interpret":
        if not args.memory_range:
            print("Error! Memory range is required for interpretation.")
            exit(1)
        binary_data = read_binary_file(args.input_file)
        memory_slice = interpret_commands(binary_data, args.memory_range)
        write_result_file(args.output_file, memory_slice)

if __name__ == "__main__":
    main()