import os

from storage.sf2_global import dir_frame, read_sequence_file, sk

for f in sorted(os.listdir(dir_frame), key=sk):
    # for sh in read_sequence_file(dir_frame, f):
    #    pass
    print(f, ':', read_sequence_file(dir_frame, f))
