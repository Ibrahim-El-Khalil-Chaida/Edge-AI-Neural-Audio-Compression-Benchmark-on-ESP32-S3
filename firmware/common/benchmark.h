#pragma once
#include <stdint.h>
typedef struct { uint32_t start_ticks,end_ticks,elapsed_ticks; } benchmark_sample_t;
void benchmark_begin(benchmark_sample_t*);
void benchmark_end(benchmark_sample_t*);
