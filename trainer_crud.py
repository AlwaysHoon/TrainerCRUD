import os
import json
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
        
        #이름, 이메일의 작성양식 추가 필요
        user_id = str(today)+f'{count:03d}'
        name = input("이름을 입력하세요: ")
        email = input("이메일을 입력하세요: ")
        
        #일단은 중복된 존재가 없다는 가정하에 모두 중복처리를 해놨고
        #만약 동명이인에 대한 논의가 끝나면 수정필요
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
        # return self.members.copy()
        print("=======전체 회원 리스트=======")
        for index, member in enumerate(self.members.copy()):
            print(f"ㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡ")
            for key, value in member.items():
                print(f"{key:<8}: {value:^10}")
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        return True
    
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
    
    #수정중
    def do_select(self):
        select_member = input("조회 할 회원 이름을 입력해주세요: ")
        count=0 #동명이인 관리할때 count=1로 만들면 바로 관리가능
        detail_member=[]
        
        for member in self.members:
            if select_member == member['name']:
                count += 1
                detail_member.append(member)
                
        if count == 0:
            print("존재하지 않는 회원입니다.")
            return False
        
        elif count == 1:
            return detail_member[0]
        
        else:
            print("동명이인입니다.")
            print("=======동명이인 리스트=======")
            for  i, m in enumerate(detail_member):
                print(f"ㅡㅡㅡㅡㅡㅡㅡNo.{i + 1:03d}ㅡㅡㅡㅡㅡㅡㅡ")
                for key, value in m.items():
                    print(f"{key:<8}: {value:^10}")
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            same_num = input("조회할 번호를 선택하세요: ")
            
            return detail_member[int(same_num)-1]
    
    
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, 'members.json')
    # train_sys = TrainerCRUD(member_path)
    with open(member_path, "r", encoding='utf-8') as f:
                members = json.load(f)
    # if login_interface():
    #     trainer_interface(members)
    train_sys = TrainerCRUD(member_path)
    trainer_interface(train_sys)