import os
import json
from datetime import datetime

from .utils import align, wrap
from functools import wraps

class MachineList:
    def __init__(self, machine_path):
        self.machine_path = machine_path
        self._yes = ("y","yes", "네", "예","ㅛ")
        self._no = ("n", "no", "아니오","ㅜ")
        try:
            with open(self.machine_path, "r", encoding="utf-8") as f:
                self.body_list = json.load(f)
                
        except FileNotFoundError:
            self.body_list = []
            with open(machine_path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    # 운동 부위를 메인, 서브로 운동 종목
    def do_save(self):
        machine_list = []
        muscle = input("운동 부위을 입력하세요: ").strip()

        # 운동 종목 이름만 중복처리
        for body in self.body_list:
            if body["muscle"] == muscle:
                print("이미 존재하는 운동 부위입니다.\n")
                return False

        # 운동부위 연속입력
        while True:
            machine = input("운동 종목을 입력하세요: ").strip()
            if machine in machine_list:
                print("중복내용입니다.\n")
            else:
                machine_list.append(machine)

            go = input("운동 종목을 계속 입력하시겠습니까?(Y/N): ").strip().lower()
            if not go in self._yes:
                break

        # 최초 등록일, 최근 수정일
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        save_time = str(today)
        modify_time = str(today)

        new_machine = {
            "muscle": muscle,
            "machines": machine_list,
            "save_time": save_time,
            "modify_time": modify_time,
        }
        print("-"*20)
        print(
            f"운동 부위\t: {muscle}\n"
            f"운동 종목\t: {machine_list}")
        print("-"*20)
        is_save = input("위 정보가 맞습니까?(Y/N): ").strip().lower()
        return self._add_muscle(is_save, new_machine)
        # 전체 멤버 데이터베이스에 새 멤버 등록

    def do_retrive(self):
        if self.body_list:
            print(f"{'=====전체 운동 부위 리스트=====':^60}")
            for index, muscle in enumerate(self.body_list.copy()):
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for key, value in muscle.items():
                    # 운동 부위는 리스트여서 따로 처리
                    if key == "machines":
                        for i, line in enumerate(wrap(value)):
                            if i == 0:
                                print(f"| {key:<{13 - align(key)}}: {line:<{45 - align(str(line))}} |")
                            else:
                                print(f"| {' ':<{13 - align(key)}}: {line:<{45 - align(str(line))}} |")

                    else:
                        print(f"| {key:<{13 - align(key)}}: {value:<{45 - align(value)}} |")
            print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
            return True

        else:
            print("등록된 운동이 없습니다.\n")
            return False
        
    
    
    def do_select_one(self, select_num="1"):
        if self.body_list:
            word = {"1": "조회", "3": "수정", "4": "삭제"}[select_num]
            select_muscle = (input(f"{word} 할 운동 부위 이름을 입력해주세요: ").strip().lower())
              # 중복이 없기에 T/F
            detail_muscle = self._find_same('muscle', select_muscle)
            is_muscle = len(detail_muscle)
            

            if is_muscle == 1:
                idx=0
                print("ㅡ" * 30)
                for key, value in detail_muscle[idx].items():
                    if key == "machines":
                        for i, line in enumerate(wrap(value)):
                            if i == 0:
                                print(f"{key:<{12 - align(key)}}: {line:<{45 - align(str(line))}}")
                            else:
                                print(f"{' ':<{12 - align(key)}}: {line:<{45 - align(str(line))}}")
                    else:
                        print(f"{key:<12}: {value:<45}")
                print("ㅡ" * 30)

                # 수정필요
                if select_num == "1":  # 전체조회"2"->개인검색"1"
                    return detail_muscle[idx]

                elif select_num == "3":  # 정보수정"3"
                    is_modify = (input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_modify(is_modify, detail_muscle, idx)
                    
                elif select_num == "4":  # 정보삭제"4"
                    is_delete = (input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower())
                    return self.do_delete(is_delete, detail_muscle, idx)
                    
            elif is_muscle == 0:
                print("존재하지 않는 운동입니다.\n")
                return True

        else:
            print("등록된 운동이 없습니다.\n")
            return False
        
    
            
    def modify_machine(self, select_muscle, idx):
        print("운동 정보 수정을 시작합니다.\n")
        # 운동 부위 수정
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[muscle, machines, ...](돌아가려면 o 입력): ").strip()
            
            for muscle in self.body_list:
                if muscle == select_muscle[idx]:
                    if modify_key == "muscle":
                        while True:
                            modify_value = input(f"기존 {modify_key}는 {muscle[modify_key]}입니다. 변경할 내용을 적어주세요(돌아가려면 o 입력): ").strip()
                            if modify_value == muscle[modify_key]:
                                print("기존 단어로 바꿀 수 없습니다.\n")
                            elif modify_value.lower() in [muscle[modify_key].lower() for muscle in self.body_list]:
                                print(f"이미 존재하는 {modify_key}입니다.\n")
                            elif modify_value == "o":
                                print("이전으로 돌아갑니다.\n")
                                return True
                            else:
                                break
                        
                        while True:
                            is_modify = (input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower())
                            if is_modify in self._yes:
                                muscle[modify_key] = modify_value
                                muscle["modify_time"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                try:
                                    self._save_muscles()
                                    print(f"{modify_key} 변경에 성공했습니다.\n")
                                    return True
                                except MemoryError:
                                    print(f"{modify_key} 변경에 실패했습니다.\n")
                            
                            elif is_modify in self._no:
                                print("이전으로 돌아갑니다.\n")
                                return True
                            else:
                                print("잘못 입력했습니다.\n")
                                break

                    # 한 종목 안에 운동부위 중복 처리 필요
                    elif modify_key == "machines":
                        while True:
                            print("ㅡ" * 30)
                            print(f"[{muscle['muscle']:^55}]")
                            print("ㅡ" * 30)
                            for key, value in muscle.items():
                                if key == "machines":
                                    for i, line in enumerate(wrap(value)):
                                        if i == 0:
                                            print(f"{key:^{13 - align(key)}}: {line:<{45 - align(str(line))}}")
                                        else:
                                            print(f"{' ':<{13 - align(key)}}: {line:<{45 - align(str(line))}}")
                            
                            print("ㅡ" * 30)
                            print(
                                " 1. 내용 추가\n"
                                " 2. 내용 수정\n"
                                " 3. 내용 삭제\n"
                                " o. 이전으로\n"
                                " p. 프로그램 종료")
                            print("ㅡ" * 30)
                            
                            choose_mod = input("모드를 선택해주세요: ").strip()
                            if choose_mod in ("1","2","3"):
                                new_machines = []
                                muscle_list = f"ㅡㅡㅡㅡ{muscle['muscle']}의 운동 부위 목록ㅡㅡㅡㅡ"
                                line = len(muscle_list)
                                print(muscle_list)
                                for i, v in enumerate(muscle[modify_key]):
                                    print(f"{i + 1:3d}. {v}")
                                    new_machines.append(v)
                                print("ㅡ" * line)  # align확인

                            if choose_mod == "1":
                                add_machine = input("추가할 운동 종류를 입력하세요: ").strip()
                                if add_machine in new_machines:
                                    print("이미 존재하는 운동입니다.\n")
                                else:
                                    new_machines.append(add_machine)
                                    muscle[modify_key] = new_machines
                                    self._save_muscles()
                                    print(f"{add_machine}을 추가했습니다.\n")

                            elif choose_mod == "2":
                                try:
                                    select_machine = int(input("변경할 운동 종류를 선택하세요(숫자): ").strip())
                                    
                                except ValueError:
                                    print("숫자만 입력해주세요.\n")
                                    
                                else:
                                    if (select_machine < len(new_machines)) and (select_machine > 0):
                                        print(f"{new_machines[select_machine - 1]}가 선택되었습니다.\n")
                                        rename_machine = input("변경할 단어를 입력해주세요: ").strip()
                                        if rename_machine == new_machines[select_machine - 1]:
                                            print("기존 단어로 변경할 수 없습니다.\n")
                                            
                                        elif rename_machine in new_machines:
                                            print("이미 존재하는 운동입니다.\n")
                                            
                                        else:
                                            new_machines[select_machine - 1] = rename_machine
                                            muscle[modify_key] = new_machines
                                            self._save_muscles()
                                            print(f"{rename_machine}으로 변경했습니다.\n")
                                    else:
                                        print("잘못 입력했습니다.\n")
                                    
                            elif choose_mod == "3":
                                try:
                                    select_machine = int(input("삭제할 운동 종류를 선택하세요(숫자). ").strip())
                                except ValueError:
                                    print("숫자만 입력하세요.\n")
                                else:
                                    if (select_machine <= len(new_machines)) and (select_machine > 0):
                                        blank = new_machines[select_machine - 1]
                                        new_machines.pop(select_machine - 1)
                                        muscle[modify_key] = new_machines
                                        self._save_muscles()
                                        print(f"{blank}를 삭제했습니다.")
                                    else:
                                        print("잘못 입력했습니다.")

                            elif choose_mod == "o":
                                print("이전으로 돌아갑니다.")
                                return True

                            elif choose_mod == "p":
                                print("프로그램을 종료합니다.")
                                return False

                            else:
                                print("잘못된 접근입니다.")
                                is_continue = (input("계속하시겠습니까?(Y/N): ").strip().lower())
                                if is_continue in self._yes:
                                    print()
                                else:
                                    return True
                                
                    elif modify_key == "o":
                        print("이전으로 돌아갑니다.\n")
                        return True
                    
                    else:
                        print("잘못된 접근입니다.\n")
                        is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                        if is_continue in self._yes:
                            print()
                        else:
                            return True
                        
    def sort_machine_list(self):
        pass
    def _find_same(self, key, value):
        return [muscles for muscles in self.body_list if muscles[key].lower() == value]
    def _save_muscles(self):
        try:
            with open(self.machine_path, mode="w", encoding="utf-8") as f:
                json.dump(self.body_list, f, ensure_ascii=False, indent=4)
                
        except OSError as e:
            print(f"파일 저장 오류: {e}\n")
            
        except (TypeError, ValueError) as e:
            print(f"데이터 변환 오류: {e}\n")
            
        else:
            print("저장 완료.\n")
            return True
        
    def _check_yn(func):
        @wraps(func)
        def decorated(self, is_yes, *args, **kwargs):
            while True:
                if is_yes in self._yes:
                    return func(self, *args, **kwargs)
                elif is_yes in self._no:
                    print("이전으로 돌아갑니다.\n")
                    return True
                else:
                    print("잘못 입력했습니다.\n")
                    is_yes = input("다시 입력해주세요(Y/N): ").strip().lower()
        return decorated 
            
    @_check_yn
    def _add_muscle(self, muscle):
        self.body_list.append(muscle)
        #try?
        self._save_muscles()
        print(f"{muscle['muscle']}: {muscle['machines']} 등록에 성공했습니다.")
        return True
    
    @_check_yn
    def do_modify(self, muscle, idx):
        if not self.modify_machine(muscle, idx):
            return False
        self._save_muscles()
        return True
    
    @_check_yn
    def do_delete(self, muscle, idx):
        self.body_list.remove(muscle[idx])
        self._save_muscles()
        print("운동 부위 삭제에 성공했습니다.")
        return True
    
    
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
    machine_path = os.path.join(DATA_DIR, "muscles.json")

    with open(machine_path, "r", encoding="utf-8") as f:
        machines = json.load(f)

    machine_list = MachineList(machine_path)
    # machine_list.save_machine()
    while True:
        select_num = input("번호 입력: ").strip()
        if select_num == "1":
            machine_list.do_save()
        elif select_num == "2":
            machine_list.do_retrive()
        elif select_num == "3" or select_num == "4":
            machine_list.do_select_one(select_num)
        elif select_num == "p":
            print("종료")
            break
