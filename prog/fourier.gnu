set t pngcairo enhanced font "Arial,25" linewidth 2.5 size 1400,600
set style data linespoint
unset key
set size 0.5,1
#set xtics ("0" 0, "1/2" 0.05, "1/1" 0.1, "1/0.66" 0.15, "1/0.5" 0.2)
set xtics ("0" 0, "0.5" 0.5, "1" 1, "1.5" 1.5, "2" 2)
#set xtics ("0" 0, "1/10" 0.1, "1/5" 0.2, "3/10" 0.3, "2/5" 0.4, "1/2" 0.5)
#set xtics ("0" 0, "30" 30, "60" 60, "90" 90, "120" 120)
spf=`/mnt/data/meas/motil/C103_high_frame/prog/framerate.py -i ../timestamp.txt 2> /dev/null || cat ../framerate.txt 2> /dev/null || echo 0.1`

# we create a temporary file in /tmp; redirect the stdin and return the name of the file to gnuplot
tmp =  "`q=$(tempfile --prefix fourier); cat > $q; echo $q`" 

set xlabel font "Arial,40"
set ylabel font "Arial,40"

set multiplot

set origin 0,0
#set xlabel "frequency [bpm]"
set xlabel "frequency [bps]"
set ylabel "relative power"
#set xrange [0:4]
set xrange [0:2]
#set xrange [0:120]
set yrange [0:.5]
#set yrange [0:0.3]
set ytics ("0" 0, "0.1" 0.1, "0.2" 0.2, "0.3" 0.3, "0.4" 0.4, "0.5" 0.5)
plot tmp u ($1/spf):2 w linespoints pt 4 ps 0.8 lt 1 lw 2 

set origin 0.5,0
#set xrange [0:4]
set xrange [0:2]
#set xrange [0:120]
#set xlabel "frequency [bpm]"
set xlabel "frequency [bps]"
set ylabel "log (relative power)"
#set logscale 
set yrange [-5:0]
set ytics ("0" 0, "-1" -1, "-2" -2, "-3" -3, "-4" -4, "-5" -5)
plot tmp u ($1/spf):( log10($2)) w linespoints pt 4 ps 0.8 lt 1 lw 2

unset multiplot

