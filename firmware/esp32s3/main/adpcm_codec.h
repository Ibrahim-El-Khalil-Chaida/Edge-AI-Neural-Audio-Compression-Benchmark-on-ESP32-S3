#pragma once
#include <cstdint>
size_t adpcm_encode_frame(const int16_t* pcm,size_t n,uint8_t* out,int16_t* predictor,int* index);
void adpcm_decode_frame(const uint8_t* in,size_t bytes,int16_t predictor,int index,int16_t* out,size_t n);
