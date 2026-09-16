import tensorflow as tf
import numpy as np

class MLCodecReference:
    def __init__(self, model_path):
        self.model=tf.keras.models.load_model(model_path)
        self.encoder=tf.keras.Model(self.model.input,self.model.get_layer("latent").output)
        zdim=self.model.get_layer("latent").output_shape[-1]
        zi=tf.keras.Input((zdim,))
        x=zi; started=False
        for layer in self.model.layers:
            if layer.name=="latent": started=True; continue
            if started: x=layer(x)
        self.decoder=tf.keras.Model(zi,x)

    def encode(self, frame):
        return self.encoder(frame[None,:,None],training=False).numpy()[0].astype(np.float32)

    def decode(self, latent):
        y=self.decoder(latent[None,:],training=False).numpy()[0,:,0]
        return np.clip(y,-1,1).astype(np.float32)
