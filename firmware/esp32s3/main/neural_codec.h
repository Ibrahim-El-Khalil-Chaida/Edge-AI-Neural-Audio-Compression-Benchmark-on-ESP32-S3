#pragma once
#include <cstddef>
#include <cstdint>
class NeuralCodec { public: bool begin(const uint8_t*,size_t,const uint8_t*,size_t); bool encode(const int16_t*,int8_t*); bool decode(const int8_t*,int16_t*); uint32_t encoder_cycles()const{return enc_cycles_;} uint32_t decoder_cycles()const{return dec_cycles_;} size_t arena_bytes()const{return arena_size_;} private: void* enc_=nullptr; void* dec_=nullptr; uint8_t* arena_enc_=nullptr; uint8_t* arena_dec_=nullptr; size_t arena_size_=0; uint32_t enc_cycles_=0,dec_cycles_=0; };
