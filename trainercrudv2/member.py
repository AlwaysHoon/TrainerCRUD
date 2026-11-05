import re
from datetime import datetime
from pathlib import Path
import json

from utils import align

class Member:
    def __init__(self, user_id:str, name:str, email:str, save_time:str, modify_time:str, same_name:int=0)->None:
        if not self.validate_user(user_id):
            raise ValueError("아이디 형식이 잘못되었습니다.")
        self.__user_id = user_id
        self.name = name
        self.email = email
        self.save_time = save_time
        self.modify_time = modify_time
        
        self.__details = None
        self.same_name = same_name
        
    def __repr__(self):
        return (
            f"Member\n"
            f"아이디: {self.user_id}\n"
            f"이름  : {self.name}\n"
            f"이메일: {self.email}\n\n"
            f"{self.details}\n"
        )
    #------------아이디(읽기전용)------------
    @property
    def user_id(self)->str:
        return self.__user_id
    @staticmethod
    def validate_user(user_id):
        if not isinstance(user_id, str):
            return False
        pattern = r"^[A-Za-z0-9]{2,10}$"
        return re.fullmatch(pattern, user_id) is not None
    
    #------------이름(읽기/수정)------------
    @property
    def name(self) ->str:
        return self.__name
    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            return False
        pattern = r"^(?:[가-힣]{2,}|[A-Za-z]{2,}\s+[A-Za-z]{2,})$"
        return re.fullmatch(pattern, name) is not None
    @name.setter
    def name(self, value:str):
        if not self.validate_name(value):
            raise ValueError("이름 형식이 다릅니다.(2자 이상)")
        self.__name = value
        
    #------------이메일(읽기/수정)------------
    @property
    def email(self)->str:
        return self.__email    
    @staticmethod
    def validate_email(email):
        if not isinstance(email, str):
            return False
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.fullmatch(pattern, email) is not None
    @email.setter
    def email(self, value:str):
        if not self.validate_email(value):
            raise ValueError("이메일 형식이 잘못되었습니다.")
        self.__email = value
    
    #------------디테일------------
    @property
    def details(self):
        return self.__details
    
    def set_details(self, details):
        if not isinstance(details, Details):
            raise TypeError("Details 정보가 없습니다.")
        self.__details = details
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "save_time": self.save_time,
            "modify_time": self.modify_time,
            "same_name": self.same_name
        }
    
class Details:
    def __init__(self, age, height, weight):
        
        self.age = age
        self.height = height
        self.weight = weight
    def __repr__(self):
        return (
            f"Details\n"
            f"나이  : {self.age}\n"
            f"키    : {self.height}\n"
            f"몸무게: {self.weight}"
        )
   
