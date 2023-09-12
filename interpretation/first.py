import pickle


class Pixel: pass


pixels: list[Pixel] = pickle.load(open('segmentation/output/rg2_pixels.pickle', 'rb'))
segments: dict[int, list[int]] = pickle.load(open('segmentation/output/rg2_segments.pickle', 'rb'))
print(pixels[0].__dict__)
print(segments[0])
