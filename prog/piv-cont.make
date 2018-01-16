stage2 : ../mean.png

stage4 : ../mean_ref.png ../fourier.png

../frame_vs_mean.txt : $(wildcard ../piv0-ORIG/*.piv0)
	cd ../piv0-ORIG	#to test that piv0-ORIG exists
	for i in $^;  do \
		j=$$(basename $$i .piv0) ; echo -n $${j##*[_-]} ; echo -n " " ;\
		$(PROG)/sum.py -i $$i; \
	done | grep -v nan | sort -g > $@

#timeseries needs timestamp file in the current directory
../mean.png : ../frame_vs_mean.txt
	cat $< | ( cd .. ; ../prog/plot_timeseries ) > $@

../ref : ../frame_vs_mean.txt
	$(PROG)/minserach.py -i $< > $@

../frame_vs_mean_ref.txt : $(wildcard ../piv0ref-ORIG/*.piv0)
	cd ../piv0ref-ORIG
	for i in $^; do \
		j=$$(basename $$i .piv0) ; echo -n $${j##*[_-]} ; echo -n " " ;\
		$(PROG)/sum.py -i $$i; \
	done | grep -v nan | sort -g > $@

../frame_vs_mean_ref_corr.txt : ../frame_vs_mean_ref.txt
	$(PROG)/piv0corr.py -i $< -p ../piv0ref-ORIG > $@

#timeseries needs timestamp file in the current directory
../mean_ref.png : ../frame_vs_mean_ref_corr.txt
	cat $< | ( cd ..; ../prog/plot_timeseries ) > $@

../frame_vs_mean_ref_corr.fourier : ../frame_vs_mean_ref_corr.txt
	$(PROG)/fourier.py -i $< > $@

../fourier.png : ../frame_vs_mean_ref_corr.fourier
	cat $< | gnuplot $(PROG)/fourier.gnu > $@
