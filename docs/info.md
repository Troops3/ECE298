## How it works

This project implements a 16 Byte memory module (it consists of 16 memory locations that store 1 byte each). The memory allows for both read and write operations, controlled by input signals.

***Control Signals*** 
* ui_in[7:0]: Dedicated input line for all control signals
* ce_n (Active Low): Chip enable signal for reading data.
* lr_n (Active Load): Load/write signal, enabling writing to memory.
* uio_in[7:0]: Bidrectional IO line for input.
* uio_out[7:0]: Bidrectional IO line for output.
* uio_oe (Active High): Bidirection IO signal for when outputing to bus
* ena (Active High):  Tiny Tapeout signal for enabling the module
* clk: global clock. Operations happen on the positive edge
* rst_n (Active low): Resets all contents in RAM to NULL.
* uo_out[7:0]: Dedicated output line 7 segment display **(Unused)**
  
***Addressing:*** 
The memory is 4-bit addressable, where the address specifies which register (out of 16) is being accessed for reading or writing.

***Write operation:***
A byte of data is written to specific register in RAM, where the location is determined by the address. Requires write enable ```lr_n``` signal as active (low) and the clock edge to occur.

***Read operation:*** 
Data can be read from a specific register in RAM determined by the input address. Requires chip enable ```ce_n``` signal as active (low). The data is output on the uio_out bus, and it is updated on the clock edge.

***Output:*** Data is presented on the uio_out line when the chip is enabled for reading, and high-impedance (Z) otherwise.

## How to test

To test, set the address and corresponding inputs to desired values. Clear ```lr_n``` for a read operation and ```ce_n``` for a write operation. Then pulse the clock to run signals.

The CocoTB testbenches located in the _test.py_ file, test various scenarios for the module. First, it tests a write operation to each address in the module followed by a read operation, to ensure correct behaviour. The script then iterates over each address setting ```ui_in```, ```lr_n``` and clearing ```ce_n``` for Read Mode while enabling RAM output. The recevied value from the read, located in ```uio_out``` is compared to the expected byte from that address. If there are any mismatches, an assertion error is raised, spcifying the faulty address and value.  

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any (add)
