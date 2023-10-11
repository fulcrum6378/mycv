from typing import Optional

bitmap_folder: str = '2'
# red pillow: 1689005849386887(2), 1689005849796309(2), 1689005850214842(-), 1689005850617867(1), 1689005851028798(2)
# shoes:      1689005891979733, 1689005892490340
# 1689005850214842 is blurred and segments are not detected even with `min_seg = 1`
bitmap: str = '1689005849386887'
dim: int = 1088

# /segmentation/
min_seg: int = 40

# /tracing/
max_export_segments: int = 10
display_segment: Optional[int] = None
shape_path_bytes: int = 1  # Byte=>1, Short=>2 - ONLY CHANGE THIS!
shape_path_max: float = {1: 256.0, 2: 65535.0, }[shape_path_bytes]
shape_path_type: str = {1: 'B', 2: '<H', }[shape_path_bytes]

# /comparison/
y_radius, u_radius, v_radius, rt_radius = 6, 2, 4, 2

# /debug/
server_address = "192.168.1.20"
