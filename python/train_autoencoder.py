import argparse
from pathlib import Path
import sys, tensorflow as tf
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset import load_training_frames
from models import build_autoencoder, build_encoder, build_decoder, LATENT_DIM

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data_dir',default='data/wav'); p.add_argument('--epochs',type=int,default=40)
    p.add_argument('--batch_size',type=int,default=32); p.add_argument('--output_dir',default='models')
    a=p.parse_args(); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    x=load_training_frames(a.data_dir)[...,None].astype('float32')
    if len(x)<10: raise RuntimeError('Need more WAV frames. Download Voxserv mono_44100 first.')
    n=len(x); ntr=max(1,int(n*.8)); nv=max(1,int(n*.1));
    train=x[:ntr]; val=x[ntr:ntr+nv]
    ae=build_autoencoder(); ae.compile(tf.keras.optimizers.Adam(1e-3),loss='mse')
    ae.summary(); ae.fit(train,train,validation_data=(val,val),epochs=a.epochs,batch_size=a.batch_size,shuffle=True,
        callbacks=[tf.keras.callbacks.EarlyStopping(patience=7,restore_best_weights=True)])
    ae.save(out/'audio_autoencoder.keras')
    build_encoder().set_weights([w for w in ae.layers if w.name=='audio_encoder'][0].get_weights()) if False else None
    enc=build_encoder(); dec=build_decoder()
    enc.set_weights(ae.get_layer('audio_encoder').get_weights())
    dec.set_weights(ae.get_layer('audio_decoder').get_weights())
    enc.save(out/'audio_encoder.keras'); dec.save(out/'audio_decoder.keras')
    print(f'Latent: {LATENT_DIM} int8 values/frame = {LATENT_DIM} bytes/frame before framing overhead')
    print('Saved encoder, decoder and combined reference model.')
if __name__=='__main__': main()
