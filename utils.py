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
        
        if len(candidate) <= width:
            current = candidate
        
        else:
            if current:
                lines.append(current)
                current = item
        
    if current:
        lines.append(current)
    return lines
    
    
# machines  = ['Arnold Press', 'Behind Overhead Press', 'Cable Rever Fly', 'Face Pull', 'Front Raise' ]
# for i in wrap_machines(machines):
#     print(i, len(i))