## How it works

This project implements a 16 Byte memory module (it consists of 16 memory locations that store 1 byte each). The memory allows for both read and write operations, controlled by input signals.

***Control Signals*** 
* ui_in[7:0]: Dedicated input line for all control signals
* ce_n (Active Low): Chip enable signal for reading data.
* lr_n (Active Load): Load/Read signal, enabling writing to memory.
* uio_in[7:0]: Bidrectional IO line for input.
* uio_out[7:0]: Bidrectional IO line for output.
* uio_oe (Active High): Bidirection IO signal for when outputing to bus
* ena (Active High):  Tiny Tapeout signal for enabling the module
* clk: global clock
* rst_n (Active low)
* uo_out[7:0]: Dedicated output line 7 segment display **(Unused)**
  
***Addressing:*** The memory 4-bit addressable, where the address specifies which register (out of 16) is being accessed for reading or writing.
***Write operation:*** A byte of data can be written into the memory when the write enable (lr_n) signal is active (low) and the clock edge occurs.
***Read operation:*** Data from a specific address can be read when the chip enable (ce_n) signal is active (low). The data is output on the uio_out bus, and it is updated on the clock edge.

***Output:*** Data is presented on the uio_out line when the chip is enabled for reading, and high-impedance (Z) otherwise.

## How to test

The test provided under tests is a simple test case to check the basic read/write functionality of the memory. 
There are many edge cases that will be tested in the future, such as inconsisitent control signals, and access/store time. 

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any (add)
