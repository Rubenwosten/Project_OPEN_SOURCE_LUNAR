#Use this file as a script for gnuplot
#(See http://www.gnuplot.info/ for details)

set title" #Blocks= 2, #Terminals= 2, #Nets= 2,Area=1.56038e+08, HPWL= 26080 "

set nokey
#   Uncomment these two lines starting with "set"
#   to save an EPS file for inclusion into a latex document
# set terminal postscript eps color solid 20
# set output "result.eps"

#   Uncomment these two lines starting with "set"
#   to save a PS file for printing
# set terminal postscript portrait color solid 20
# set output "result.ps"


set xrange [-50:5210]

set yrange [-50:30290]

set label "X_M0" at 2580 , 7560 center 

set label "D" at 1720 , 14280


set label "G" at 1720 , 5880


set label "S" at 3440 , 7560


set label "X_M1" at 2580 , 22680 center 

set label "D" at 1720 , 15960


set label "G" at 1720 , 24360


set label "S" at 3440 , 22680


set label "ZN" at 0 , 14280 center                

set label "I" at 0 , 5880 center                

plot[:][:] '-' with lines linestyle 3, '-' with lines linestyle 7, '-' with lines linestyle 1, '-' with lines linestyle 0

# block X_M0 select 0 bsize 4
	0	0
	0	15120
	5160	15120
	5160	0
	0	0

# block X_M1 select 0 bsize 4
	0	15120
	0	30240
	5160	30240
	5160	15120
	0	15120


EOF
	520	14560
	520	14000
	2920	14000
	2920	14560
	520	14560

	520	6160
	520	5600
	2920	5600
	2920	6160
	520	6160

	3160	13760
	3160	1360
	3720	1360
	3720	13760
	3160	13760

	520	15680
	520	16240
	2920	16240
	2920	15680
	520	15680

	520	24080
	520	24640
	2920	24640
	2920	24080
	520	24080

	3160	16480
	3160	28880
	3720	28880
	3720	16480
	3160	16480


EOF

	0	14280
	0	14280
	0	14280
	0	14280
	0	14280

	0	5880
	0	5880
	0	5880
	0	5880
	0	5880

EOF

#Net: ZN
	1720	14280
	1720	15960
	1720	14280

	1720	14280
	0	14280
	1720	14280


#Net: I
	1720	5880
	1720	24360
	1720	5880

	1720	5880
	0	5880
	1720	5880


EOF

pause -1 'Press any key'