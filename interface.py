import os
import json

from trainer_crud import TrainerCRUD
from machine_list import MachineList
from utils import align

# from extra_service import ExtraServiceCRUD, extra_interface
from extra_service import ExtraServiceCRUD
from diet import DietCRUD

def login_interface():
    print("========관리자 로그인========")
    line1 = len("========관리자 로그인========")
    login_count = 0

    while True:
        login_id = input("관리자id: ").strip()
        login_pw = input("관리자pw: ").strip()
        if login_id != "admin" or login_pw != "0000":
            login_count += 1
            print(f"존재하지 않는 관리자입니다.({login_count}/5회 틀림)")

            if login_count >= 5:
                print("아이디 입력 횟수를 초과하였습니다.\n")
                print("=" * line1)
                return
        else:
            print("로그인에 성공했습니다.")
            print("=" * line1)
            return True


def admin_interface(members, machines, extra, diets):
    while True:
        print(
            "\n+=========관리자 모드=========+\n"
            " 1. 회원 관리\n"
            " 2. 운동 종목 관리\n"
            " 3. 부가 서비스 관리\n"
            " 0. 프로그램 종료\n"
            "+=============================+"
        )
        select_num = input("번호를 입력하세요: ").strip()

        if select_num == "1":
            print("1. 회원 관리를 선택하셨습니다. ")
            if not trainer_interface(members, diets):
                return

        elif select_num == "2":
            print("2. 운동 종목 관리를 선택하셨습니다.\n")
            if not manage_machine(machines):
                return
        elif select_num == "3":
            print("3. 부가 서비스 관리를 선택하셨습니다.")
            if not extra_interface(extra):
                return

        elif select_num == "0":
            print("프로그램을 종료합니다.")
            return
        else:
            print("잘못된 접근입니다.\n")


def trainer_interface(members, diets):
    while True:
        print(
            "\n========회원 관리 모드========\n"
            " 1. 회원 등록\n"
            " 2. 전체 회원 조회\n"
            " 3. 회원 정보 수정\n"
            " 4. 회원 삭제\n"
            " 9. 이전으로\n"
            " 0. 프로그램 종료\n"
            "============================="
        )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")

        if select_num == "1":
            print("1. 회원 등록을 선택하셨습니다.\n")
            members.do_save()

        elif select_num == "2":
            print("2. 전체 회원 조회를 선택하셨습니다.\n")
            if not search_interface(members, diets):
                return False

        elif select_num == "3":
            print("3. 회원 정보 수정을 선택하셨습니다.\n")
            members.do_select_one(select_num)

        elif select_num == "4":
            print("4. 회원 삭제를 선택하셨습니다.\n")
            members.do_select_one(select_num)

        elif select_num == "9":
            print("이전으로 돌아갑니다.\n")
            return True

        elif select_num == "0":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")


def search_interface(members, diets):
    while True:
        if not members.do_retrive():
            return True

        print(
            "\n=======회원 검색 모드=======\n"
            " 1. 회원 이름으로 검색"
            " 2. 회원 ID로 검색\n"
            " 9. 이전으로\n"
            " 0. 프로그램 종료\n"
            "============================"
        )
        search_num = input("번호를 선택하세요: ").strip()

        if search_num == "1":
            print("1. 회원 이름으로 검색을 시작합니다.")
            detail_member = members.do_select_one(search_num)
            if detail_member and (not detail_interface(detail_member, diets)):
                return False
        
        elif search_num == "2":
            print("2. 회원 ID로 검색을 시작합니다.")
            detail_member = members.do_select_id(search_num)
        elif search_num == "9":
            print("이전 화면으로 돌아갑니다.")
            return True

        elif search_num == "0":
            print("프로그램을 종료합니다.")
            return False

        else:
            print("잘못된 접근입니다.\n")


