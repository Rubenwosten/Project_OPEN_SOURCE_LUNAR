#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 4, #Terminals= 2, #Nets= 3,Area=3.12077e+08, HPWL= 50960 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:10370]

set yrange [-50:30290]

set label "X_M0" at 7740 , 7560 center 

set label "D" at 6880 , 14280


set label "G" at 6880 , 5880


set label "S" at 8600 , 7560


set label "X_M2" at 2580 , 7560 center 

set label "D" at 3440 , 14280


set label "G" at 3440 , 5880


set label "S" at 1720 , 7560


set label "X_M1" at 7740 , 22680 center 

set label "D" at 6880 , 15960


set label "G" at 6880 , 24360


set label "S" at 8600 , 22680


set label "X_M3" at 2580 , 22680 center 

set label "D" at 3440 , 15960


set label "G" at 3440 , 24360


set label "S" at 1720 , 22680


set label "VI" at 10320 , 5880 center                

set label "VO" at 0 , 14280 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M0 select 0 bsize 4
	5160	0
	5160	15120
	10320	15120
	10320	0
	5160	0

# block X_M2 select 0 bsize 4
	0	0
	0	15120
	5160	15120
	5160	0
	0	0

# block X_M1 select 0 bsize 4
	5160	15120
	5160	30240
	10320	30240
	10320	15120
	5160	15120

# block X_M3 select 0 bsize 4
	0	15120
	0	30240
	5160	30240
	5160	15120
	0	15120


EOF
	5680	14560
	5680	14000
	8080	14000
	8080	14560
	5680	14560

	5680	6160
	5680	5600
	8080	5600
	8080	6160
	5680	6160

	8320	13760
	8320	1360
	8880	1360
	8880	13760
	8320	13760

	4640	14560
	4640	14000
	2240	14000
	2240	14560
	4640	14560

	4640	6160
	4640	5600
	2240	5600
	2240	6160
	4640	6160

	2000	13760
	2000	1360
	1440	1360
	1440	13760
	2000	13760

	5680	15680
	5680	16240
	8080	16240
	8080	15680
	5680	15680

	5680	24080
	5680	24640
	8080	24640
	8080	24080
	5680	24080

	8320	16480
	8320	28880
	8880	28880
	8880	16480
	8320	16480

	4640	15680
	4640	16240
	2240	16240
	2240	15680
	4640	15680

	4640	24080
	4640	24640
	2240	24640
	2240	24080
	4640	24080

	2000	16480
	2000	28880
	1440	28880
	1440	16480
	2000	16480


EOF

	10320	5880
	10320	5880
	10320	5880
	10320	5880
	10320	5880

	0	14280
	0	14280
	0	14280
	0	14280
	0	14280

EOF

#Net: VM
	6880	14280
	3440	5880
	6880	14280

	6880	14280
	6880	15960
	6880	14280

	6880	14280
	3440	24360
	6880	14280


#Net: VI
	6880	5880
	6880	24360
	6880	5880

	6880	5880
	10320	5880
	6880	5880


#Net: VO
	3440	14280
	3440	15960
	3440	14280

	3440	14280
	0	14280
	3440	14280


EOF

pause -1 'Press any key'