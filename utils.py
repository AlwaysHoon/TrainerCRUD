'''
for interface
'''

import unicodedata


def align(word):
    count = sum(1 for i in word if unicodedata.east_asian_width(i) in 'WF')
    return count

def wrap(machines, width=45):
    lines=[]
    current=""
    
    for machine in machines:
        item = f"{machine}"
        candidate = f"{current}, {item}" if current else item
        
        if (len(candidate) + align(candidate)) <= width:
            current = candidate
        
        else:
            if current:
                lines.append(current)
                current = item
        
    if current:
        lines.append(current)
    return lines
    
# machines = ['가가', '나나', '다다', '라라', '가나다가나다', '가나다라마바사아', '가가가가' ]

# for i in wrap(machines):
#     print(i, len(i))

# machines2  = ['Arnold Press', 'Behind Overhead Press', 'Cable Rever Fly', 'Face Pull', 'Front Raise' ]
# for i in wrap(machines2):
#     print(i, len(i))