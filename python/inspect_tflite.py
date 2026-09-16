import argparse
import tensorflow as tf

def inspect(path):
    data=open(path,'rb').read(); i=tf.lite.Interpreter(model_path=path); i.allocate_tensors()
    print(f'\n{path}: {len(data)} bytes')
    for d in i.get_input_details()+i.get_output_details(): print(d['name'],d['shape'],d['dtype'],'quant=',d['quantization'])
    print('ops:', [x['op_name'] for x in i._get_ops_details()])
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('models',nargs='+'); a=p.parse_args()
    for m in a.models: inspect(m)
