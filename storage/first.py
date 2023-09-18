import json
import os

import numpy as np


class Shape:
    def __init__(self, id_: str, y_: int, u_: int, v_: int, r_: int, ):
        self.id: str = id_
        self.y: int = y_
        self.u: int = u_
        self.v: int = v_
        self.r: int = r_  # ratio (width / height)


output_dir, ext = 'tracing/output/', '.json'
shapes: np.ndarray[Shape] = np.array([], dtype=Shape, ndmin=1)
for o in os.listdir(output_dir):
    if not o.endswith(ext): continue
    seg = json.loads(open(os.path.join(output_dir, o), 'r').read())
    y, u, v = seg['mean']
    w, h = seg['dimensions']
    # noinspection PyTypeChecker
    shapes = np.append(shapes, Shape(o[:-len(ext)], *seg['mean'], w / h))
print(shapes, shapes.shape)
