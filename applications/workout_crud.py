
"""GYM LOG 운동 기록 CRUD."""

import json
import math
import unicodedata
from datetime import datetime
from pathlib import Path


class WorkoutCRUD:
    def __init__(self, member_dir):
        self.member_dir = Path(member_dir)

    def get_folder(self, user_id):
        return self.member_dir / str(user_id)

    def get_path(self, user_id):
        return self.get_folder(user_id) / "workouts.json"

    def get_user_id(self, member):
        return member.get("아이디") or member.get("user_id")

    def get_user_name(self, member):
        return member.get("이름") or member.get("name")

    # ==============================
    # JSON 파일 읽기 / 저장
    # ==============================

    def read_data(self, user_id):
        path = self.get_path(user_id)

        if not path.exists():
            return []

        try:
            with path.open("r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                print("운동 기록은 리스트 형식이어야 합니다.")
                return None

            if not all(isinstance(x, dict) for x in records):
                print("운동 기록 데이터 형식이 올바르지 않습니다.")
                return None

            return records

        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print(f"운동 기록 읽기 오류: {error}")
            return None

    def write_data(self, user_id, workouts):
        path = self.get_path(user_id)
        temporary = path.with_name(path.name + ".tmp")

        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with temporary.open("w", encoding="utf-8") as file:
                json.dump(
                    workouts,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    allow_nan=False
                )

            temporary.replace(path)
            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"운동 기록 저장 오류: {error}")

            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass

            return False

    # ==============================
    # 입력 예외처리
    # ==============================

    @staticmethod
    def ask_yes_no(prompt):
        while True:
            answer = input(prompt).strip().lower()

            if answer == "y":
                return True

            elif answer == "n":
                return False

            elif answer == "0":
                return None

            else:
                print("Y 또는 N을 입력해주세요. (0: 취소)")

    @staticmethod
    def ask_number(prompt, kind="float", minimum=0):
        while True:
            raw = input(f"{prompt} (q: 취소): ").strip()

            if raw.lower() == "q":
                return None

            try:
                if kind == "int":
                    if not raw.isdecimal():
                        raise ValueError
                    value = int(raw)

                else:
                    value = float(raw)

                    if not math.isfinite(value):
                        raise ValueError

            except ValueError:
                print("올바른 숫자를 입력해주세요.")
                continue

            if value < minimum:
                print(f"{minimum} 이상의 값을 입력해주세요.")
                continue

            return value

    @staticmethod
    def ask_date():
        while True:
            raw = input(
                "운동 날짜(YYYY-MM-DD, 0: 취소): "
            ).strip()

            if raw == "0":
                return None

            try:
                parsed = datetime.strptime(raw, "%Y-%m-%d")

                if parsed.strftime("%Y-%m-%d") != raw:
                    raise ValueError

                return raw

            except ValueError:
                print("올바른 날짜를 입력해주세요. 예: 2026-10-28")

    # ==============================
    # 일반 목록 페이지
    # ==============================

    def select_page(self, items, title, page_size=10):
        if not items:
            print("선택할 항목이 없습니다.")
            return None

        page = 0
        last_page = (len(items) - 1) // page_size

        while True:
            start = page * page_size
            end = min(start + page_size, len(items))

            print(f"\n========== {title} ==========")
            print(f"페이지 {page + 1} / {last_page + 1}")

            for index in range(start, end):
                print(f"{index + 1}. {items[index]}")

            print("< 이전 | > 다음 | 0 취소")

            answer = input("번호 선택: ").strip()

            if answer == "0":
                return None

            elif answer == "<":
                if page > 0:
                    page -= 1
                else:
                    print("첫 번째 페이지입니다.")

            elif answer == ">":
                if page < last_page:
                    page += 1
                else:
                    print("마지막 페이지입니다.")

            elif answer.isdecimal():
                number = int(answer)

                if start + 1 <= number <= end:
                    return number - 1

                print("현재 페이지의 번호를 선택해주세요.")

            else:
                print("올바른 번호를 입력해주세요.")

    # ==============================
    # 회원 카드 정렬
    # ==============================

    @staticmethod
    def display_width(value):
        return sum(
            2 if unicodedata.east_asian_width(char) in ("W", "F") else 1
            for char in str(value)
        )

    @classmethod
    def pad(cls, value, width):
        value = str(value)

        while value and cls.display_width(value) > width:
            value = value[:-1]

        return value + " " * (width - cls.display_width(value))

    # ==============================
    # 2열 회원 카드 선택
    # ==============================

    def select_member_card(self, members, title="회원 선택", summary=None, show_workout_count=True):
        if not members:
            print("선택할 회원이 없습니다.")
            return None

        keyword = ""
        page = 0
        page_size = 10
        cell_width = 41

        # 회원별 운동 기록 개수를 화면 진입 시 한 번만 읽습니다.
        workout_counts = {}
        if show_workout_count:
            for member in members:
                user_id = self.get_user_id(member)
                if user_id not in workout_counts:
                    records = self.read_data(user_id) if user_id else []
                    workout_counts[user_id] = "읽기 오류" if records is None else f"{len(records)}개"

        line = (
            "+"
            + "-" * cell_width
            + "+"
            + "-" * cell_width
            + "+"
        )

        while True:
            shown = [
                member
                for member in members
                if keyword in str(member.get("아이디", "")).lower()
                or keyword in str(member.get("이름", "")).lower()
            ]

            last_page = max(
                (len(shown) - 1) // page_size,
                0
            )

            page = min(page, last_page)

            start = page * page_size
            current = shown[start:start + page_size]

            print(f"\n========== {title} ==========")

            if summary:
                print(summary)

            if keyword:
                print(f"검색: '{keyword}' ({len(shown)}명)")

            if not current:
                print("검색 결과가 없습니다.")

            else:
                for offset in range(0, len(current), 2):
                    pair = current[offset:offset + 2]

                    print(line)

                    headings = []

                    for j in range(2):
                        if j < len(pair):
                            number = start + offset + j + 1

                            headings.append(
                                self.pad(
                                    f" No.{number:03d}",
                                    cell_width
                                )
                            )
                        else:
                            headings.append(" " * cell_width)

                    print("|" + "|".join(headings) + "|")

                    for key in (("아이디", "이름", "운동기록") if show_workout_count else ("아이디", "이름")):
                        columns = []

                        for j in range(2):
                            if j < len(pair):
                                if key == "운동기록":
                                    value = workout_counts.get(self.get_user_id(pair[j]), "0개")
                                else:
                                    value = pair[j].get(key, "-")

                                content = (
                                    f" {self.pad(key, 8)} : "
                                    f"{self.pad(value, 27)}"
                                )

                                columns.append(
                                    self.pad(content, cell_width)
                                )

                            else:
                                columns.append(" " * cell_width)

                        print("|" + "|".join(columns) + "|")

                print(line)

            # 회원 카드 하단 메뉴 정렬
            total_width = cell_width * 2 + 3

            left_text = "[돌아가기: o]"
            center_text = "< 이전 | ^ 검색 | 다음 >"
            right_text = f"({page + 1}/{last_page + 1} 페이지)"

            # 한글 글자 너비를 고려한 가운데 및 오른쪽 정렬
            left_width = self.display_width(left_text)
            center_width = self.display_width(center_text)
            right_width = self.display_width(right_text)

            # 가운데 메뉴의 시작 위치
            center_start = (total_width - center_width) // 2

            # 페이지 표시의 시작 위치 (오른쪽 끝)
            right_start = total_width - right_width

            # 전체 폭만큼 공백 생성
            footer = [" "] * total_width

            # 각 텍스트를 화면 너비 기준으로 배치
            def put_text(start, value):
                position = start

                for char in value:
                    width = self.display_width(char)

                    if position + width > total_width:
                        break
                    
                    footer[position] = char

                    if width == 2:
                        footer[position + 1] = ""

                    position += width

            put_text(0, left_text)
            put_text(center_start, center_text)
            put_text(right_start, right_text)

            print("".join(footer).rstrip())

            print("회원 아이디를 입력하면 선택됩니다.")

            cmd = input("입력: ").strip()

            if cmd.lower() == "o":
                print("이전 화면으로 돌아갑니다.")
                return None

            elif cmd == "<":
                if page > 0:
                    page -= 1
                else:
                    print("첫 페이지입니다.")

            elif cmd == ">":
                if page < last_page:
                    page += 1
                else:
                    print("마지막 페이지입니다.")

            elif cmd == "^":
                keyword = input(
                    "검색할 이름 또는 아이디(전체 보기: 엔터): "
                ).strip().lower()

                page = 0

            else:
                selected = next(
                    (
                        member
                        for member in shown
                        if str(member.get("아이디", "")).lower()
                        == cmd.lower()
                    ),
                    None
                )

                if selected is not None:
                    return selected

                print(
                    "목록에 없는 회원입니다. "
                    "회원 아이디를 다시 입력해주세요."
                )

    # ==============================
    # 운동 세트 데이터 처리
    # ==============================

    @staticmethod
    def get_set_list(record):
        sets = record.get("sets", [])

        if isinstance(sets, list):
            return sets

        try:
            count = int(sets)
            weight = float(record.get("weight", 0))
            reps = int(record.get("reps", 0))

            if count < 0:
                return []

            return [
                {
                    "set": index,
                    "weight": weight,
                    "reps": reps
                }
                for index in range(1, count + 1)
            ]

        except (ValueError, TypeError):
            return []

    def print_workout_record(self, record):
        print("\n" + "=" * 48)
        print(f"기록 번호: {record.get('record_id', '-')}")
        print(f"운동 날짜: {record.get('date', '-')}")
        print(f"운동 종목: {record.get('exercise', '-')}")
        print("-" * 48)

        total_volume = 0
        sets = self.get_set_list(record)

        for index, item in enumerate(sets, start=1):
            try:
                weight = float(item.get("weight", 0))
                reps = int(item.get("reps", 0))

                if not math.isfinite(weight):
                    raise ValueError

                volume = weight * reps

            except (ValueError, TypeError, AttributeError):
                print(f"{index}세트: 잘못된 데이터")
                continue

            total_volume += volume

            print(
                f"{index}세트 | "
                f"{weight:g}kg | "
                f"{reps}회 | "
                f"볼륨 {volume:,.1f}kg"
            )

        print("-" * 48)
        print(f"총 세트: {len(sets)}세트")
        print(f"총 볼륨: {total_volume:,.1f}kg")
        print("=" * 48)

    # ==============================
    # 운동 부위 및 종목 선택
    # ==============================

    def select_exercise(self):
        path = self.member_dir.parent / "muscles.json"

        if not path.exists():
            print(f"운동 종목 파일이 없습니다: {path}")
            return None

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print(f"운동 종목 읽기 오류: {error}")
            return None

        if not isinstance(data, list):
            print("운동 종목 파일 형식이 올바르지 않습니다.")
            return None

        muscle_names = [
            "Core",
            "Back",
            "Chest",
            "Shoulders",
            "Arms",
            "Legs"
        ]

        muscle_index = self.select_page(
            muscle_names,
            "운동 부위 선택"
        )

        if muscle_index is None:
            return None

        muscle = muscle_names[muscle_index]
        machines = []

        for item in data:
            if not isinstance(item, dict):
                continue

            if item.get("muscle") == muscle:
                values = item.get("machines", [])

                if isinstance(values, list):
                    machines.extend(values)

        machines = [
            value
            for value in machines
            if isinstance(value, str) and value.strip()
        ]

        index = self.select_page(
            machines,
            f"{muscle} 운동 종목 선택"
        )

        if index is None:
            return None

        return machines[index]

    # ==============================
    # 1. 운동 기록 등록
    # ==============================

    def register_workout(self, member):
        print("\n========== 운동 기록 등록 ==========")

        user_id = self.get_user_id(member)

        if not user_id:
            print("회원 아이디가 없어 등록할 수 없습니다.")
            return

        date = self.ask_date()

        if date is None:
            print("등록을 취소했습니다.")
            return

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        registered = 0

        while True:
            exercise = self.select_exercise()

            if exercise is None:
                break

            sets = []
            cancelled = False

            while True:
                print(f"\n----- {len(sets) + 1}세트 -----")

                weight = self.ask_number(
                    "무게(kg)",
                    minimum=0
                )

                if weight is None:
                    print("현재 운동 종목 입력을 취소했습니다.")
                    cancelled = True
                    break

                reps = self.ask_number(
                    "반복 횟수",
                    kind="int",
                    minimum=1
                )

                if reps is None:
                    print("현재 운동 종목 입력을 취소했습니다.")
                    cancelled = True
                    break

                sets.append({
                    "set": len(sets) + 1,
                    "weight": weight,
                    "reps": reps
                })

                more = self.ask_yes_no(
                    "세트를 추가하시겠습니까? (Y/N, 0: 취소): "
                )

                if more is None:
                    print("현재 운동 종목 입력을 취소했습니다.")
                    cancelled = True
                    break

                if not more:
                    break

            if not cancelled and sets:
                ids = []

                for item in workouts:
                    try:
                        ids.append(
                            int(item.get("record_id", 0))
                        )
                    except (ValueError, TypeError):
                        continue

                record = {
                    "record_id": max(ids, default=0) + 1,
                    "user_id": user_id,
                    "date": date,
                    "exercise": exercise,
                    "sets": sets
                }

                updated = workouts + [record]

                if not self.write_data(user_id, updated):
                    return

                workouts = updated
                registered += 1

                print(f"\n{exercise} 운동 기록 등록 완료!")

            again = self.ask_yes_no(
                "다른 운동을 등록하시겠습니까? (Y/N, 0: 취소): "
            )

            if again is not True:
                break

        print(f"\n이번에 등록한 운동 종목: {registered}개")

    # ==============================
    # 날짜 및 기록 선택
    # ==============================

    def select_date(self, workouts, user_id):
        dates = sorted(
            {
                record.get("date")
                for record in workouts
                if isinstance(record.get("date"), str)
            },
            reverse=True
        )

        index = self.select_page(
            dates,
            "운동 날짜 선택"
        )

        if index is None:
            return None

        return dates[index]

    def select_record(self, workouts, date, title):
        records = [
            record
            for record in workouts
            if record.get("date") == date
        ]

        labels = [
            f"[기록 #{record.get('record_id', '-')}] "
            f"{record.get('exercise', '-')}"
            for record in records
        ]

        index = self.select_page(labels, title)

        if index is None:
            return None

        return records[index]

    # ==============================
    # 2. 회원별 운동 기록 조회
    # ==============================

    def search_workout(self, member):
        print("\n========== 운동 기록 조회 ==========")

        user_id = self.get_user_id(member)

        if not user_id:
            print("회원 아이디가 없습니다.")
            return

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("등록된 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        records = [
            record
            for record in workouts
            if record.get("date") == date
        ]

        for record in records:
            self.print_workout_record(record)

        print(f"\n총 운동 종목: {len(records)}개")

    # ==============================
    # 3. 운동 기록 수정
    # ==============================

    def update_workout(self, member):
        print("\n========== 운동 기록 수정 ==========")

        user_id = self.get_user_id(member)

        if not user_id:
            print("회원 아이디가 없습니다.")
            return

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("수정할 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        record = self.select_record(
            workouts,
            date,
            "수정할 운동 종목 선택"
        )

        if record is None:
            return

        self.print_workout_record(record)

        sets = self.get_set_list(record)

        if not sets:
            print("수정할 세트가 없습니다.")
            return

        labels = [
            f"{index}세트"
            for index in range(1, len(sets) + 1)
        ]

        index = self.select_page(
            labels,
            "수정할 세트 선택"
        )

        if index is None:
            return

        weight = self.ask_number(
            "새로운 무게(kg)",
            minimum=0
        )

        if weight is None:
            return

        reps = self.ask_number(
            "새로운 반복 횟수",
            kind="int",
            minimum=1
        )

        if reps is None:
            return

        new_sets = [
            dict(item)
            for item in sets
        ]

        new_sets[index]["weight"] = weight
        new_sets[index]["reps"] = reps

        updated_records = []

        for item in workouts:
            if item is record:
                new_record = dict(item)

                new_record["sets"] = new_sets
                new_record.pop("weight", None)
                new_record.pop("reps", None)

                updated_records.append(new_record)

            else:
                updated_records.append(item)

        if self.write_data(user_id, updated_records):
            print("\n운동 기록 수정 완료!")

    # ==============================
    # 4. 운동 기록 삭제
    # ==============================

    def delete_workout(self, member):
        print("\n========== 운동 기록 삭제 ==========")

        user_id = self.get_user_id(member)

        if not user_id:
            print("회원 아이디가 없습니다.")
            return

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("삭제할 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        record = self.select_record(
            workouts,
            date,
            "삭제할 운동 종목 선택"
        )

        if record is None:
            return

        self.print_workout_record(record)

        confirm = self.ask_yes_no(
            "정말 삭제하시겠습니까? (Y/N, 0: 취소): "
        )

        if confirm is not True:
            print("삭제를 취소했습니다.")
            return

        updated = [
            item
            for item in workouts
            if item is not record
        ]

        if self.write_data(user_id, updated):
            print("\n운동 기록 삭제 완료!")

    # ==============================
    # 5. 전체 운동 기록 조회
    # ==============================

    def show_workouts(self):
        print("\n========== 전체 운동 기록 조회 ==========")

        if not self.member_dir.exists():
            print("등록된 운동 기록이 없습니다.")
            return

        users = []

        try:
            folders = sorted(self.member_dir.iterdir())

        except OSError as error:
            print(f"회원 폴더 조회 오류: {error}")
            return

        for folder in folders:
            if not folder.is_dir():
                continue

            if not (folder / "workouts.json").exists():
                continue

            records = self.read_data(folder.name)

            if records:
                users.append(folder.name)

        if not users:
            print("등록된 운동 기록이 없습니다.")
            return

        # 회원 이름 불러오기
        member_path = self.member_dir.parent / "members.json"
        members = load_members(member_path)

        name_map = {
            member["아이디"]: member["이름"]
            for member in (members or [])
        }

        choices = [
            {
                "아이디": user_id,
                "이름": name_map.get(user_id, "이름 없음")
            }
            for user_id in users
        ]

        selected = self.select_member_card(
            choices,
            "운동 기록이 있는 회원 선택",
            (
                f"운동 기록 보유 {len(users)}명 / "
                f"전체 회원 {len(members or [])}명"
            ),
            show_workout_count=True
        )

        if selected is None:
            return

        user_id = selected["아이디"]
        records = self.read_data(user_id)

        if not records:
            return

        date = self.select_date(records, user_id)

        if date is None:
            return

        filtered = [
            record
            for record in records
            if record.get("date") == date
        ]

        for record in filtered:
            self.print_workout_record(record)

        print(f"\n총 운동 종목: {len(filtered)}개")


