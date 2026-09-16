#include "telemetry.h"
#include <cstdio>
void print_header(){printf("file,frame,codec,payload_bytes,cycles,latency_us,mse,snr_db,free_heap,min_free_heap\n");}
void print_row(const char*f,int fr,const char*c,size_t p,uint32_t cy,uint32_t us,float m,float s,size_t h,size_t mh){printf("%s,%d,%s,%u,%u,%u,%.9g,%.4f,%u,%u\n",f,fr,c,(unsigned)p,(unsigned)cy,(unsigned)us,m,s,(unsigned)h,(unsigned)mh);}
