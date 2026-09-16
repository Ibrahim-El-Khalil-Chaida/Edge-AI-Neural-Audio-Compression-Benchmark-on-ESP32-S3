#pragma once
#include <stddef.h>
#include <stdint.h>
typedef enum { CODEC_PCM=0, CODEC_ADPCM=1, CODEC_ML_INT8=2 } codec_type_t;
typedef struct { codec_type_t codec; uint32_t sample_rate; uint16_t frame_samples; } compression_config_t;
typedef struct { const int16_t *samples; size_t sample_count; } audio_frame_t;
typedef struct { uint8_t *data; size_t capacity; size_t size; } compressed_frame_t;
int compression_init(const compression_config_t *cfg);
int compression_encode(const audio_frame_t *input, compressed_frame_t *output);
int compression_decode(const compressed_frame_t *input, audio_frame_t *output);
