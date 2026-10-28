import time
import os
import json
import unicodedata
def align(word):
    count = sum(1 for i in word if unicodedata.east_asian_width(i) in 'WF')
    return count

def do_retrive():
    if members:
        print(f"{'=======전체 회원 리스트=======':^86}")
        for index, member in enumerate(members):
            if (index % 2) == 0:
                l = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
                if index == (len(members) - 1):
                    print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 2:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                    for i in range(len(l)):
                        l_key, l_value = l[i][0], l[i][1]
                        print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {' ':<15}:   {'':<23} |")
            else:
                r = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for i in range(len(l)):
                    l_key, l_value, r_key, r_value = (l[i][0], l[i][1], r[i][0], r[i][1],)
                    print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {r_key:<{15 - align(r_key)}}:   {r_value:<{23 - align(r_value)}} |")
        print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
        print(f"{"< 이전 | 검색 | 다음 >":^85}")
        return True

    else:
        print("등록된 회원이 없습니다.")
        return False
def do_retrive2(members):

    print(f"{'=======전체 회원 리스트=======':^86}")
    for index, member in enumerate(members):
        if (index % 2) == 0:
            l = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
            if index == (len(members) - 1):
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 2:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for i in range(len(l)):
                    l_key, l_value = l[i][0], l[i][1]
                    print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {' ':<15}:   {'':<23} |")
        else:
            r = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
            print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
            for i in range(len(l)):
                l_key, l_value, r_key, r_value = (l[i][0], l[i][1], r[i][0], r[i][1],)
                print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {r_key:<{15 - align(r_key)}}:   {r_value:<{23 - align(r_value)}} |")
    print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
    
    print(f"{"< 이전 | ^검색 | 다음 >":^85}")
    return True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # C:\Users\jihun\Archive\aicon\mini_project
DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
member_path = os.path.join(DATA_DIR, "members2.json")

with open(member_path, "r", encoding="utf-8") as f:
    members = json.load(f)

# do_retrive2(members)

# # print(len(members))
# page_max = len(members) // 10 + 1
# page_size = 10
# for page in range(page_max):
#     start = page * page_size
#     end = start + page_size
#     print(start, end)
#     page_list = members[start:end]
#     do_retrive2(page_list)
#     input()

def member_page(members, page, page_size=10):
    max_page = len(members) //10
    print(max_page)
    print(len(members))
    start = page * page_size
    end = start + page_size
    page_list = members[start:end]
    do_retrive2(page_list)
    curser = input()
    if (curser == "<") and (page != 0):
        page -= 1
        member_page(members, page)
    elif (curser == ">") and (page != max_page):
        page += 1
        member_page(members, page)
        
    elif curser == "^":
        print("검색 실행")
        return
    else:
        member_page(members, page)
    
# member_page(members,0)
def save_members(member_path, members):
    with open(member_path, mode="w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=4)
        
def do_sort(keys, rev=False):
    return members.sort(key=lambda x:x[keys], reverse=rev)
    
    
    
    
def do_modify(self, member):
    user_id = member["아이디"]
    details = self._read_data(user_id)

    existing = next((d for d in details if d["아이디"] == user_id),None)

    if existing is None:
        print("등록된 신체 정보가 없습니다.\n")
        return False

    print(f"\n{member['이름']}님의 기존 정보")
    self.show_details(member)

    height = input(f"키를 입력하세요(cm, 기존: {existing['키']}): ").strip()

    weight = input(f"몸무게를 입력하세요(kg, 기존: {existing['몸무게']}): ").strip()

    # 입력하지 않은 항목은 기존 값 유지
    new_details = existing.copy()

    if height:
        new_details["키"] = height

    if weight:
        new_details["몸무게"] = weight

    new_details["최근 수정일"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")

    print("\n수정할 정보")
    print("-" * 40)
    for key, value in new_details.items():
        print(f"{key:<{12-align(key)}}: {value}")
    print("-" * 40)

    is_modify = input("위 정보로 수정하시겠습니까?(Y/N): ").strip().lower()

    return self._update_details(is_modify, member, new_details)
