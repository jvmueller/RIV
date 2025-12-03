import subprocess
import json


test = subprocess.check_output(['curl', 'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/-122.418563,37.751659;-122.422969,37.75529;-122.426904,37.759617?&annotations=distance&access_token=pk.eyJ1IjoicmF5cmF5MSIsImEiOiJjbWlwOXcwcGowMng5M2Rwc3BhcHNlcXN1In0.sI8bIOdD0QZ3H_eMGtBogg'])
x = json.loads(test.decode('ascii'))





'''
y = ""
for i in x:
    if i != '\\':
        y += i
'''

#pk.eyJ1IjoicmF5cmF5MSIsImEiOiJjbWlwOXcwcGowMng5M2Rwc3BhcHNlcXN1In0.sI8bIOdD0QZ3H_eMGtBogg


with open("test.json", "w") as json_file:
    json.dump(x, json_file)

