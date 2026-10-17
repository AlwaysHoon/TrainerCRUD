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

def login_interface():
    print("========관리자===========")
    while True:
        login_id = input("관리자id: ").strip()
        if login_id != "admin":
            print("존재하지 않는 관리자입니다.")
        else:
            break
        
    while True:
        pw = input("관리자pw: ").strip()
        if pw != "0000":
            print("비밀번호가 틀렸습니다.")
        else:
            break
    print("========================")   

def trainer_interface():
    while True:        
        print(
            "========회원 관리 모드========\n"
            "1. 회원 등록\n"
            "2. 전체 회원 조회\n"
            "3. 회원 정보 수정\n"
            "4. 회원 삭제\n"
            "5. 처음으로\n"
            "6. 프로그램 종료\n"
            "=======================\n"
            )
        select_num = input("번호를 입력하세요: ").strip()
        if select_num == "1":
            print(
                "1. 회원 등록을 선택하셨습니다.\n")
            
            print("중복된다면 회원 등록 실패")
            print("아니라면 등록에 성공")
            
            print("user_id, name 등록에 성공했습니다.")
            # 여기서 작성한 고유번호/이름/이메일을 이용하여 개인폴더 생성
            #그리고 각 폴더에 details/diet/records/requires.json 생성  
                
        elif select_num == "2":
            print("전체 회원 조회: ")
            print("members.json의 전체 멤버를 출력")
            # 그냥 리스트 자체를 출력할지, 틀에 맞춰 출력할지 선택
            #detail_interface()
        elif select_num == "3":
            print("회원 정보 수정")
            
        elif select_num == "4":
            print("회원 삭제")
        
        elif select_num == "5":
            pass
        elif select_num == "6":
            print("프로그램을 종료합니다.\n")
            break
        else:
            print("잘못된 접근입니다.\n")
        
def detail_interface():
    #members.json의 리스트를 가져왔다고 가정
    #리스트를 고유번호, 이름, 이메일만 추출
    #
    while True:
        see_more = input("(회원 이름)님을 조회하시겠습니까?(Y/N): ").strip().lower()
        if see_more in ("y", "yes", "네", "예"):
            
            print(
                "========(회원 이름)========\n"
                "1. 상세 기록 조회\n"
                "2. 요구사항 조회\n"
                "3. 운동 기록 조회\n"
                "4. 식단 조회\n"
                "5. 처음으로\n"
                "6. 프로그램 종료\n"
                "=======================\n"
                )
            detail_num = input("조회할 내용(번호)을 선택해주세요: ").strip()
            if detail_num == "1":
                print("상세 기록 조회")
            elif detail_num == "2":
                print("요구사항 조회")
            elif detail_num == "3":
                print("운동 기록 조회")
            elif detail_num == "4":
                print("식단 조회")
                
            elif detail_num == "5":
                pass
            elif detail_num == "6":
                print("프로그램을 종료합니다.\n")
                break
            else:
                print("잘못된 접근입니다.\n")
    
    
    
    
    print("------------------------------") 
        




if __name__ == "__main__":
    login_interface()
    trainer_interface()
    
            
            
            
'''
트레이너 앱
트레이너 로그인



'''
