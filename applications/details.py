import os
import json
from datetime import datetime
from functools import wraps
from .utils import align

class DetailsCRUD:
    def __init__(self, member_dir):
        self.member_dir = member_dir  # 예: data/members
        self._yes = ("y","yes", "네", "예","ㅛ")
        self._no = ("n", "no", "아니오","ㅜ")

    def _get_folder(self, user_id):
        return os.path.join(self.member_dir, user_id)

    def _get_path(self, user_id):
        return os.path.join(self._get_folder(user_id), "details.json")

    def _read_data(self, user_id):
        path = self._get_path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _write_data(self, user_id, details):
        
        details.sort(key=lambda details: details["최근 수정일"])

        os.makedirs(self._get_folder(user_id), exist_ok=True)  # 개인 폴더가 없으면 생성
        with open(self._get_path(user_id), "w", encoding="utf-8") as f:
            json.dump(details, f, ensure_ascii=False, indent=4)
            
    def _delete_data(self, user_id):
        path = self._get_path(user_id)
        folder = self._get_folder(user_id)

        try:
            os.remove(path)
            print("파일 삭제 완료.\n")

        except FileNotFoundError:
            print("파일이 존재하지 않습니다.\n")
            return False

        except OSError as e:
            print(f"파일 삭제 실패: {e}\n")
            return False

        try:
            os.rmdir(folder)
            print("빈 폴더 삭제 완료.\n")

        except OSError:
            pass  # 폴더에 다른 파일이 남아 있다면 유지

        return True

    def do_save(self, member):
        user_id = member["아이디"]
        details = self._read_data(user_id)

        existing = next(
            (d for d in details if d["아이디"] == user_id),
            None
        )

        # 기존 데이터가 존재하면 수정 여부 확인
        if existing is not None:
            print(f"{member['이름']}님의 기존 정보가 존재합니다.")

            is_modify = input("기존 정보를 수정하시겠습니까?(Y/N): ").strip().lower()

            return self._move_modify(is_modify, member)

        # 신규 데이터 등록
        age = input("나이를 입력하세요: ").strip()
        gender = input("성별을 입력하세요: ").strip()
        height = input("키를 입력하세요(cm): ").strip()
        weight = input("몸무게를 입력하세요(kg): ").strip()
        fat = input("체지방량을 입력하세요(kg): ").strip()
        skl_muscle = input("골격근량을 입력하세요(kg): ").strip()
        
        bmi = round(int(weight) / (int(height) / 100) ** 2, 2)
        
        bmr = 10 * int(weight) + 6.25 * int(height) - 5 * int(age)
        bmr += 5 if gender == "남" else -161
        bmr = round(bmr, 2)
        # 기초대사량, bmi, 골격근량, 체지방량
        
        
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")

        new_details = {
            "아이디": user_id,
            "이름": member["이름"],
            "나이": age,
            "성별": gender,
            "키": height,
            "몸무게": weight,
            "체지방량": fat,
            "골격근량": skl_muscle,
            "BMI": bmi,
            "기초대사량": bmr,
            "최초 등록일": today,
            "최근 수정일": today
        }

        print("-" * 40)
        for key, value in new_details.items():
            print(f"{key:<{12-align(key)}}: {value}")
        print("-" * 40)

        is_save = input("위 정보를 등록하시겠습니까?(Y/N): ").strip().lower()

        return self._add_details(is_save, member, new_details)
    
    def show_details(self, member):
        details = self._read_data(member["아이디"])
        
        for detail in details:
            if detail["아이디"] == member["아이디"]:
                print("-"*40)
                for key, value in detail.items():
                    print(f"{key:<{12-align(key)}}: {value}")
                print("-"*40)

    def _check_yn(func):
        
        @wraps(func)
        def decorated(self, is_yes, *args, **kwargs):
            while True:
                if is_yes in self._yes:
                    return func(self, *args, **kwargs)
                elif is_yes in self._no:
                    print("이전으로 돌아갑니다.\n")
                    return False
                else:
                    print("잘못 입력했습니다.\n")
                    is_yes = input("다시 입력해주세요(Y/N): ").strip().lower()
                    
        return decorated 
    
    def do_modify(self, member):
        user_id = member["아이디"]
        details = self._read_data(user_id)

        existing = next(
            (d for d in details if d["아이디"] == user_id),
            None
        )

        if existing is None:
            print("등록된 신체 정보가 없습니다.\n")
            return False

        print(f"\n{member['이름']}님의 기존 정보")
        self.show_details(member)

        height = input(
            f"키를 입력하세요(cm, 기존: {existing['키']}): "
        ).strip()

        weight = input(
            f"몸무게를 입력하세요(kg, 기존: {existing['몸무게']}): "
        ).strip()

        # 입력하지 않은 항목은 기존 값 유지
        new_details = existing.copy()

        if height:
            new_details["키"] = height

        if weight:
            new_details["몸무게"] = weight

        new_details["최근 수정일"] = datetime.now().strftime(
            "%y/%m/%d %H:%M:%S"
        )

        print("\n수정할 정보")
        print("-" * 40)
        for key, value in new_details.items():
            print(f"{key:<{12-align(key)}}: {value}")
        print("-" * 40)

        is_modify = input(
            "위 정보로 수정하시겠습니까?(Y/N): "
        ).strip().lower()

        return self._update_details(is_modify, member, new_details)
    
    def do_delete(self, member):
        user_id = member["아이디"]
        details = self._read_data(user_id)

        existing = next(
            (d for d in details if d["아이디"] == user_id),
            None
        )

        if existing is None:
            print("삭제할 신체 정보가 없습니다.\n")
            return False

        print(f"\n{member['이름']}님의 신체 정보")
        self.show_details(member)

        is_delete = input(
            "정말 해당 정보를 삭제하시겠습니까?(Y/N): "
        ).strip().lower()

        return self._remove_details(is_delete, member)
        
    @_check_yn
    def _move_modify(self, member):
        return self.do_modify(member)


    @_check_yn
    def _add_details(self, member, new_details):
        details = self._read_data(member["아이디"])

        details.append(new_details)
        self._write_data(member["아이디"], details)

        print(f"{member['이름']}님 정보 등록에 성공했습니다.")
        return True

    @_check_yn
    def _update_details(self, member, new_details):
        details = self._read_data(member["아이디"])

        for i, detail in enumerate(details):
            if detail["아이디"] == member["아이디"]:
                details[i] = new_details
                self._write_data(member["아이디"], details)

                print(f"{member['이름']}님 정보 수정에 성공했습니다.")
                return True

        print("수정할 데이터를 찾지 못했습니다.")
        return False

    @_check_yn
    def _remove_details(self, member):
        return self._delete_data(member["아이디"])
    
    # ---------- 회원 삭제 연동 ----------
    def remove_member_data(self, user_id):
        '''회원 삭제 시 호출: 식단 기록을 빈 리스트로 초기화 (개인 폴더의 다른 파일은 건드리지 않음)'''
        return self._delete_data(user_id)


if __name__ == "__main__":
    # 단독 테스트용: members.json의 첫 번째 회원으로 식단 관리 실행
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    member_path = os.path.join(DATA_DIR, "members.json")

    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)

   
    
    if members:
        diet = DetailsCRUD(os.path.join(DATA_DIR, "members"))
        
    else:
        print("등록된 회원이 없습니다.")
