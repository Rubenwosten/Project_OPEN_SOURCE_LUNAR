#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 2, #Terminals= 1, #Nets= 2,Area=4.68115e+08, HPWL= 56640 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:15530]

set yrange [-50:30290]

set label "X_XM1_XM2_XM4_XM5" at 10320 , 15120 center 

set label "VI" at 8600 , 5880


set label "VI" at 8600 , 24360


set label "VO" at 12040 , 14280


set label "VO" at 12040 , 15960


set label "S" at 6880 , 7560


set label "S" at 13760 , 7560


set label "S" at 6880 , 22680


set label "S" at 13760 , 22680


set label "X_XM3_XM6" at 2580 , 15120 center 

set label "I" at 3440 , 5880


set label "I" at 3440 , 24360


set label "ZN" at 3440 , 14280


set label "ZN" at 3440 , 15960


set label "S" at 1720 , 7560


set label "S" at 1720 , 22680


set label "OUT" at 0 , 14280 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_XM1_XM2_XM4_XM5 select 0 bsize 4
	5160	0
	5160	30240
	15480	30240
	15480	0
	5160	0

# block X_XM3_XM6 select 0 bsize 4
	0	0
	0	30240
	5160	30240
	5160	0
	0	0


EOF
	9800	5600
	9800	6160
	7400	6160
	7400	5600
	9800	5600

	9800	24080
	9800	24640
	7400	24640
	7400	24080
	9800	24080

	13240	14000
	13240	14560
	10840	14560
	10840	14000
	13240	14000

	13240	15680
	13240	16240
	10840	16240
	10840	15680
	13240	15680

	7160	1360
	7160	13760
	6600	13760
	6600	1360
	7160	1360

	14040	1360
	14040	13760
	13480	13760
	13480	1360
	14040	1360

	7160	16480
	7160	28880
	6600	28880
	6600	16480
	7160	16480

	14040	16480
	14040	28880
	13480	28880
	13480	16480
	14040	16480

	4640	5600
	4640	6160
	2240	6160
	2240	5600
	4640	5600

	4640	24080
	4640	24640
	2240	24640
	2240	24080
	4640	24080

	4640	14000
	4640	14560
	2240	14560
	2240	14000
	4640	14000

	4640	15680
	4640	16240
	2240	16240
	2240	15680
	4640	15680

	2000	1360
	2000	13760
	1440	13760
	1440	1360
	2000	1360

	2000	16480
	2000	28880
	1440	28880
	1440	16480
	2000	16480


EOF

	0	14280
	0	14280
	0	14280
	0	14280
	0	14280

EOF

#Net: OUT
	8600	5880
	3440	14280
	8600	5880

	8600	5880
	0	14280
	8600	5880


#Net: NET2
	12040	14280
	3440	5880
	12040	14280


EOF

pause -1 'Press any key'