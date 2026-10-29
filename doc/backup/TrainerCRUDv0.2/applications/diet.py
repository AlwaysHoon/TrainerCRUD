import os
import json
from datetime import datetime

from .utils import align

YES = ("y", "yes", "예", "네", "ㅛ")  # Y로 받는 입력 (ㅛ: 한글 자판 상태의 y)
NO = ("n", "no", "아니오", "아니요", "ㅜ")  # N으로 받는 입력 (ㅜ: 한글 자판 상태의 n)
BACK = ("o", "ㅒ", "ㅐ")  # 이전으로 돌아가기 키 (ㅐ/ㅒ: 한글 자판 상태의 o/O)

class DietCRUD:
    '''
    회원별 식단 관리.
    회원별 폴더 data/members/<아이디>/diet.json 에 저장한다.
    detail_interface()에서 이미 선택된 member(dict)를 받아서 사용한다.
    '''

    def __init__(self, member_dir):
        self.member_dir = member_dir  # 예: data/members

    # ---------- 도우미 ----------
    def get_folder(self, user_id):
        return os.path.join(self.member_dir, user_id)

    def get_path(self, user_id):
        return os.path.join(self.get_folder(user_id), "diet.json")

    # 날짜순 -> 같은 날짜는 아침-점심-저녁-간식 순 (같은 구분은 입력한 순서 유지)
    def sort_diets(self, diets):
        meal_order = {"아침": 1, "점심": 2, "저녁": 3, "간식": 4}
        diets.sort(key=lambda diet: (diet["날짜"], meal_order.get(diet["식사 구분"], 5)))

    # DIET_007 식단 데이터 불러오기
    def read_data(self, user_id):
        path = self.get_path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # {아이디, 이름, 식단} 모양이면 식단 목록만 꺼냄
            if isinstance(data, dict):
                data = data.get("식단", [])
            # 예전에 저장된 데이터도 정렬된 순서로 보이도록
            self.sort_diets(data)
            return data
        # 파일이 없으면 빈 리스트
        return []

    # DIET_007 식단 데이터 저장 (성공하면 True, 실패하면 False)
    def write_data(self, user_id, diets):
        self.sort_diets(diets)

        try:
            os.makedirs(self.get_folder(user_id), exist_ok=True)  # 개인 폴더가 없으면 생성
            with open(self.get_path(user_id), "w", encoding="utf-8") as f:
                json.dump(diets, f, ensure_ascii=False, indent=4)

        except OSError as e:  # 폴더/파일을 만들거나 쓸 수 없을 때
            print(f"파일 저장 오류: {e}\n")
            return False

        except (TypeError, ValueError) as e:  # JSON으로 바꿀 수 없는 값이 있을 때
            print(f"데이터 변환 오류: {e}\n")
            return False

        return True

    # 날짜 입력 (형식: 26/10/22, 그냥 Enter는 오늘 날짜, o 입력 시 None)
    def input_date(self):
        while True:
            today = datetime.now().strftime("%y/%m/%d")
            date = input(f"식사 날짜를 입력하세요(예: {today}, 오늘은 Enter, o:이전으로): ").strip()
            if date.lower() in BACK:
                return None
            if date == "": # Enter 누르면 오늘 날짜
                return datetime.now().strftime("%y/%m/%d") # 형식: 26/10/22

            # 1. 형식 확인: 8글자이고 3번째, 6번째 글자가 '/' 이고 나머지는 숫자
            if not (len(date) == 8 and date[2] == "/" and date[5] == "/"
                    and date[0:2].isdigit() and date[3:5].isdigit() and date[6:8].isdigit()):
                print(f"날짜 형식이 잘못되었습니다. (예: {today})")
                continue  # 잘못된 건 건너띄고 다시 물어보기

            # 2. 실제로 있는 날짜인지 확인
            year = int(date[0:2])
            month = int(date[3:5])
            day = int(date[6:8])

            if month < 1 or month > 12:
                print("존재하지 않는 월입니다.")
                continue  # 존재하지 않는 월은 건너띄고 다시 확인하기

            # 월별 마지막 날 (1월~12월)
            last_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if year % 4 == 0:  # 2000~2099년은 4로 나누어떨어지면 윤년 -> 2월 29일까지
                last_days[1] = 29

            if day < 1 or day > last_days[month - 1]:
                print(f"{month}월은 1일~{last_days[month - 1]}일까지 있습니다.")
                continue

            # 3. 미래 날짜는 막기 (yy/mm/dd 형식이라 글자 비교로 날짜 순서 비교 가능)
            if date > today:
                print(f"미래 날짜는 입력할 수 없습니다. (오늘: {today})")
                continue

            return date
    
    # 식사 구분 입력 (번호로 선택, o 입력 시 None)
    def input_meal(self):
        while True:
            meal_num = input("식사 구분을 선택하세요(1.아침 2.점심 3.저녁 4.간식, o:이전으로): ").strip()
            if meal_num.lower() in BACK:
                return None
            if meal_num == "1":
                return "아침"
            elif meal_num == "2":
                return "점심"
            elif meal_num == "3":
                return "저녁"
            elif meal_num == "4":
                return "간식"
            elif not meal_num.isdigit():  # 문자나 빈 입력
                print("식사 구분은 숫자로 입력해주세요.")
            else:  # 숫자지만 1~4가 아님
                print("1~4 중에서 선택해주세요.")

    # DIET_005 섭취 칼로리 입력(kcal, 1~5000, o 입력 시 None)
    def input_kcal(self):
        while True:
            kcal = input("섭취 칼로리를 입력하세요(kcal, o:이전으로): ").strip()
            if kcal.lower() in BACK:
                return None
            if not kcal.isdigit():
                print("칼로리는 숫자로 입력해주세요.")
                continue
            if not (1 <= int(kcal) <= 5000):  # 한 음식 칼로리로 너무 작거나 큰 값 막기
                print("칼로리는 1~5000 사이로 입력해주세요.")
                continue
            return int(kcal)

    # 식단 목록을 번호와 함께 출력
    def print_diets(self, diets):
        print("ㅡ" * 30)
        print(f"{'No.':<5}{'구분':<6}{'음식명':<17}{'칼로리(kcal)'}")
        print("ㅡ" * 30)
        before_meal = None  # 식사 구분 한 번씩만 나오게 하기 위한 시작값 넣기
        for index, diet in enumerate(diets):
            # 식사 구분은 한 번씩만 나오게
            if diet['식사 구분'] == before_meal:
                meal = ""
            else:
                meal = diet['식사 구분']
            print(f"{index + 1:<5}{meal:<{8 - align(meal)}}{diet['음식명']:<{20 - align(diet['음식명'])}}{diet['칼로리']}")
            before_meal = diet['식사 구분']  # 다음 줄과 비교하기 위해 지금 구분 기억
        print("ㅡ" * 30)

    # ---------- DIET_001 식단 기록 등록 ----------
    def do_save(self, member):
        diets = self.read_data(member["아이디"])
        count = 0  # 이번에 등록한 음식 수
        total = 0  # 이번에 등록한 칼로리 합

        # 지금 입력할 단계: 날짜 -> 식사 구분 -> 음식명 -> 칼로리 -> 계속
        # o를 누르면 바로 전 단계로 돌아감
        step = "날짜"
        while True:
            if step == "날짜":
                date = self.input_date()
                if date is None:
                    print("\n이전으로 돌아갑니다.\n")
                    return False
                step = "식사 구분"

            elif step == "식사 구분":
                meal = self.input_meal()
                if meal is None:
                    print("\n날짜 입력으로 돌아갑니다.\n")
                    step = "날짜"
                else:
                    step = "음식명"

            elif step == "음식명":
                food = input("음식명을 입력하세요(o:이전으로): ").strip()
                if food.lower() in BACK:
                    if count == 0:  # 아직 등록한 음식이 없으면 식사 구분으로
                        print("\n식사 구분 선택으로 돌아갑니다.\n")
                        step = "식사 구분"
                    else:  # 이미 등록한 음식이 있으면 계속 입력 질문으로
                        print("\n계속 입력 질문으로 돌아갑니다.\n")
                        step = "계속"
                elif food == "":
                    print("음식명을 입력해주세요.")
                else:
                    step = "칼로리"

            elif step == "칼로리":
                kcal = self.input_kcal()
                if kcal is None:
                    print("\n음식명 입력으로 돌아갑니다.\n")
                    step = "음식명"
                    continue

                # 최초 등록일, 최근 수정일
                today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                save_time = str(today)
                modify_time = str(today)

                new_diet = {
                    "날짜": date,
                    "식사 구분": meal,
                    "음식명": food,
                    "칼로리": kcal,
                    "최초 등록일": save_time,
                    "최근 수정일": modify_time,
                }
                diets.append(new_diet)
                count += 1
                total += kcal
                step = "계속"

            elif step == "계속":
                # Y: 계속 입력 / N: 등록 끝 / 그 외: 다시 물어봄
                go = input("음식을 계속 입력하시겠습니까?(Y/N): ").strip().lower()
                if go in YES:
                    step = "음식명"
                elif go in NO:
                    break  # 등록 끝 -> 저장
                else:
                    print("Y 또는 N으로 입력해주세요.")

        if not self.write_data(member["아이디"], diets):
            print("식단 등록에 실패했습니다. 입력한 식단이 저장되지 않았습니다.\n")
            return False
        print()
        print(f"{member['이름']}님 {date} {meal} 식단 {count}건({total}kcal) 등록에 성공했습니다.")
        print()
        return True

    # 식단 기록 월 -> 날짜 순서로 골라서 날짜 하나 돌려줌 (o 입력 시 None)
    # start_month를 주면 월 선택을 건너뛰고 그 달의 날짜 목록부터 보여줌 (이전 단계로 돌아올 때 사용)
    def select_date(self, member, diets, word, start_month=None):
        # 식단을 기록한 날짜만 월별로 모으기 (예: "26/10" -> ["26/10/27", "26/10/28"])
        months = {}
        for diet in diets:
            month = diet["날짜"][:5]  # "26/10/28" -> "26/10"
            if month not in months:
                months[month] = []
            if diet["날짜"] not in months[month]:
                months[month].append(diet["날짜"])
        month_list = list(months)

        while True:
            # 1. 월 선택 (기록한 달이 하나뿐이면 건너뜀)
            if len(month_list) == 1:
                month = month_list[0]
            elif start_month in months:
                month = start_month
                start_month = None  # 한 번만 건너뜀 (날짜 목록에서 o를 누르면 월 목록으로)
            else:
                print(f"=======[ {member['이름']} ] 식단 기록 월=======")
                for index, key in enumerate(month_list):
                    print(f"{index + 1}. 20{key[:2]}년 {int(key[3:5])}월 ({len(months[key])}일 기록)")
                print("ㅡ" * 20)

                select = input(f"{word}할 월 번호를 선택하세요(1~{len(month_list)}, o:이전으로): ").strip()
                if select.lower() in BACK:
                    print("\n이전으로 돌아갑니다.\n")
                    return None
                if not select.isdigit():
                    print()
                    print("숫자를 입력해주세요.")
                    print()
                    continue
                if not (1 <= int(select) <= len(month_list)):
                    print()
                    print("범위 밖입니다.")
                    print()
                    continue
                month = month_list[int(select) - 1]
                print()  # 월 선택과 날짜 목록 사이 한 줄 띄우기

            # 2. 그 달의 날짜 선택 (한 달은 최대 31일)
            dates = months[month]
            print(f"=======[ {member['이름']} ] 20{month[:2]}년 {int(month[3:5])}월 식단 기록 날짜=======")
            for index, date in enumerate(dates):
                print(f"{index + 1}. {date}")
            print("ㅡ" * 20)

            while True:
                select = input(f"{word}할 날짜 번호를 선택하세요(1~{len(dates)}, o:이전으로): ").strip()
                if select.lower() in BACK:
                    break
                if not select.isdigit():
                    print()
                    print("숫자를 입력해주세요.")
                    print()
                    continue
                if not (1 <= int(select) <= len(dates)):
                    print()
                    print("범위 밖입니다.")
                    print()
                    continue
                return dates[int(select) - 1]

            # 날짜 선택에서 o: 달이 하나뿐이면 메뉴로, 여러 달이면 월 목록으로
            if len(month_list) == 1:
                print("\n이전으로 돌아갑니다.\n")
                return None
            print("\n월 목록으로 돌아갑니다.\n")

    # 선택한 날짜의 식단을 하루 총 섭취 칼로리와 함께 출력, 전체 목록에서의 위치(index)들을 돌려줌
    def print_day(self, member, diets, date):
        day_indexes = []
        total = 0
        for index, diet in enumerate(diets):
            if diet["날짜"] == date:
                day_indexes.append(index)
                total += diet["칼로리"]

        # 하루 총 섭취 칼로리를 맨 위에 출력
        print(f"\n=======[ {member['이름']} ] {date} 식단=======")
        print(f"하루 총 섭취 칼로리: {total}kcal")
        self.print_diets([diets[index] for index in day_indexes])
        return day_indexes

    # ---------- DIET_002 회원별 식단 조회 / DIET_006 일일 섭취 칼로리 합계 ----------
    def do_retrieve(self, member):
        diets = self.read_data(member["아이디"])
        if not diets:
            print(f"{member['이름']}님의 등록된 식단이 없습니다.")
            print()
            return False

        back_month = None  # "다른 날짜도 조회?"에서 Y면 그 달의 날짜 목록으로 돌아가기 위해 기억
        while True:
            date = self.select_date(member, diets, "조회", back_month)
            if date is None:
                return True
            back_month = date[:5]  # "26/10/28" -> "26/10"
            self.print_day(member, diets, date)

            # Y를 눌렀을 때만 날짜 목록을 다시 보여줌 (Y/N 외의 입력은 다시 물어봄)
            while True:
                again = input("다른 날짜도 조회하시겠습니까?(Y: 날짜 목록 / N: 메뉴로): ").strip().lower()
                if again in YES:
                    break
                if again in NO:
                    print("\n이전으로 돌아갑니다.\n")
                    return True
                print()
                print("Y 또는 N으로 입력해주세요.")
                print()
            print()

    # ---------- DIET_003 식단 수정 / DIET_004 식단 삭제 ----------
    def do_select_one(self, member, select_num="3"):
        diets = self.read_data(member["아이디"])
        if not diets:
            print(f"{member['이름']}님의 등록된 식단이 없습니다.")
            print()
            return False

        # 수정/삭제를 통합
        word = {"3": "수정", "4": "삭제"}[select_num]

        # 이전으로(o)는 항상 바로 전 단계로: 식단 번호 -> 날짜 목록, 수정 항목 -> 그날 식단 목록
        back_month = None  # 식단 번호에서 o를 누르면 그 달의 날짜 목록으로 돌아가기 위해 기억
        while True:
            # 날짜 먼저 선택 -> 그 날짜의 식단만 보여줌
            date = self.select_date(member, diets, word, back_month)
            if date is None:
                return False

            while True:
                day_indexes = self.print_day(member, diets, date)

                select = None  # o를 누르면 None으로 남음
                while True:
                    answer = input(f"{word}할 식단 번호를 선택하세요(1~{len(day_indexes)}, o:이전으로): ").strip()
                    if answer.lower() in BACK:
                        break
                    if answer.isdigit():
                        if (int(answer) >= 1) and (int(answer) <= len(day_indexes)):
                            select = answer
                            break
                        else:
                            print()
                            print("범위 밖입니다.")
                            print()
                    else:
                        print()
                        print("숫자를 입력해주세요.")
                        print()

                if select is None:
                    print("\n날짜 목록으로 돌아갑니다.\n")
                    back_month = date[:5]  # "26/10/28" -> "26/10"
                    break  # 날짜 선택으로

                # 그날 목록의 번호 -> 전체 목록에서의 위치
                idx = day_indexes[int(select) - 1]

                print("ㅡ" * 20)
                for key, value in diets[idx].items():
                    print(f"{key:<{12 - align(key)}}: {value}")
                print("ㅡ" * 20)

                if select_num == "3":  # 식단수정"3"
                    # Y: 수정 / N: 그날 식단 목록으로 / 그 외: 다시 물어봄
                    while True:
                        is_modify = input("수정하실 정보가 맞습니까?(Y/N): ").strip().lower()
                        if is_modify in YES:
                            break
                        elif is_modify in NO:
                            break
                        else:
                            print()
                            print("Y 또는 N으로 입력해주세요.")
                            print()

                    if is_modify in YES:
                        if self.modify_diet(diets[idx]):
                            if not self.write_data(member["아이디"], diets):
                                print("식단 수정 내용을 저장하지 못했습니다.\n")
                                return False
                            return True
                    # N이거나 수정 항목에서 o -> 그날 식단 목록으로
                    print("\n그날 식단 목록으로 돌아갑니다.")  # 아래 빈 줄은 print_day가 넣음
                    continue

                elif select_num == "4":  # 식단삭제"4"
                    # Y: 삭제 / N: 그날 식단 목록으로 / 그 외: 다시 물어봄
                    while True:
                        is_delete = input("삭제하실 정보가 맞습니까?(Y/N): ").strip().lower()
                        if is_delete in YES:
                            break
                        elif is_delete in NO:
                            break
                        else:
                            print()
                            print("Y 또는 N으로 입력해주세요.")
                            print()

                    if is_delete in YES:
                        diets.pop(idx)
                        if not self.write_data(member["아이디"], diets):
                            print("식단 삭제 내용을 저장하지 못했습니다.\n")
                            return False
                        print()
                        print("삭제되었습니다.")
                        print()
                        return True
                    else:
                        print("\n그날 식단 목록으로 돌아갑니다.")  # 아래 빈 줄은 print_day가 넣음
                        continue

    # 수정했으면 True, 수정하지 않고 돌아가면 False
    def modify_diet(self, select_diet):
        print("\n식단 정보 수정을 시작합니다.\n")
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[날짜, 식사 구분, 음식명, 칼로리](돌아가려면 o 입력): ").strip()
            if modify_key.lower() in BACK:
                return False
            if modify_key == "식사구분":  # 띄어쓰기 없이 써도 받기
                modify_key = "식사 구분"

            if modify_key in ("날짜", "식사 구분", "음식명", "칼로리"):
                print(f"기존 {modify_key}: {select_diet[modify_key]}")

                # 항목마다 입력 방식이 달라서 따로 처리
                if modify_key == "날짜":
                    modify_value = self.input_date()
                elif modify_key == "식사 구분":
                    modify_value = self.input_meal()
                elif modify_key == "칼로리":
                    modify_value = self.input_kcal()
                else:
                    modify_value = input("변경할 음식명을 적어주세요(o:이전으로): ").strip()
                    if modify_value.lower() in BACK:
                        modify_value = None

                # 새 값 입력에서 o -> 수정할 정보 선택으로
                if modify_value is None:
                    print("\n수정할 정보 선택으로 돌아갑니다.\n")
                    continue

                # Y: 변경 / N: 수정할 정보 선택으로 / 그 외: 다시 물어봄
                while True:
                    is_modify = input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower()
                    if is_modify in YES:
                        break
                    elif is_modify in NO:
                        break
                    else:
                        print()
                        print("Y 또는 N으로 입력해주세요.")
                        print()

                if is_modify in YES:
                    select_diet[modify_key] = modify_value
                    select_diet["최근 수정일"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                    print()
                    print(f"{modify_key} 변경에 성공했습니다.")
                    print()
                    return True
                else:
                    print("\n수정할 정보 선택으로 돌아갑니다.\n")

            else:  # 잘못 입력한 경우 안내 후 다시 물어봄 (그만두려면 o)
                print()
                print("날짜, 식사 구분, 음식명, 칼로리 중에서 입력해주세요.")
                print()

    # ---------- 회원 삭제 연동 ----------
    def remove_member_data(self, user_id):
        '''회원 삭제 시 호출: 식단 기록을 빈 리스트로 초기화 (개인 폴더의 다른 파일은 건드리지 않음)'''
        if os.path.exists(self.get_path(user_id)):
            self.write_data(user_id, [])


if __name__ == "__main__":
    # 단독 테스트용: members.json의 첫 번째 회원으로 식단 관리 실행
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
