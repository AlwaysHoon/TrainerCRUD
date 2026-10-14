'''
=======GYM LOG=======
1. 회원 등록 및 관리
2. 운동 종목 관리
3. 회원별 운동 기록 등록
4. 회원별 운동 기록 조회
5. 프로그램 종료

메뉴를 선택하세요:4
회원 ID 입력: user01

[김철수 회원 운동 기록]
10/12|벤치프레스|40kg|10회|3세트
10/13|스쿼트|60kg|12회|3세트

회원 관리CRUD: 등록, 조회, 수정, 삭제 ->필수
운동 종목 관리CRUD: 운동 종목 등록, 조회, 수정, 삭제 -> 필수
개인별 운동 기록: 회원별 운동 날짜, 무게, 횟수, 세트 기록 및 조회->핵심추가기능
데이터 저장: JSON 파일 저장 및 불러오기 ->필수
운동 기록 통계: 운동별 기록 변화 확인 ->선택

데스크 직원: 회원등록조회/회원복 및 락커 이용 기간 확인
트레이너: 회원별 운동 기록 등록 조회/운동 종목 관리

-외부 API 및 크롤링: 회원 인바디에 따른 섭취 음식 칼로리 계산(식품안전나라에서 '식품 영양성분 데이터베이스'를 오픈API 형태로 무상 제공)


'''


class GymCRUD: #회원 관리CRUD: 등록, 조회, 수정, 삭제 ->필수
    def __init__(self):
        self.members= []
    
    def do_save(self, user_id, name, email):
        """회원을 등록합니다.

        Args:
            user_id (str): user_id
            name (str): 이름
            email (str): email

        Returns:
            True  : 등록에 성공
            False : 등록에 실패(user_id가 이미 존재)
        """
        for member in self.members:
            if member['user_id'] == user_id:
                print("이미 존재하는 회원입니다.")
                return False
        
        member = {'user_id': user_id,
                  'name': name,
                  'email': email}
        self.members.append(member)
        print("회원 등록에 성공했습니다.")
        return True
    
    def do_retrive(self):
        """전체 회원 목록을 반환합니다.

        Returns:
            self.members.copy(): 전체 회원 목록
        """
        print("전체 회원 목록")
        return self.members.copy()
    
    def do_select_one(self, user_id):
        """회원 한명을 조회합니다.

        Args:
            user_id (str): user_id

        Returns:
            member: 조회한 회원
            None: 조회 실패
        """

        for member in self.members:
            if member['user_id'] == user_id:
                print("회원 조회에 성공했습니다.")
                return member
        print("회원이 존재하지 않습니다.")
        return None
    
    def do_delete(self, user_id):
        """회원 정보 삭제

        Args:
            user_id (str): 

        Returns:
            True  : 삭제 성공
            False : 삭제 실패
        """
        for member in self.members:
            if member['user_id'] == user_id:
                self.members.remove(member)
                print("회원 삭제에 성공했습니다.")
                return True
        print("회원 삭제에 실패했습니다.")
        return False

class GymMember(GymCRUD):
    def __init__(self):
        super().__init__()
    
    def do_save(self):
        self.members=[]
        if self.members:
            self.user_id = self.members[-1]['user_id'] + 1
        else:
            self.user_id = 'user01'
        print(f"user_id: {self.user_id}")
        
        
        self.name = input("이름을 입력하세요: ")
        self.email = input("이메일을 입력하세요: ")
        member = {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email}
        self.members.append(member)
        
if __name__ == "__main__":
    mod = GymMember()
    while True:
        print(
            "========GYM LOG========\n"
            "1. 회원 등록 및 관리\n"
            "2. 운동 종목 관리\n"
            "3. 회원별 운동 기록 등록\n"
            "4. 회원별 운동 기록 조회\n"
            "5. 프로그램 종료\n"
            "=======================\n"
            )
        
        select = input("번호를 입력하세요: ")
        if select == "1":
            print("1. 회원 등록 및 관리를 선택하셨습니다.\n")
            
            print("===========")
            print("1.회원 등록")
            print("2.회원 조회")
            print("===========")
            select1 = input("번호를 입력하세요: ")
            if select1 == "1":
                mod.do_save()
            elif select1 == "2":
                tot_mem = mod.do_retrive()
                print("전체 회원: ", tot_mem)
            else:
                pass
            
            
        
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
            
            
            
'''
트레이너 앱
트레이너 로그인



'''