# ==============================
# 회원 JSON 불러오기
# ==============================

def load_members(member_path):
    member_path = Path(member_path)

    if not member_path.exists():
        print(f"회원 정보 파일이 없습니다: {member_path}")
        return None

    try:
        with member_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"회원 정보 읽기 오류: {error}")
        return None

    if isinstance(data, list):
        members = data

    elif isinstance(data, dict):
        members = data.get(
            "members",
            data.get("회원목록", [])
        )

    else:
        print("회원 정보 형식이 올바르지 않습니다.")
        return None

    if not isinstance(members, list):
        print("회원 목록 형식이 올바르지 않습니다.")
        return None

    normalized = []

    for member in members:
        if not isinstance(member, dict):
            continue

        user_id = member.get("아이디") or member.get("user_id")
        name = member.get("이름") or member.get("name")

        if user_id and name:
            normalized.append({
                **member,
                "아이디": str(user_id),
                "이름": str(name)
            })

    return normalized


# ==============================
# 회원 선택
# ==============================

def select_member(workout, member_path, mode=None):
    members = load_members(member_path)

    if members is None:
        return None

    if not members:
        print("등록된 회원이 없습니다.")
        return None

    title_map = {
        "register": "운동 기록 등록 (회원 선택)",
        "search": "운동 기록 조회 (회원 선택)",
        "update": "운동 기록 수정 (회원 선택)",
        "delete": "운동 기록 삭제 (회원 선택)"
    }

    title = title_map.get(
        mode,
        "운동 기록 관리 (회원 선택)"
    )

    return workout.select_member_card(
        members,
        title,
        f"전체 회원 {len(members)}명",
        show_workout_count=True
    )


