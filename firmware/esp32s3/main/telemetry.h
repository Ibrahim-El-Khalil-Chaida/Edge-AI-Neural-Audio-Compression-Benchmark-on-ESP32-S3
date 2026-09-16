#pragma once
#include <cstdint>
void print_header();
void print_row(const char* file,int frame,const char* codec,size_t payload,uint32_t cycles,uint32_t latency_us,float mse,float snr,size_t free_heap,size_t min_heap);
