#if !defined(KWS_MFCC__INCLUDED_)
#define KWS_MFCC__INCLUDED_
#define     FS 16.0F       
#define     PI 3.1415926536F   
#define     FiltNum 25
#define     FFTLen  512
#define     H_FRAME 200
#define     FRAMEL  400
#define     FRAMELL 401
#define     PCEP    12 

class MFCC{
private:
   float   FiltCoe1[FFTLen/2+1];
   float   FiltCoe2[FFTLen/2+1];
   _int16  Num[FFTLen/2+1];
   void InitFilt();
   _int16 CFilt(float *,float *En);
   void fft(float *,float *,_int16);
   void MultiHamming(double *data);
public:
	MFCC();
 virtual ~MFCC();
	void GetVector(float *,float *);
  void GetFeature(short *, float *,int);
};
#endif