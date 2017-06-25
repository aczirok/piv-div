//read image, return standard deviation as a PNM image
//
//standard deviation calculation according to 
//Kenong Wu et al 1995
//based on code from threshold.c
//
//compile:
//g++ imgstddev.cpp -o imgstddev -L/usr/X11R6/lib -lm -lpthread -lX11 -Wall


#include "CImg.h"
using namespace cimg_library;
#include <math.h>

#define XY (xs*y+x)
#define NONZERO nonzero == 1
int nonzero=1;
#define MASK masking == 1
int masking=0;

#include <unistd.h>					//getopt
extern	int	 getopt(int, char *const*, const char *);
extern	int	 optind;
extern	char	*optarg;

double mini (double a, double b){
	if (a > b) return (b);
	else return (a);
};

int Heavi0 (double x){
  if (x > 0) 	 return (1);
  else if (x==0) return (0);
  else 		 return (0);
};

void stddev (
	cimg_library::CImg<unsigned char> in, 
	int Msize) 
{
//the algorithm is modified: pixels with zero value do not count
  
  int x, y, xs, ys, SS;
  int Wsize=Msize*2+1;
  double WindCorr;		
  int *Cn,*Rn,*D;		//to get # of non-zero pixels
  double *In,*A,*B,*Cs,*Cp,*Rs,*Rp,*szoras,q;

  xs=in.dimx(); ys=in.dimy(); SS=xs*ys;

  CImg<unsigned char> out(xs,ys);	//the output image
  
  In=(double*)calloc(SS,sizeof(double));
  A=(double*)calloc(SS,sizeof(double));
  B=(double*)calloc(SS,sizeof(double));
  D=(int*)calloc(SS,sizeof(int));	//for the # of non-zero pixels
  Cs=(double*)calloc(SS,sizeof(double));
  Cp=(double*)calloc(SS,sizeof(double));
  Cn=(int*)calloc(SS,sizeof(int));	//for the # of non-zero pixels
  Rs=(double*)calloc(SS,sizeof(double));
  Rp=(double*)calloc(SS,sizeof(double));
  Rn=(int*)calloc(SS,sizeof(int));	//for the # of non-zero pixels
  szoras=(double*)calloc(SS,sizeof(double));

  for (x=0;x<SS;x++) In[x]=((double)(in[x]))*((double)(in[x])); 	//I=i^2
  for(x=0;x<xs;x++) {				//calculate Cs[xy], Cp[xy]
	Cs[Msize*xs+x]=0;			//and Cn[xy]
	Cp[Msize*xs+x]=0;
	Cn[Msize*xs+x]=0;
	for (y=0;y<Wsize;y++) {
		Cs[Msize*xs+x]+=In[XY];
		Cp[Msize*xs+x]+=(double)(in[XY]);
		Cn[Msize*xs+x]+=Heavi0((double)(in[XY]));
	}
	for (y=Msize+1;y<ys-Msize;y++) {
		Cs[XY]=Cs[XY-xs]+In[XY+Msize*xs]-In[XY-(Msize+1)*xs];
		Cp[XY]=Cp[XY-xs]+(double)(in[XY+Msize*xs])-(double)(in[XY-(Msize+1)*xs]);
		Cn[XY]=Cn[XY-xs]+Heavi0((double)(in[XY+Msize*xs]))-Heavi0((double)(in[XY-(Msize+1)*xs]));
	}
  } 

  for(y=0;y<ys;y++) {				//calculate Rs[xy], Rp[xy]
	Rs[y*xs+Msize]=0;			//and Rn[xy]
	Rp[y*xs+Msize]=0;
	Rn[y*xs+Msize]=0;
	for (x=0;x<Wsize;x++) {
		Rs[y*xs+Msize]+=In[XY];
		Rp[y*xs+Msize]+=(double)(in[XY]);
		Rn[y*xs+Msize]+=Heavi0((double)(in[XY]));
	}
  } 

  A[Msize*xs+Msize]=0;				//calculate initial A, B
  B[Msize*xs+Msize]=0;				//and initial D from Cn...
  D[Msize*xs+Msize]=0;
  for(x=0;x<Wsize;x++) {
	A[Msize*xs+Msize]+=Cs[Msize*xs+x];
	B[Msize*xs+Msize]+=Cp[Msize*xs+x];
  	D[Msize*xs+Msize]+=Cn[Msize*xs+x];
  } 

  for(x=Msize+1;x<xs-Msize;x++){		//calculate first row of A,B
  	A[x+Msize*xs]=
		A[x-1+Msize*xs]-Cs[x-Msize-1+Msize*xs]+Cs[x+Msize+Msize*xs];
	B[x+Msize*xs]=
		B[x-1+Msize*xs]-Cp[x-Msize-1+Msize*xs]+Cp[x+Msize+Msize*xs];
  	D[x+Msize*xs]=
		D[x-1+Msize*xs]-Cn[x-Msize-1+Msize*xs]+Cn[x+Msize+Msize*xs];
  } 
	
  
  for(y=Msize+1;y<ys-Msize;y++){		//calculate A[xy], B[xy]
	A[y*xs+Msize]=
	    A[(y-1)*xs+Msize]-Rs[Msize+(y-Msize-1)*xs]+Rs[Msize+(y+Msize)*xs];
	B[y*xs+Msize]=
	    B[(y-1)*xs+Msize]-Rp[Msize+(y-Msize-1)*xs]+Rp[Msize+(y+Msize)*xs];
	D[y*xs+Msize]=
	    D[(y-1)*xs+Msize]-Rn[Msize+(y-Msize-1)*xs]+Rn[Msize+(y+Msize)*xs];
	for(x=Msize+1;x<xs-Msize;x++){
	    A[XY]=A[x-1+y*xs]-Cs[x-Msize-1+y*xs]+Cs[x+Msize+y*xs];
	    B[XY]=B[x-1+y*xs]-Cp[x-Msize-1+y*xs]+Cp[x+Msize+y*xs];
	    D[XY]=D[x-1+y*xs]-Cn[x-Msize-1+y*xs]+Cn[x+Msize+y*xs];
	}
  }

  if (NONZERO){ 	//only the non-zero pixels count
    for(x=Msize;x<xs-Msize-3;x++)
      for(y=Msize+1;y<ys-Msize;y++) {
	if (D[XY] > 0) { 
		WindCorr=1/(double)(D[XY]);	//the # of non-zero pixels
		q=WindCorr*(A[XY]-WindCorr*B[XY]*B[XY]);
	} else { q = 0; };	//no valid points in neighborhood
	if (q>=0) szoras[XY]=sqrt(q); else szoras[XY]=0;
      }
  } else {
    WindCorr=(1.0/(Wsize*Wsize));
    for(x=Msize;x<xs-Msize-3;x++)
      for(y=Msize+1;y<ys-Msize;y++) {
        q=WindCorr*(A[XY]-WindCorr*B[XY]*B[XY]);
        if (q>=0) szoras[XY]=sqrt(q); else szoras[XY]=0;
      }
  };
  
  for (x=0;x<SS;x++) {
  	if (MASK && in[x]==0) {}
	else   out[x]=(unsigned char)(mini(szoras[x],255.0));
  }
  out.save_pnm ("/dev/stdout");		//save output image

  free(In);
  free(A);
  free(B);
  free(D);
  free(Cs);
  free(Cp);
  free(Cn);
  free(Rs);
  free(Rp);
  free(Rn);
  free(szoras);		
}

void usage(void) {
	fprintf(stderr,"\
options: \n\
	-f imagefile		: input file name \n\
	-w sttdev_window	: window size (half-length)\n\
	-n 			: turns on all pixels in the calculation\n\
				  (non-zero and zero pixels as well)\n\
	-m			: masking, output only, where the original\n\
				  image is non-zero\n\
output :  on stdout, pnm format\n");
	exit(1);
}

int main(int argn, char **argstr) {
    	int		option;
	int 	ww=10;				//stddev window size
	int 	dum=0;
	char	filename[200];

	while ((option = getopt(argn, argstr, "f:w:nm")) != EOF) 
	{
		switch ((char)option) 
		{
			case 'f' :
				sprintf(filename,"%s",optarg);
				dum=1;
				break;
			case 'w' :							//stddev window size
				ww=atoi(optarg);
				break;
			case 'n' :		//use all pixels
				nonzero = 0;
				break;
			case 'm' :		//mask output
				masking = 1;
				break;
			default:
				usage();
		}
	}
	if (dum == 0) usage ();
	CImg<unsigned char> in_img(filename);
	stddev(in_img, ww);

	return (0);

}
