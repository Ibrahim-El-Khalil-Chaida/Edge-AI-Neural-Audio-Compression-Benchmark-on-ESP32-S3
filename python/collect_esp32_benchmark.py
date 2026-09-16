"""Parse ESP32 CSV telemetry exported from serial monitor.
Expected: file,frame,codec,payload_bytes,cycles,latency_us,mse,snr_db,free_heap,min_free_heap
"""
import argparse,csv,statistics

def main():
 p=argparse.ArgumentParser();p.add_argument('csv_file');a=p.parse_args(); rows=list(csv.DictReader(open(a.csv_file)))
 for codec in sorted(set(r['codec'] for r in rows)):
  x=[float(r['latency_us']) for r in rows if r['codec']==codec]
  cyc=[float(r['cycles']) for r in rows if r['codec']==codec]
  print(codec, 'n=',len(x),'p50_us=',statistics.median(x),'p95_us=',sorted(x)[int(.95*(len(x)-1))],'max_us=',max(x),'mean_cycles=',statistics.mean(cyc))
if __name__=='__main__':main()
