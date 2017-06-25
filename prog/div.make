piv0ref = $(wildcard ../piv0ref-ORIG/*.piv0 )

.PRECIOUS : ../div-piv0-ORIG/%.piv0.div \
	../div-piv0ref-ORIG/%.piv0.div \
	../median-div-piv0ref-ORIG/%.piv0.div \
	../reversed.txt \
	../highpass-median-div-piv0ref-ORIG/%.piv0.div

div_files = $(patsubst ../piv0ref-ORIG/%.piv0,../div-piv0ref-ORIG/%.piv0.div, $(piv0ref) ) 

div : $(div_files)

../div-piv0ref-ORIG/%.piv0.div : ../piv0ref-ORIG/%.piv0
	mkdir -p $$(dirname $@) 
	$(PROG)/divergence.py -i $< > $@

##################### reversed beating center filter #####################

reversed : ../reversed.txt

../reversed.txt : $(piv0ref)  
	@ ls $^ | $(PROG)/filter.py -r > $@

##################### median filter #####################

median_files = $(patsubst ../piv0ref-ORIG/%.piv0,../median-div-piv0ref-ORIG/%.piv0.div, $(piv0ref) ) 

.INTERMEDIATE : $(median_files) 

median : $(median_files) $(patsubst ../%,../png-%.png, $(median_files) ) $(patsubst ../%,../png-%.png, $(median_files) )

../median-div-piv0ref-ORIG/%.piv0.div : ../div-piv0ref-ORIG/%.piv0.div
	mkdir -p ../median-div-piv0ref-ORIG
	@ ls $< | $(PROG)/filter.py -t median > $@

##################### highpass filter #####################

highpass_files = $(patsubst ../piv0ref-ORIG/%.piv0,../highpass-median-div-piv0ref-ORIG/%.piv0.div, $(piv0ref) ) 

highpass : $(highpass_files) $(patsubst ../%,../png-%.png, $(highpass_files) )

###multiple output files: highpass-median....div : median...div
###see http://stackoverflow.com/questions/2973445/gnu-makefile-rule-generating-a-few-targets-from-a-single-source-file

$(highpass_files) : highpass.intermediate

.INTERMEDIATE: highpass.intermediate
highpass.intermediate : $(median_files)
	[ "$<" ] || exit 1
	@ ls $^ | $(PROG)/filter.py -t highpass -d ../highpass-median-div-piv0ref-ORIG

##################### highpass2 filter #####################

highpass2_files = $(patsubst ../piv0ref-ORIG/%.piv0,../highpass2-median-div-piv0ref-ORIG/%.piv0.div, $(piv0ref) ) 

highpass2 : $(highpass2_files) \
	$(patsubst ../%,../png-%.png, $(highpass2_files) ) \
	../avg-highpass2-median-div-piv0ref-ORIG.div.png

###multiple output files: highpass2-median....div : median...div
###see http://stackoverflow.com/questions/2973445/gnu-makefile-rule-generating-a-few-targets-from-a-single-source-file

$(highpass2_files) : highpass2.intermediate

.INTERMEDIATE: highpass2.intermediate
highpass2.intermediate : $(median_files)
	[ "$<" ] || exit 1
	ls $^ | $(PROG)/filter.py -t highpass2 -d ../highpass2-median-div-piv0ref-ORIG

../avg-highpass2-median-div-piv0ref-ORIG.div : $(highpass2_files)
	[ "$<" ] || exit 1
	ls $^ | $(PROG)/filter.py -t avg > $@

../avg-highpass2-median-div-piv0ref-ORIG.div.png : ../avg-highpass2-median-div-piv0ref-ORIG.div 
	 $(PROG)/divergence-map.sh $< > $@

###################### visualization ##################

../png-%.div.png : ../%.div
	mkdir -p $$(dirname $@) 
	 $(PROG)/divergence-map.sh $< > $@

png-div-piv0-ORIG : $(patsubst ../piv0-ORIG/%.piv0,../png-div-piv0-ORIG/%.piv0.div.png, $(wildcard ../piv0-ORIG/*.piv0 ) )

png-div-piv0ref-ORIG : $(patsubst ../piv0ref-ORIG/%.piv0,../png-div-piv0ref-ORIG/%.piv0.div.png, $(piv0ref) )

png-median-div-piv0ref-ORIG : $(patsubst ../%,../png-%.png, $(median_files) )