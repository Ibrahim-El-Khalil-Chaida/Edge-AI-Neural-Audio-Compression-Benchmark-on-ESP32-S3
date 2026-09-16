from pathlib import Path
import sys
import numpy as np
import tensorflow as tf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load_training_frames
from metrics import calculate_snr  # or compute inline: 10 * log10(var(orig) / var(orig - recon))

def eval_tflite_codec(encoder_path, decoder_path, data_dir):
    frames = load_training_frames(data_dir)
    
    # Load INT8 TFLite Interpreters
    enc_interpreter = tf.lite.Interpreter(model_path=encoder_path)
    enc_interpreter.allocate_tensors()
    dec_interpreter = tf.lite.Interpreter(model_path=decoder_path)
    dec_interpreter.allocate_tensors()
    
    enc_in = enc_interpreter.get_input_details()[0]
    enc_out = enc_interpreter.get_output_details()[0]
    dec_in = dec_interpreter.get_input_details()[0]
    dec_out = dec_interpreter.get_output_details()[0]
    
    reconstructed = []
    for frame in frames[:200]:  # Evaluate on first 200 frames
        # Quantize Float32 to INT8 Input
        q_frame = (frame / enc_in['quantization'][0] + enc_in['quantization'][1]).astype(np.int8)
        enc_interpreter.set_tensor(enc_in['index'], q_frame[None, :, None])
        enc_interpreter.invoke()
        latent = enc_interpreter.get_tensor(enc_out['index'])
        
        # Pass Latent through Decoder
        dec_interpreter.set_tensor(dec_in['index'], latent)
        dec_interpreter.invoke()
        dec_int8 = dec_interpreter.get_tensor(dec_out['index'])[0, :, 0]
        
        # Dequantize INT8 to Float32 Output
        recon_frame = (dec_int8.astype(np.float32) - dec_out['quantization'][1]) * dec_out['quantization'][0]
        reconstructed.append(recon_frame)
        
    orig = frames[:200]
    recon = np.array(reconstructed)
    
    mse = np.mean((orig - recon) ** 2)
    snr = 10 * np.log10(np.var(orig) / np.var(orig - recon))
    
    print(f"=== INT8 Neural Codec Evaluation ===")
    print(f"MSE: {mse:.6f}")
    print(f"SNR: {snr:.2f} dB")

if __name__ == '__main__':
    eval_tflite_codec('models/audio_encoder_int8.tflite', 'models/audio_decoder_int8.tflite', 'data/wav')