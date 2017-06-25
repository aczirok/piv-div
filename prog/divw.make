../norm.file :  $(word 1, $(wildcard ../ORIG/*.png ) $(wildcard ../ORIG/*.jpg ))
	$(PROG)/piv-w-norm 0.9 $< >  $@


##################################### weighted div files ###################################
 
.PRECIOUS : ../div-w/%.div-w

../div-w/%.div-w : ../highpass2-median-div-piv0ref-ORIG/%.piv0.div ../piv0-w/%.piv0-w 
	mkdir -p ../div-w
	$(PROG)/weightedDiv.py -d $< -p $(word 2, $^) -o $@

####################################### png files ##########################################

.PRECIOUS : ../png-div-w/%.div-w.png

../png-div-w/%.div-w.png : ../div-w/%.div-w
	mkdir -p ../png-div-w
	$(PROG)/divergence-map-w.sh $< > $@

#################################### weighted piv file ####################################
.PRECIOUS : ../piv0-w/%.piv0-w


../piv0-w/%.piv0-w  :  ../piv0ref-ORIG/%.piv0   ../ORIG/%.jpg   ../ORIG/%.jpg  ../norm.file
	mkdir -p ../piv0-w
	$(PROG)/piv-w $+ >$@

../piv0-w/%.piv0-w  :  ../piv0ref-ORIG/%.piv0   ../ORIG/%.png   ../ORIG/%.png  ../norm.file
	mkdir -p ../piv0-w
	$(PROG)/piv-w $+ >$@

######################################### avg div-w ##########################################
ORIG_PIV = $(wildcard ../piv0ref-ORIG/*.piv0 )

../avg-w.div-w : ../avg-highpass2-median-div-piv0ref-ORIG.div $(patsubst ../piv0ref-ORIG/%.piv0, ../piv0-w/%.piv0-w, $(ORIG_PIV) )
	$(PROG)/weightedDiv.py -d $< -p $(word 2, $^) -o $@

################################ avg div-w + reversed contracting center ################################

../avg-w_rev.div-w : ../avg-w.div-w  ../reversed.txt
	$(PROG)/mergeReversedDivW.py -div $< -rev $(word 2, $^) > $@

####################################### avg png #############################################

../avg-w.div-w.png : ../avg-w_rev.div-w
	$(PROG)/divergence-map-w-overlay.sh $< ../ORIG/*00100.[jp][pn]g > $@

#############################################################################################

div-w : \
	$(patsubst ../piv0ref-ORIG/%.piv0, ../png-div-w/%.div-w.png, $(ORIG_PIV) ) \
	../avg-w.div-w.png
