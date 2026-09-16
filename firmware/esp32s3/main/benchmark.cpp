#include "benchmark.h"
#include "wav_reader.h"
#include "adpcm_codec.h"
#include "telemetry.h"
#include "esp_timer.h"
#include "esp_cpu.h"
#include "esp_heap_caps.h"
#include <algorithm>
#include <cmath>
#include <cstring>
static float mse(const int16_t*a,const int16_t*b,size_t n){double s=0;for(size_t i=0;i<n;i++){double d=(double)a[i]-b[i];s+=d*d;}return s/n/((32768.0)*(32768.0));}
void run_benchmark(const char* path){WavReader w;if(!w.open(path)){printf("WAV_ERROR,%s\n",path);return;} static int16_t pcm[882],rec[882];static uint8_t payload[900];int16_t pred=0;int idx=0;int frame=0;print_header();while(w.read_frame(pcm,882)){uint32_t mh=heap_caps_get_minimum_free_size(MALLOC_CAP_INTERNAL),fh=heap_caps_get_free_size(MALLOC_CAP_INTERNAL);uint32_t c0=esp_cpu_get_cycle_count();int16_t p=pcm[0];size_t n=adpcm_encode_frame(pcm,882,payload,&pred,&idx);uint32_t c1=esp_cpu_get_cycle_count();adpcm_decode_frame(payload,n,p,idx,rec,882);uint32_t c2=esp_cpu_get_cycle_count();float m=mse(pcm,rec,882);float snr=10*log10f((m>0)?1.0f/m:1e9f);print_row(path,frame,"IMA_ADPCM",n+4,c1-c0,(c1-c0)*1000000/240000000,m,snr,fh,mh);frame++;}}
