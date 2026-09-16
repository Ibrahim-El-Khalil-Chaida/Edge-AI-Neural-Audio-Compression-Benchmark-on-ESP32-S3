#include "audio_buffer.h"
// Real microphone integration boundary.
// Recommended ESP32-S3 configuration: I2S/PDM, 16 kHz, mono, 16-bit,
// DMA with double/multiple buffering and 20 ms application frames.
