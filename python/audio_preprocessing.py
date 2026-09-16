import wave
import numpy as np

def load_wav(path):
    """Loads a WAV file and returns a mono float32 signal [-1.0, 1.0]."""
    with wave.open(str(path), "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        n_frames = wf.getnframes()
        
        raw_data = wf.readframes(n_frames)
        
        # Convert raw bytes to numpy array
        if sampwidth == 2: # 16-bit PCM
            data = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
        elif sampwidth == 4: # 32-bit PCM
            data = np.frombuffer(raw_data, dtype=np.int32).astype(np.float32) / 2147483648.0
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth} bytes")
            
        # If stereo, take only the left channel
        if n_channels > 1:
            data = data.reshape(-1, n_channels)[:, 0]
            
    return data

def frame_signal(signal, frame_size=882):
    """Slices a 1D audio signal into multiple frames of length `frame_size`."""
    num_frames = len(signal) // frame_size
    if num_frames == 0:
        raise ValueError(f"Signal is too short to extract a frame of size {frame_size}")
        
    # Truncate any trailing samples that don't fit into a full frame
    truncated_signal = signal[:num_frames * frame_size]
    
    # Reshape into (N, frame_size)
    frames = truncated_signal.reshape((num_frames, frame_size))
    return frames