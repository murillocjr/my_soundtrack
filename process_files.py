import time
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggopus import OggOpus

import json
import numpy as np

from env import MUSIC_PATH, AUDIO_FEATURES_PATH
from extract_audio_features import get_audio_features

directory_path = Path(MUSIC_PATH)
output_path = Path(AUDIO_FEATURES_PATH)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

skipped_ext = set()

for file_path in directory_path.rglob('*'):
    audio = None
    if file_path.is_file():
        # if "ith My Ex" not in str(file_path):
        #     continue
        # print(file_path)
        if file_path.suffix.lower() == '.mp3':
            try:
                audio = MP3(str(file_path))
            except:
                audio = None
        elif file_path.suffix == '.m4a':
            audio = MP4(str(file_path))
        elif file_path.suffix == '.flac':
            audio = FLAC(str(file_path))
        elif file_path.suffix == '.opus':
            audio = OggOpus(str(file_path))
            # print(audio.tags['musicbrainz_trackid'][0])
            # break
        else:
            # print('Skipped:', file_path)
            skipped_ext.add(file_path.suffix)
            continue

        if audio is not None:
            # print(audio)
            mb_id = ""

            if file_path.suffix.lower() == '.mp3':
                try:
                    mb_id = audio.tags.getall('TXXX:MusicBrainz Release Track Id')[0]
                    if type(mb_id) != str:
                        mb_id = mb_id.text[0]
                except:
                    mb_id = audio.tags.getall('UFID:http://musicbrainz.org')[0].data.decode('utf-8')
            elif file_path.suffix == '.m4a':
                try:
                    mb_id = audio.tags['----:com.apple.iTunes:MusicBrainz Release Track Id'][0].decode('utf-8')
                    if not mb_id:
                        raise ValueError("empty mbid")
                except:
                    mb_id = audio.tags['----:com.apple.iTunes:MusicBrainz Track Id'][0].decode('utf-8')
            elif file_path.suffix in ['.flac', '.opus']:
                try:
                    mb_id = audio.tags['musicbrainz_releasetrackid'][0]
                    if not mb_id:
                        raise ValueError("empty mbid")
                except:
                    mb_id = audio.tags['musicbrainz_trackid'][0]


            if mb_id:
                # print(str(mb_id))
                output_file = output_path.joinpath(str(mb_id)+'.json')
                if not output_file.is_file():
                    # print(file_path)
                    a_feats = None
                    try:
                        # time.sleep(3)
                        a_feats = get_audio_features(str(file_path))
                    except Exception as e:
                        print("Feats error:", file_path, e)

                    if a_feats is not None:
                        with open(output_file, "w") as json_file:
                            json.dump(a_feats, json_file, indent=4, cls=CustomEncoder)
                            print("Feats saved:", output_file)
                    # print(a_feats)

            else:
                print("Empty ID:", file_path)
                print(audio)
                break
        else:
            print('No Audio:', file_path)
            # file_path.unlink()

print(skipped_ext)