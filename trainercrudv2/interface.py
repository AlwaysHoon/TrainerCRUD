from ..applications.utils import align, progress_bar
from member import *
import os

def trainer_interface(members):
    
    while True:
        manage_mod = "========회원 관리 모드========"
        line3 = len(manage_mod) + align(manage_mod)
        print(manage_mod)
        print(
            " 1. 회원 등록\n"
            " 2. 전체 회원 조회\n"
            " 3. 회원 정보 수정\n"
            " 4. 회원 삭제\n"
            " o. 이전으로\n"
            " p. 프로그램 종료")
        print("=" * line3)
        
        select_num = input("번호를 입력하세요: ").strip()
        print()

        if select_num == "1":
            print("1. 회원 등록을 선택하셨습니다.\n")
            members.do_save()

        elif select_num == "2":
            print("2. 전체 회원 조회를 선택하셨습니다.")
            progress_bar(line3)
            if not search_interface(members, select_num):
                return False

        elif select_num == "3":
            print("3. 회원 정보 수정을 선택하셨습니다.\n")
            if not search_interface(members, select_num):
                return False
            
        elif select_num == "4":
            print("4. 회원 삭제를 선택하셨습니다.\n")
            if not search_interface(members, select_num):
                return False

        elif select_num in ("o", "ㅐ"):
            print("이전으로 돌아갑니다.\n")
            return True

        elif select_num in ("p", "ㅔ"):
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")

def search_interface(members, select_num):
    count = True
    while True:
        if members:
            if select_num == "2" or count:
                count = False
                member_list = members.member_page(0)
                if not member_list:
                    return True
                if member_list == "0":
                    return False
                
            search_mod = "========회원 검색 모드========"
            line3 = len(search_mod) + align(search_mod)
            print(search_mod)
            print(
                " 1. 회원 이름으로 검색\n"
                " 2. 회원 ID로 검색\n"
                " 3. 회원 리스트\n"
                " 4. 리스트 정렬\n"
                " o. 이전으로\n"
                " p. 프로그램 종료")
            print("=" * line3)
            
            search_num = input("번호를 선택하세요: ").strip()
            
            mod = {'1': '1. 회원 이름으로 검색', '2': '2. 회원 ID로 검색'}
            if (search_num == "1") or (search_num == "2"):
                print(f"{mod[search_num]}을 시작합니다.")
                detail_member = members.do_select_one(select_num, search_num)
                
                if not detail_member: # members.json에 없는 member를 입력했을 때 False반환
                    continue
                # if select_num == "2" and (not member_interface(detail_member, workout, diets, detail_sys)):
                    # return False
                print("검색완료")
            elif search_num == "3":
                count = True
            
            elif search_num == "4":
                print("1.아이디, 2.이름, 3.이메일, 4.최초 등록일, 5.최근 수정일")
                try:
                    sort_input = int(input("원하는 정렬 번호를 입력해주세요: "))
                except ValueError:
                    print("숫자를 입력해주세요.\n")
                else:
                    sort_keys=["아이디","이름","email","최초 등록일","최근 수정일"]
                    is_reverse = int(input("1.내림차순, 2.오름차순 선택해주세요: "))
                    if is_reverse == 1:
                        members.do_sort(sort_keys[sort_input-1], rev=True)
                        
                    elif is_reverse == 2:
                        members.do_sort(sort_keys[sort_input-1], rev=False)
                        
                    else:
                        print("잘못 입력했습니다.\n")             
                
            elif search_num in ("o", "ㅐ"):
                print("이전 화면으로 돌아갑니다.\n")
                return True

            elif search_num in ("p", "ㅔ"):
                print("프로그램을 종료합니다.\n")
                return False

            else:
                print("잘못된 접근입니다.\n")
                
        else:
            print("등록된 회원이 없습니다.\n")
            return False


if __name__ == "__main__":
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    # DATA_DIR = os.path.join(BASE_DIR, "data")
    # MEMBER_PATH = os.path.join(DATA_DIR, "members.json")
    
    # os.makedirs(DATA_DIR, exist_ok=True)
    
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    MEMBER_PATH = DATA_DIR / "members.json"
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    member = MemberCRUD(MEMBER_PATH)
    
    print()