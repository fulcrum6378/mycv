import os

# configurations
width = 1088
height = 1088
dimensions = str(width) + 'x' + str(height)
frame_size = {
    '1088x1088': 3551232
}

# create a folder with the highest ordinal name
num = 1
for i in os.listdir('vis'):
    try:
        ii = int(i)
        if ii > num: num = ii
    except ValueError:
        pass
num += 1
os.mkdir('vis/' + str(num))

# read the metadata
with open('vis/metadata/' + dimensions, 'rb') as f:
    metadata: bytes = f.read()

# extract the raw RGB file
frame_length = frame_size[dimensions]
with open('vis/vis.rgb', 'rb') as rgb:
    f = 1
    while frame_data := rgb.read(frame_length):
        with open('vis/' + str(num) + '/' + str(f) + '.bmp', 'wb') as frame:
            frame.write(metadata + frame_data)
        f += 1
