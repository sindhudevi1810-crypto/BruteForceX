import time

from database import get_user
from security import verify_password


# Controlled password guesses for our demo
PASSWORD_LIST = [
    "password",
    "123456",
    "admin123",
    "welcome",
    "cat123",
    "student123",
    "StrongDemo@123"
]


def simulate_attack(username):
    user = get_user(username)

    if user is None:
        print("Demo account not found.")
        return

    print("\n================================")
    print("       BRUTEFORCEX ATTACK")
    print("================================")
    print("Target:", username)
    print("Security mode:", user["security_mode"])
    print("Starting password guessing...\n")

    start_time = time.time()
    found = False
    attempts = 0

    for guess in PASSWORD_LIST:
        attempts += 1
        print(f"Attempt {attempts}: {guess}")

        if user["security_mode"] == "vulnerable":
            match = guess == user["password"]
        else:
            match = verify_password(
                user["password_hash"], guess
            )

        if match:
            print("\nPassword discovered in demo!")
            print("Matching password:", guess)
            found = True
            break

    elapsed = time.time() - start_time

    print("\n========== RESULTS ==========")
    print("Attempts:", attempts)
    print("Time taken:", round(elapsed, 3), "seconds")

    if found:
        print("Result: PASSWORD FOUND")
    else:
        print("Result: PASSWORD NOT FOUND")

    print("=============================\n")


if __name__ == "__main__":
    print("1. Test vulnerable account")
    print("2. Test protected account")

    choice = input("\nChoose an option: ")

    if choice == "1":
        simulate_attack("weak_user")
    elif choice == "2":
        simulate_attack("secure_user")
    else:
        print("Invalid option.")