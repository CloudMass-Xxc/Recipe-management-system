from app.auth.password import verify_password

# 测试密码验证
password_hash = '$pbkdf2-sha256$100000$6b23NubcOyeEkPLeuzfmHA$Q3WzchKl.n88GTxtnysLaZ.uUtSyc3ucb2iY9MYwDw0'

# 测试正确的密码
print("Testing correct password...")
result = verify_password("testpassword", password_hash)
print(f"Result: {result}")

# 测试错误的密码
print("\nTesting incorrect password...")
result = verify_password("wrongpassword", password_hash)
print(f"Result: {result}")

# 测试不同的密码
print("\nTesting other passwords...")
for pwd in ["password123", "123456", "test123", "xxiaochang"]:
    result = verify_password(pwd, password_hash)
    print(f"Password '{pwd}': {result}")
