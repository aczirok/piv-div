SCALE=${3:-5}	# $3, if exist, otherwise 5
XS=$(identify $2 | tr "x" " " | cut -d" " -f3 )
YS=$(identify $2 | tr "x" " " | cut -d" " -f4 )
t=$(mktemp)
t2=$(mktemp)

# weighted files have 4 columns, others have only 3
col=$(head -1 $1 | wc -w)
w=1.0
if [ $col -eq 4 ]
then w=\$4
fi

if [ -e ../cbrange.txt ]
then SCALE=$(cat ../cbrange.txt)
fi

gnuplot <<EOI  > $t
    xs=$XS
    ys=$YS
	set t pngcairo enhanced font ",16" size xs,ys
	unset key
	set size ratio -1     
	set view map
	set cbrange [-${SCALE}:${SCALE}]
	set xrange [0:xs]
	set yrange [0:ys] reverse
	set lmargin at screen 0
	set rmargin at screen 1
	set tmargin at screen 1
	set bmargin at screen 0
	unset xtics
	unset ytics
	set palette defined (-1 "#00008B", 0 "blue",33 "#00ffff",50 "white",66 "yellow",100 "red",101 "#8B0000")
	f(x)=1/(1+exp(-10*(x-0.5)))
	print "$1"
	sp "$1"  using 1:2:(\$3*f($w)) with points palette pointsize 2 pointtype 5
EOI
composite -blend 50 $t $2 png:$t2
cat $t2
rm $t $t2

