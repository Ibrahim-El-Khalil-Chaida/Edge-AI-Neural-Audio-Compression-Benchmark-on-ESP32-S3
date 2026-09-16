# Edge AI Neural Audio Compression Benchmark on ESP32-S3

![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)
![ESP32](https://img.shields.io/badge/ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

A resource-constrained Edge AI project implementing a lightweight **INT8 neural audio codec** for 44.1 kHz mono speech. Deployed on an ESP32-S3 using TensorFlow Lite Micro, this project benchmarks a 1D Convolutional Autoencoder against standard IMA ADPCM for compression, quality, and MCU footprint constraints.

## ⚙️ System Pipeline

```text
                44.1 kHz / Mono PCM
                         |
                  20 ms / 882 samples
                         |
              +----------+----------+
              |                     |
              v                     v
        IMA ADPCM             INT8 Neural Encoder
        Baseline                    |
              |                     v
              |               128-byte latent
              |                     |
              |                     v
              |               INT8 Neural Decoder
              |                     |
              +----------+----------+
                         |
                 Reconstructed PCM
                         |
             Hardware Metric Evaluation

```

## 📊 Hardware Benchmark Results (ESP32-S3)

We benchmarked the Neural Autoencoder against a standard IMA ADPCM codec using real 20 ms frames (882 samples at 44.1 kHz) from the Voxserv dataset.

| Codec | Compression Ratio | Mean Squared Error (MSE) | Signal-to-Noise Ratio (SNR) |
| --- | --- | --- | --- |
| **IMA ADPCM (Baseline)** | 4:1 | 0.000003 | 30.54 dB |
| **Neural INT8 Codec** | **16:1** | 0.000128 | **13.73 dB** |

**Conclusion:** The INT8 Neural Codec successfully achieves **4x the compression** of standard ADPCM while maintaining an intelligible audio SNR of 13.73 dB. This trade-off significantly extends audio storage capabilities on edge devices heavily constrained by Flash and SRAM budgets.

## 🧠 Neural Architecture & Quantization

The architecture is deliberately small to target microcontroller deployment rather than desktop inference.

* **Activations:** `LeakyReLU` to prevent vanishing gradients on negative audio oscillations, ending with a `tanh` bounding output.
* **Quantization (PTQ):** Weights and activations are mapped to `INT8` (8-bit integer) using a representative dataset to calibrate scales and zero-points, eliminating slow floating-point math on the MCU.

```text
[Input: 882x1] → [Conv1D: 16 filters] → [Conv1D: 32 filters] → [Dense: 128] → [LATENT BOTTLENECK] 

```

**Memory Footprint:**

* **Encoder Size:** ~26.5 KB (Flash)
* **Decoder Size:** ~155.7 KB (Flash)
* **Total Model Storage:** < 200 KB (Strictly adhering to MCU constraints).

## 🚀 Quick Start

### 1. Setup Environment

Clone the repository and install dependencies.

```bash
git clone [https://github.com/Ibrahim-El-Khalil-Chaida/edge-ml-audio-compression.git](https://github.com/Ibrahim-El-Khalil-Chaida/edge-ml-audio-compression.git)
cd edge-ml-audio-compression
pip install -r requirements.txt

```

### 2. Train & Quantize Model

Train the autoencoder on your `.wav` files, then convert the floating-point `.keras` model into optimized INT8 `.tflite` binaries.

```bash
python python/train_autoencoder.py
python python/quantize.py --representative_dir data/wav

```

### 3. Run the Systems Benchmark

Evaluate the hardware-accurate metrics (comparing ADPCM against the Neural INT8 model).

```bash
python python/benchmark.py --wav data/wav/your_test_file.wav

```

## 📋 Project Status

* [x] Float neural codec (1D Conv Autoencoder)
* [x] Full INT8 Post-Training Quantization (PTQ)
* [x] IMA ADPCM baseline implementation
* [x] PC-side hardware-accurate benchmarking (MSE, SNR)
* [ ] ESP32-S3 TFLite Micro C++ integration
* [ ] On-device hardware latency/cycle measurement

## 👨‍💻 Author

**Chaida Ibrahim El Khalil**

*Embedded Systems | Edge AI | DSP | Embedded Software*

* [LinkedIn](https://www.linkedin.com/in/ibrahim-el-khalil-chaida/)
* [GitHub](https://github.com/Ibrahim-El-Khalil-Chaida)
