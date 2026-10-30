from interface import start_application

def show_logo():
    logo = [
        "╔════════════════════════════════════════════════════╗",
        "║                                                    ║",
        "║                      T M S                         ║",
        "║                                                    ║",
        "║       ┏━━┓ ┏━━┓                  ┏━━┓ ┏━━┓         ║",
        "║       ┃  ┃ ┃  ┃                  ┃  ┃ ┃  ┃         ║",
        "║     ━━┫  ┣━┫  ┣━━━━━━━━━━━━━━━━━━┫  ┣━┫  ┣━━       ║",
        "║       ┃  ┃ ┃  ┃                  ┃  ┃ ┃  ┃         ║",
        "║       ┗━━┛ ┗━━┛                  ┗━━┛ ┗━━┛         ║",
        "║                                                    ║",
        "║            TRAINER MANAGEMENT SYSTEM               ║",
        "║                                                    ║",
        "║                LIFT · TRACK · GROW                 ║",
        "║                                                    ║",
        "║               Press Enter to Start...              ║",
        "╚════════════════════════════════════════════════════╝"
    ]
    
    width = 52
    # print("\033[93m")
    for line in logo:
        if line.startswith("║") and line.endswith("║"):
            content = line[1:-1].strip()
            print("║" + content.center(width) + "║")
        else:
            print(line)
    # print("\033[0m")


if __name__ == "__main__":
    show_logo()
    a = input()
    start_application()