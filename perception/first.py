from storage.sf2_global import read_frames_file

for fid, rng in read_frames_file().items():
    print(fid, ':', rng)