class MemberCRUD:
    def __init__(self, file_path: str):
        if file_path is None:
            file_path = Path(__file__).resolve().parent / "data" / "members.json"
       
        self.file_path = Path(file_path)
        self.__members=[]
        self.load_json()
        
    def save_json(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with self.file_path.open("w", encoding='utf-8') as f:
            json.dump(self.__members, f, ensure_ascii=False, indent=4)
        
    def load_json(self):
        if not self.file_path.exists():
            self.__members = []
            return
        
        with self.file_path.open("r", encoding='utf-8') as r:
            data = json.load(r)
        
        if not isinstance(data, list):
            raise ValueError("회원 JSON 데이터는 리스트여야 합니다.")
        self.__members = data
    
    def do_save(self):
        print(self.__members)
        while True:
            user_id = input("아이디: ")
            
            if not Member.validate_user(user_id):
                print("아이디 형식이 잘못되었습니다.")
                continue
            if any(m['user_id'] == user_id for m in self.__members):
                print("이미 존재하는 아이디입니다.")
                continue
            break
        
        while True:
            name = input("이름: ")
            
            if not Member.validate_name(name):
                print("이름 형식이 잘못되었습니다.")
                continue
            same_name = sum(m['name'] == name for m in self.__members)
            if same_name > 0:
                print(f"동명이인이 {same_name}명 존재합니다.")
           
            break
        
        while True:
            email = input("이메일: ")

            if not Member.validate_email(email):
                print("이메일 형식이 잘못되었습니다.")
                continue
            
            if any(m['email'].lower()==email.lower() for m in self.__members):
                print("이미 존재하는 이메일입니다.")
            
            break
        
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        save_time = str(today)
        modify_time = str(today)
        
        member = Member(user_id, name, email, save_time, modify_time, same_name)
        
        self.__members.append(member.to_dict())
        self.save_json()
        print("회원 등록 완료.")
        return member
        
    def do_read_one(self, user_id=None, name=None):
        pass
    
    def do_update(self, user_id=None, name=None, email=None):
        pass
    def do_delete(self, user_id=None, name=None):
        pass
    
    def add_details(self, user_id, age, height, weight):
        pass
        
    def member_page(self, page=0, page_size=10):
        max_page = (len(self.__members)-1) //10
        
        while True:
            start = page * page_size
            end = start + page_size
            page_list = self.__members[start:end]
            self.do_retrive(page_list, page, max_page)
            
            curser = input()
            if curser == "<" and page > 0:
                page -= 1
                
            elif curser == ">" and page < max_page:
                page += 1
                
            elif curser == "^":
                print("검색 실행\n")
                return True
            
            elif curser in ("o", "ㅐ"):
                print("이전으로 돌아갑니다.\n")
                return False
            
            elif curser in ("p","ㅐ"):
                print("프로그램을 종료합니다.\n")
                return "0"
            
            else:
                print("잘못된 접근입니다.\n")
            
    def do_retrive(self, members, page, max_page):
        print(f"{'=======전체 회원 리스트=======':^78}")
        for index, member in enumerate(members):
            
            if (index % 2) == 0:
                l = [(key, value) for key, value in member.items() if key not in ("최초 등록일", "최근 수정일")]
                if index == (len(members) - 1):
                    print(f"+ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ+ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 2:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ+")
                    for i in range(len(l)):
                        l_key, l_value = l[i][0], l[i][1]
                        print(f"| {l_key:<{12 - align(l_key)}}:   {l_value:<{24 - align(l_value)}} | {' ':<12}:   {'':<24} |")
            else:
                r = [(key, value) for key, value in member.items() if key not in ("최초 등록일", "최근 수정일")]
                print(f"+ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ+ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{(page * 10) + index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ+")
                for i in range(len(l)):
                    l_key, l_value, r_key, r_value = (l[i][0], l[i][1], r[i][0], r[i][1],)
                    print(f"| {l_key:<{12 - align(l_key)}}:   {l_value:<{24 - align(l_value)}} | {r_key:<{12 - align(r_key)}}:   {r_value:<{24 - align(r_value)}} |")
        print("+ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ+ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ+")
        print("[돌아가기: o, 종료: p]",f"{"< 이전 | ^검색 | 다음 >":^30}",f"({page + 1}/{max_page + 1} 페이지)")
        return True
    
    
def member_interface(member):
    while True:
        manage_mod = "========회원 관리 모드========"
        line3 = len(manage_mod) + align(manage_mod)
        print(manage_mod)
        print(
            " 1. 회원 등록\n"
            " 2. 전체 회원 조회\n"
            " 3. 회원 정보 수정\n"
            " 4. 회원 삭제\n"
            " o. 이전으로\n"
            " p. 프로그램 종료")
        print("=" * line3)
        
        num = input("번호선택: ")
        if num == "1":
            member.do_save()
        elif num == "2":
            member.member_page()
        elif num == "3":
            member.do_update()
        elif num == "4":
            member.do_delete()
        elif num == "o":
            print('돌아가기')
            return True
        elif num == "p":
            print("프로그램 종료")
            return False
        
        
if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    member_path = DATA_DIR / "members.json"
    
    # DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    member = MemberCRUD(member_path)
    member_interface(member)
            
    
    