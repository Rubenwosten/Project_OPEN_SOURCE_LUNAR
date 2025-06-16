`timescale 1ns / 1ps
module d-flip-flop_tb;
reg d_tb;
reg clk_tb;
wire q_tb;
d-flip-flop dut (
    .d(d_tb),
    .clk(clk_tb),
    .q(q_tb)
);
initial begin
$dumpfile("d-flip-flop_tb.vcd");
$dumpvars(0, d-flip-flop_tb);
$monitor("%0t: d_tb=%b clk_tb=%b q_tb=%b", $time, d_tb, clk_tb, q_tb);
simulation_lines_placeholder
end
endmodule