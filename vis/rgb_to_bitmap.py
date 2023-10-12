import os

# configurations
root = 'vis'
width = 1088
height = 1088
dimensions = str(width) + 'x' + str(height)
frame_size = {
    '1088x1088': 3551232
}

# create a folder with the highest ordinal name
num = 1
for i in os.listdir(os.path.join('vis', 'output')):
    try:
        ii = int(i)
        if ii > num: num = ii
    except ValueError:
        pass
num += 1
os.mkdir(os.path.join(root, 'output', str(num)))

# read the metadata
with open(os.path.join(root, 'metadata', dimensions), 'rb') as f:
    metadata: bytes = f.read()

# extract the raw RGB file
frame_length = frame_size[dimensions]
with open(os.path.join(root, 'temp', 'vis.rgb'), 'rb') as rgb:
    f = 1
    while frame_data := rgb.read(frame_length):
        with open(os.path.join(root, 'output', str(num), str(f) + '.bmp'), 'wb') as frame:
            frame.write(metadata + frame_data)
        f += 1
