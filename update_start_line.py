import boto3
import json

start_line_dict = {1: [120, 1280, '^'],
                   2: [-1341, 2800, '<'],
                   3: [-1228, 100, '<'],
                   4: [-1533, -650, '<'],
                   5: [2633, 128, '>'],
                   6: [25, -469, '<'],
                   7: [-8065, -6549, '^'],
                   8: [700, 350, '>'],
                   9: [3700, 800, 'v']
}

for i in range(1,23):
    if i in start_line_dict:
        continue
    else:
        start_line_dict[i] = [0, 0, '<']
        
with open('data/start_line_dict.json', 'w') as f:
    json.dump(start_line_dict, f, indent=4)
    
session = boto3.Session()
s3 = boto3.resource('s3')

s3.Bucket('f1-jedha-bucket').upload_file('/home/guillaume/Python_Projects/Jedha_F1_Project/data/start_line_dict.json', 'data/start_line_dict.json', ExtraArgs={'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'})