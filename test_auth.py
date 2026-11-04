from auth import authenticate_user

print("===== BRUTEFORCEX LOGIN SECURITY TEST =====")

username = "secure_user"

for i in range(5):
    success, message = authenticate_user(
        username,
        "wrongpassword"
    )

    print(f"Attempt {i + 1}: {message}")

print("\nTrying correct password after lockout:")

success, message = authenticate_user(
    username,
    "StrongDemo@123"
)

print(message)