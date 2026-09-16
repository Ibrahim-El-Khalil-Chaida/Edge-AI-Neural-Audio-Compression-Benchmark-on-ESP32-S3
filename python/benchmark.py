import argparse
from pathlib import Path
import sys
import numpy as np
import tensorflow as tf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audio_preprocessing import load_wav, frame_signal
from adpcm import encode_ima_adpcm, decode_ima_adpcm
from metrics import calculate_snr, calculate_mse

def run_tflite(model_path, data):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    inp = interpreter.get_input_details()[0]
    out = interpreter.get_output_details()[0]
    
    scale, zero_point = inp['quantization']
    out_scale, out_zero_point = out['quantization']
    expected_shape = inp['shape'] # Dynamically grab the exact shape the model expects
    
    results = []
    for sample in data:
        # Quantize Float to INT8
        if scale != 0:
            q_in = np.round(sample / scale + zero_point).clip(-128, 127).astype(np.int8)
        else:
            q_in = sample.astype(np.int8)
            
        # Dynamically reshape to fit the exact TFLite signature (e.g., [1, 882, 1] or [1, 128])
        q_in = q_in.reshape(expected_shape)
            
        interpreter.set_tensor(inp['index'], q_in)
        interpreter.invoke()
        res = interpreter.get_tensor(out['index'])
        
        # Dequantize INT8 to Float
        if out_scale != 0:
            res_float = (res.astype(np.float32) - out_zero_point) * out_scale
        else:
            res_float = res.astype(np.float32)
            
        results.append(res_float)
        
    return np.squeeze(np.array(results))

def benchmark(wav_path, enc_path, dec_path, frame_size=882):
    x = load_wav(wav_path)
    frames = frame_signal(x, frame_size=frame_size)
    
    # 1. Neural Codec Pass
    latents = run_tflite(enc_path, np.asarray(frames, dtype=np.float32)[..., None])
    recon_neural = run_tflite(dec_path, latents)
    
    # 2. IMA ADPCM Baseline Pass
    pcm_flat = np.concatenate(frames)
    adpcm_codes = encode_ima_adpcm(pcm_flat)
    recon_adpcm = decode_ima_adpcm(adpcm_codes)
    recon_adpcm_framed = recon_adpcm[:len(pcm_flat)].reshape(-1, frame_size)
    
    # 3. Calculate Metrics
    mse_neural = calculate_mse(frames, recon_neural)
    snr_neural = calculate_snr(frames, recon_neural)
    
    mse_adpcm = calculate_mse(frames, recon_adpcm_framed)
    snr_adpcm = calculate_snr(frames, recon_adpcm_framed)
    
    print("\n" + "="*50)
    print("         AUDIO CODEC HARDWARE BENCHMARK       ")
    print("="*50)
    print(f"Sample File : {Path(wav_path).name}")
    print(f"Frame Size  : {frame_size} samples (20 ms @ 44.1 kHz)\n")
    print(f"{'Codec':<20} | {'MSE':<12} | {'SNR (dB)':<10}")
    print("-" * 50)
    print(f"{'IMA ADPCM (4:1)':<20} | {mse_adpcm:<12.6f} | {snr_adpcm:<10.2f}")
    print(f"{'Neural INT8 (16:1)':<20} | {mse_neural:<12.6f} | {snr_neural:<10.2f}")
    print("="*50 + "\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--wav', required=True)
    p.add_argument('--encoder', default='models/audio_encoder_int8.tflite')
    p.add_argument('--decoder', default='models/audio_decoder_int8.tflite')
    p.add_argument('--frame_size', type=int, default=882)
    a = p.parse_args()
    
    benchmark(a.wav, a.encoder, a.decoder, a.frame_size)

if __name__ == '__main__':
    main()