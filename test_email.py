import requests
import json

# 简单测试邮箱重复的情况
def test_email_duplicate():
    print('测试邮箱重复的情况...')
    
    # 使用一个全新的用户名和已存在的邮箱
    try:
        response = requests.post('http://localhost:8001/auth/register', 
                                headers={'Content-Type': 'application/json'},
                                json={
                                    'username': 'completely_new_username_12345',
                                    'email': 'test@example.com',
                                    'phone': '13100009999',
                                    'password': 'Test@1234',
                                    'display_name': 'Test User'
                                })
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
        
        # 检查响应是否正确
        if response.status_code == 400:
            if response.json().get('detail') == 'Email already registered':
                print('✓ 邮箱重复检查正常工作')
            else:
                print(f'✗ 错误：返回了错误的消息: {response.json().get("detail")}')
        else:
            print(f'✗ 错误：返回了意外的状态码: {response.status_code}')
    except Exception as e:
        print(f'请求失败: {e}')

if __name__ == '__main__':
    test_email_duplicate()