def detail_interface(member, diets):
    see_more = input(f"{member['name']}님을 조회하시겠습니까?(Y/N): ").strip().lower()
    if see_more in ("y", "yes", "네", "예"):
        while True:
            print(
                f"\n===========[ {member['name']} ]===========\n"
                " 1. 상세 기록 조회\n"
                " 2. 운동 기록 관리\n"
                " 3. 식단 관리\n"
                " 9. 이전으로\n"
                " 0. 프로그램 종료"
            )
            print("=" * (len(f"\n===========[ {member['name']} ]===========\n")- align(f"{member['name']}")))

            detail_num = input("조회할 내용(번호)을 선택해주세요: ").strip()
            if detail_num == "1":
                print("\n1. 상세 기록 조회를 선택하셨습니다.")

                for key, value in member.items():
                    print(f"{key:<15}: {value:^25}")
                # 지금은 members.json의 내용들만 반환하지만 details.json을 추가함에 따라 변동될 예정

            elif detail_num == "2":
                print("\n2. 운동 기록 관리를 선택하셨습니다.")
                # record

            elif detail_num == "3":
                print("\n3. 식단 관리를 선택하셨습니다.")
                if not diet_interface(diets, member):
                    return False

            elif detail_num == "9":
                print("이전 화면으로 돌아갑니다.\n")
                return True

            elif detail_num == "0":
                print("프로그램을 종료합니다.\n")
                return False

            else:
                print("잘못된 접근입니다.\n")
    else:
        return True

def diet_interface(diets, member):
    while True:
        print(
            f"\n=======[ {member['name']} ] 식단 관리=======\n"
            " 1. 식단 기록 등록\n"
            " 2. 식단 조회\n"
            " 3. 식단 수정\n"
            " 4. 식단 삭제\n"
            " 5. 일일 섭취 칼로리 합계\n"
            " 9. 이전으로\n"
            " 0. 프로그램 종료\n"
            "=============================="
        )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")

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

        elif select_num == "5":
            print("5. 일일 섭취 칼로리 합계를 선택하셨습니다.\n")
            diets.do_daily_kcal(member)

        elif select_num == "9":
            print("이전 화면으로 돌아갑니다.\n")
            return True

        elif select_num == "0":
            print("프로그램을 종료합니다.\n")
            return False

        else:
            print("잘못된 접근입니다.\n")

def extra_interface(extra):
    while True:
        print(
            "\n=======부가 서비스 관리=======\n"
            "1. 락커 배정\n"
            "2. 락커 배정 현황 조회\n"
            "3. 락커 변경\n"
            "4. 락커 해제\n"
            "5. 운동복 이용 여부 등록\n"
            "6. 운동복 이용 현황 조회\n"
            "9. 이전으로\n"
            "0. 프로그램 종료\n"
            "=============================="
        )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")

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
            print("1. 전체 회원 조회\n2. 특정 회원 조회")
            sub = input("번호를 입력하세요: ").strip()
            if sub == "1":
                extra.do_retrieve_uniform_all()
            elif sub == "2":
                extra.do_retrieve_uniform_one()
            else:
                print("잘못된 접근입니다.")
        elif select_num == "9":
            print("이전 화면으로 돌아갑니다.")
            return True
        elif select_num == "0":
            print("프로그램을 종료합니다.")
            return False
        else:
            print("잘못된 접근입니다.\n")

def manage_machine(machines):
    while True:
        print(
            "\n=======운동 관리 모드=======\n"
            " 1. 운동 종목 등록\n"
            " 2. 전체 운동 종목 조회\n"
            " 3. 운동 종목 수정\n"
            " 4. 운동 종목 삭제\n"
            " 9. 이전으로\n"
            " 0. 프로그램 종료"
        )
        print("=" * 28)
        select_num = input("번호 입력: ").strip()
        if select_num == "1":
            print("1. 운동 종목 등록을 선택하셨습니다.\n")
            machines.do_save()

        elif select_num == "2":
            print("2. 전체 운동 종목을 조회합니다.")
            machines.do_retrive()

        elif select_num == "3":
            print("운동 종목 수정을 선택하셨습니다.")
            if not machines.do_select_one(select_num):
                return False

        elif select_num == "4":
            print("운동 종목 삭제를 선택하셨습니다.")
            if not machines.do_select_one(select_num):
                return False

        elif select_num == "9":
            print("이전으로 돌아갑니다.")
            return True

        elif select_num == "0":
            print("프로그램을 종료합니다.")
            return False

        else:
            print("잘못된 접근입니다.\n")



