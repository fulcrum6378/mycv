import os

from storage.sf2_global import dir_frame, read_sequence_file, sk

# TODO remove dir_frame and specify 2-bit start IDs in a single file called "frames"
# TODO Sequence Files should be abolished and indexes be transferred to RAM!

for f in sorted(os.listdir(dir_frame), key=sk):
    # for sh in read_sequence_file(dir_frame, f):
    #    pass
    print(f, ':', read_sequence_file(dir_frame, f))
