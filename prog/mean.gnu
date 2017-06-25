
set term pngcairo enhanced font ",16" size 1400,640
set style data linespoint
unset key

# we create a temporary file in /tmp; redirect the stdin and return the name of the file to gnuplot
tmp =  "`q=$(tempfile --prefix beatpattern); awk '{if ($2>0) {print} else {print $1, old;}; old=$2;}' > $q; echo $q`"
#spf = 0.1
spf=`cat framerate.txt 2> /dev/null || echo 0.1`

if (spf==0.033) {
	set term pngcairo enhanced font ",16" size 650,640
	set xlabel "sec"
	set xtics nomirror
    set x2tics nomirror
	set x2label "frames" offset 0, screen -0.17
	set xrange [0:10]
	set x2range [0:10/spf]
	#set yrange [:1.0]
	p tmp u 1:($2 > 0 ? $2 : NaN)  w linespoints pt 7 ps 0.3 axes x2y1

} else {
	set xlabel "sec" offset 0, screen 0.02
	set xtics nomirror
	set x2tics nomirror
	set x2label "frames" offset 0, screen -0.17
	set size 0.5,1
	
	set multiplot
	
	set origin 0,0
	set xrange [0:10]
	set x2range [0:10/spf]
	#set yrange [:1.0]
	p tmp u 1:($2 > 0 ? $2 : NaN)  w linespoints pt 7 ps 0.3 axes x2y1
	
	set origin 0.5,0
	set xrange [0:50]
	set x2range [0:50/spf]
	#set yrange [:1.0]
	p tmp u 1:($2 > 0 ? $2 : NaN) w linespoints pt 7 ps 0.3 axes x2y1
	
	unset multiplot
}

