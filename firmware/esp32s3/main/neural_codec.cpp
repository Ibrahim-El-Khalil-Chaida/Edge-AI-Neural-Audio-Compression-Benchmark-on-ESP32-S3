#include "neural_codec.h"
#include "esp_cpu.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/c/common.h"
static const char* TAG="neural";
// The exact resolver set must match the converted model. Add/remove operators after inspecting
// with python/inspect_tflite.py. This skeleton includes the common kernels for the architecture.
static tflite::MicroMutableOpResolver<16> resolver(){tflite::MicroMutableOpResolver<16> r; r.AddConv2D(); r.AddFullyConnected(); r.AddReshape(); r.AddMean(); r.AddMul(); r.AddAdd(); r.AddQuantize(); r.AddDequantize(); r.AddAveragePool2D(); r.AddResizeNearestNeighbor(); return r;}
bool NeuralCodec::begin(const uint8_t* eb,size_t es,const uint8_t* db,size_t ds){
 const tflite::Model* em=tflite::GetModel(eb); const tflite::Model* dm=tflite::GetModel(db); if(em->version()!=TFLITE_SCHEMA_VERSION||dm->version()!=TFLITE_SCHEMA_VERSION)return false;
 // Production integration should use separately sized static arenas after observing arena usage.
 arena_size_=160*1024; arena_enc_=(uint8_t*)heap_caps_malloc(arena_size_,MALLOC_CAP_INTERNAL|MALLOC_CAP_8BIT); arena_dec_=(uint8_t*)heap_caps_malloc(arena_size_,MALLOC_CAP_INTERNAL|MALLOC_CAP_8BIT); if(!arena_enc_||!arena_dec_)return false;
 (void)es;(void)ds; ESP_LOGI(TAG,"models loaded; arenas allocated"); return true;
}
bool NeuralCodec::encode(const int16_t*,int8_t*){return false;}
bool NeuralCodec::decode(const int8_t*,int16_t*){return false;}
