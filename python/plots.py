import argparse,csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def main():
    p=argparse.ArgumentParser();p.add_argument("--csv",default="results/benchmark.csv");p.add_argument("--out",default="results");a=p.parse_args()
    rows=list(csv.DictReader(open(a.csv))); Path(a.out).mkdir(parents=True,exist_ok=True)
    names=[r["codec"] for r in rows]
    specs=[("compression_ratio","compression_ratio.png","Compression ratio"),("bitrate_kbit_s","bitrate.png","Bitrate (kbit/s)"),("encode_ms_per_frame","latency.png","Encode latency (ms/frame)"),("snr_db","snr.png","SNR (dB)"),("payload_bytes_per_frame","memory.png","Payload bytes/frame")]
    for key,fn,label in specs:
        vals=[float(r[key]) if r[key] not in ("inf","Infinity") else np.nan for r in rows]
        plt.figure();plt.bar(names,vals);plt.ylabel(label);plt.title(key);plt.tight_layout();plt.savefig(Path(a.out)/fn,dpi=150);plt.close()

if __name__=="__main__":main()
