<h1 align="center"> EVM-for-assembler  </h1>
This project implements an assembler and interpreter for an **Educational Virtual Machine (EVM)**. The EVM is designed to process a predefined instruction set, enabling efficient testing and execution of programs for educational purposes.

The system includes:
1. **Assembler**: Translates human-readable assembly instructions into machine code (binary format).
2. **Interpreter**: Executes the binary program on the virtual machine and produces memory-based results.

# ✨ Features

- **Instruction Support**: Implements essential EVM commands:
  - Load constant (`198`)
  - Read memory (`67`)
  - Write memory (`244`)
  - Subtract (`103`)
- **File Input/Output**:
  - Reads assembly source code in a custom format.
  - Produces binary files, logs (CSV format), and result files (CSV format).
- **Flexible Command-line Interface**: Supports options for input/output files, logging, and memory slicing.
- **Custom Memory Management**: Handles a 256-byte virtual memory model with configurable slices.

# 📘 Installation and running

```commandline
git clone https://github.com/Nikindrik/EVM-for-assembler
python -m venv venv
```

For windows
```commandline
.\venv\Scripts\activate
```

For linux/UNIX/MAC
```commandline
source venv/bin/activate
```

Run
```commandline
python main.py assemble <path_to_input.txt> <path_to_output.bin> --log_file <path_to_log.csv>
python main.py interpret <path_to_output.bin> <path_to_result.csv> --memory_range=0:10
```

**Example**

**input.txt**
```editorconfig
A=198,B=2,C=352
A=67,B=17,C=459,D=6
A=244,B=22,C=28
A=103,B=15,C=18,D=21
```

Run
```editorconfig
python main.py assemble source/input.txt source/output.bin --log_file source/log.csv
python main.py interpret source/output.bin source/result.csv --memory_range=0:10
```

# 📑 Instruction Format

**Assembly Commands**

The following table summarizes the EVM's supported instructions:

| Command         | Opcode | Size (bytes) | Description                                                  |
|------------------|-------------|---------------|-----------------------------------------------------------|
| **Load constant** | `198`       | 6             | Loads a constant into a memory register                   |
| **Read memory**     | `67`        | 4             | Reads a value from memory using a base address and offset |
| **Write memory**    | `244`       | 3             | Writes a register's value to a memory location            |
| **Subtract**        | `103`       | 3             | ubtracts two register values and stores the result in memory |


# 🖼️ Results Gallery

