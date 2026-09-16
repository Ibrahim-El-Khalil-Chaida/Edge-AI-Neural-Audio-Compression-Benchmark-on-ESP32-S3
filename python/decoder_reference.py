import numpy as np

def quantize_latent(latent,bits=4):
    levels=(1<<bits)-1
    lo,hi=float(np.min(latent)),float(np.max(latent))
    if hi-lo<1e-9: return np.zeros_like(latent,dtype=np.uint8),lo,hi
    q=np.round((latent-lo)/(hi-lo)*levels)
    return np.clip(q,0,levels).astype(np.uint8),lo,hi

def dequantize_latent(q,lo,hi,bits=4):
    levels=(1<<bits)-1
    if hi-lo<1e-9: return np.full(len(q),lo,dtype=np.float32)
    return (lo+q.astype(np.float32)/levels*(hi-lo)).astype(np.float32)

def pack_bits(values,bits):
    values=np.asarray(values,dtype=np.uint8); acc=0; nbits=0; out=bytearray()
    mask=(1<<bits)-1
    for v in values:
        acc |= (int(v)&mask)<<nbits; nbits += bits
        while nbits>=8:
            out.append(acc&255); acc >>= 8; nbits-=8
    if nbits: out.append(acc&255)
    return bytes(out)

def unpack_bits(data,count,bits):
    mask=(1<<bits)-1; vals=[]; acc=0; nbits=0; pos=0
    for _ in range(count):
        while nbits<bits:
            if pos>=len(data): raise ValueError("Truncated bitstream")
            acc |= data[pos]<<nbits; pos+=1; nbits+=8
        vals.append(acc&mask); acc>>=bits; nbits-=bits
    return np.asarray(vals,dtype=np.uint8)

def encode_latent(latent,bits=4):
    q,lo,hi=quantize_latent(latent,bits)
    return np.asarray([lo,hi],dtype="<f4").tobytes()+bytes([bits,len(q)])+pack_bits(q,bits)

def decode_latent(bitstream):
    lo,hi=np.frombuffer(bitstream[:8],dtype="<f4")
    bits,count=bitstream[8],bitstream[9]
    q=unpack_bits(bitstream[10:],count,bits)
    return dequantize_latent(q,float(lo),float(hi),bits)
