`timescale 1ns / 1ps
module inverter_tb;
reg a_tb;
wire y_tb;
inverter dut (
    .a(a_tb),
    .y(y_tb)
);
initial begin
$dumpfile("inverter_tb.vcd");
$dumpvars(0, inverter_tb);
$monitor("%0t: y_tb=%b", $time, y_tb);
simulation_lines_placeholder
end
endmodule