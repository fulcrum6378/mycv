import json
import os

import feature_database as fdb

# initialise databases
db_y, db_u, db_v = fdb.FeatureDB('y'), fdb.FeatureDB('u'), fdb.FeatureDB('v')
db_ratio = fdb.FractionalFeatureDB('ratio')

# load data
input_dir, ext_json = os.path.join('tracing', 'output'), '.json'
for o in os.listdir(input_dir):
    if not o.endswith(ext_json): continue
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    w, h = seg['dimensions']
    sid = int(o[:-len(ext_json)])  # id
    seg['path']

    if seg['mean'][0] not in db_y.data: db_y.data[seg['mean'][0]] = set()
    db_y.data[seg['mean'][0]].add(sid)
    if seg['mean'][1] not in db_u.data: db_u.data[seg['mean'][1]] = set()
    db_u.data[seg['mean'][1]].add(sid)
    if seg['mean'][2] not in db_v.data: db_v.data[seg['mean'][2]] = set()
    db_v.data[seg['mean'][2]].add(sid)

    w / h  # ratio

# TODO WE STORED FEATURES OF SHAPES. NOW HOW TO STORE SHAPES?!?
