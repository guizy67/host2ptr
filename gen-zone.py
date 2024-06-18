#!/usr/local/bin/python3

import json

with open('hostfile-converted-ptr-data.json') as f:
    data = json.load(f)


for item in data:
    zonefile = item[1]['zonename']+'.db'
    record = str(item[1]['ptr_record'])+'\n'

    with open(zonefile, 'a') as zf:
        zf.write(record)


