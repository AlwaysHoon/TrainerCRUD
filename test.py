import json
import os
from datetime import datetime, date

import os
import json
from datetime import datetime, date

import unicodedata  # unicodedata.east_asian_width


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
    muscle_path = os.path.join(DATA_DIR, "muscle.json")
    # train_sys = TrainerCRUD(member_path)
    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)
    with open(muscle_path, "r", encoding="utf-8") as f:
        muscles = json.load(f)
    # # if login_interface():
    # #     trainer_interface(members)
    # train_sys = TrainerCRUD(member_path)
    # # trainer_interface(train_sys)

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
    print(members)
    for member in members:
        print(member.items())
