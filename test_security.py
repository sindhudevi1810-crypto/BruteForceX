from security import hash_password, verify_password

password = "student123"

hashed = hash_password(password)

print("Original password:", password)
print("Stored password hash:", hashed)

print("\nCorrect password:",
      verify_password(hashed, "student123"))

print("Wrong password:",
      verify_password(hashed, "wrongpassword"))