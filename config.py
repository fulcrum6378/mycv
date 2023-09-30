from typing import Optional

bitmap_folder: str = '2'
# red pillow: 1689005849386887(2), 1689005849796309(2), 1689005850214842(-), 1689005850617867(1), 1689005851028798(2)
# shoes:      1689005891979733, 1689005892490340
# 1689005850214842 is blurred and segments are not detected even with `min_seg = 1`
bitmap: str = '1689005849386887'
dim: int = 1088

# /segmentation/
min_seg: int = 100

# /tracing/
max_export_segments: int = 10
display_segment: Optional[int] = None

# /comparison/
y_radius, u_radius, v_radius, rt_radius = 6, 2, 4, 2
