import os
import json
from datetime import datetime

class MachineList2:
    def __init__(self):
        self.machine = []
        self.body=[]
        pass
    
    #운동 부위별 분류
    def sort_machine(self):
        print("운동 부위별 분류")
        
        
        
class MachineList:
    def __init__(self, machine_path):
        self.machine_path = machine_path
        with open(self.machine_path, "r", encoding='utf-8') as f:
            self.machines = json.load(f)  # load machines.json
            
    def do_save(self):
        print("운동 종목을 등록합니다.")    
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        
        body_list=[]
        #machine id?
        # machine_id = input("운동id를 입력하세요: ")
        machine_name = input("운동 종목을 입력하세요: ")
        for machine in self.machines:
            if (machine['machine'] == machine_name):
                print("이미 존재하는 운동 종목입니다.")
                return False
        
        while True :
            body = input("운동 부위를 입력하세요: ")
            body_list.append(body)
            go = input("운동 부위를 계속 입력하시겠습니까?(Y/N): ").strip().lower()
            if not go in ("y", "yes", "네", "예"):
                break
            
        save_time = str(today)
        modify_time = str(today)
        
        new_machine = {'machine': machine_name,
                       'body_list': body_list,
                       'save_time': save_time,
                      'modify_time': modify_time}
        
        # 전체 멤버 데이터베이스에 새 멤버 등록
        self.machines.append(new_machine)
        with open(self.machine_path, mode='w', encoding='utf-8') as f:
            json.dump(self.machines, f, ensure_ascii=False, indent=4)
            
        print(f"{machine_name}: {body_list} 등록에 성공했습니다.")
        
        return True
    
    def do_retrive(self):
        if self.machines:
            
            print("=======전체 운동 리스트=======")
            for index, machine in enumerate(self.machines.copy()):
                print(f"+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
                for key, value in machine.items():
                    if type(value) == type([]):
                        print(f"| {key:<13}: {str(value)[1:-1]:^45} |")
                    else:
                        print(f"| {key:<13}: {value:^45} |")
            print("+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+")
            return True
        
        else:
            print("등록된 운동이 없습니다.")
            return False
            
            
            
    def do_select_one(self, select_num="1"):
        if self.machines:
            word = {"1":"조회", "3":"수정", "4":"삭제"}[select_num]
            print(f"{select_num}. 운동 종목 {word}를 선택했습니다.")
            select_machine = input(f"{word} 할 운동 이름을 입력해주세요: ")
            is_machine=False #중복운동 관리할때 count=1로 만들면 바로 관리가능
            detail_machine=None
            
            for machine in self.machines:
                if select_machine == machine['machine']:
                    is_machine =True
                    detail_machine = machine
                    break
            
            if is_machine:
                print("ㅡ" * 25)
                for key, value in detail_machine.items():
                    print(f"{key:<12}: ", value)
                print("ㅡ" * 25)
                
                if select_num == "1": #전체조회"2"->개인검색"1"
                    return detail_machine
                
                elif select_num == "3": #정보수정"3"
                    is_modify = input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_modify in ("y", "yes", "예", "네"):
                        self.modify_machine(detail_machine)
                        
                        with open(self.machine_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.machines, f, ensure_ascii=False, indent=4)
                        
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
                    
                elif select_num == "4": #정보삭제"4"
                    is_delete = input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_delete in ("y", "yes", "예", "네"):
                        self.machines.remove(detail_machine)
                        
                        with open(self.machine_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.machines, f, ensure_ascii=False, indent=4)
                        print("운동 삭제에 성공했습니다.")
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
        
        #list인 운동부위를 따로 지정해야함
        
    def modify_machine(self, select_machine):
        print("운동 정보 수정을 시작합니다.\n")
        # option = [key for key, _ in select_machine.items()]
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[machine, body_list, ...]: ")
            if modify_key in select_machine:
                for machine in self.machines:
                    if machine == select_machine:
                        while True:
                            modify_value=input(f"기존 {modify_key}는 {machine[modify_key]}입니다. 변경할 내용을 적어주세요: ")
                            if modify_value in [machine[modify_key] for machine in self.machines]:
                                print(f"이미 존재하는 {modify_key}입니다.")
                            else:
                                break
                        is_modify = input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower()
                        if is_modify in ("y", "yes", "예", "네"):
                        
                            machine[modify_key]=modify_value
                            machine['modify_time'] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                            print(f"{modify_key} 변경에 성공했습니다.")
                            return True
                        else:
                            print("\n이전으로 돌아갑니다.\n")
            
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
        select_num = input("번호 입력: ")
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
                