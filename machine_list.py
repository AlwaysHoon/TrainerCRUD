import os
import json
from datetime import datetime

from utils import align, wrap

#body_list->machine_list, machine->muscle
class MachineList:
    def __init__(self, machine_path):
        self.machine_path = machine_path
        with open(self.machine_path, "r", encoding='utf-8') as f:
            self.body_list = json.load(f)  # load machines.json
            
    # 운동 부위를 메인, 서브로 운동 종목
    def do_save(self):
            machine_list = []
            #machine id?
            # machine_id = input("운동id를 입력하세요: ")
            muscle = input("운동 부위을 입력하세요: ").strip()
            
            #운동 종목 이름만 중복처리
            for body in self.body_list:
                if body['muscle'] == muscle:
                    print("이미 존재하는 운동 부위입니다.")
                    return False
            
            #운동부위 연속입력
            while True :
                machine = input("운동 종목을 입력하세요: ").strip()
                machine_list.append(machine)
                go = input("운동 종목을 계속 입력하시겠습니까?(Y/N): ").strip().lower()
                if not go in ("y", "yes", "네", "예"):
                    break
            
            #최초 등록일, 최근 수정일
            today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
            save_time = str(today)
            modify_time = str(today)
            
            new_machine = {
                           'muscle': muscle,
                           'machines': machine_list,
                           'save_time': save_time,
                          'modify_time': modify_time}
            
            # 전체 멤버 데이터베이스에 새 멤버 등록
            self.body_list.append(new_machine)
            with open(self.machine_path, mode='w', encoding='utf-8') as f:
                json.dump(self.body_list, f, ensure_ascii=False, indent=4)
                
            print(f"{muscle}: {machine_list} 등록에 성공했습니다.")
            return True
    
    def do_retrive(self):
        if self.body_list:
            print(f"{"=====전체 운동 부위 리스트=====":^60}")
            for index, muscle in enumerate(self.body_list.copy()):
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for key, value in muscle.items():
                    #운동 부위는 리스트여서 따로 처리
                    if key == 'machines':
                        for i, line in enumerate(wrap(value)):
                            if i == 0:
                                print(f"| {key:<{13-align(key)}}: {line:^{45-align(str(line))}} |")
                            else:
                                print(f"| {" ":<{13-align(key)}}: {line:^{45-align(str(line))}} |")

                    else:
                        print(f"| {key:<{13-align(key)}}: {value:^{45-align(value)}} |")
            print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
            return True
        
        else:
            print("등록된 운동이 없습니다.")
            return False
            
    def do_select_one(self, select_num="1"):
        if self.body_list:
            word = {"1":"조회", "3":"수정", "4":"삭제"}[select_num]
            select_muscle = input(f"{word} 할 운동 부위 이름을 입력해주세요: ").strip().lower()
            is_muscle = False # 중복이 없기에 T/F
            detail_muscle = None
            
            for muscle in self.body_list:
                if select_muscle == muscle['muscle'].lower():
                    is_muscle = True
                    detail_muscle = muscle
                    break
            
            if is_muscle:
                print("ㅡ" * 25)
                for key, value in detail_muscle.items():
                    print(f"{key:<12}: ", value)
                print("ㅡ" * 25)
                
                #수정필요
                if select_num == "1": #전체조회"2"->개인검색"1"
                    return detail_muscle
                
                elif select_num == "3": #정보수정"3"
                    is_modify = input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_modify in ("y", "yes", "예", "네"):
                        # have to solve
                        if not self.modify_machine(detail_muscle):
                            return False
                        
                        with open(self.machine_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.body_list, f, ensure_ascii=False, indent=4)
                        return True
                    
                    else:
                        print("이전으로 돌아갑니다.")
                        return True
                    
                elif select_num == "4": #정보삭제"4"
                    is_delete = input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_delete in ("y", "yes", "예", "네"):
                        self.body_list.remove(detail_muscle)
                        
                        with open(self.machine_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.body_list, f, ensure_ascii=False, indent=4)
                        print("운동 부위 삭제에 성공했습니다.")
                        return True
                    
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
            else:
                print("존재하지 않는 운동입니다.")
                return False        
            
        else:
            print("등록된 운동이 없습니다.")
            return False
        
    def modify_machine(self, select_muscle):
        print("운동 정보 수정을 시작합니다.\n")
        #운동 부위 수정
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[muscle, machines, ...]: ").strip()
            for muscle in self.body_list:
                if muscle == select_muscle:
                    if modify_key == "muscle":
                        while True:
                            modify_value = input(f"기존 {modify_key}는 {muscle[modify_key]}입니다. 변경할 내용을 적어주세요: ").strip()
                            if modify_value in [muscle[modify_key] for muscle in self.body_list]:
                                print(f"이미 존재하는 {modify_key}입니다.")
                            else:
                                break
                            
                            is_modify = input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower()
                            if is_modify in ("y", "yes", "예", "네"):
                                muscle[modify_key] = modify_value
                                muscle['modify_time'] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                print(f"{modify_key} 변경에 성공했습니다.")
                                return True
                            
                            else:
                                print("\n이전으로 돌아갑니다.\n")
                    
                    
                    #한 종목 안에 운동부위 중복 처리 필요
                    elif modify_key == "machines":
                        while True:
                            print(
                                "ㅡㅡㅡㅡㅡㅡㅡㅡ\n"
                                f"{muscle['muscle']:^16}\n"
                                "ㅡㅡㅡㅡㅡㅡㅡㅡ\n"
                                " 1. 내용 수정\n"
                                " 2. 내용 삭제\n"
                                " 3. 내용 추가\n"
                                " 9. 이전으로\n"
                                " 0. 프로그램 종료\n"
                                "ㅡㅡㅡㅡㅡㅡㅡㅡ")
                            choose_mod = input("모드를 선택해주세요: ").strip()
                            if (choose_mod == "1") or (choose_mod == "2") or (choose_mod == "3"):
                                new_machines=[]
                                print(f"ㅡㅡㅡㅡ{muscle['muscle']}의 운동 부위 목록ㅡㅡㅡㅡ")
                                for i, v in enumerate(muscle[modify_key]):
                                    print(f"{i+1:3d}. {v}")
                                    new_machines.append(v)
                                print("ㅡ"*len(f"ㅡㅡㅡㅡ{[muscle['muscle']]}의 운동 부위 목록ㅡㅡㅡㅡ")) #align확인
                            
                            if choose_mod == "1":
                                select_machine = int(input("변경할 운동 종류를 선택하세요(숫자). ").strip())
                                if select_machine > len(new_machines):
                                    print("잘못 입력했습니다.")
                                    
                                else:
                                    print(f"{new_machines[select_machine-1]}가 선택되었습니다.")
                                    rename_machine = input("변경할 단어를 입력해주세요: ").strip()
                                    new_machines[select_machine-1] = rename_machine
                                    muscle[modify_key] = new_machines
                                    print(f"{rename_machine}으로 변경했습니다.")
                                    #계속하십니까를 넣어도 되고
                                    
                            
                            elif choose_mod == "2":
                                select_machine = int(input("삭제할 운동 종류를 선택하세요(숫자). ").strip())
                                if select_machine > len(new_machines):
                                    print("잘못 입력했습니다.")
                                    
                                else:
                                    blank = new_machines[select_machine-1]
                                    new_machines.pop(select_machine-1)
                                    print(new_machines)
                                    muscle[modify_key] = new_machines
                                    print(f"{blank}를 삭제했습니다.")
                            
                            elif choose_mod == "3":
                                add_machine = input("추가할 운동 종류를 입력하세요: ").strip()
                                new_machines.append(add_machine)
                                muscle[modify_key] = new_machines
                                print(f"{add_machine}을 추가했습니다.")
                            
                            elif choose_mod == "9":
                                print("이전으로 돌아갑니다.")
                                return True
                            
                            elif choose_mod == "0":
                                print("프로그램을 종료합니다.")
                                return False
                            
                            else:
                                print("잘못된 접근입니다.")
                                is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                                if is_continue in ("y", "yes", "예", "네"):
                                    print("\n")
                                else:
                                    return 
                        
                        
                    else:
                        print("잘못된 접근입니다.")
                        is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                        if is_continue in ("y", "yes", "예", "네"):
                            print("\n")
                        else:
                            return 
        
    def sort_body_list(self):
        pass
    
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
    machine_path = os.path.join(DATA_DIR, 'machines.json')
    
    with open(machine_path, "r", encoding='utf-8') as f:
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
        # elif select_num == "4":
        #     machine_list.do_select_one(select_num)
        elif select_num == "5":
            print("종료")
            break               
                