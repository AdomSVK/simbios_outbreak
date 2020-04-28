import json

from numpy import unicode

with open('data/SR_virus_spread_across_unicipalities_v17april_MRandMGmodel.json') as f:
    data = json.load(f)

print(data)

