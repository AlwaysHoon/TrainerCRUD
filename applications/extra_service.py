import os
import json
from datetime import datetime, timedelta
from .utils import *

LOCKER_COUNT = 30  # 전체 락커 수 (팀과 합의 후 변경)
TIME_FORMAT = "%y/%m/%d %H:%M:%S"
DATE_FORMAT = "%y/%m/%d"  # 등록일, 만료일 표시 형식
EXPIRE_DAYS = 30  # 만료일 = 등록일 + 30일
YES = ("y", "yes", "예", "네")
NO = ("n", "no", "아니오", "아니요")
BACK = ("o", "ㅒ", "ㅐ")  # 이전 화면으로 돌아가기 키 (B, 한글 자판 상태의 ㅠ)
PAGE_SIZE = 10  # 회원 카드 목록에서 한 페이지에 보여줄 회원 수 (2열 x 5행)


class ExtraServiceCRUD:
    '''
    부가 서비스(락커, 운동복) 관리.
    회원별 폴더 data/members/<user_id>/extra_service.json 에 저장한다.
    락커 사용 현황은 '현재 등록된 회원'들의 파일을 읽어서 계산한다.
    '''
    
    def __init__(self, member_dir, member_crud):
        self.member_dir = member_dir      # 예: data/members
        self.member_crud = member_crud    # TrainerCRUD 객체 (.members 를 항상 최신으로 참조)

    # ---------- 도우미 ----------
    def get_folder(self, user_id):
        return os.path.join(self.member_dir, user_id)

    def get_path(self, user_id):
        return os.path.join(self.get_folder(user_id), "extra_service.json")

    def read_data(self, user_id):
        path = self.get_path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        # 파일이 없으면 빈 기본값
        return {"locker_no": None, "assign_time": None, "expire_time": None,
                "use_uniform": None, "uniform_modify_time": None, "uniform_expire_time": None}

    def write_data(self, user_id, data):
        os.makedirs(self.get_folder(user_id), exist_ok=True)  # 개인 폴더가 없으면 생성
        with open(self.get_path(user_id), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def delete_data(self, user_id):
        path = self.get_path(user_id)
        folder = self.get_folder(user_id)

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

    def save_or_delete(self, user_id, data):
        '''락커도 운동복도 이용하지 않으면 null 로 저장하지 않고 파일을 삭제한다. (아니면 저장)'''
        if data["locker_no"] is None and not data["use_uniform"]:
            if os.path.exists(self.get_path(user_id)):
                self.delete_data(user_id)
        else:
            self.write_data(user_id, data)

    def now_time(self):
        return datetime.now().strftime(TIME_FORMAT)

    def today(self):
        '''오늘 날짜 (등록일)'''
        return datetime.now().strftime(DATE_FORMAT)

    def expire_day(self):
        '''만료일: 오늘 + 30일'''
        return (datetime.now() + timedelta(days=EXPIRE_DAYS)).strftime(DATE_FORMAT)

    def get_dates(self, reg, expire):
        '''(등록일, 만료일) 반환. 예전 데이터(만료일 없음)는 등록일 + 30일로 계산한다.'''
        if reg is None:
            return None, None
        reg_day = reg.split(" ")[0]  # 예전 데이터의 시간 부분은 버린다
        if expire is None:
            expire = (datetime.strptime(reg_day, DATE_FORMAT) + timedelta(days=EXPIRE_DAYS)).strftime(DATE_FORMAT)
        return reg_day, expire

    def find_member(self, user_id):
        for member in self.member_crud.members:
            if member["아이디"] == user_id:
                return member
        return None

    def locker_map(self):
        '''{락커번호: (member, data)} - 현재 사용 중인 락커만'''
        used = {}
        for member in self.member_crud.members:
            data = self.read_data(member["아이디"])
            if data["locker_no"] is not None:
                used[data["locker_no"]] = (member, data)
        return used

    def input_member(self):
        while True:
            user_id = input("회원 아이디를 입력하세요(뒤로가기: o): ").strip()
            if user_id.lower() in BACK:
                print("이전으로 돌아갑니다.")
                return None
            member = self.find_member(user_id)
            if member is None:
                print("등록되지 않은 회원입니다. 다시 입력해주세요.")
                continue
            return member

    def input_locker_no(self, message):
        while True:
            value = input(message).strip()
            if value.lower() in BACK:
                print("이전으로 돌아갑니다.")
                return None
            if not value.isdigit():
                print("락커 번호는 숫자로 입력해주세요.")
                continue
            number = int(value)
            if number < 1 or number > LOCKER_COUNT:
                print(f"존재하지 않는 락커 번호입니다. (1~{LOCKER_COUNT})")
                continue
            return number

    def uniform_text(self, use):
        if use is None:
            return "미등록"
        return "사용" if use else "미사용"

    # ---------- 회원 카드 목록 (전체 회원 리스트 화면과 같은 모양) ----------
    def display_width(self, text):
        '''화면에서 차지하는 칸 수 (한글은 2칸)'''
        text = str(text)
        return len(text) + align(text)

    def pad(self, text, width):
        '''width 칸에 맞춰 왼쪽 정렬 (한글 고려, 넘치면 잘라냄)'''
        text = str(text)
        while self.display_width(text) > width:
            text = text[:-1]
        return text + " " * (width - self.display_width(text))

    def locker_info(self, member):
        '''카드에 보여줄 락커 정보'''
        data = self.read_data(member["아이디"])
        locker = f"{data['locker_no']}번" if data["locker_no"] is not None else "미배정"
        reg, expire = self.get_dates(data["assign_time"], data.get("expire_time"))
        return [("아이디", member["아이디"]),
                ("이름", member["이름"]),
                ("락커 번호", locker),
                ("등록일", reg or "-"),
                ("만료일", expire or "-")]

    def uniform_info(self, member):
        '''카드에 보여줄 운동복 정보'''
        data = self.read_data(member["아이디"])
        reg, expire = self.get_dates(data["uniform_modify_time"], data.get("uniform_expire_time"))
        if not data["use_uniform"]:
            expire = None  # 운동복을 사용하지 않으면 만료일은 없다
        return [("아이디", member["아이디"]),
                ("이름", member["이름"]),
                ("운동복", self.uniform_text(data["use_uniform"])),
                ("등록일", reg or "-"),
                ("만료일", expire or "-")]

    def print_member_cards(self, items, info_fn, start_no=1, label_fn=None):
        '''카드를 2열로 출력한다. (No.001 | No.002)  label_fn 이 있으면 No. 자리에 그 값을 쓴다.'''
        bar = "ㅡ" * 9
        for i in range(0, len(items), 2):
            left = items[i]
            right = items[i + 1] if i + 1 < len(items) else None

            l_no = label_fn(left) if label_fn else start_no + i
            l_head = f"+-{bar}No.{l_no:03d}{bar}-+"
            if right:
                r_no = label_fn(right) if label_fn else start_no + i + 1
                r_head = f"-{bar}No.{r_no:03d}{bar}-+"
            else:
                r_head = f"-{'ㅡ' * 21}-+"
            print(l_head + r_head)

            l_info = info_fn(left)
            r_info = info_fn(right) if right else [("", "")] * len(l_info)
            for (l_key, l_value), (r_key, r_value) in zip(l_info, r_info):
                l_colon = ":" if l_key else " "
                r_colon = ":" if r_key else " "
                print(f"| {self.pad(l_key, 15)}{l_colon}   {self.pad(l_value, 23)} "
                      f"| {self.pad(r_key, 15)}{r_colon}   {self.pad(r_value, 23)} |")
        print(f"+-{'ㅡ' * 21}-+-{'ㅡ' * 21}-+")

    def match_member(self, member, word):
        '''검색어(이름 또는 아이디)가 들어있는 회원인지'''
        return word in str(member.get("아이디", "")).lower() or word in str(member.get("이름", "")).lower()

    def member_card_page(self, title, members, info_fn, summary=None, label_fn=None, match_fn=None,
                         pick_fn=None, pick_help="", back_keys=("o",) + BACK, back_text="o", start_page=0):
        '''
        카드 목록을 페이지(10개)별로 보여준다.
        < : 이전 페이지 / > : 다음 페이지 / ^ : 검색 / back_text(기본 9) : 돌아가기
        pick_fn 이 있으면 입력값으로 항목을 선택할 수 있다.
          pick_fn(입력값) -> (선택한 항목, 안내 메시지)  / 선택에 성공하면 그 항목을 돌려준다.
        (돌아가기를 누르면 pick_fn 이 있을 때 None, 없을 때 True 를 돌려준다.)
        '''
        match_fn = match_fn or self.match_member
        keyword = ""
        page = start_page
        while True:
            shown = [m for m in members if match_fn(m, keyword)]
            max_page = max((len(shown) - 1) // PAGE_SIZE, 0)
            page = min(page, max_page)
            start = page * PAGE_SIZE

            print(" " * ((91 - self.display_width(title)) // 2) + title)
            for line in (summary or []):
                print(line)
            if keyword:
                print(f"검색: '{keyword}' ({len(shown)}개)")
            if shown:
                self.print_member_cards(shown[start:start + PAGE_SIZE], info_fn, start + 1, label_fn)
            else:
                print("표시할 내용이 없습니다.")
            print(f"[돌아가기: {back_text}]", f"{'< 이전 | ^검색 | 다음 >':^40}", f"({page + 1}/{max_page + 1} 페이지)")
            if pick_help:
                print(pick_help)

            cmd = input("입력: ").strip()
            if cmd.lower() in back_keys:
                print("이전으로 돌아갑니다.\n")
                return None if pick_fn else True

            elif cmd == "<":
                if page > 0:
                    page -= 1
                else:
                    print("첫 페이지입니다.\n")

            elif cmd == ">":
                if page < max_page:
                    page += 1
                else:
                    print("마지막 페이지입니다.\n")

            elif cmd == "^":
                word = input("검색할 이름 또는 아이디(전체 보기: 엔터): ").strip().lower()
                if not any(match_fn(m, word) for m in members):
                    print("검색 결과가 없습니다.\n")
                else:
                    keyword = word
                    page = 0

            elif pick_fn and cmd:
                picked, message = pick_fn(cmd)
                if picked is not None:
                    return picked
                print(message + "\n")

            else:
                print("잘못된 접근입니다.\n")

    def locker_slots(self):
        '''락커 1번 ~ LOCKER_COUNT번 전부를 번호 순서로 돌려준다. (배정 안 된 락커는 member 가 None)'''
        used = self.locker_map()
        slots = []
        for no in range(1, LOCKER_COUNT + 1):
            member, data = used.get(no, (None, None))
            slots.append({"no": no, "member": member, "data": data})
        return slots

    def slot_info(self, slot):
        '''락커 카드에 보여줄 정보 (비어 있는 락커는 빈 칸)'''
        member, data = slot["member"], slot["data"]
        if member is None:
            return [("", "")] * 4
        reg, expire = self.get_dates(data["assign_time"], data.get("expire_time"))
        return [("아이디", member["아이디"]),
                ("이름", member["이름"]),
                ("등록일", reg or "-"),
                ("만료일", expire or "-")]

    def match_slot(self, slot, word):
        '''락커 검색: 락커 번호 또는 회원 이름/아이디로 찾는다. (빈 락커는 번호로만 찾을 수 있다.)'''
        if not word or word == str(slot["no"]):
            return True
        if slot["member"] is None:
            return False
        return self.match_member(slot["member"], word)

    def pick_locker_member(self, title, empty_msg):
        '''
        락커 1~LOCKER_COUNT번을 번호 순서대로 카드로 보여주고, 락커 번호를 입력받아
        그 락커를 사용 중인 회원을 돌려준다. (비어 있는 락커는 빈 칸으로 보인다.)
        '''
        slots = self.locker_slots()
        if all(slot["member"] is None for slot in slots):
            print(empty_msg)
            return None

        def pick(cmd):
            if not cmd.isdigit():
                return None, "락커 번호는 숫자로 입력해주세요."
            no = int(cmd)
            if no < 1 or no > LOCKER_COUNT:
                return None, f"존재하지 않는 락커 번호입니다. (1~{LOCKER_COUNT})"
            slot = slots[no - 1]
            if slot["member"] is None:
                return None, "비어 있는 락커입니다. 사용 중인 락커 번호를 입력해주세요."
            return slot["member"], None

        used_count = sum(1 for slot in slots if slot["member"] is not None)
        summary = [f"사용 {used_count} / 전체 {LOCKER_COUNT} (카드의 No. 는 락커 번호입니다.)"]
        return self.member_card_page(title, slots, self.slot_info, summary=summary,
                                     label_fn=lambda slot: slot["no"], match_fn=self.match_slot,
                                     pick_fn=pick, pick_help="락커 번호를 입력하면 선택됩니다.",
                                     back_keys=BACK, back_text="o")

    def pick_locker_number(self, title, help_text, current_no=None):
        '''
        락커 1~LOCKER_COUNT번을 번호 순서대로 카드로 보여주고, 배정할(비어 있는) 락커 번호를 입력받는다.
        < 이전 / > 다음 / ^ 검색 / B 돌아가기 를 쓸 수 있다. (돌아가면 None)
        '''
        slots = self.locker_slots()

        def pick(cmd):
            if not cmd.isdigit():
                return None, "락커 번호는 숫자로 입력해주세요."
            no = int(cmd)
            if no < 1 or no > LOCKER_COUNT:
                return None, f"존재하지 않는 락커 번호입니다. (1~{LOCKER_COUNT})"
            if no == current_no:
                return None, "현재 사용 중인 락커와 같은 번호입니다."
            if slots[no - 1]["member"] is not None:
                return None, "이미 사용 중인 락커입니다. 비어 있는 락커 번호를 입력해주세요."
            return no, None

        used_count = sum(1 for slot in slots if slot["member"] is not None)
        summary = [f"사용 {used_count} / 전체 {LOCKER_COUNT} (카드의 No. 는 락커 번호, 빈 칸은 비어 있는 락커입니다.)"]
        return self.member_card_page(title, slots, self.slot_info, summary=summary,
                                     label_fn=lambda slot: slot["no"], match_fn=self.match_slot,
                                     pick_fn=pick, pick_help=help_text,
                                     back_keys=BACK, back_text="o")

    def pick_member(self, title, info_fn, summary):
        '''
        전체 회원을 카드로 보여주고, 회원 아이디를 입력받아 회원을 선택한다.
        < 이전 / > 다음 / ^ 검색 / B 돌아가기 를 쓸 수 있다. (돌아가면 None)
        '''
        members = self.member_crud.members
        if not members:
            print("등록된 회원이 없습니다.")
            return None

        def pick(cmd):
            for m in members:
                if m["아이디"] == cmd:
                    return m, None
            return None, "목록에 없는 회원입니다. 회원 아이디를 다시 입력해주세요."

        return self.member_card_page(title, members, info_fn, summary=summary,
                                     pick_fn=pick, pick_help="회원 아이디를 입력하면 선택됩니다.",
                                     back_keys=BACK, back_text="o")

    def pick_uniform_member(self, title):
        '''운동복 상태가 보이는 전체 회원 카드에서 회원을 선택한다.'''
        members = self.member_crud.members
        use_count = sum(1 for m in members if self.read_data(m["아이디"])["use_uniform"])
        return self.pick_member(title, self.uniform_info,
                                [f"사용 {use_count}명 / 전체 {len(members)}명"])

    def pick_assign_member(self, title):
        '''락커 정보가 보이는 전체 회원 카드에서 회원을 선택한다.'''
        members = self.member_crud.members
        used_count = len(self.locker_map())
        return self.pick_member(title, self.locker_info,
                                [f"락커 사용 {used_count} / 전체 {LOCKER_COUNT}  (회원 {len(members)}명)"])

    def show_assigned_locker(self, locker_no):
        '''락커를 배정한 직후, 배정된 락커가 있는 페이지의 카드 화면을 보여준다.'''
        slots = self.locker_slots()

        def info(slot):
            rows = self.slot_info(slot)
            if slot["no"] == locker_no:  # 방금 배정한 락커는 표시해준다
                rows = [(k, f"{v} (방금 배정)" if k == "아이디" else v) for k, v in rows]
            return rows

        used_count = sum(1 for slot in slots if slot["member"] is not None)
        summary = [f"사용 {used_count} / 전체 {LOCKER_COUNT} (방금 배정한 락커에는 '(방금 배정)'이 표시됩니다.)"]
        self.member_card_page("=======락커 배정 완료=======", slots, info, summary=summary,
                              label_fn=lambda slot: slot["no"], match_fn=self.match_slot,
                              start_page=(locker_no - 1) // PAGE_SIZE)

    # ---------- 1. 락커 배정 ----------
    def do_assign_locker(self):
        member = self.pick_assign_member("=======락커 배정 (회원 선택)=======")
        if member is None:
            return False
        data = self.read_data(member["아이디"])
        if data["locker_no"] is not None:
            print(f"{member['이름']}님은 이미 {data['locker_no']}번 락커를 사용 중입니다. (변경은 '락커 변경' 메뉴)")
            return False

        locker_no = self.pick_locker_number("=======락커 배정=======",
                                            "배정할 락커 번호를 입력하면 선택됩니다. (비어 있는 락커만 가능)")
        if locker_no is None:
            return False
        if locker_no in self.locker_map():
            print("이미 사용 중인 락커입니다.")
            return False

        data["locker_no"] = locker_no
        data["assign_time"] = self.today()      # 등록일
        data["expire_time"] = self.expire_day()  # 만료일 (등록일 + 30일)
        self.write_data(member["아이디"], data)
        print(f"{member['이름']}님에게 {locker_no}번 락커를 배정했습니다.")
        print(f"등록일: {data['assign_time']} / 만료일: {data['expire_time']}")
        self.show_assigned_locker(locker_no)
        return True

    # ---------- 2. 락커 현황 조회 ----------
    def do_retrieve_lockers(self):
        members = self.member_crud.members
        if not members:
            print("등록된 회원이 없습니다.")
            return False
        used = self.locker_map()
        empty = [no for no in range(1, LOCKER_COUNT + 1) if no not in used]
        summary = [f"사용 {len(used)} / 전체 {LOCKER_COUNT} (빈 락커 {len(empty)}, 카드의 No. 는 락커 번호입니다.)"]
        lines = wrap(empty, 70)
        if lines:
            summary.append("빈 락커 번호: " + lines[0])
            summary += ["              " + line for line in lines[1:]]
        self.member_card_page("=======락커 배정 현황=======", self.locker_slots(), self.slot_info, summary=summary,
                              label_fn=lambda slot: slot["no"], match_fn=self.match_slot)
        return True

    # ---------- 3. 락커 변경 및 해제 ----------
    def do_change_locker(self):
        member = self.pick_locker_member("=======락커 변경=======",
                                         "배정된 락커가 없습니다. 먼저 락커를 배정해주세요.")
        if member is None:
            return False
        data = self.read_data(member["아이디"])

        print(f"현재 {data['locker_no']}번 락커를 사용 중입니다.")
        new_no = self.pick_locker_number("=======락커 변경 (새 락커 선택)=======",
                                         "변경할 락커 번호를 입력하면 선택됩니다. (비어 있는 락커만 가능)",
                                         current_no=data["locker_no"])
        if new_no is None:
            return False
        if new_no == data["locker_no"]:
            print("현재 사용 중인 락커와 같은 번호입니다.")
            return False
        if new_no in self.locker_map():
            print("이미 사용 중인 락커입니다.")
            return False

        old_no = data["locker_no"]
        data["locker_no"] = new_no
        data["assign_time"] = self.today()      # 등록일
        data["expire_time"] = self.expire_day()  # 만료일 (등록일 + 30일)
        self.write_data(member["아이디"], data)
        print(f"{old_no}번 -> {new_no}번 락커로 변경했습니다.")
        print(f"등록일: {data['assign_time']} / 만료일: {data['expire_time']}")
        return True

    def do_release_locker(self):
        member = self.pick_locker_member("=======락커 해제=======", "배정된 락커가 없습니다.")
        if member is None:
            return False
        data = self.read_data(member["아이디"])

        while True:
            check = input(f"{data['locker_no']}번 락커 사용을 해제하시겠습니까?(Y/N, 돌아가기: o): ").strip().lower()
            if check in YES:
                break
            elif check in NO or check in BACK:
                print("이전으로 돌아갑니다.")
                return False
            else:
                print("Y, N 또는 o 로 입력해주세요.")

        released = data["locker_no"]
        data["locker_no"] = None
        data["assign_time"] = None
        data["expire_time"] = None
        self.save_or_delete(member["아이디"], data)
        print(f"{released}번 락커를 해제했습니다. 다시 배정할 수 있습니다.")
        return True

    # ---------- 4. 운동복 이용 여부 등록 ----------
    def do_register_uniform(self):
        member = self.pick_uniform_member("=======운동복 이용 여부 등록=======")
        if member is None:
            return False
        data = self.read_data(member["아이디"])
        print(f"{member['이름']}님의 현재 운동복 상태: {self.uniform_text(data['use_uniform'])}")

        while True:
            answer = input("운동복을 이용하시나요?(Y/N, 뒤로가기: o): ").strip().lower()
            if answer in YES:
                use = True
                break
            elif answer in NO:
                use = False
                break
            elif answer in BACK:
                print("이전으로 돌아갑니다.")
                return False
            else:
                print("Y, N 또는 o 로 입력해주세요.")

        data["use_uniform"] = use
        data["uniform_modify_time"] = self.today()  # 등록일
        # 만료일 (등록일 + 30일) - 운동복을 사용할 때만 정해진다
        data["uniform_expire_time"] = self.expire_day() if use else None
        self.save_or_delete(member["아이디"], data)
        print(f"{member['이름']}님 운동복 {self.uniform_text(use)}으로 등록했습니다.")
        if use:
            print(f"등록일: {data['uniform_modify_time']} / 만료일: {data['uniform_expire_time']}")
        return True

    # ---------- 5. 운동복 이용 현황 조회 ----------
    def do_retrieve_uniform_all(self):
        members = self.member_crud.members
        if not members:
            print("등록된 회원이 없습니다.")
            return False
        use_count = sum(1 for m in members if self.read_data(m["아이디"])["use_uniform"])
        summary = [f"사용 {use_count}명 / 전체 {len(members)}명"]
        self.member_card_page("=======운동복 이용 현황=======", members, self.uniform_info, summary=summary)
        return True

    def do_retrieve_uniform_one(self):
        member = self.input_member()
        if member is None:
            return False
        data = self.read_data(member["아이디"])
        if data["use_uniform"] is None:
            print(f"{member['이름']}님은 운동복 이용 여부가 등록되지 않았습니다.")
        else:
            reg, expire = self.get_dates(data["uniform_modify_time"], data.get("uniform_expire_time"))
            if data["use_uniform"]:
                print(f"{member['이름']}님 운동복: {self.uniform_text(data['use_uniform'])} "
                      f"(등록일 {reg} / 만료일 {expire})")
            else:
                print(f"{member['이름']}님 운동복: {self.uniform_text(data['use_uniform'])} "
                      f"(등록일 {reg})")
        return True

    # ---------- 회원 삭제 연동 ----------
    def remove_member_data(self, user_id):
        '''회원 삭제 시 호출: 부가 서비스 정보를 빈 값으로 초기화 (개인 폴더의 다른 파일은 건드리지 않음)'''
        if os.path.exists(self.get_path(user_id)):
            self.delete_data(user_id)


def extra_interface(extra):
    while True:
        print(
            "\n=======부가 서비스 관리=======\n"
            "1. 락커 배정\n"
            "2. 락커 배정 현황 조회\n"
            "3. 락커 변경\n"
            "4. 락커 해제\n"
            "5. 운동복 이용 여부 등록\n"
            "6. 운동복 이용 현황 조회\n"
            "o. 이전으로\n"
            "p. 프로그램 종료\n"
            "=============================="
        )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")

        if select_num == "1":
            extra.do_assign_locker()

        elif select_num == "2":
            extra.do_retrieve_lockers()
            
        elif select_num == "3":
            extra.do_change_locker()
            
        elif select_num == "4":
            extra.do_release_locker()
            
        elif select_num == "5":
            extra.do_register_uniform()
            
        elif select_num == "6":
            while True:
                print("1. 전체 회원 조회\n2. 특정 회원 조회\no. 뒤로가기")
                sub = input("번호를 입력하세요: ").strip()
                if sub == "1":
                    extra.do_retrieve_uniform_all()
                    break
                elif sub == "2":
                    extra.do_retrieve_uniform_one()
                    break
                elif sub.lower() in BACK:
                    print("이전으로 돌아갑니다.")
                    break
                else:
                    print("1, 2 또는 o 로 입력해주세요.\n")
        elif select_num == "o":
            print("이전 화면으로 돌아갑니다.")
            return True
        elif select_num == "p":
            print("프로그램을 종료합니다.")
            return False
        else:
            print("잘못된 접근입니다.\n")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, "data")  # C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, "members.json")

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(member_path):
        with open(member_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)
            
    from trainer_crud import TrainerCRUD
    train_sys = TrainerCRUD(member_path)
    
    extra_sys = ExtraServiceCRUD(os.path.join(DATA_DIR, "members"), train_sys)
    train_sys.extra = extra_sys
    with open(member_path, "r", encoding="utf-8") as f:
        members = json.load(f)
    
    extra_interface(extra_sys)