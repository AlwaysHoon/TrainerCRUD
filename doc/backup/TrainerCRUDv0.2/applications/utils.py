'''
for interface
'''
import time
import unicodedata
import re
import os

def validate_user(user_id):
    if not isinstance(user_id, str):
        return False
    pattern = r"^[A-Za-z0-9]{2,10}$"
    return re.fullmatch(pattern, user_id) is not None

def validate_name(name):
    if not isinstance(name, str):
        return False
    pattern = r"^(?:[가-힣]{2,}|[A-Za-z]{2,}\s+[A-Za-z]{2,})$"
    return re.fullmatch(pattern, name) is not None

def validate_email(email):
    if not isinstance(email, str):
        return False
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

def align(word):
    kor_word = str(word)
    count = sum(1 for i in kor_word if unicodedata.east_asian_width(i) in 'WF')
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

def progress_bar(len, sleep=0.001):
    total=100
    for current in range(total + 1):
        progress = current / total
        filled = int(progress * len)

        bar = "█" * filled + " " * (len - filled)
        print(f"\r|{bar}|", end="", flush=False)

        time.sleep(sleep)
    print('\n')
def delete_data(self, user_id):
    path = self.get_path(user_id)
    folder = self.get_folder(user_id)

    try:
        os.remove(path)
        print("파일 삭제 완료.\n")

    except FileNotFoundError:
        print("파일이 존재하지 않습니다.\n")
        return False

    except OSError as e:
        print(f"파일 삭제 실패: {e}\n")
        return False

    try:
        os.rmdir(folder)
        print("빈 폴더 삭제 완료.\n")

    except OSError:
        pass  # 폴더에 다른 파일이 남아 있다면 유지

    return True


if __name__ == "__main__":
    progress_bar(40, 0.001)
    progress_bar(100, 0.005)