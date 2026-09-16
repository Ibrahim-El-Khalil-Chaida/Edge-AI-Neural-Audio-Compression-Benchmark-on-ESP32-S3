import argparse
from pathlib import Path
import sys
import tensorflow as tf
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load_training_frames

def convert(model, frames, output):
    def rep():
        for f in frames[:500]:
            yield [f[None, :, None].astype('float32')]
            
    c = tf.lite.TFLiteConverter.from_keras_model(model)
    c.optimizations = [tf.lite.Optimize.DEFAULT]
    c.representative_dataset = rep
    c.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    c.inference_input_type = tf.int8
    c.inference_output_type = tf.int8
    data = c.convert()
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_bytes(data)
    print(f'{output}: {len(data)} bytes')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--representative_dir', default='data/wav')
    p.add_argument('--encoder', default='models/audio_encoder.keras')
    p.add_argument('--decoder', default='models/audio_decoder.keras')
    p.add_argument('--encoder_output', default='models/audio_encoder_int8.tflite')
    p.add_argument('--decoder_output', default='models/audio_decoder_int8.tflite')
    a = p.parse_args()

    frames = load_training_frames(a.representative_dir)
    convert(tf.keras.models.load_model(a.encoder), frames, a.encoder_output)
    
    # Decoder representative input is latent-shaped, generated from trained encoder.
    enc = tf.keras.models.load_model(a.encoder)
    
    # FIX: Use frames[:500, ..., None] to yield shape (500, 882, 1)
    lat = enc.predict(frames[:500, ..., None], verbose=0).astype('float32')
    
    dec = tf.keras.models.load_model(a.decoder)
    
    def rep_dec():
        for z in lat:
            yield [z[None, :]]
            
    c = tf.lite.TFLiteConverter.from_keras_model(dec)
    c.optimizations = [tf.lite.Optimize.DEFAULT]
    c.representative_dataset = rep_dec
    c.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    c.inference_input_type = tf.int8
    c.inference_output_type = tf.int8
    data = c.convert()
    Path(a.decoder_output).write_bytes(data)
    print(f'{a.decoder_output}: {len(data)} bytes')

if __name__ == '__main__':
    main()