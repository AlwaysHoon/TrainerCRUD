import json
import os
from datetime import datetime, date



class TrainerCRUD():
    def __init__(self, member_path):
        self.member_path = member_path
        with open(self.member_path, "r", encoding='utf-8') as f:
            self.members = json.load(f)  # load members.json
        
    def do_save(self):
        today = datetime.now().strftime("%y%m%d")
        if self.members:
            ymd = self.members[-1]['user_id']
            if ymd[:6] == str(datetime.now().strftime("%y%m%d")):
                count = int(ymd[6:]) + 1
            else:
                count = 0
        else:    
            count = 0
            
        if count>999:
            print("하루 최대 등록 인원을 초과했습니다.")
            return False
        
        user_id = str(today)+f'{count:03d}'
        name = input("이름을 입력하세요: ")
        email = input("이메일을 입력하세요: ")
        
        for member in self.members:
            if (member['user_id'] == user_id):
                print("이미 존재하는 멤버입니다.")
                return False
            elif (member['name'] == name):
                print("이미 존재하는 이름입니다.")
                return False
            elif (member['email'] == email):
                print("이미 존재하는 이메일입니다.")
                return False
        
        new_member = {'user_id': user_id,
                      'name': name,
                      'email': email}
        self.members.append(new_member)
        
        with open(self.member_path, mode='w', encoding='utf-8') as f:
            json.dump(self.members, f, ensure_ascii=False, indent=4)
            
        print(f"{user_id}: {name} 등록에 성공했습니다.")
        
        return True
    
    
    def do_retrive(self):
        return self.members.copy()
    
    def do_select_one(self, user_id):
    
            for member in self.members:
                if member['user_id'] == user_id:
                    print("회원 조회에 성공했습니다.")
                    return member
            print("회원이 존재하지 않습니다.")
            return None
        
    def do_delete(self, user_id):

        for member in self.members:
            if member['user_id'] == user_id:
                self.members.remove(member)
                print("회원 삭제에 성공했습니다.")
                return True
        print("회원 삭제에 실패했습니다.")
        return False
        
        
def trainer_interface(t_system):
    
    while True:
        print(
            "=========GYM LOG=========\n"
            "1. 회원 등록 및 관리\n"
            "2. 운동 종목 관리\n"
            "3. 회원별 운동 기록 등록\n"
            "4. 회원별 운동 기록 조회\n"
            "5. 프로그램 종료\n"
            "=========================\n"
            )
        
        select = input("번호를 입력하세요: ")
        if select == "1":
            print(
                "1. 회원 등록 및 관리를 선택하셨습니다.\n"
                "ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n"
                "1.회원 등록\n"
                "2.회원 조회\n"
                "ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
            
            select1 = input("번호를 입력하세요: ")
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            if select1 == "1":
                
                print("회원 등록")
                t_system.do_save()
                
                # 여기서 작성한 고유번호/이름/이메일을 이용하여 개인폴더 생성
                #그리고 각 폴더에 details/diet/records/requires.json 생성
                
            elif select1 == "2":
                tot_mem = t_system.do_retrive()
                print("전체 회원: ", tot_mem)
            else:
                pass
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        
        elif select == "2":
            print("2. 운동 종목 관리를 선택하셨습니다.\n")
        elif select == "3":
            print("3. 회원별 운동 기록 등록을 선택하셨습니다.\n")
        elif select == "4":
            print("4. 회원별 운동 기록 조회를 선택하셨습니다.\n")
        elif select == "5":     
            print("프로그램을 종료합니다.\n")
            break
        else:
            print("잘못된 접근입니다.\n")

if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, 'members.json') 
    train_sys = TrainerCRUD(member_path)
    # details_path = os.path.join(DATA_DIR,'details.json')
    # records_path = os.path.join(DATA_DIR,'records.json')
    # requires_path = os.path.join(DATA_DIR,'requires.json')
    # diet_path = os.path.join(DATA_DIR,'diet.json')
    
    # with open(member_path, "r", encoding='utf-8') as f:
    #     member_data = json.load(f)
        
    # print(f"data: {member_data}, type: {type(member_data)}")
    
    
    
    trainer_interface(train_sys)