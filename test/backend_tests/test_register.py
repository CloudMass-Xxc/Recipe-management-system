import requests
import json

# 测试注册功能的错误处理
def test_register():
    print('开始测试注册功能的错误处理...')
    
    # 测试1: 使用已存在的用户名
    print('\n测试1: 使用已存在的用户名')
    try:
        response = requests.post('http://localhost:8001/auth/register', json={
            'username': 'testuser',
            'email': 'newemail@example.com',
            'phone': '13100001111',
            'password': 'Test@1234',
            'display_name': 'Test User'
        })
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'请求失败: {e}')
    
    # 测试2: 使用已存在的邮箱
    print('\n测试2: 使用已存在的邮箱')
    try:
        response = requests.post('http://localhost:8001/auth/register', json={
            'username': 'newuser123',
            'email': 'test@example.com',
            'phone': '13100002222',
            'password': 'Test@1234',
            'display_name': 'New User'
        })
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'请求失败: {e}')
    
    # 测试3: 使用弱密码
    print('\n测试3: 使用弱密码')
    try:
        response = requests.post('http://localhost:8001/auth/register', json={
            'username': 'weakpassuser',
            'email': 'weakpass@example.com',
            'phone': '13100003333',
            'password': 'weakpass',
            'display_name': 'Weak Pass User'
        })
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'请求失败: {e}')

if __name__ == '__main__':
    test_register()
