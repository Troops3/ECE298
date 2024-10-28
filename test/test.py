import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# Define control signals
LR_N = 1 << 7  # Bit 7 for lr_n (active low)
CE_N = 1 << 6  # Bit 6 for ce_n (active low)

@cocotb.test()
async def test_ram(dut):
    dut._log.info("Start")

    # Initialize clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = LR_N | CE_N  # Set lr_n and ce_n high (inactive)
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # All bidirectional ports are inputs at reset
    assert int(dut.uio_oe.value) == 0

    # Write 4 bytes to addresses 8, 9, 10, 11
    dut._log.info("write 4 bytes to addresses 8, 9, 10, 11")

    # Write to address 8
    dut.ui_in.value = CE_N | 8       # lr_n=0 (write), ce_n=1 (inactive), address=8
    dut.uio_in.value = 0x55
    await ClockCycles(dut.clk, 1)

    # Write to address 9
    dut.ui_in.value = CE_N | 9       # lr_n=0 (write), ce_n=1 (inactive), address=9
    dut.uio_in.value = 0x66
    await ClockCycles(dut.clk, 1)

    # Write to address 10
    dut.ui_in.value = CE_N | 10      # lr_n=0 (write), ce_n=1 (inactive), address=10
    dut.uio_in.value = 0x77
    await ClockCycles(dut.clk, 1)

    # Write to address 11
    dut.ui_in.value = CE_N | 11      # lr_n=0 (write), ce_n=1 (inactive), address=11
    dut.uio_in.value = 0x88
    await ClockCycles(dut.clk, 1)

    # Read back the bytes and verify they are correct
    dut._log.info("read back the bytes and verify they are correct")
    dut.uio_in.value = 0  # Not used during read

    # Read from address 8
    dut.ui_in.value = LR_N | 8       # lr_n=1 (read), ce_n=0 (active), address=8
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x55

    # Read from address 9
    dut.ui_in.value = LR_N | 9       # lr_n=1 (read), ce_n=0 (active), address=9
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x66

    # Read from address 10
    dut.ui_in.value = LR_N | 10      # lr_n=1 (read), ce_n=0 (active), address=10
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x77

    # Read from address 11
    dut.ui_in.value = LR_N | 11      # lr_n=1 (read), ce_n=0 (active), address=11
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x88

    # Write a byte at address 12
    dut._log.info("write a byte at address 12")
    dut.ui_in.value = CE_N | 12      # lr_n=0 (write), ce_n=1 (inactive), address=12
    dut.uio_in.value = 0x99
    await ClockCycles(dut.clk, 1)

    # Overwrite the byte at address 10
    dut._log.info("overwrite the byte at address 10")
    dut.ui_in.value = CE_N | 10      # lr_n=0 (write), ce_n=1 (inactive), address=10
    dut.uio_in.value = 0xAA
    await ClockCycles(dut.clk, 1)

    # Read back the bytes and verify they are correct
    dut._log.info("read back the bytes and verify they are correct")

    # Read from address 12
    dut.ui_in.value = LR_N | 12      # lr_n=1 (read), ce_n=0 (active), address=12
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x99

    # Read from address 10
    dut.ui_in.value = LR_N | 10      # lr_n=1 (read), ce_n=0 (active), address=10
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0xAA

    # Read from address 8
    dut.ui_in.value = LR_N | 8       # lr_n=1 (read), ce_n=0 (active), address=8
    await ClockCycles(dut.clk, 2)
    assert int(dut.uio_out.value) == 0x55

    # Reset again
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Ensure that the memory is cleared
    for i in range(16):  # RAM size is now 16 bytes
        dut.ui_in.value = LR_N | i   # lr_n=1 (read), ce_n=0 (active), address=i
        await ClockCycles(dut.clk, 2)
        assert int(dut.uio_out.value) == 0

    dut._log.info("all good!")
