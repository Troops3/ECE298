`default_nettype none

module tt_um_dff_mem (
    input  wire [7:0] ui_in,    // Dedicated inputs - connected to the input switches
    output reg  [7:0] uo_out,   // Dedicated outputs - connected to the 7 segment display
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  //parameters to define the size of the memory (16 bytes)
  localparam RAM_BYTES = 16;  
  localparam addr_bits = $clog2(RAM_BYTES);    //number of address bits is log2(ram size)
    
  assign uio_oe = 8'h00;     //assign all bidirectional pins as outputs
  assign uio_out = 8'b0;
    
  wire [addr_bits-1:0] addr = ui_in[addr_bits-1:0];
  wire lr_n = ui_in[7];  // lr_n signal (active low)
  wire ce_n = ui_in[6];  // ce_n signal (active low)

  //Declare register memory as a 2d array consisting of 16 words of 8 bits
  reg [7:0] RAM[RAM_BYTES - 1:0];

  // If ce_n is low (active), output ram at addr and output 
  assign uo_out = (!ce_n) ? RAM[addr] : 8'bZ;  
    
  //positive edge enabled
  always @(posedge clk) begin
    if (!rst_n) begin
        integer i;
      for (i = 0; i < RAM_BYTES; i++) begin
        RAM[i] <= 8'b0;  // Reset RAM contents
      end
    end else if (!lr_n) begin
    // Load data into RAM when lr_n is low
        RAM[addr] <= uio_in;
    end
  end

endmodule  // tt_um_dff_mem
