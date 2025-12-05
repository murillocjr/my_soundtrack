# import librosa
# import essentia
# import essentia.standard as es
#
# from env import MUSIC_PATH
# from extract_audio_features import pitch_classes
#
#
# # pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
#
# def extract_features(y, sr):
#
#     tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
#     features = {}
#
#     features['tempo'] = tempo[0]
#
#     return features
#
# def get_audio_features(audio_path):
#     y, sr = librosa.load(audio_path)
#     audio_features = extract_features(y, sr)
#
#     ###
#     audio = es.MonoLoader(filename=audio_path)()
#     danceability_extractor = es.Danceability()
#     danceability_value, dfa_vector = danceability_extractor(audio)
#     audio_features['danceability'] = danceability_value
#     print(audio_features)
#     ###
#
#
#     return audio_features
#
# # get_audio_features(MUSIC_PATH + "/yt/00 English - Sailor Moon Theme.mp3")
# # get_audio_features(MUSIC_PATH + 'flac/01 - Arabian Nights.flac')
# # get_audio_features(MUSIC_PATH + 'assorted/9/Alcoholika La Christo - Celia [RJ8DCvPbxzQ].m4a')
# # get_audio_features(MUSIC_PATH + 'yt/Sadness and Sorrow-HQRbfBZYCNY.opus')
