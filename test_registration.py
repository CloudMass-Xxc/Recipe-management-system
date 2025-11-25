import requests
import json
import sys
import time

BASE_URL = 'http://localhost:8001'
REGISTER_ENDPOINT = f'{BASE_URL}/auth/register'

def print_separator():
    print('=' * 60)

def print_title(title):
    print_separator()
    print(f'🔍 {title}')
    print_separator()

def test_registration(test_name, user_data, expect_success=True):
    """
    执行注册测试
    """
    print_title(f'测试: {test_name}')
    print(f'请求数据: {json.dumps(user_data, ensure_ascii=False)}')
    
    try:
        start_time = time.time()
        response = requests.post(
            REGISTER_ENDPOINT,
            json=user_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        end_time = time.time()
        
        print(f'响应状态码: {response.status_code}')
        print(f'响应时间: {(end_time - start_time) * 1000:.2f} ms')
        
        # 尝试解析响应内容
        try:
            response_data = response.json()
            print(f'响应内容: {json.dumps(response_data, ensure_ascii=False, indent=2)}')
        except json.JSONDecodeError:
            print(f'响应内容: {response.text}')
            response_data = None
        
        # 检查结果
        if expect_success and response.status_code == 201:
            print('✅ 测试通过: 注册成功')
            return True, response_data
        elif not expect_success and response.status_code >= 400:
            print('✅ 测试通过: 按预期返回错误')
            return True, response_data
        else:
            print('❌ 测试失败: 结果不符合预期')
            return False, response_data
            
    except requests.exceptions.RequestException as e:
        print(f'❌ 测试失败: 请求异常 - {str(e)}')
        return False, None
    finally:
        print_separator()
        print()

def run_diagnostic_tests():
    """
    运行诊断测试套件
    """
    print_title('开始注册功能诊断测试')
    
    # 测试1: 基本注册测试
    test1_data = {
        "username": "testuser123",
        "email": "test123@example.com",
        "phone": "13812345678",
        "password": "Password123!",
        "display_name": "测试用户",
        "diet_preferences": []
    }
    test1_success, test1_data = test_registration('基本注册测试', test1_data, expect_success=True)
    
    # 测试2: 检查API是否可达
    test_api_reachability()
    
    # 测试3: 密码强度测试
    test_password_strength()
    
    # 测试4: 检查字段格式要求
    test_field_validations()
    
    # 测试5: 检查响应格式
    test_response_format(test1_data)
    
    print_title('诊断测试完成')
    
    # 打印诊断总结
    if not test1_success:
        print("🚨 主要问题: 注册请求失败")
        print("💡 可能的原因:")
        print("1. 后端服务未正常运行")
        print("2. API路径错误")
        print("3. 数据格式不匹配")
        print("4. 密码强度要求不满足")
        print("5. 数据库连接问题")

def test_api_reachability():
    """
    测试API是否可达
    """
    print_title('测试API可达性')
    
    try:
        # 测试根路径
        root_response = requests.get(BASE_URL, timeout=5)
        print(f'根路径状态码: {root_response.status_code}')
        
        # 测试健康检查端点（如果存在）
        try:
            health_response = requests.get(f'{BASE_URL}/health', timeout=5)
            print(f'健康检查端点状态码: {health_response.status_code}')
        except Exception:
            print('健康检查端点可能不存在')
            
        # 测试注册端点的OPTIONS请求
        options_response = requests.options(REGISTER_ENDPOINT, timeout=5)
        print(f'OPTIONS请求状态码: {options_response.status_code}')
        print(f'允许的方法: {options_response.headers.get("Allow", "未知")}')
        print(f'CORS允许的来源: {options_response.headers.get("Access-Control-Allow-Origin", "未设置")}')
        
    except requests.exceptions.RequestException as e:
        print(f'❌ API不可达: {str(e)}')
        print('💡 建议: 检查后端服务是否正在运行，以及端口配置是否正确')

def test_password_strength():
    """
    测试密码强度要求
    """
    print_title('测试密码强度要求')
    
    weak_passwords = [
        ("123456", "过短的密码"),
        ("password", "常见密码"),
        ("qwerty123", "弱密码"),
        ("Test123", "缺少特殊字符")
    ]
    
    for password, desc in weak_passwords:
        test_data = {
            "username": f"weakpwtest_{int(time.time())}",
            "email": f"weakpwtest_{int(time.time())}@example.com",
            "phone": f"138{int(time.time()) % 10000000}",
            "password": password,
            "display_name": "弱密码测试",
            "diet_preferences": []
        }
        test_registration(f"弱密码测试: {desc}", test_data, expect_success=False)

def test_field_validations():
    """
    测试字段验证
    """
    print_title('测试字段验证')
    
    # 缺少必填字段
    missing_username = {
        "email": "missingname@example.com",
        "phone": "13887654321",
        "password": "Password123!",
        "display_name": "无用户名测试",
        "diet_preferences": []
    }
    test_registration('缺少用户名', missing_username, expect_success=False)
    
    # 邮箱格式错误
    invalid_email = {
        "username": "invalidemail",
        "email": "not-an-email",
        "phone": "13811112222",
        "password": "Password123!",
        "display_name": "无效邮箱测试",
        "diet_preferences": []
    }
    test_registration('无效邮箱格式', invalid_email, expect_success=False)
    
    # 手机号格式错误
    invalid_phone = {
        "username": "invalidphone",
        "email": "valid@example.com",
        "phone": "123456789012",
        "password": "Password123!",
        "display_name": "无效手机号测试",
        "diet_preferences": []
    }
    test_registration('无效手机号格式', invalid_phone, expect_success=False)

def test_response_format(response_data):
    """
    测试响应格式
    """
    print_title('测试响应格式')
    
    if not response_data:
        print('❌ 没有有效的响应数据进行格式检查')
        return
    
    # 检查必要的响应字段
    required_fields = ['user_id', 'username', 'email', 'phone', 'display_name', 'created_at']
    missing_fields = [field for field in required_fields if field not in response_data]
    
    if missing_fields:
        print(f'❌ 缺少必要的响应字段: {missing_fields}')
    else:
        print('✅ 所有必要的响应字段都存在')
    
    # 检查字段类型
    print('字段类型检查:')
    for field in response_data:
        print(f"  - {field}: {type(response_data[field]).__name__}")

def check_frontend_api_mismatch():
    """
    检查前后端API不匹配的可能原因
    """
    print_title('前后端API匹配检查')
    
    print('🔍 检查点1: 请求URL匹配')
    print(f'前端注册请求URL: http://localhost:8000/auth/register')
    print(f'测试脚本使用的URL: {REGISTER_ENDPOINT}')
    
    print('\n🔍 检查点2: 请求数据格式')
    frontend_data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13812345678",
        "password": "password123",
        "display_name": "testuser",
        "diet_preferences": []
    }
    print(f'前端发送的数据格式: {json.dumps(frontend_data, ensure_ascii=False)}')
    
    print('\n🔍 检查点3: 常见的前后端不匹配问题')
    print('1. CORS配置问题')
    print('2. 字段名称不匹配')
    print('3. 数据类型不匹配')
    print('4. 密码强度要求不一致')
    print('5. 缺少必填字段')
    print('6. API版本不一致')

if __name__ == "__main__":
    print("🚀 注册功能诊断工具\n")
    run_diagnostic_tests()
    check_frontend_api_mismatch()
    print("\n🎉 诊断测试完成！请查看详细日志分析问题。")
