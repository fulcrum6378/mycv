import json
import os

# load data from the /tracing/ section
input_dir, ext_json = os.path.join('tracing', 'output'), '.json'
for o in os.listdir(input_dir):
    if not o.endswith(ext_json): continue
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    w, h = seg['dimensions']
    sid = int(o[:-len(ext_json)])  # id
    seg['path']
    seg['mean']
    w / h  # ratio

# TODO USE FILES AND FOLDERS INSTEAD AND WRITE IDS IN SEQUENCE BINARY FILES!
