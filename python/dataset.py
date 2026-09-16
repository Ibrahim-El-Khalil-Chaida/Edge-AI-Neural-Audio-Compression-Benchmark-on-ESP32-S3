from pathlib import Path
import glob
import scipy.io.wavfile as wavfile
import numpy as np

def load_training_frames(data_dir, frame_size=882, max_files=None):
    """Loads WAV files from data_dir and slices them into frame_size chunks."""
    wav_paths = glob.glob(str(Path(data_dir) / "*.wav"))
    print(f"Found {len(wav_paths)} WAV files in {data_dir}.")
    
    if max_files and max_files < len(wav_paths):
        wav_paths = wav_paths[:max_files]
        print(f"Limiting to first {max_files} files for testing.")
        
    frames = []
    for p in wav_paths:
        rate, data = wavfile.read(p)
        if data.ndim > 1:
            data = data[:, 0]  # Take mono channel
            
        # Normalize int16/int32 to float32 [-1.0, 1.0]
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483648.0
            
        num_frames = len(data) // frame_size
        if num_frames > 0:
            f = data[:num_frames * frame_size].reshape((num_frames, frame_size))
            frames.append(f)
            
    if not frames:
        raise ValueError(f"No valid audio frames extracted from {data_dir}")
        
    return np.concatenate(frames, axis=0)