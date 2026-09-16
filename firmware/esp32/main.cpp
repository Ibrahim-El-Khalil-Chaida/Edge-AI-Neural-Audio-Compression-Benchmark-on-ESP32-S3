#include <Arduino.h>
#include <math.h>
#include <string.h>
#include "audio_buffer.h"
#include "benchmark.h"
#include "compression.h"

static audio_frame_buffer_t frame;

void audio_buffer_reset(audio_frame_buffer_t*b){b->count=0;b->ready=0;}
int audio_buffer_push(audio_frame_buffer_t*b,int16_t s){if(b->count>=AUDIO_FRAME_SAMPLES)return -1;b->samples[b->count++]=s;if(b->count==AUDIO_FRAME_SAMPLES)b->ready=1;return 0;}
int audio_buffer_is_ready(const audio_frame_buffer_t*b){return b->ready!=0;}
void benchmark_begin(benchmark_sample_t*b){b->start_ticks=micros();}
void benchmark_end(benchmark_sample_t*b){b->end_ticks=micros();b->elapsed_ticks=b->end_ticks-b->start_ticks;}

int compression_init(const compression_config_t*){return 0;}
int compression_encode(const audio_frame_t*in,compressed_frame_t*out){
    if(!in||!out||out->capacity<in->sample_count*2)return -1;
    memcpy(out->data,in->samples,in->sample_count*2);out->size=in->sample_count*2;return 0;
}
int compression_decode(const compressed_frame_t*,audio_frame_t*){return -1;}

void setup(){
    Serial.begin(115200);delay(500);audio_buffer_reset(&frame);
    compression_config_t cfg{CODEC_PCM,AUDIO_SAMPLE_RATE_HZ,AUDIO_FRAME_SAMPLES};compression_init(&cfg);
    Serial.println("Edge ML Audio Compression Benchmark");
}
void loop(){
    for(size_t n=0;n<AUDIO_FRAME_SAMPLES;n++){
        float t=(float)n/AUDIO_SAMPLE_RATE_HZ;
        audio_buffer_push(&frame,(int16_t)(12000.0f*sinf(2.0f*PI*440.0f*t)));
    }
    if(audio_buffer_is_ready(&frame)){
        benchmark_sample_t b{};benchmark_begin(&b);
        uint8_t payload[AUDIO_FRAME_SAMPLES*2];compressed_frame_t out{payload,sizeof(payload),0};
        audio_frame_t in{frame.samples,AUDIO_FRAME_SAMPLES};int rc=compression_encode(&in,&out);benchmark_end(&b);
        Serial.printf("codec=PCM rc=%d bytes=%u encode_us=%u\n",rc,(unsigned)out.size,(unsigned)b.elapsed_ticks);
        audio_buffer_reset(&frame);
    }
    delay(1000);
}
