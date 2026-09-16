# Benchmark methodology

1. Use Voxserv `mono_44100` recordings only.
2. Validate WAV: mono, 44100 Hz, 16-bit PCM.
3. Split recordings into train/validation/test by recording, never by adjacent frames.
4. Normalize PCM to [-1, 1]. Frame at 882 samples with no overlap for the first benchmark.
5. Train the reference autoencoder, then export encoder and decoder separately.
6. Full integer INT8 quantize using representative Voxserv frames.
7. Report actual TFLite file sizes and operator list.
8. On ESP32-S3, benchmark warm steady-state inference separately from model load and filesystem I/O.
9. Measure cycles with `esp_cpu_get_cycle_count()` and time with `esp_timer_get_time()`.
10. Report p50, p95, max latency and real-time factor. One 20 ms frame must have <20 ms processing time for real-time operation.
11. Report minimum internal heap and tensor-arena allocation separately where possible.
12. Quality: MSE and SNR against the original PCM. Add SI-SDR if used consistently for all codecs.
13. Compression: report raw payload bitrate and effective framed bitrate separately.

Never replace hardware measurements with estimates. Calculated bitrates are explicitly marked as nominal.
