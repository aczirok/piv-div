# piv-div

This code is used to extract divergence/convergence measures from optical flow
data.

### SETUP ###

* Dependency: 
  * Python 2.7

### USAGE ###
* for test data, download the datasets posted at http://osf.io/2w63u
  * example.zip will extract into the example folder, containing
    * ORIG: the original image sequence
    * piv0-ORIG: optical flow (PIV) data calculated from two consecutive frames. Each file contains lines in the format x y dx dy. The x y values form a grid, dx and dy is the estimated displacement at that point between two consecutive image.
    * piv0ref-ORIG: similar to piv0-ORIG, but here the displacement values are calculated relative to a certain reference frame
    * ref: reference frame number
    * cbrange.txt: divergence range used for plotting
    * makefiles: makefiles and scripts used for the analysis. The makefiles are distributed in the prog folder in this repository. A usual sequence of make targets is listed in run.sh:
```
make -k stage2
make -k stage4
make -k div median highpass2 reversed
make -k div-w
```

  * example_expected.zip will extract into the example_expected folder. This is the expected output after running example/makefiles/run.sh. The folder contains (in addition to the ones in example):
  
    * div-piv0ref-ORIG: folder containing the divergence field calculated from each optical flow field. Each file contains lines with x y divergence.
    * median-div-piv0ref-ORIG, highpass2-median-div-piv0ref-ORIG: filtered versions of the above divergence data
    * png-highpass2-median-div-piv0ref-ORIG: visualized filtered divergence data
    * avg-highpass2-median-div-piv0ref-ORIG.div: time-averaged filtered divergence data
    * avg-highpass2-median-div-piv0ref-ORIG.div.png: visualization of the above data file
    * piv0-w: contrast weighted optical flow data. Each file containes lines in the format x y dx dy weight, where x y is the location, dx and dy is the estimated displacement, and 0<weight<~1 is the reliability assigned to that particular displacement value.
    * avg-w_rev.div-w time-averaged, contrast weighted and filtered divergence data
    * avg-w.div-w.png: visualization of the above
    * frame_vs_mean.txt: spatial average displacement for each frame, calculated from consecutive images
    * frame_vs_mean_ref.txt: beat pattern: spatial average displacement for each frame, calculated with a single reference image 
    * frame_vs_mean_ref_corr.txt: phase corrected beat pattern (different only if the reference frame is in a contraction peak instead of being within the resting state)
    
### FILES ###

* Makefiles:
  * piv-cont.make - directives to calculate the beat pattern from consecutive images
  * path.make - directives about the location of the prog folder
  * div.make - directives to calculate the divergence from the image sequence
  * divw.make - directives to calculate contrast-weighted divergences 

* Bash scripts:
  * divergence-map.sh - visualize  divergence data as an image
  * divergence-map-w.sh - visualize contrast-weighted divergence data as an image
  * divergence-map-w-overlay.sh - visualize contrast-weighted divergence data superimposed on one of the original image
  * piv-w - assign weights to PIV data based on the local standard deviation of the images used to calculate the PIV data
  * piv-w-norm - calculate the weight of each pixel
  * plot_timeseries - generates the beat pattern graph. If exact timestamps / framerates are not given, a 10 fps (frame per second) frame rate is assumed.

* Python scripts:
  * sum.py - Calculates the average displacement from a field of PIV displacements.
  * piv0corr.py - Baseline correction. Estimates displacements using each minima of the piv0 files as a reference state. Calculations usually are limited only to the first 500 frames
  * divergence.py - Calculates divergence from a file containing the PIV displacement data.
  * weightedDiv.py - Adds weight to divergence data
  * pixlist.py - Calculates the list of all pixels, for the "piv-w" bash script.
  * filter.py - Filters divergence files to reduce noise. Possible choices: median, highpass, stdev, avg, search for reversed pixels.
  * mergeReversedDivW.py - Correction of reversed divergence. An area can beat off phase and this file will detect and correct that.

* Gnuplot Visualization:
  * mean.gnu - Generates a beat pattern graph if exact timestamps are not given for each image. A 10 fps (frame per second) frame rate is assumed.



