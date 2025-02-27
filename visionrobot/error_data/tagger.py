import json

f1 = open("v3_error_data.json")
j = json.load(f1)

new_json = {}

for idx, blub in enumerate(j):
    entry = {}
    entry['x'] = blub[0]
    entry['y'] = blub[1]
    entry['opti_dist'] = blub[2]
    entry['opti_angle'] = blub[3]
    entry['cam_dist'] = blub[4]
    entry['cam_angle'] = blub[5]
    entry['err_x'] = blub[6]
    entry['err_y'] = blub[7]
    entry['err_dist'] = blub[8]
    entry['err_angle'] = blub[9]
    new_json[str(idx)] = entry

with open('./v3_tagged_error_data.json', 'w') as f:   
    json.dump(new_json, f, indent=4)