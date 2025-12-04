from env import DATA_PATH, AUDIO_FEATURES_PATH
from pathlib import Path

output_path = Path(AUDIO_FEATURES_PATH)

file_path = DATA_PATH + 'lib_stats_bkp_musicbrainz_trackid.txt'
with open(file_path, 'r') as file:
    musicbrainz_trackid = file.read().splitlines()
#
file_path = DATA_PATH + 'lib_stats_bkp_path.txt'
with open(file_path, 'r') as file:
    paths = file.read().splitlines()

print(len(musicbrainz_trackid))

for index, mb_id in enumerate(musicbrainz_trackid):

    output_file = output_path.joinpath(str(mb_id) + '.json')

    if not output_file.is_file():
        print(output_file)
        print(paths[index])
        break