if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, "members.json")
    machine_path = os.path.join(DATA_DIR, "muscles.json")

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(member_path):
        with open(member_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    if not os.path.exists(machine_path):
        with open(machine_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    # train_sys = TrainerCRUD(member_path)

    # if login_interface():
    #     trainer_interface(members)
    train_sys = TrainerCRUD(member_path)
    machine_sys = MachineList(machine_path)

    extra_sys = ExtraServiceCRUD(os.path.join(DATA_DIR, "members"), train_sys)
    
    train_sys.extra = extra_sys  # 회원 삭제 시 락커/운동복 정리
    diet_sys = DietCRUD(os.path.join(DATA_DIR, "members"))  # 회원별 식단 관리
    admin_interface(train_sys, machine_sys, extra_sys, diet_sys)

    # trainer_interface(train_sys, extra_sys)

"""
===============================================================================
~2026.10.16
트레이너 앱
트레이너 로그인

=======GYM LOG=======
1. 회원 등록 및 관리
2. 운동 종목 관리
3. 회원별 운동 기록 등록
4. 회원별 운동 기록 조회
5. 프로그램 종료

메뉴를 선택하세요:4
회원 ID 입력: user01

[김철수 회원 운동 기록]
10/12|벤치프레스|40kg|10회|3세트
10/13|스쿼트|60kg|12회|3세트

회원 관리CRUD: 등록, 조회, 수정, 삭제 ->필수
운동 종목 관리CRUD: 운동 종목 등록, 조회, 수정, 삭제 -> 필수
개인별 운동 기록: 회원별 운동 날짜, 무게, 횟수, 세트 기록 및 조회->핵심추가기능
데이터 저장: JSON 파일 저장 및 불러오기 ->필수
운동 기록 통계: 운동별 기록 변화 확인 ->선택

데스크 직원: 회원등록조회/회원복 및 락커 이용 기간 확인
트레이너: 회원별 운동 기록 등록 조회/운동 종목 관리

-외부 API 및 크롤링: 회원 인바디에 따른 섭취 음식 칼로리 계산(식품안전나라에서 '식품 영양성분 데이터베이스'를 오픈API 형태로 무상 제공)

"""
"""
=================================================================
2026.10.17
코딩을 하려고 보니까 회원리스트를 먼저 내보내면 선택화면이 가려질 우려가 있어서 뒤로 옮기고
"전체 멤버 조회" -> "회원 검색" -> "개별 데이터 조회" 시스템으로 구성
관계도도 TrainerCRUD2.png로 수정

이거에 맞게 login_interface(), trainer_interface(), search_interface(), detail_interface() 작성
login_interface(): 로그인 화면
trainer_interface(): 회원관리CRUD
search_interface(): 검색 화면
detail_interface(): 개인관리 CRUD

일단 내용은 텍스트로 대체

주요 의논점
1. 중복처리 기준 마련(이름, 이메일로 끝낼건지, 전화번호도 추가할건지 아니면 다른 기준이 있는지)
2. 전체적인 구조에 조금 디테일이 필요해보임
3. 개인관리 CRUD에 해당하는 데이터들의 관리 형식(개인별 폴더 or 주제별 파일)
4. 전체 회원 조회 출력방식(정제된 데이터 OR lIST그대로)

"""
# if elif 로 번호를 쓴 것들 match-case로 바꿔도됨
