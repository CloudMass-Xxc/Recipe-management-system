from app.auth.password import get_password_hash, verify_password

# 测试密码哈希生成和验证
print("Testing password hashing and verification...")

# 生成新的密码哈希
test_password = "testpassword"
new_hash = get_password_hash(test_password)
print(f"Original password: {test_password}")
print(f"Generated hash: {new_hash}")

# 验证新生成的哈希
result = verify_password(test_password, new_hash)
print(f"Verification result: {result}")

# 测试存储的哈希值
stored_hash = '$pbkdf2-sha256$100000$6b23NubcOyeEkPLeuzfmHA$Q3WzchKl.n88GTxtnysLaZ.uUtSyc3ucb2iY9MYwDw0'
print(f"\nStored hash: {stored_hash}")
print(f"Hash length: {len(stored_hash)}")
print(f"Hash starts with pbkdf2-sha256: {stored_hash.startswith('$pbkdf2-sha256$')}")

# 尝试使用不同的算法验证
from passlib.context import CryptContext

# 测试不同的密码上下文配置
print("\nTesting different password context configurations...")

# 配置1：使用默认配置
pwd_context1 = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", deprecated="auto")
result1 = pwd_context1.verify(test_password, stored_hash)
print(f"Configuration 1 result: {result1}")

# 配置2：明确指定迭代次数
pwd_context2 = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=100000, deprecated="auto")
result2 = pwd_context2.verify(test_password, stored_hash)
print(f"Configuration 2 result: {result2}")

# 配置3：添加更多算法支持
pwd_context3 = CryptContext(schemes=["pbkdf2_sha256", "bcrypt", "sha256_crypt"], default="pbkdf2_sha256", deprecated="auto")
result3 = pwd_context3.verify(test_password, stored_hash)
print(f"Configuration 3 result: {result3}")

# 测试使用bcrypt算法
print("\nTesting bcrypt algorithm...")
bcrypt_hash = pwd_context3.hash(test_password, scheme="bcrypt")
print(f"bcrypt hash: {bcrypt_hash}")
result_bcrypt = pwd_context3.verify(test_password, bcrypt_hash)
print(f"bcrypt verification result: {result_bcrypt}")
