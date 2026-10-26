import os
import json
from datetime import datetime

from .utils import *
from functools import wraps



class TrainerCRUD:
    def __init__(self, member_path):
        self.extra = None  # 부가 서비스 객체 (회원 삭제 시 락커/운동복 정리용)
        self.member_path = member_path
        self._yes = ("y","yes", "네", "예","ㅛ")
        self._no = ("n", "no", "아니오","ㅜ")
        try:
            with open(self.member_path, "r", encoding="utf-8") as f:
                self.members = json.load(f)
                
        except FileNotFoundError:
            self.members = []
            with open(self.member_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
                
    # user_id와 email은 중복불가
    # 동명이인의 경우 이름과 이메일이 모두 같을 때만 중복 처리
    def do_save(self):
        user_id = input("아이디를 입력하세요: ").strip()  # 영어, 숫자 합쳐서 10자이내
        if not self._check_id(user_id):
            return

        name = input("이름을 입력하세요: ").strip()
        email = input("이메일을 입력하세요: ").strip()
        if not self._check_email(name, email):
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
        
        print("-"*20)
        print(
            f"id\t: {user_id}\n"
            f"이름\t: {name}\n"
            f"e-mail\t: {email}")
        print("-"*20)
        is_save = input("위 정보가 맞습니까?(Y/N)").strip().lower()
        return self._add_member(is_save, new_member)
            
    def member_page(self, page=0, page_size=10):
        max_page = len(self.members) //10
        while True:
            start = page * page_size
            end = start + page_size
            page_list = self.members[start:end]
            self.do_retrive(page_list, page)
            
            curser = input()
            if curser == "<" and page > 0:
                page -= 1
                
            elif curser == ">" and page < max_page:
                page += 1
                
            elif curser == "^":
                print("검색 실행\n")
                return True
            
            elif curser == "9":
                print("이전으로 돌아갑니다.\n")
                return False
            
            elif curser == "0":
                print("프로그램을 종료합니다.\n")
                return "0"
            
            else:
                print("잘못된 접근입니다.\n")
           
    def do_retrive(self, members, page):
        print(f"{'=======전체 회원 리스트=======':^86}")
        for index, member in enumerate(members):
            
            if (index % 2) == 0:
                l = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
                if index == (len(members) - 1):
                    print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 2:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                    for i in range(len(l)):
                        l_key, l_value = l[i][0], l[i][1]
                        print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {' ':<15}:   {'':<23} |")
            else:
                r = [(key, value) for key, value in member.items() if key not in ("save_time", "modify_time")]
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for i in range(len(l)):
                    l_key, l_value, r_key, r_value = (l[i][0], l[i][1], r[i][0], r[i][1],)
                    print(f"| {l_key:<{15 - align(l_key)}}:   {l_value:<{23 - align(l_value)}} | {r_key:<{15 - align(r_key)}}:   {r_value:<{23 - align(r_value)}} |")
        print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
        print("[돌아가기: 9, 종료: 0]",f"{"< 이전 | ^검색 | 다음 >":^40}")
        return True
    
    def _find_same(self, key, value):
        return [member for member in self.members if member[key] == value]
    
    def do_select_one(self, select_num="2", search_num="1"):
        if self.members:
            # 단순조회/수정/삭제를 통합
            word = {"2": "조회", "3": "수정", "4": "삭제"}[select_num]
            
            if search_num == "1":
                select_member = input(f"{word} 할 회원 이름을 입력해주세요: ").strip()
                detail_member = self._find_same("name",select_member)
                
            elif search_num == "2":
                select_member = input(f"{word} 할 회원 ID를 입력해주세요: ").strip()
                detail_member = self._find_same("user_id", select_member)
                
            count = len(detail_member)
            
            # 동명이인 처리
            if count == 0:
                print("존재하지 않는 회원입니다.\n")
                return False
            
            # 중복이름이 없는 경우
            elif count == 1:
                print("ㅡ" * 20)
                for key, value in detail_member[0].items():
                    print(f"{key:<12}: {value:^10}")
                print("ㅡ" * 20)
                idx = 0
                if select_num == "2":  # 전체조회"2"->개인검색"1"
                    return detail_member[idx]

                elif select_num == "3":  # 정보수정"3"
                    is_modify = (input("수정하실 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_modify(is_modify, detail_member, idx, count)

                elif select_num == "4":  # 정보삭제"4"
                    is_delete = (input("삭제하실 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_delete(is_delete, detail_member, idx)

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
                    is_modify = (input("수정하실 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_modify(is_modify, detail_member, idx, count)

                elif select_num == "4":  # 정보삭제"4"
                    is_delete = (input("삭제하실 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_delete(is_delete, detail_member, idx)
                           
        else:
            print("등록된 회원이 없습니다.")
            return False
    
    #save가 안됨
    # 수정 후 중복 체크
    def modify_member(self, select_member, check_member):
        print("\n회원 정보 수정을 시작합니다.\n")
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[name, email, ...]: ").strip()
            if modify_key in select_member:
                for member in self.members:
                    if member == select_member:
                        while True:
                            modify_value = input(f"기존 {modify_key}는 {select_member[modify_key]}입니다. 변경할 내용을 적어주세요(9:이전으로): ")

                            # 중복처리
                            if modify_key == "email":
                                if modify_value == "9":
                                    print()
                                    return True
                                elif self._check_email(member["name"],modify_value):
                                    break
                                
                            elif (modify_key != "name") and (modify_value in [member[modify_key] for member in self.members]):
                                print(f"이미 존재하는 {modify_key}입니다.\n")

                            elif modify_key == "name":  # 동명이인은 이메일로 비교
                                for mem in check_member:
                                    if member["email"] == mem["email"]:
                                        print(f"이미 존재하는 {modify_key}입니다.\n")
                            else:
                                break

                        is_modify = (input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower())
                        if is_modify in self._yes:
                            member[modify_key] = modify_value
                            member["modify_time"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            print(f"{modify_key} 변경에 성공했습니다.")
                            return True

                        else:
                            print("\n이전으로 돌아갑니다.\n")

            else:  # str잘못입력한 경우 재진입 기회 제공
                print("잘못된 접근입니다.")
                while True:
                    is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                    if is_continue in self._yes:
                        print()
                        break
                    elif is_continue in self._no:
                        return
                    else:
                        print("잘못 입력했습니다.")
    
        #================================================================================================================
    def modify_member2(self, select_member, check_member):
            print("\n회원 정보 수정을 시작합니다.\n")
            while True:
                modify_key = input("수정할 정보를 선택해주세요?[name, email, ...]: ").strip()
                if modify_key in select_member:
                    for member in self.members:
                        if member == select_member:
                            while True:
                                modify_value = input(f"기존 {modify_key}는 {select_member[modify_key]}입니다. 변경할 내용을 적어주세요(9:이전으로): ")
    
                                # 중복처리
                                if modify_key == "email":
                                    if modify_value == "9":
                                        print()
                                        return True
                                    elif self._check_email(member["name"],modify_value):
                                        break
                                    
                                elif (modify_key != "name") and (modify_value in [member[modify_key] for member in self.members]):
                                    print(f"이미 존재하는 {modify_key}입니다.\n")
    
                                elif modify_key == "name":  # 동명이인은 이메일로 비교
                                    for mem in check_member:
                                        if member["email"] == mem["email"]:
                                            print(f"이미 존재하는 {modify_key}입니다.\n")
                                else:
                                    break
    
                            is_modify = (input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower())
                            if is_modify in self._yes:
                                member[modify_key] = modify_value
                                member["modify_time"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                print(f"{modify_key} 변경에 성공했습니다.")
                                return True
    
                            else:
                                print("\n이전으로 돌아갑니다.\n")
    
                else:  # str잘못입력한 경우 재진입 기회 제공
                    print("잘못된 접근입니다.")
                    while True:
                        is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                        if is_continue in self._yes:
                            print()
                            break
                        elif is_continue in self._no:
                            return
                        else:
                            print("잘못 입력했습니다.")
                            
                            
    #================================================================================================================
    def do_sort(self, keys, rev=False):
        return self.members.sort(key=lambda x:x[keys], reverse=rev)        
    
    def _save_members(self):
        with open(self.member_path, mode="w", encoding="utf-8") as f:
            json.dump(self.members, f, ensure_ascii=False, indent=4)
    
    def _check_yn(func):
        @wraps(func)
        def decorated(self, is_yes, *args, **kwargs):
            while True:
                if is_yes in self._yes:
                    return func(self, *args, **kwargs)
                elif is_yes in self._no:
                    print("이전으로 돌아갑니다.\n")
                    return False
                else:
                    print("잘못 입력했습니다.\n")
                    is_yes = input("다시 입력해주세요(Y/N): ").strip().lower()
        return decorated 
    
    def _check_id(self,user_id):
        if not validate_user(user_id):
            print("아이디 형식이 잘못되었습니다.\n")
            return False
        
        if any(member["user_id"] == user_id for member in self.members):
            print("이미 존재하는 아이디입니다.\n")
            return False
        return True
    
    def _check_email(self, name, email):
        if not validate_email(email):
            print("이메일 형식이 아닙니다.\n")
            return False
        
        for member in self.members:
            if member["email"] == email:
                print("이미 존재하는 이메일입니다.\n")
                return False

            elif (member["name"] == name) and (member["email"] == email):
                print("이미 등록되어 있습니다.\n")
                return False
        return True
    @_check_yn
    def _add_member(self, member):
        self.members.append(member)
        self._save_members()
        print(f"{member['name']}님 등록에 성공했습니다.(id: {member['user_id']})\n")
        return True
    
    @_check_yn
    def do_modify(self, member, idx, count):
        if count >1:
            check_member = [v for i, v in enumerate(member) if i != idx]
            self.modify_member(member[idx], check_member)
        elif count == 1:
            self.modify_member(member[idx], member[idx])
            
        self._save_members()
        return True
    
    # 회원 삭제 시 부가서비스, 식단, 운동기록의 삭제도 필요함
    # 세 json이 담긴 폴더를 통째로 삭제 추가 필요
    @_check_yn
    def do_delete(self, member, idx):       
        deleted_member = member[idx]
        self.members.remove(deleted_member)
        self._save_members()
        print("회원 삭제에 성공했습니다.\n")

        if self.extra:
            self.extra.remove_member_data(deleted_member['user_id'])
        return True
    
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

