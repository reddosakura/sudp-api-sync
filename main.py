from werkzeug.security import generate_password_hash

print(generate_password_hash("1234qwerty",method="pbkdf2:sha256", salt_length=8))
