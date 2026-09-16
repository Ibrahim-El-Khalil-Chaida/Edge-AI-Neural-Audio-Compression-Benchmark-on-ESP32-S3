import tensorflow as tf
from tensorflow.keras import layers, Model

def build_encoder(frame_size=882, latent_dim=128):
    inputs = layers.Input(shape=(frame_size, 1), name='audio')
    
    x = layers.Conv1D(16, 8, strides=4, padding='same')(inputs)
    x = layers.LeakyReLU(alpha=0.2)(x)
    
    x = layers.Conv1D(32, 8, strides=4, padding='same')(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    
    x = layers.Flatten()(x)
    latent = layers.Dense(latent_dim, name='latent')(x)
    
    return Model(inputs, latent, name='audio_encoder')

def build_decoder(frame_size=882, latent_dim=128):
    inputs = layers.Input(shape=(latent_dim,), name='latent')
    
    # 882 / 4 / 4 = 56 (with 'same' padding)
    x = layers.Dense(56 * 32)(inputs)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Reshape((56, 32))(x)
    
    x = layers.Conv1DTranspose(16, 8, strides=4, padding='same')(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    
    # Use tanh for the final output to bound audio between -1.0 and 1.0
    x = layers.Conv1DTranspose(1, 8, strides=4, padding='same', activation='tanh')(x)
    
    # Crop exactly to 882 in case of padding rounding differences
    outputs = layers.Cropping1D(cropping=(0, x.shape[1] - frame_size))(x) if x.shape[1] > frame_size else x
    
    return Model(inputs, outputs, name='audio_decoder')

def build_autoencoder(frame_size=882, latent_dim=128):
    encoder = build_encoder(frame_size, latent_dim)
    decoder = build_decoder(frame_size, latent_dim)
    
    inputs = layers.Input(shape=(frame_size, 1), name='audio')
    latents = encoder(inputs)
    outputs = decoder(latents)
    
    return Model(inputs, outputs, name='audio_autoencoder')