from datetime import datetime

read_time = datetime.now()
f = open("segmentation/output/rg2_pixels.pickle", "rb")  # example of a big file (44mb)
f.seek(100)
x = f.read(3)
f.close()
print('Offset read time:', datetime.now() - read_time)  # 0:00:00 (44MB), 0:00:00 (699MB, a movie)
print(x)

read_time = datetime.now()
f = open("segmentation/output/rg2_pixels.pickle", "rb")
x = f.read()[100:103]
f.close()
print('Complete read time:', datetime.now() - read_time)  # 0:00:00.043871, 0:00:02.274496 (699MB)
print(x)  # I am using an SSD.
