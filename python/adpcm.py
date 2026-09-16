import numpy as np

# IMA ADPCM step size table
STEP_TABLE = [
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
]

INDEX_TABLE = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]

def encode_ima_adpcm(pcm):
    if np.issubdtype(pcm.dtype, np.floating):
        pcm = (pcm * 32767.0).clip(-32768, 32767).astype(np.int16)
        
    predicted = 0
    step_index = 0
    encoded = []
    
    for sample in pcm.flatten():
        diff = sample - predicted
        sign = 0x08 if diff < 0 else 0
        if sign:
            diff = -diff
            
        step = STEP_TABLE[step_index]
        delta = 0
        
        if diff >= step:
            delta |= 4
            diff -= step
        step >>= 1
        if diff >= step:
            delta |= 2
            diff -= step
        step >>= 1
        if diff >= step:
            delta |= 1
            
        nibble = sign | delta
        encoded.append(nibble)
        
        diff_q = (STEP_TABLE[step_index] >> 3)
        if delta & 4: diff_q += STEP_TABLE[step_index]
        if delta & 2: diff_q += (STEP_TABLE[step_index] >> 1)
        if delta & 1: diff_q += (STEP_TABLE[step_index] >> 2)
        
        if sign:
            predicted -= diff_q
        else:
            predicted += diff_q
            
        predicted = max(-32768, min(32767, predicted))
        step_index += INDEX_TABLE[nibble]
        step_index = max(0, min(88, step_index))
        
    return np.array(encoded, dtype=np.uint8)

def decode_ima_adpcm(codes):
    predicted = 0
    step_index = 0
    decoded = []
    
    for nibble in codes.flatten():
        nibble = int(nibble)
        sign = nibble & 8
        delta = nibble & 7
        
        step = STEP_TABLE[step_index]
        diff_q = step >> 3
        if delta & 4: diff_q += step
        if delta & 2: diff_q += (step >> 1)
        if delta & 1: diff_q += (step >> 2)
        
        if sign:
            predicted -= diff_q
        else:
            predicted += diff_q
            
        predicted = max(-32768, min(32767, predicted))
        step_index += INDEX_TABLE[nibble]
        step_index = max(0, min(88, step_index))
        
        decoded.append(predicted / 32768.0)
        
    return np.array(decoded, dtype=np.float32)