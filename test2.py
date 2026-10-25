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
member_path = os.path.join(DATA_DIR, "members.json")

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
    
member_page(members,0)