# ==============================
# 메인 메뉴
# ==============================

def workout_menu(workout, member_path):
    while True:
        print("\n========== GYM LOG ==========")
        print("       운동 기록 관리")
        print("=============================")
        print("1. 운동 기록 등록")
        print("2. 운동 기록 조회")
        print("3. 운동 기록 수정")
        print("4. 운동 기록 삭제")
        print("5. 전체 운동 기록 조회")
        print("0. 종료")
        print("=============================")

        choice = input("메뉴 선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            return

        elif choice in ("1", "2", "3", "4"):
            mode_map = {"1": "register", "2": "search", "3": "update", "4": "delete"}
            member = select_member(
                workout,
                member_path,
                mode=mode_map[choice]
            )

            if member is None:
                continue

            if choice == "1":
                workout.register_workout(member)

            elif choice == "2":
                workout.search_workout(member)

            elif choice == "3":
                workout.update_workout(member)

            elif choice == "4":
                workout.delete_workout(member)

        elif choice == "5":
            workout.show_workouts()

        else:
            print("올바른 메뉴 번호(0~5)를 입력해주세요.")


# ==============================
# 프로그램 실행
# ==============================

def main():
    base = Path(__file__).resolve().parent

    if (base / "data").is_dir():
        project = base
    else:
        project = base.parent

    data = project / "data"

    workout = WorkoutCRUD(
        data / "members"
    )

    workout_menu(
        workout,
        data / "members.json"
    )


if __name__ == "__main__":
    main()
