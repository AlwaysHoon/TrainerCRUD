import os
import json


from applications import TrainerCRUD, MachineList, ExtraServiceCRUD, WorkoutCRUD, DietCRUD
from applications.utils import *

def login_interface(): #만약 관리자가 많다면 클래스로 변경 및 id/pw에 대한 데이터파일과 검증코드를 만들었을 것이다.
    login_count = 0
    admin_login = "========관리자 로그인========"
    line1 = len(admin_login) + align(admin_login)
    print(admin_login)
    while True:
        # login_id = input(" 관리자id: ").strip()
        # login_pw = input(" 관리자pw: ").strip()
        login_id = "admin"
        login_pw = "0000"
        print(f" 관리자id: {login_id}")
        print(f" 관리자pw: {login_pw}")

        if login_id != "admin" or login_pw != "0000":
            login_count += 1
            print(f"존재하지 않는 관리자입니다.({login_count}/5회 틀림)")

            if login_count >= 5:
                print("아이디 입력 횟수를 초과하였습니다.\n")
                print("=" * line1)
                return
        else:
            print("=" * line1)
            print("로그인에 성공했습니다.")
            progress_bar(30, 0.003)

            return True


def admin_interface(members, machines, extra, workout, diets):
    while True:
        admin_mod = "========관리자 모드========"
        line2 = len(admin_mod) + align(admin_mod)
        print(admin_mod)
        print(
            " 1. 회원 관리\n"
            " 2. 운동 종목 관리\n"
            " 3. 부가 서비스 관리\n"
            " p. 프로그램 종료")
        print("=" * line2)

        select_num = input("번호를 입력하세요: ").strip()
        print()
        
        if select_num == "1":
            print("1. 회원 관리를 선택하셨습니다.\n")
            if not trainer_interface(members, workout, diets):
                return

        elif select_num == "2":
            print("2. 운동 종목 관리를 선택하셨습니다.\n")
            if not manage_machine(machines):
                return
            
        elif select_num == "3":
            print("3. 부가 서비스 관리를 선택하셨습니다.\n")
            if not extra_interface(extra):
                return

        elif select_num == "p":
            print("프로그램을 종료합니다.")
            return
        
        else:
            print("잘못된 접근입니다.\n")


def trainer_interface(members, workout, diets):
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
            progress_bar(30)
            if not search_interface(members, workout, diets, select_num):
                return False

        elif select_num == "3":
            print("3. 회원 정보 수정을 선택하셨습니다.\n")
            if not search_interface(members, workout, diets, select_num):
                return False
            
        elif select_num == "4":
            print("4. 회원 삭제를 선택하셨습니다.\n")
            if not search_interface(members, workout, diets, select_num):
                return False

        elif select_num == "o":
            print("이전으로 돌아갑니다.\n")
            return True

        elif select_num == "p":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")

def search_interface(members, workout, diets, select_num):
    count = True
    while True:
        if members:
            if select_num == "2" and count:
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
                if select_num == "2" and (not detail_interface(detail_member, workout, diets)):
                    return False
                
            elif search_num == "3":
                count = True
                continue
            
            elif search_num == "o":
                print("이전 화면으로 돌아갑니다.\n")
                return True

            elif search_num == "p":
                print("프로그램을 종료합니다.\n")
                return False

            else:
                print("잘못된 접근입니다.\n")
                
        else:
            print("등록된 회원이 없습니다.\n")
            return False

