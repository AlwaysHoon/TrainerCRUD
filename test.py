import json
import os
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
member_path = os.path.join(DATA_DIR, 'members.json')

with open(member_path, "r", encoding='utf-8') as f:
    members = json.load(f)
# print(members)
print(members)
# print(members[-1]['user_id'][:6])
print(bool(members))
# a = members[-1]['user_id']
print(len("=======================")    )

# if a[:6] == str(datetime.now().strftime("%y%m%D")):
#     count = int(a[6:]) + 1
# else:
#     count = 0
    
# print(count)