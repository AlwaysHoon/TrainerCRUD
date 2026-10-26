import os
import json
from datetime import datetime

from .utils import align


class DietCRUD:
    '''
    회원별 식단 관리.
    회원별 폴더 data/members/<user_id>/diet.json 에 저장한다.
    detail_interface()에서 이미 선택된 member(dict)를 받아서 사용한다.
    '''

    def __init__(self, member_dir):
        self.member_dir = member_dir  # 예: data/members

    # ---------- 도우미 ----------
    def get_folder(self, user_id):
        return os.path.join(self.member_dir, user_id)

    def get_path(self, user_id):
        return os.path.join(self.get_folder(user_id), "diet.json")

    # DIET_007 식단 데이터 불러오기
    def read_data(self, user_id):
        path = self.get_path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        # 파일이 없으면 빈 리스트
        return []

    # DIET_007 식단 데이터 저장
    def write_data(self, user_id, diets):
        # 날짜순으로 정렬해서 저장 (같은 날짜는 입력한 순서 유지)
        diets.sort(key=lambda diet: diet["date"])

        os.makedirs(self.get_folder(user_id), exist_ok=True)  # 개인 폴더가 없으면 생성
        with open(self.get_path(user_id), "w", encoding="utf-8") as f:
            json.dump(diets, f, ensure_ascii=False, indent=4)

    # 날짜 입력 (형식: 26/10/22, 그냥 Enter는 오늘 날짜)
    def input_date(self):
        while True:
            today = datetime.now().strftime("%y/%m/%d")
            date = input(f"식사 날짜를 입력하세요(예: {today}, 오늘은 Enter): ").strip()
            if date == "":
                return datetime.now().strftime("%y/%m/%d")

            # 1. 형식 확인: 8글자이고 3번째, 6번째 글자가 '/' 이고 나머지는 숫자
            if not (len(date) == 8 and date[2] == "/" and date[5] == "/"
                    and date[0:2].isdigit() and date[3:5].isdigit() and date[6:8].isdigit()):
                print(f"날짜 형식이 잘못되었습니다. 예) {today}")
                continue

            # 2. 실제로 있는 날짜인지 확인
            year = int(date[0:2])
            month = int(date[3:5])
            day = int(date[6:8])

            if month < 1 or month > 12:
                print("존재하지 않는 월입니다.")
                continue

            # 월별 마지막 날 (1월~12월)
            last_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0:  # 2000~2099년은 4로 나누어떨어지면 윤년 -> 2월 29일까지
                last_days[1] = 29

            if day < 1 or day > last_days[month - 1]:
                print(f"{month}월은 1일~{last_days[month - 1]}일까지 있습니다.")
                continue

            return date
    
    ##Q. 잘못 진입할 경우: 1~4 외에 다른 키를 선택할건지 입력 전에 확인을 한번 더 할건지
    
    # 식사 구분 입력 (번호로 선택)
    def input_meal(self):
        while True:
            meal_num = input("식사 구분을 선택하세요(1.아침 2.점심 3.저녁 4.간식): ").strip()
            if meal_num == "1":
                return "아침"
            elif meal_num == "2":
                return "점심"
            elif meal_num == "3":
                return "저녁"
            elif meal_num == "4":
                return "간식"
            else:
                print("1~4 중에서 선택해주세요.")

    # DIET_005 섭취 칼로리 입력(kcal)
    def input_kcal(self):
        while True:
            kcal = input("섭취 칼로리를 입력하세요(kcal): ").strip()
            if kcal.isdigit():
                return int(kcal)
            print("칼로리는 숫자로 입력해주세요.")

    # 식단 목록을 번호와 함께 출력
    def print_diets(self, diets):
        print("ㅡ" * 30)
        print(f"{'No.':<5}{'날짜':<8}{'구분':<6}{'음식명':<17}{'칼로리(kcal)'}")
        print("ㅡ" * 30)
        for index, diet in enumerate(diets):
            print(f"{index + 1:<5}{diet['date']:<10}{diet['meal']:<6}{diet['food']:<{20 - align(diet['food'])}}{diet['kcal']}")
        print("ㅡ" * 30)

    # ---------- DIET_001 식단 기록 등록 ----------
    def do_save(self, member):
        date = self.input_date()
        meal = self.input_meal()

        diets = self.read_data(member["user_id"])
        count = 0  # 이번에 등록한 음식 수
        total = 0  # 이번에 등록한 칼로리 합

        # 음식 연속입력
        while True:
            food = input("음식명을 입력하세요: ").strip()
            if food == "":
                print("음식명을 입력해주세요.")
                continue
            kcal = self.input_kcal()

            # 최초 등록일, 최근 수정일
            today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
            save_time = str(today)
            modify_time = str(today)

            new_diet = {
                "date": date,
                "meal": meal,
                "food": food,
                "kcal": kcal,
                "save_time": save_time,
                "modify_time": modify_time,
            }
            diets.append(new_diet)
            count += 1
            total += kcal

            go = input("음식을 계속 입력하시겠습니까?(Y/N): ").strip().lower()
            if not go in ("y", "yes", "네", "예"):
                break

        self.write_data(member["user_id"], diets)
        print(f"{member['name']}님 {date} {meal} 식단 {count}건({total}kcal) 등록에 성공했습니다.")
        return True

    ##Q. 날짜선택해서 들어가면 정렬 기능 넣을건지 아침>점심>저녁 순으로
    # ---------- DIET_002 회원별 식단 조회 / DIET_006 일일 섭취 칼로리 합계 ----------
    def do_retrieve(self, member):
        diets = self.read_data(member["user_id"])
        if not diets:
            print(f"{member['name']}님의 등록된 식단이 없습니다.")
            return False

        # 식단을 기록한 날짜만 모으기 (중복 없이)
        dates = []
        for diet in diets:
            if diet["date"] not in dates:
                dates.append(diet["date"])

        while True:
            print(f"=======[ {member['name']} ] 식단 기록 날짜=======")
            for index, date in enumerate(dates):
                print(f"{index + 1}. {date}")
            print("ㅡ" * 20)

            select = input(f"조회할 날짜 번호를 선택하세요(1~{len(dates)}, o:이전으로): ").strip()
            if select.lower() == "o":
                print("이전으로 돌아갑니다.")
                return True
            if not select.isdigit():
                print("숫자를 입력해주세요")
                continue
            if not (1 <= int(select) <= len(dates)):
                print("범위 밖입니다.")
                continue

            date = dates[int(select) - 1]

            # 선택한 날짜의 식단만 모으기
            day_diets = []
            total = 0
            for diet in diets:
                if diet["date"] == date:
                    day_diets.append(diet)
                    total += diet["kcal"]

            # 하루 총 섭취 칼로리를 맨 위에 출력
            print(f"\n=======[ {member['name']} ] {date} 식단=======")
            print(f"하루 총 섭취 칼로리: {total}kcal")
            self.print_diets(day_diets)
            print()

    # ---------- DIET_003 식단 수정 / DIET_004 식단 삭제 ----------
    def do_select_one(self, member, select_num="3"):
        diets = self.read_data(member["user_id"])
        if not diets:
            print(f"{member['name']}님의 등록된 식단이 없습니다.")
            return False

        # 수정/삭제를 통합
        word = {"3": "수정", "4": "삭제"}[select_num]
        self.print_diets(diets)

        while True:
            select = input(f"{word}할 식단 번호를 선택하세요(1~{len(diets)}, o:이전으로): ").strip()
            if select.lower() == "o":
                print("이전으로 돌아갑니다.")
                return False
            if select.isdigit():
                if (int(select) >= 1) and (int(select) <= len(diets)):
                    break
                else:
                    print("범위 밖입니다.")
            else:
                print("숫자를 입력해주세요")

        idx = int(select) - 1

        print("ㅡ" * 20)
        for key, value in diets[idx].items():
            print(f"{key:<12}: {value}")
        print("ㅡ" * 20)

        if select_num == "3":  # 식단수정"3"
            is_modify = input("수정하실 정보가 맞습니까?(Y/N): ").strip().lower()
            if is_modify in ("y", "yes", "예", "네"):
                self.modify_diet(diets[idx])
                self.write_data(member["user_id"], diets)
                return True
            else:
                print("이전으로 돌아갑니다.")
                return False

        elif select_num == "4":  # 식단삭제"4"
            is_delete = input("삭제하실 정보가 맞습니까?(Y/N): ").strip().lower()
            if is_delete in ("y", "yes", "예", "네"):
                diets.pop(idx)
                self.write_data(member["user_id"], diets)
                print("식단 삭제에 성공했습니다.")
                return True
            else:
                print("이전으로 돌아갑니다.")
                return False

    def modify_diet(self, select_diet):
        print("\n식단 정보 수정을 시작합니다.\n")
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[date, meal, food, kcal](돌아가려면 o 입력): ").strip()
            if modify_key.lower() == "o":
                print("이전으로 돌아갑니다.")
                return

            if modify_key in ("date", "meal", "food", "kcal"):
                print(f"기존 {modify_key}는 {select_diet[modify_key]}입니다.")

                # 항목마다 입력 방식이 달라서 따로 처리
                if modify_key == "date":
                    modify_value = self.input_date()
                elif modify_key == "meal":
                    modify_value = self.input_meal()
                elif modify_key == "kcal":
                    modify_value = self.input_kcal()
                else:
                    modify_value = input("변경할 음식명을 적어주세요: ").strip()

                is_modify = input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower()
                if is_modify in ("y", "yes", "예", "네"):
                    select_diet[modify_key] = modify_value
                    select_diet["modify_time"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                    print(f"{modify_key} 변경에 성공했습니다.")
                    return
                else:
                    print("\n이전으로 돌아갑니다.\n")

            else:  # str잘못입력한 경우 재진입 기회 제공
                print("잘못된 접근입니다.")
                is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                if not is_continue in ("y", "yes", "예", "네"):
                    return

    # ---------- 회원 삭제 연동 ----------
    def remove_member_data(self, user_id):
        '''회원 삭제 시 호출: 식단 기록을 빈 리스트로 초기화 (개인 폴더의 다른 파일은 건드리지 않음)'''
        if os.path.exists(self.get_path(user_id)):
            self.write_data(user_id, [])


if __name__ == "__main__":
    # 단독 테스트용: members.json의 첫 번째 회원으로 식단 관리 실행
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    member_path = os.path.join(DATA_DIR, "members.json")

    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)

    from interface import diet_interface  # 메뉴 함수는 interface.py에 있음

    if members:
        diet_sys = DietCRUD(os.path.join(DATA_DIR, "members"))
        diet_interface(diet_sys, members[0])
    else:
        print("등록된 회원이 없습니다.")
