import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# Define control signals
LR_N = 1 << 7  # Bit 7 for lr_n (active low)
CE_N = 1 << 6  # Bit 6 for ce_n (active low)

@cocotb.test()
async def test_write_read_all_addresses(dut):
    dut._log.info("Start test for writing to all addresses and verifying each read")

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

    # Write a unique byte to each address
    dut._log.info("Writing a unique byte to each address in RAM")
    for address in range(16):
        dut.ui_in.value = address  # Specify address with ce_n inactive
        dut.uio_in.value = address * 0x11  # Unique byte for each address (0x00, 0x11, 0x22, ...)
        dut.ui_in.value = address | CE_N   # Activate lr_n low to write
        await ClockCycles(dut.clk, 1)
        dut.ui_in.value = LR_N | CE_N  # Deactivate lr_n and ce_n (inactive)

    # Read back each byte and verify correctness
    dut._log.info("Reading back each address and verifying data")
    for address in range(16):
        dut.ui_in.value = address | CE_N  # Set lr_n=1 (read), ce_n=0 (active), specify address
        await ClockCycles(dut.clk, 1)  # Single-cycle delay to read
        expected_value = address * 0x11
        assert int(dut.uio_out.value) == expected_value, f"Readback error at address {address}: expected {expected_value}, got {int(dut.uio_out.value)}"

    dut._log.info("All addresses verified successfully!")
