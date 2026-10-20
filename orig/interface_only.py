import os
import json

from trainer_crud import TrainerCRUD

def login_interface():
    # 대부분의 사이트는 id/pw를 한번에 입력해서 실패하면 다시 둘다 입력하게 하는데
    # 유사하게 구현할지 카운트만 같이하고 따로 할지 고민중
    print("========관리자===========")
    login_count = 0
    
    while True:
        login_id = input("관리자id: ").strip()
        if login_id != "admin":
            login_count += 1
            print(f"존재하지 않는 관리자입니다.({login_count}/5회 틀림)")
            if login_count >= 5:
                print("아이디 입력 횟수를 초과하였습니다.")
                return
        else:
            break
        
    while True:
        pw = input("관리자pw: ").strip()
        if pw != "0000":
            login_count += 1
            print(f"비밀번호가 틀렸습니다.({login_count}/5회 틀림)")
            
            if login_count >= 5:
                print("비밀번호 입력 횟수를 초과하였습니다.")
                return
        else:
            break
    print("========================")   

def trainer_interface(members):
    while True:        
        print(
            "\n=======회원 관리 모드=======\n"
            "1. 회원 등록\n"
            "2. 전체 회원 조회\n"
            "3. 회원 정보 수정\n"
            "4. 회원 삭제\n"
            "5. 프로그램 종료\n"
            "============================"
            )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")
        
        if select_num == "1":
            print("1. 회원 등록을 선택하셨습니다.\n")
            members.do_save()
            
                
        elif select_num == "2":
            print("2. 전체 회원 조회를 선택하셨습니다. ")
            if not search_interface(members):
                return False
            
        elif select_num == "3":
            print("3. 회원 정보 수정을 선택하셨습니다.")
            members.do_modify_one()
            
        elif select_num == "4":
            print("4. 회원 삭제를 선택하셨습니다.")
            members.do_delete_one()
            
        elif select_num == "5":
            print("프로그램을 종료합니다.\n")
            break
        else:
            print("잘못된 접근입니다.\n")
        
def search_interface(members):
    while True:
        members.do_retrive()
        
        print(
            "\n=======회원 검색 모드=======\n"
            "1. 회원 검색\n"
            "2. 이전으로\n"
            "3. 프로그램 종료\n"
            "============================"
            )
        search_num = input("번호를 선택하세요: ")
        if search_num == "1":
            print("1. 회원 검색을 시작합니다.")
            detail_member = members.do_select_one()
            
            if detail_member:
                if not detail_interface(detail_member):
                    return False
                
            else:
                pass
            
        elif search_num == "2":
            print("이전 화면으로 돌아갑니다.")
            return True
        elif search_num == "3":
            print("프로그램을 종료합니다.")
            return False
        else:
            print("잘못된 접근입니다.\n")
        
def detail_interface(member):
    see_more = input(f"{member['name']}님을 조회하시겠습니까?(Y/N): ").strip().lower()
    if see_more in ("y", "yes", "네", "예"):
        
        while True:    
            print(
                f"\n==========={member['name']}===========\n"
                "1. 상세 기록 조회\n"
                "2. 요구사항 조회\n"
                "3. 운동 기록 조회\n"
                "4. 식단 조회\n"
                "5. 이전으로\n"
                "6. 프로그램 종료\n"
                "==========================\n"
                )
            
            detail_num = input("조회할 내용(번호)을 선택해주세요: ").strip()
            if detail_num == "1":
                print("1. 상세 기록 조회를 선택하셨습니다.")
                for key, value in member.items():
                    print(f"{key:<10}: {value:^10}")
                #지금은 members.json의 내용들만 반환하지만 details.json을 추가함에 따라 변동될 예정
            elif detail_num == "2":
                print("2. 요구사항 조회를 선택하셨습니다.")
                
            elif detail_num == "3":
                print("3. 운동 기록 조회를 선택하셨습니다.")
                
            elif detail_num == "4":
                print("4. 식단 조회를 선택하셨습니다.")
                
            elif detail_num == "5":
                print("이전 화면으로 돌아갑니다.")
                return True
            
            elif detail_num == "6":
                print("프로그램을 종료합니다.\n")
                return False
            
            else:
                print("잘못된 접근입니다.\n")

class ExampleCRUD:
    def __init__(self, member_path):
        self.member_path = member_path
        with open(self.member_path, "r", encoding='utf-8') as f:
            self.members = json.load(f)  # load members.json
            
    def do_save(self):
        print("등록에 성공했습니다.")
        return True
        
    def do_retrive(self):
        print("=======전체 회원 리스트=======")
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        return True
    
    
    def do_select_one(self):
        print("aa님을 조회하였습니다.")
        return self.members[0]
        
    def do_modify_one(self):
        print("회원 정보 수정에 성공했습니다.")
        return True 
    
    def do_delete_one(self):
        print("회원 삭제에 성공했습니다.")
        return True
        



if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, 'members.json')
    # train_sys = TrainerCRUD(member_path)
    with open(member_path, "r", encoding='utf-8') as f:
                members = json.load(f)
    # if login_interface():
    #     trainer_interface(members)
    # train_sys = TrainerCRUD(member_path)
    train_sys = ExampleCRUD(member_path)
    trainer_interface(train_sys)
