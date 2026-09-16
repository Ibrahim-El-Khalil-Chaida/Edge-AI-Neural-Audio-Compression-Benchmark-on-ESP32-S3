#include <stdint.h>
#include <stddef.h>
// TFLite Micro integration boundary:
// PCM -> TFLM encoder -> latent tensor -> quantization -> bit packing.
// Add measured results only after executing the converted model on hardware.
