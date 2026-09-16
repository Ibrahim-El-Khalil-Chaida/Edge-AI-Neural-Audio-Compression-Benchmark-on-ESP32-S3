#pragma once
#include <stdint.h>
#include <stddef.h>
#define AUDIO_SAMPLE_RATE_HZ 16000
#define AUDIO_FRAME_MS 20
#define AUDIO_FRAME_SAMPLES ((AUDIO_SAMPLE_RATE_HZ*AUDIO_FRAME_MS)/1000)
typedef struct { int16_t samples[AUDIO_FRAME_SAMPLES]; volatile size_t count; volatile int ready; } audio_frame_buffer_t;
void audio_buffer_reset(audio_frame_buffer_t*);
int audio_buffer_push(audio_frame_buffer_t*,int16_t);
int audio_buffer_is_ready(const audio_frame_buffer_t*);
