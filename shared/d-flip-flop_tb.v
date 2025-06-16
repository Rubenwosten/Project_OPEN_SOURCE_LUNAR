`timescale 1ns/1ps
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
$monitor("%0t: d_tb=%b clk_tb=%b q_tb=%b", $time, d_tb, clk_tb, q_tb);
#0 d_tb = 0;
#0 clk_tb = 1;
#5 clk_tb = 0;
#10 clk_tb = 1;
#10 clk_tb = 0;
end
endmodule