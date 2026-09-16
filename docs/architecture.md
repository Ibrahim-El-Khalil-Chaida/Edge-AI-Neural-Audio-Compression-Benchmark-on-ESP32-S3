# Architecture

Input: mono 44.1 kHz, signed 16-bit PCM. Frame = 20 ms = 882 samples = 1764 bytes.

## Neural codec

Separate encoder and decoder are required for a real codec. The encoder maps 882 samples to 128 latent values. The decoder reconstructs 882 samples from those 128 values.

Encoder: Conv1D 16/9/2 -> Conv1D 24/9/2 -> Conv1D 32/9/2 -> GlobalAveragePooling -> Dense 128 tanh.
Decoder: Dense 888 -> reshape 111x8 -> upsample x2 + Conv1D 8 -> upsample x2 + Conv1D 16 -> upsample x2 + Conv1D 8 -> crop 888 to 882 -> Conv1D 1 tanh.

Nominal neural payload = 128 bytes/frame = 51.2 kbit/s. PCM = 705.6 kbit/s. Nominal payload compression = 13.78:1 before headers.

The actual TFLite operator set and tensor-arena requirement must be measured after conversion. Do not claim the model fits a particular arena until the target firmware has allocated and invoked it successfully.
