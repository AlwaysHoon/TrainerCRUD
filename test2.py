import time

total = 100
for current in range(total + 1):
    progress = current / total
    filled = int(progress * 30)

    bar = "█" * filled + " " * (30 - filled)
    print(f"\r|{bar}|", end="", flush=False)
    # print(f"\r|{bar}| {progress * 100:.1f}%", end="", flush=True)

    time.sleep(0.005)
print('\n')


format
print("a",end="",flush=True)
print("b", flush=False)