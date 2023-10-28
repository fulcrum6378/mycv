from storage.sf2_global import read_frames_file_with_ranges, read_pif_index

for fid, rng in read_frames_file_with_ranges().items():
    print('Frame', fid, ':')
    pif: list[tuple[int, int]] = read_pif_index(fid)
    i = 0
    for sid in rng:
        print(sid, ':', pif[i])
        i += 1
