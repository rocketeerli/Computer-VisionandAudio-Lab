#include "stdafx.h"
#include "math.h"
#include "mfcc.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif
 
MFCC::MFCC()
{
	InitFilt();
}
MFCC::~MFCC()
{

}

//======================================================
void MFCC::InitFilt()
{
_int16 i,j;
float Freq;
_int16 FiltFreq[FiltNum+1]={0,100,200,300,400,500,600,700,800,900,1000,
		  1149,1320,1516,1741,2000,2297,2639,3031,3482,4000,
		  4595,5278,6063,6964,8001};
_int16 BW[FiltNum+1]={100,100,100,100,100,100,100,100,100,100,124,
		       160,184,211,242,278,320,367,422,484,556,
		       639,734,843,969,1112};

for(i=0;i<=FFTLen/2;i++)
	{
	Freq=FS*1000.0F*(float)(i)/(float)(FFTLen);
	for(j=0;j<FiltNum;j++)
		{
		if(Freq>=(float)FiltFreq[j] && Freq<=(float)FiltFreq[j+1])
			{
			Num[i]=j;
			if(j == 0)
				FiltCoe1[i]=0.0F;
			else
				FiltCoe1[i]=((float)(FiltFreq[j]+BW[j])-Freq)/(float)(BW[j]);

			FiltCoe2[i]=(Freq-(float)(FiltFreq[j+1]-BW[j+1]))/(float)(BW[j+1]);
			FiltCoe1[i]=FiltCoe1[i]*FiltCoe1[i];
			FiltCoe2[i]=FiltCoe2[i]*FiltCoe2[i];
			break;
			}
		}
	}
}
//==========================================================
/*              Get energy from triangle filter                                             */
/*    spdata[]  :speech signal                                                    */
/*    FiltCoe1[]:plus K of filter coefficients                                    */
/*    FiltCoe2[]:minus K of filter coefficients                                   */
/*    Num[]     :decide the filter that one point belongs                         */
/*    En[]      :output energy after speech signal is filted by triangle filters  */

_int16 MFCC::CFilt(float *spdata,float *En)
{
float real[FFTLen+1],imgi[FFTLen+1],temp;
_int16 id,id1,id2;

for(id=0;id<FFTLen;id++)
	{
	if(id<FRAMEL)
		real[id+1]=spdata[id];
	else
		real[id+1]=0.0F;
	imgi[id+1]=0.0F;
	}
fft(real,imgi,0);

for(id=0;id<=FiltNum;id++)
	En[id]=0.0F;
for(id=0;id<=FFTLen/2;id++)
	{
	temp=real[id+1]*real[id+1]+imgi[id+1]*imgi[id+1];
	id1=Num[id];
	id2=id1+1;
	En[id1]=En[id1]+FiltCoe1[id]*temp;
	En[id2]=En[id2]+FiltCoe2[id]*temp;
	}

for(id=1;id<=FiltNum;id++)
	{
	if(En[id] == 0)
		return(-1);
	else
		En[id]=log(En[id]);
	}
return(0);
}

/*              get mel_frequency cepstrum                                 */
/*                                                                         */
/*    En[]  : energy after speech signal is filted by the triangle filters */
/*    Cep[] : cepstrum coefficent                                          */
/*    Ceplen: lengthen of cepstrum coefficent                              */
//==========================================================
void MFCC::GetVector(float *data,float *Cep)
{
_int16 idcep,iden;
float En[FiltNum+1];
CFilt(data,En);
for(idcep=0;idcep<PCEP;idcep++)
	{
	Cep[idcep]=0.0F;
	for(iden=1;iden<=FiltNum;iden++)
		{
		Cep[idcep]=Cep[idcep]+En[iden]*cos((idcep+1)*(iden-0.5F)*PI/(FiltNum));
		}
	Cep[idcep]=Cep[idcep]/10.0F;
	}
}
 void GetFeature(short *RdBuf, float *Cep,int len)
 {
 	int j;
 	double data[Frame];
 	for(j=1;j<len/2;j++)
		data[j]=(double)RdBuf[j]-0.93*(double)RdBuf[j-1];
	
	for(j=len/2;j<Frame;j++)
		data[j]=0.0;
	data[0]=(double)RdBuf[0];
	MultiHamming(data);
	GetVector(data,Cep);
}


void MultiHamming(double *data)
{
	double twopi;
	double Hamming[Frame];
	twopi=8.0F*atan(1.0F);
	for(int i=0;i<Frame;i++)
	{
		Hamming[i]=(double)(0.54-0.46*cos((double)i*twopi/(double)(Frame-1)));
		 data[i]*=Hamming[i];
    } 
	twopi=0.0;
}

}
//
//=================================================================
void MFCC::fft(float *xr,float *xi,_int16 inv)
{
_int16 m,nv2,i,j,nm1,k,l,le1,ip,n=FFTLen;
float tr,ti,ur,ui,wr,wi,ur1,ui1;
m=(_int16)(log((double)n)/log(2.)+.1);
nv2=n/2;
nm1=n-1;
j=1;
for(i=1;i<=nm1;++i)
	{
	if(i<j)
		{
		tr=xr[j];
		ti=xi[j];
		xr[j]=xr[i];
		xi[j]=xi[i];
		xr[i]=tr;
		xi[i]=ti;
		}
	k=nv2;
R20:    if(k>=j) goto R30;
		j=j-k;
	k=(_int16)(k/2);
	goto R20;
R30:    j=j+k;
	}
for(l=1;l<=m;++l)
	{
	le1=(_int16)(pow(2,(l-1)));
	ur=1.0f;
	ui=0.f;
	wr=(float)cos(PI/(float)(le1));
	wi=-(float)sin(PI/(float)(le1));
	if(inv!=0) wi=-wi;
	for(j=1;j<=le1;++j)
		{
		for(i=j;i<=n;i=i+2*le1)
			{
			ip=i+le1;
			tr=xr[ip]*ur-xi[ip]*ui;
			ti=xr[ip]*ui+xi[ip]*ur;
			xr[ip]=xr[i]-tr;
			xi[ip]=xi[i]-ti;
			xr[i]=xr[i]+tr;
			xi[i]=xi[i]+ti;
			}
		ur1=ur*wr-ui*wi;
		ui1=ur*wi+ui*wr;
		ur=ur1;
		ui=ui1;
		}
	}
if(inv == 0) return;
for(i=1;i<=n;++i)
	{
	xr[i]=xr[i]/(float)(n);
	xi[i]=xi[i]/(float)(n);
	}
//TRACE("SpeechEnd=",SpeechEnd);
}