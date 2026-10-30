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

        existing = next((d for d in details if d["아이디"] == user_id), None)

        # 기존 데이터가 존재하면 수정 여부 확인
        if existing is not None:
            print(f"{member['이름']}님의 기존 정보가 존재합니다.")

            is_modify = input("기존 정보를 수정하시겠습니까?(Y/N): ").strip().lower()

            return self._move_modify(is_modify, member)

        # 신규 데이터 등록
        age, gender, height, weight, fat, skl_muscle = self._input_data()
        
        bmi = self._calc_bmi(weight, height)
        bmr = self._calc_bmr(age, gender, height, weight)
        
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
    
    def _calc_bmi(self,weight, height):
        return round(float(weight) / (float(height) / 100) ** 2, 2)
    
    def _calc_bmr(self, age, gender, weight, height):
        bmr = 10 * float(weight) + 6.25 * float(height) - 5 * int(age)
        bmr += 5 if gender == "남" else -161
        bmr = round(bmr, 2)
        return bmr
    
    def _input_data(self):
        while True:
            try:
                age = int(input("나이를 입력하세요: ").strip())
                if age <= 0:
                    raise ValueError
                break
            
            except ValueError:
                print("0 이상의 숫자를 입력하세요.")
        while True:
            
            gender = input("성별을 입력하세요(남/여): ").strip()
            if gender in ("남","여"):
                break
            
            else:
                print("성별을 남/여 둘중에 하나로 입력하세요.")
        while True:
            try:
                height = float(input("키를 입력하세요(cm): ").strip())
                if height <= 0:
                    raise ValueError
                break
            
            except ValueError:
                print("0이상의 숫자를 입력하세요.")
        while True:
            try:
                weight = float(input("몸무게를 입력하세요(kg): ").strip())
                if weight <= 0:
                    raise ValueError
                break
            
            except ValueError:
                print("0 이상의 숫자를 입력하세요.")
                
        while True:
            try:
                fat = float(input("체지방량을 입력하세요(kg): ").strip())
                if fat <= 0:
                    raise ValueError
                break
            
            except ValueError:
                print("0 이상의 숫자를 입력하세요.")
                
        while True:
            try:
                skl_muscle = float(input("골격근량을 입력하세요(kg): ").strip())
                if skl_muscle <= 0:
                    raise ValueError
                break
            
            except ValueError:
                print("0 이상의 숫자를 입력하세요.")
        
        return  age, gender, height, weight, fat, skl_muscle
    
    def do_modify(self, member):
        user_id = member["아이디"]
        details = self._read_data(user_id)

        existing = next((d for d in details if d["아이디"] == user_id), None)

        if existing is None:
            print("등록된 신체 정보가 없습니다.\n")
            return False

        print(f"\n{member['이름']}님의 기존 정보")
        self.show_details(member)

        new_details = existing.copy()

        input_keys = {
            "나이": int,
            "성별": str,
            "키": float,
            "몸무게": float,
            "체지방량": float,
            "골격근량": float
        }

        for key, dtype in input_keys.items():
            while True:
                try:
                    value = input(f"{key}를 입력하세요(기존: {existing[key]}, Enter: 유지): ").strip()

                    if not value:
                        break

                    value = dtype(value)

                    if key == "성별":
                        if value not in ("남", "여"):
                            raise ValueError

                    elif key in ("나이", "키", "몸무게"):
                        if value <= 0:
                            raise ValueError

                    elif value < 0:
                        raise ValueError

                    new_details[key] = value
                    break

                except ValueError:
                    print(f"올바른 {key} 값을 입력하세요.\n")

        # BMI 및 기초대사량 재계산
        new_details["BMI"] = self._calc_bmi(new_details["몸무게"], new_details["키"])
        new_details["기초대사량"] = self._calc_bmr(new_details["나이"], new_details["성별"], new_details["몸무게"], new_details["키"])
        new_details["최근 수정일"] = datetime.now().strftime("%y/%m/%d %H:%M:%S")

        print("\n수정할 정보")
        print("-" * 40)
        for key, value in new_details.items():
            print(f"{key:<{12-align(key)}}: {value}")
        print("-" * 40)

        is_modify = input("위 정보로 수정하시겠습니까?(Y/N): ").strip().lower()

        return self._update_details(is_modify, member, new_details)
    
    def do_delete(self, member):
        user_id = member["아이디"]
        details = self._read_data(user_id)

        existing = next((d for d in details if d["아이디"] == user_id), None)

        if existing is None:
            print("삭제할 신체 정보가 없습니다.\n")
            return False

        print(f"\n{member['이름']}님의 신체 정보")
        self.show_details(member)

        is_delete = input("정말 해당 정보를 삭제하시겠습니까?(Y/N): ").strip().lower()

        return self._remove_details(is_delete, member)
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
        
    @_check_yn
    def _move_modify(self, member):
        return self.do_modify(member)


    @_check_yn
    def _add_details(self, member, new_details):
        details = self._read_data(member["아이디"])

        details.append(new_details)
        self._write_data(member["아이디"], details)

        print(f"{member['이름']}님 정보 등록에 성공했습니다.\n")
        return True

    @_check_yn
    def _update_details(self, member, new_details):
        details = self._read_data(member["아이디"])

        for i, detail in enumerate(details):
            if detail["아이디"] == member["아이디"]:
                details[i] = new_details
                self._write_data(member["아이디"], details)

                print(f"{member['이름']}님 정보 수정에 성공했습니다.\n")
                return True

        print("수정할 데이터를 찾지 못했습니다.\n")
        return False

    @_check_yn
    def _remove_details(self, member):
        return self._delete_data(member["아이디"])
    
    # ---------- 회원 삭제 연동 ----------
    def remove_member_data(self, user_id):
        return self._delete_data(user_id)


if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    member_path = os.path.join(DATA_DIR, "members.json")

    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)

    if members:
        diet = DetailsCRUD(os.path.join(DATA_DIR, "members"))
        
    else:
        print("등록된 회원이 없습니다.")
