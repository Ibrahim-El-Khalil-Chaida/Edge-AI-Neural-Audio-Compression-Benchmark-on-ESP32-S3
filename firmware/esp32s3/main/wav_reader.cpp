#include "wav_reader.h"
#include <cstring>
static uint32_t u32(const uint8_t*b){return b[0]|b[1]<<8|b[2]<<16|b[3]<<24;} static uint16_t u16(const uint8_t*b){return b[0]|b[1]<<8;}
bool WavReader::open(const char* path){f_=fopen(path,"rb"); if(!f_)return false; uint8_t h[12]; if(fread(h,1,12,f)!=12||memcmp(h,"RIFF",4)||memcmp(h+8,"WAVE",4))return false; bool fmt=false,data=false; while(!data){uint8_t ch[8]; if(fread(ch,1,8,f)!=8)return false; uint32_t n=u32(ch+4); long pos=ftell(f); if(!memcmp(ch,"fmt ",4)){uint8_t b[40]; if(n>40)return false; if(fread(b,1,n,f)!=n)return false; if(u16(b)!=1)return false; ch_=u16(b+2);sr_=u32(b+4);bits_=u16(b+14);fmt=true;} else if(!memcmp(ch,"data",4)){data_left_=n;data=true;} else fseek(f,n,SEEK_CUR); if(!fmt&&data)return false; if(ftell(f)==pos)break;} return fmt&&data&&sr_==44100&&ch_==1&&bits_==16;}
bool WavReader::read_frame(int16_t* dst,size_t n){if(!f_||data_left_<n*2)return false; size_t got=fread(dst,2,n,f_);data_left_-=got*2;return got==n;}
