SCALE=${2:-5}
if [ -e ../cbrange.txt ] 
then SCALE=$(cat ../cbrange.txt)
fi

gnuplot <<EOI
	set t pngcairo enhanced font ",16" size 640,480
	unset key
	set size ratio -1     
	set view map
	set cbrange [-${SCALE}:${SCALE}]
	set yrange [:] reverse
	set palette defined (-1 "#00008B", 0 "blue",33 "#00ffff",50 "white",66 "yellow",100 "red",101 "#8B0000")
	sp "$1"  using 1:2:3 with points palette pointsize 1 pointtype 5
EOI
