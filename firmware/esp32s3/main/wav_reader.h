#pragma once
#include <cstdio>
#include <cstdint>
class WavReader { public: bool open(const char* path); bool read_frame(int16_t* dst, size_t n); uint32_t sample_rate() const{return sr_;} uint16_t channels() const{return ch_;} uint16_t bits() const{return bits_;} private: FILE* f_=nullptr; uint32_t sr_=0; uint16_t ch_=0,bits_=0; uint32_t data_left_=0; };
