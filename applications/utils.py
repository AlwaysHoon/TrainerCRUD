'''
for interface
'''
import time
import unicodedata
import re

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

def validate_email(email):
        if not isinstance(email, str):
            return False
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.fullmatch(pattern, email) is not None

def progress_bar(len, sleep=0.001):
    total=100
    for current in range(total + 1):
        progress = current / total
        filled = int(progress * len)

        bar = "█" * filled + " " * (len - filled)
        print(f"\r|{bar}|", end="", flush=False)
        # print(f"\r|{bar}| {progress * 100:.1f}%", end="", flush=True)

        time.sleep(sleep)
    print('\n')
    
if __name__ == "__main__":
    progress_bar(40, 0.003)