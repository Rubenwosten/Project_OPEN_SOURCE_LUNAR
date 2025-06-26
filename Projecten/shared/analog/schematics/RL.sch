v {xschem version=3.4.7RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -0 -50 110 -50 {lab=Vout}
N 60 -50 60 -40 {lab=Vout}
N 60 20 60 40 {lab=GND}
N -70 -50 -60 -50 {lab=VinL}
C {ipin.sym} -70 -50 0 0 {name=p1 lab=VinL}
C {opin.sym} 110 -50 0 0 {name=p2 lab=Vout
}
C {res.sym} 60 -10 0 0 {name=R1
value=1k
footprint=1206
device=resistor
m=1}
C {gnd.sym} 60 40 0 0 {name=l1 lab=GND}
C {res.sym} -30 -50 3 0 {name=R2
value=1k
footprint=1206
device=resistor
m=1}
