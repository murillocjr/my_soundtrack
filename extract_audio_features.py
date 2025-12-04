import librosa

pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def extract_features(y, sr):
    """
    Extract various audio features from an audio signal.

    Parameters:
    y (np.ndarray): Audio time series
    sr (int): Sampling rate

    Returns:
    dict: Dictionary of extracted features
    """
    features = {}

    # Time-domain features
    features['rms'] = librosa.feature.rms(y=y).mean()
    features['zcr'] = librosa.feature.zero_crossing_rate(y).mean()

    # Frequency-domain features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    features['spectral_centroid'] = spectral_centroid.mean()
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features['spectral_rolloff'] = spectral_rolloff.mean()

    # MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    for i, mfcc in enumerate(mfccs):
        features[f'mfcc_{i + 1}'] = mfcc.mean()

    # Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    for i, pitch_class in enumerate(pitch_classes):
        features[f'chroma_{pitch_class}'] = chroma[i].mean()

    return features

def get_audio_features(audio_path):
    y, sr = librosa.load(audio_path)
    audio_features = extract_features(y, sr)
    return audio_features

# get_audio_features(MUSIC_PATH + "/yt/00 English - Sailor Moon Theme.mp3")