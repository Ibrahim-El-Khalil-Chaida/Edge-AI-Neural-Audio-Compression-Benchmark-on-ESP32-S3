import argparse,urllib.request
from pathlib import Path
FILES=['127389__acclivity__thetimehascome.wav','156550__acclivity__a-dream-within-a-dream.wav','34210__acclivity__i-am-female.wav','165187__blaukreuz__global-village-hochdeutsch.wav','167554__Speedenza__memory-eva-gore-booth.wav','352762__kennysvoice__audiokingsz-illusion.wav','382326__scott-simpson__crossing-the-bar.wav','72001__corsica-s__electric-masquerade.wav','75064__corsica-s__farah-faucet.wav']
BASE='https://github.com/voxserv/audio_quality_testing_samples/raw/refs/heads/master/mono_44100/'
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='data/wav');a=p.parse_args();o=Path(a.output);o.mkdir(parents=True,exist_ok=True)
 for n in FILES:
  d=o/n
  if not d.exists(): print('Downloading',n); urllib.request.urlretrieve(BASE+n,d)
 print('Downloaded/available:',len(list(o.glob('*.wav'))))
if __name__=='__main__':main()
