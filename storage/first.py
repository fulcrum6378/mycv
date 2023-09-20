import json
import os

import feature_database as fdb


class Shape:
    def __init__(self, id_: str, y_: int, u_: int, v_: int, r_: float):
        self.id: str = id_
        self.y: int = y_
        self.u: int = u_
        self.v: int = v_
        self.r: float = r_  # ratio (width / height)


# load data
output_dir, ext = os.path.join('tracing', 'output'), '.json'
shapes: list[Shape] = []
for o in os.listdir(output_dir):
    if not o.endswith(ext): continue
    seg = json.loads(open(os.path.join(output_dir, o), 'r').read())
    w, h = seg['dimensions']
    shapes.append(Shape(o[:-len(ext)], *seg['mean'], w / h))

shapes.sort(key=lambda s: s.u)
for s1 in shapes:
    # for s2 in s1:
    print(s1.__dict__)
