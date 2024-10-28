## How it works

This project implements a 1-byte x 16 register memory module (it consists of 16 memory locations that store 1 byte each). The memory allows for both read and write operations, controlled by input signals.

Addressing: The memory is accessed by a 4-bit address (since 16 memory locations require 2^4 addresses). The address specifies which register (out of 16) is being accessed for reading or writing.
Write operation: A byte of data can be written into the memory when the write enable (lr_n) signal is active (low) and the clock edge occurs.
Read operation: Data from a specific address can be read when the chip enable (ce_n) signal is active (low). The data is output on the uio_out bus, and it is updated on the clock edge.
Control Signals:
  ce_n (Chip Enable): Active low, it enables the chip for reading data.
  lr_n (Load/Read Enable): Active low, it enables writing to memory.
Output: Data is presented on the uio_out line when the chip is enabled for reading, and high-impedance (Z) otherwise.

## How to test

The test provided under tests is a simple test case to check the basic read/write functionality of the memory. 
There are many edge cases that will be tested in the future, such as inconsisitent control signals, and access/store time. 

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any (add)
