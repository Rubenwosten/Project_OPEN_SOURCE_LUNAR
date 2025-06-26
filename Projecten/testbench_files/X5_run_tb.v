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
#0 a_tb = 0;
#2.38 a_tb = 1;
#4.79 a_tb = 0;
#6.0 a_tb = 1;
#4.0 a_tb = 0;
#6.0 a_tb = 1;
#4.0 a_tb = 0;
#6.0 a_tb = 1;
#4.0 a_tb = 0;
#6.0 a_tb = 1;
#4.0 a_tb = 0;
end
endmodule
