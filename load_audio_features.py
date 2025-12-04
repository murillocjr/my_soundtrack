import json
from env import DATA_PATH, AUDIO_FEATURES_PATH
from pathlib import Path
import pandas as pd

output_path = Path(AUDIO_FEATURES_PATH)

file_path = DATA_PATH + 'lib_stats_bkp_musicbrainz_trackid.txt'
with open(file_path, 'r') as file:
    musicbrainz_trackid = file.read().splitlines()

df_all = None
for index, mb_id in enumerate(musicbrainz_trackid):

    output_file = output_path.joinpath(str(mb_id) + '.json')
    with open(output_file, 'r') as f:
        data = json.load(f)
    data['mbid'] = mb_id
    df = pd.DataFrame([data])
    if df_all is None:
        df_all = df
    else:
        df_all = pd.concat([df_all, df], ignore_index=True)

print(len(df_all))
print(df_all.head())

df_all.to_csv(AUDIO_FEATURES_PATH + '/audio_features.csv', index=False)