def detail_interface(member, workout, diets):
    while True:
        see_more = input(f"{member['name']}님을 조회하시겠습니까?(Y/N): ").strip().lower()
        if see_more in ("y", "yes", "네", "예", "ㅛ"):
            while True:
                print()
                search_name = f"========[ {member['name']} ]========"
                line4 = len(search_name) + align(search_name)
                print(search_name)
                print(
                    " 1. 상세 기록 조회\n"
                    " 2. 운동 기록 관리\n"
                    " 3. 식단 관리\n"
                    " o. 이전으로\n"
                    " p. 프로그램 종료")
                print("=" * line4)

                detail_num = input("조회할 내용(번호)을 선택해주세요: ").strip()
                print()
                
                if detail_num == "1":
                    print("1. 상세 기록 조회를 선택하셨습니다.")

                    for key, value in member.items():
                        print(f" {key:<15}: {value:^25}")
                    # 지금은 members.json의 내용들만 반환하지만 details.json을 추가함에 따라 변동될 예정
                    print()
                    
                elif detail_num == "2":
                    print("2. 운동 기록 관리를 선택하셨습니다.")
                    if not workout_interface(workout, member):
                        return False
                    # record

                elif detail_num == "3":
                    print("3. 식단 관리를 선택하셨습니다.")
                    if not diet_interface(diets, member):
                        return False

                elif detail_num == "o":
                    print("이전 화면으로 돌아갑니다.\n")
                    return True

                elif detail_num == "p":
                    print("프로그램을 종료합니다.\n")
                    return False

                else:
                    print("잘못된 접근입니다.\n")
        elif see_more in ("n", "no", "아니오", "ㅜ"):
            return True
        else:
            print("잘못 입력했습니다.")
            
def diet_interface(diets, member):
    while True:
        diet_mod = f"=======[ {member['name']} ] 식단 관리======="
        line5 = len(diet_mod) + align(diet_mod)
        print(diet_mod)
        
        print(
            " 1. 식단 기록 등록\n"
            " 2. 식단 조회\n"
            " 3. 식단 수정\n"
            " 4. 식단 삭제\n"
            " o. 이전으로\n"
            " p. 프로그램 종료")
        print("=" * line5)
        
        select_num = input("번호를 입력하세요: ").strip()
        print()

        if select_num == "1":
            print("1. 식단 기록 등록을 선택하셨습니다.\n")
            diets.do_save(member)

        elif select_num == "2":
            print("2. 식단 조회를 선택하셨습니다.\n")
            diets.do_retrieve(member)

        elif select_num == "3":
            print("3. 식단 수정을 선택하셨습니다.\n")
            diets.do_select_one(member, select_num)

        elif select_num == "4":
            print("4. 식단 삭제를 선택하셨습니다.\n")
            diets.do_select_one(member, select_num)

        elif select_num.lower() == "o":
            print("이전 화면으로 돌아갑니다.\n")
            return True

        elif select_num.lower() == "p":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")
            
def workout_interface(workout, member):
    while True:
        workout_mod = f"========[ {member['name']} ] 운동 기록 관리========"
        line6 = len(workout_mod) + align(workout_mod)
        print(workout_mod)
        print(
            " 1. 운동 기록 등록\n"
            " 2. 회원별 운동 기록 조회\n"
            " 3. 운동 기록 수정\n"
            " 4. 운동 기록 삭제\n"
            " 5. 전체 운동 기록 조회\n"
            " o. 이전으로\n"
            " p. 프로그램 종료")
        print("=" * line6)
        
        select_num = input("번호를 입력하세요: ").strip()
        print()

        if select_num == "1":
            print("1. 운동 기록 등록을 선택하셨습니다.\n")
            workout.register_workout(member)

        elif select_num == "2":
            print("2. 회원별 운동 기록 조회를 선택하셨습니다.\n")
            workout.search_workout(member)

        elif select_num == "3":
            print("3. 운동 기록 수정을 선택하셨습니다.\n")
            workout.update_workout(member)

        elif select_num == "4":
            print("4. 운동 기록 삭제를 선택하셨습니다.\n")
            workout.delete_workout(member)
        elif select_num == "5":
            print("5. 전체 운동 기록 조회를 선택하셨습니다.\n")
            workout.show_workouts()
            
        elif select_num == "o":
            print("이전 화면으로 돌아갑니다.\n")
            return True

        elif select_num == "p":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")
            
            
