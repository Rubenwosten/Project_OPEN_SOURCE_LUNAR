* NGSPICE file created from RING_0.ext - technology: sky130A

.SUBCKT RING VDD GND out

XM1 net1 out GND GND sky130_fd_pr__nfet_01v8 L=150e-9 w=21e-7 nf=2
XM2 net2 net1 GND GND sky130_fd_pr__nfet_01v8 L=150e-9 w=21e-7 nf=2
XM3 out net2 GND GND sky130_fd_pr__nfet_01v8 L=150e-9 w=21e-7 nf=2
XM4 net1 out VDD VDD sky130_fd_pr__pfet_01v8 L=150e-9 w=21e-7 nf=2
XM5 net2 net1 VDD VDD sky130_fd_pr__pfet_01v8 L=150e-9 w=21e-7 nf=2
XM6 out net2 VDD VDD sky130_fd_pr__pfet_01v8 L=150e-9 w=21e-7 nf=2
.ends