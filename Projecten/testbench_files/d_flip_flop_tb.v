`timescale 1ns / 1ps
module d_flip_flop_tb;
reg d_tb;
reg clk_tb;
wire q_tb;
d_flip_flop dut (
    .d(d_tb),
    .clk(clk_tb),
    .q(q_tb)
);
initial begin
$dumpfile("d_flip_flop_tb.vcd");
$dumpvars(0, d_flip_flop_tb);
$monitor("%0t: q_tb=%b", $time, q_tb);
simulation_lines_placeholder
end
endmodule