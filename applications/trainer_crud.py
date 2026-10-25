import os
import json
from datetime import datetime

from .utils import *


class TrainerCRUD:
    def __init__(self, member_path):
        self.extra = None  # 부가 서비스 객체 (회원 삭제 시 락커/운동복 정리용)
        self.member_path = member_path
        
        try:
            with open(self.member_path, "r", encoding="utf-8") as f:
                self.members = json.load(f)
                
        except FileNotFoundError:
            self.members = []
            with open(self.member_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    # 동명이인의 경우 이름과 이메일이 모두 같을 때만 중복 처리
    # user_id와 email은 세상에 단 하나밖에 없다는 가정       
    def do_save(self):
        # 이름(한글or영어) 양식 의논
        # 분할시켜서 각 입력란에 배치해도됨 추후 논의(선택사항)
        user_id = input("아이디를 입력하세요: ").strip()  # 영어, 숫자 합쳐서 10자이내

        # if not validate_user(user_id):
        #     print("아이디 형식이 잘못되었습니다.")
        #     return False
        if any(member["user_id"] == user_id for member in self.members):
            print("이미 존재하는 아이디입니다.")
            return

        name = input("이름을 입력하세요: ").strip()
        email = input("이메일을 입력하세요: ").strip()

        if not validate_email(email):
            print("이메일 형식이 아닙니다.")
            return
        
        for member in self.members:
            if member["email"] == email:
                print("이미 존재하는 이메일입니다.")
                return

            elif (member["name"] == name) and (member["email"] == email):
                print("이미 등록되어 있습니다.")
                return

        # 최초 등록일, 최근 수정일
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        save_time = str(today)
        modify_time = str(today)

        new_member = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "save_time": save_time,
            "modify_time": modify_time,
        }

        # 전체 멤버 데이터베이스(members.json)에 새 멤버 등록
        self.members.append(new_member)
        with open(self.member_path, mode="w", encoding="utf-8") as f:
            json.dump(self.members, f, ensure_ascii=False, indent=4)

        print(f"{name}님 등록에 성공했습니다.(id: {user_id})\n")
        return True
    
    def member_page(self, page, page_size=10):
        max_page = len(self.members) //10
        start = page * page_size
        end = start + page_size
        page_list = self.members[start:end]
        self.do_retrive(page_list)
        curser = input()
        if (curser == "<") and (page != 0):
            page -= 1
            self.member_page(page)
            
        elif (curser == ">") and (page != max_page):
            page += 1
            self.member_page(page)
            
        elif curser == "^":
            print("검색 실행\n")
            return True
        
        elif curser == "9":
            print("이전으로 돌아갑니다.\n")
            return False
        
        else:
            self.member_page(page)
            
            
    def do_retrive(self, members):
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


    # 회원 삭제 시 부가서비스, 식단, 운동기록의 삭제도 필요함
    # 세 json이 담긴 폴더를 통째로 삭제 추가 필요
    def do_select_one(self, select_num="2", search_num="1"):
        if self.members:
            # 단순조회/수정/삭제를 통합
            count = 0
            detail_member = []
            word = {"2": "조회", "3": "수정", "4": "삭제"}[select_num]
            
            if search_num == "1":
                select_member = input(f"{word} 할 회원 이름을 입력해주세요: ").strip()
                for member in self.members:
                    if select_member == member["name"]:
                        count += 1
                        detail_member.append(member)
            
            elif search_num == "2":
                select_member = input(f"{word} 할 회원 ID를 입력해주세요: ").strip()
                for member in self.members:
                    if select_member == member["user_id"]:
                        count = 1
                        detail_member.append(member)
                        break
            
            # 동명이인 처리
            if count == 0:
                print("존재하지 않는 회원입니다.")
                return False
            
            # 중복이름이 없는 경우
            elif count == 1:
                print("ㅡ" * 20)
                
                for key, value in detail_member[0].items():
                    print(f"{key:<12}: {value:^10}")
                print("ㅡ" * 20)

                if select_num == "2":  # 전체조회"2"->개인검색"1"
                    return detail_member[0]

                elif select_num == "3":  # 정보수정"3"
                    is_modify = (
                        input("수정하실 정보가 맞습니까?(Y/N): ").strip().lower()
                    )

                    if is_modify in ("y", "yes", "예", "네"):
                        self.modify_member(detail_member[0], detail_member[0])

                        with open(self.member_path, mode="w", encoding="utf-8") as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False

                elif select_num == "4":  # 정보삭제"4"
                    is_delete = (input("삭제하실 정보가 맞습니까?(Y/N): ").strip().lower())

                    if is_delete in ("y", "yes", "예", "네"):
                        deleted_member = detail_member[0]
                        self.members.remove(detail_member[0])

                        with open(self.member_path, mode="w", encoding="utf-8") as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        print("회원 삭제에 성공했습니다.")
                        if self.extra:
                            self.extra.remove_member_data(deleted_member['user_id'])
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False

            # 동명이인(2인이상 모두 탐지)
            else:
                print("동명이인이 존재합니다.\n")
                progress_bar(45,0.001)
                print(f"{'=======동명이인 리스트=======':^40}")
                for i, m in enumerate(detail_member):
                    print(f"+ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{i + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ+")
                    for key, value in m.items():
                        print(f"| {key:<12}: {value:^26} |")
                print("+ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ+")

                while True:
                    same_num = input(f"조회할 번호를 선택하세요(1~{len(detail_member)}, 9:이전으로): ").strip()

                    if same_num.isdigit():
                        if (int(same_num) >= 1) and (int(same_num) <= len(detail_member)):
                            break
                        elif int(same_num) == 9:
                            print("이전으로 돌아갑니다.\n")
                            return False
                        else:
                            print("범위 밖입니다.\n")

                    else:
                        print("숫자를 입력해주세요")

                idx = int(same_num) - 1

                print("ㅡ" * 20)
                for key, value in detail_member[idx].items():
                    print(f" {key:<15}: {value:^25}")
                print("ㅡ" * 20)

                if select_num == "2":  # 전체조회"2"->개인검색"1"
                    return detail_member[idx]

                elif select_num == "3":  # 정보수정"3"
                    is_modify = (input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower())
                    if is_modify in ("y", "yes", "예", "네"):
                        check_member = [v for i, v in enumerate(detail_member) if i != idx]
                        self.modify_member(detail_member[idx], check_member)
                        
                        with open(self.member_path, mode="w", encoding="utf-8") as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False

                elif select_num == "4":  # 정보삭제"4"
                    is_delete = (input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower())
                    if is_delete in ("y", "yes", "예", "네"):
                        deleted_member = detail_member[int(same_num)-1]
                        self.members.remove(detail_member[int(same_num) - 1])

                        with open(self.member_path, mode="w", encoding="utf-8") as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        print("회원 삭제에 성공했습니다.\n")

                        if self.extra:
                            self.extra.remove_member_data(deleted_member['user_id'])
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return True
        else:
            print("등록된 회원이 없습니다.")
            return False
        
    # 수정 후 중복 체크
    def modify_member(self, select_member, check_member):
        print("\n회원 정보 수정을 시작합니다.\n")
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[name, email, ...]: ").strip()
            if modify_key in select_member:
                for member in self.members:
                    if member == select_member:
                        while True:
                            modify_value = input(f"기존 {modify_key}는 {select_member[modify_key]}입니다. 변경할 내용을 적어주세요: ")

                            # 중복처리
                            if (modify_key != "name") and (modify_value in [member[modify_key] for member in self.members]):
                                print(f"이미 존재하는 {modify_key}입니다.")

                            elif modify_key == "name":  # 동명이인은 이메일로 비교
                                for mem in check_member:
                                    if member["email"] == mem["email"]:
                                        print(f"이미 존재하는 {modify_key}입니다.")
                            else:
                                break

                        is_modify = (input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower())
                        if is_modify in ("y", "yes", "예", "네"):
                            member[modify_key] = modify_value
                            member["modify_time"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            print(f"{modify_key} 변경에 성공했습니다.")
                            return True

                        else:
                            print("\n이전으로 돌아갑니다.\n")

            else:  # str잘못입력한 경우 재진입 기회 제공
                print("잘못된 접근입니다.")
                is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                if is_continue in ("y", "yes", "예", "네"):
                    print("\n")

                else:
                    return


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, "members.json")

    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(member_path):
        with open(member_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)
    
    train_sys = TrainerCRUD(member_path)
    a = input("num 1~5: ")
    if a == "1":
        train_sys.do_save()
    elif a == "2":
        train_sys.do_retrive()
    elif a == "3":
        train_sys.do_select_one("2","1")
    elif a == "4":
        train_sys.do_select_one("3","1")
    elif a == "5":
        train_sys.do_select_one("4","1")