def extra_interface(extra):
    while True:
        extra_mod = "========부가 서비스 관리========"
        line7 = len(extra_mod) + align(extra_mod)
        
        print(extra_mod)
        print(
            "1. 락커 배정\n"
            "2. 락커 배정 현황 조회\n"
            "3. 락커 변경\n"
            "4. 락커 해제\n"
            "5. 운동복 이용 여부 등록\n"
            "6. 운동복 이용 현황 조회\n"
            "o. 이전으로\n"
            "p. 프로그램 종료")
        print("=" * line7)
        
        select_num = input("번호를 입력하세요: ").strip()
        print()

        if select_num == "1":
            extra.do_assign_locker()

        elif select_num == "2":
            extra.do_retrieve_lockers()
            
        elif select_num == "3":
            extra.do_change_locker()
            
        elif select_num == "4":
            extra.do_release_locker()
            
        elif select_num == "5":
            extra.do_register_uniform()
            
        elif select_num == "6":
            # print("1. 전체 회원 조회\n2. 특정 회원 조회")
            # sub = input("번호를 입력하세요: ").strip()
            # if sub == "1":
            #     extra.do_retrieve_uniform_all()
            # elif sub == "2":
            #     extra.do_retrieve_uniform_one()
            # else:
            #     print("잘못된 접근입니다.\n")
            while True:
                print("1. 전체 회원 조회\n2. 특정 회원 조회\no. 뒤로가기")
                sub = input("번호를 입력하세요: ").strip()
                if sub == "1":
                    extra.do_retrieve_uniform_all()
                    break
                elif sub == "2":
                    extra.do_retrieve_uniform_one()
                    break
                elif sub.lower() in ("o","ㅒ","ㅐ"):
                    print("이전으로 돌아갑니다.")
                    break
                else:
                    print("1, 2 또는 o 로 입력해주세요.\n")    
        elif select_num == "o":
            print("이전 화면으로 돌아갑니다.\n")
            return True
        
        elif select_num == "p":
            print("프로그램을 종료합니다.\n")
            return False
        
        else:
            print("잘못된 접근입니다.\n")


def manage_machine(machines):
    while True:
        machine_mod = "========운동 관리 모드========"
        line8 = len(machine_mod) + align(machine_mod)
        
        print(machine_mod)
        print(
            " 1. 운동 종목 등록\n"
            " 2. 전체 운동 종목 조회\n"
            " 3. 운동 종목 수정\n"
            " 4. 운동 종목 삭제\n"
            " o. 이전으로\n"
            " p. 프로그램 종료")
        print("=" * line8)
        
        select_num = input("번호 입력: ").strip()
        print()
        
        if select_num == "1":
            print("1. 운동 종목 등록을 선택하셨습니다.\n")
            machines.do_save()

        elif select_num == "2":
            print("2. 전체 운동 종목을 조회합니다.\n")
            machines.do_retrive()

        elif select_num == "3":
            print("운동 종목 수정을 선택하셨습니다.\n")
            if not machines.do_select_one(select_num):
                return False

        elif select_num == "4":
            print("운동 종목 삭제를 선택하셨습니다.\n")
            if not machines.do_select_one(select_num):
                return False

        elif select_num == "o":
            print("이전으로 돌아갑니다.\n")
            return True

        elif select_num == "p":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")


if __name__ == "__main__":
    
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, "members.json")
    machine_path = os.path.join(DATA_DIR, "muscles.json")
    workout_path = os.path.join(DATA_DIR, 'workouts.json')  
          
    os.makedirs(DATA_DIR, exist_ok=True)

    train_sys = TrainerCRUD(member_path)
    machine_sys = MachineList(machine_path)
    workout = WorkoutCRUD(workout_path)
    
    extra_sys = ExtraServiceCRUD(os.path.join(DATA_DIR, "members"), train_sys)
    
    train_sys.extra = extra_sys
    diet_sys = DietCRUD(os.path.join(DATA_DIR, "members"))
    if login_interface():
        admin_interface(train_sys, machine_sys, extra_sys, workout, diet_sys)
    # admin_interface(train_sys, machine_sys, extra_sys, workout, diet_sys)






