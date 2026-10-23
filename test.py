import json
import os
from datetime import datetime, date


from datetime import datetime, date

import unicodedata  # unicodedata.east_asian_width
from utils import align

import msvcrt

def show_members(members):
    if not members:
        print("등록된 회원이 없습니다.")
        return False

    selected = 0
    page_size = 6  # 한 화면에 회원 6명 (3행 × 2열)

    while True:
        

        start = (selected // page_size) * page_size
        end = min(start + page_size, len(members))

        print(f"{'=======전체 회원 리스트=======':^86}")
        print()

        for index in range(start, end, 2):
            left = members[index]
            right = (
                members[index + 1]
                if index + 1 < end
                else None
            )

            # 선택된 회원 표시
            l_mark = ">" if selected == index else " "
            r_mark = ">" if selected == index + 1 else " "

            print(
                f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡ No.{index + 1:03d}{l_mark}ㅡㅡㅡㅡㅡㅡㅡㅡ-+"
                f"-ㅡㅡㅡㅡㅡㅡㅡㅡㅡ No.{index + 2:03d}{r_mark}ㅡㅡㅡㅡㅡㅡㅡㅡ-+"
            )

            l = list(left.items())
            r = list(right.items()) if right else []

            for i in range(len(l)):
                l_key, l_value = l[i]
                l_key = str(l_key)
                l_value = str(l_value)

                if i < len(r):
                    r_key, r_value = r[i]
                    r_key = str(r_key)
                    r_value = str(r_value)
                else:
                    r_key, r_value = "", ""

                print(
                    f"| {l_key:<{15 - align(l_key)}}: "
                    f"{l_value:^{25 - align(l_value)}} | "
                    f"{r_key:<{15 - align(r_key)}}: "
                    f"{r_value:^{25 - align(r_value)}} |"
                )

        print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")

        print(f"\n선택 회원: No.{selected + 1:03d}")
        print("↑↓←→: 이동 | Enter: 선택 | Q: 종료")

        key = msvcrt.getch()

        if key in (b'\x00', b'\xe0'):
            key = msvcrt.getch()

            if key == b'H':  # ↑
                if selected >= 2:
                    selected -= 2

            elif key == b'P':  # ↓
                if selected + 2 < len(members):
                    selected += 2

            elif key == b'K':  # ←
                if selected % 2 == 1:
                    selected -= 1

            elif key == b'M':  # →
                if selected % 2 == 0 and selected + 1 < len(members):
                    selected += 1

        elif key == b'\r':
            return members[selected]

        elif key.lower() == b'q':
            return False
        
def align(word):
    count = sum(1 for i in word if unicodedata.east_asian_width(i) in "WF")
    return count


if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )  # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(
        BASE_DIR, "data"
    )  # C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, "members.json")
    muscle_path = os.path.join(DATA_DIR, "muscles.json")
    # train_sys = TrainerCRUD(member_path)
    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)
    with open(muscle_path, "r", encoding="utf-8") as f:
        muscles = json.load(f)
    # # if login_interface():
    # #     trainer_interface(members)
    # train_sys = TrainerCRUD(member_path)
    # # trainer_interface(train_sys)
    show_members(members)
    # print(len(members))
    # left_num, left_mem, right_num, right_mem = 0,None,0,None
    # print("=======전체 회원 리스트=======")
    # for index, member in enumerate(members):
    #     print(f"ㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡ")
    #     for key, value in member.items():
    #         print(f"{key:<8}: {value:^10}")
    # print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
    ## 2줄보기
    def align(word):
        count = sum(1 for i in word if unicodedata.east_asian_width(i) in "WF")
        return count

    # print(f"{"=======전체 회원 리스트=======":^77}")
    # for index, member in enumerate(members):
    #     if (index % 2) == 0:
    #         left=[(key,value) for key, value in member.items()]
    #         if index == (len(members)-1):
    #             print(f'+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+1:3d}ㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+2:3d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
    #             for i in range(len(left)):

    #                 print(f"| {left[i][0]:<{15-align(left[i][0])}}: {left[i][1]:^{25-align(left[i][0])}} | {" ":<13}: {" ":^25} |")
    #     else:
    #         right=[(key,value) for key, value in member.items()]
    #         print(f'+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index:3d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+1:3d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
    #         for i in range(len(left)):

    #             print(f"| {left[i][0]:<{15-align(left[i][0])}}: {left[i][1]:^{25-align(left[i][1])}} | {right[i][0]:<{15-align(right[i][0])}}: {right[i][1]:^{25-align(right[i][1])}} |")
    # print('+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
    # import os
    # import msvcrt

    # items = [f"회원 {i}" for i in range(1, 101)]

    # index = 0
    # page_size = 10

    # while True:
    #     os.system("cls")

    #     print("===== 회원 목록 =====")

    #     for item in items[index:index + page_size]:
    #         print(item)

    #     print("\n↑↓: 스크롤 | Q: 종료")

    #     key = msvcrt.getch()

    #     if key in (b'\x00', b'\xe0'):
    #         key = msvcrt.getch()

    #         if key == b'H':  # 위쪽 방향키
    #             index = max(0, index - 1)

    #         elif key == b'P':  # 아래쪽 방향키
    #             index = min(len(items) - page_size, index + 1)

    #     elif key.lower() == b'q':
    #         break
    