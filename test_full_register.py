import requests
import json

# 测试完整的注册功能
def test_full_register():
    print('测试完整的注册功能...')
    
    # 使用全新的用户信息
    new_username = 'brand_new_user_999'
    new_email = 'brand_new_email_999@example.com'
    new_phone = '13100008888'
    
    print(f'\n使用全新的用户信息注册:')
    print(f'- 用户名: {new_username}')
    print(f'- 邮箱: {new_email}')
    print(f'- 手机号: {new_phone}')
    print(f'- 密码: Test@1234')
    
    try:
        response = requests.post('http://localhost:8001/auth/register', 
                                headers={'Content-Type': 'application/json'},
                                json={
                                    'username': new_username,
                                    'email': new_email,
                                    'phone': new_phone,
                                    'password': 'Test@1234',
                                    'display_name': 'Brand New User'
                                })
        print(f'\n状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
        
        # 检查响应是否成功
        if response.status_code == 201:
            print('\n✓ 注册成功!')
            
            # 测试登录，验证注册的用户可以正常登录
            print('\n\n测试登录，验证注册的用户可以正常登录...')
            try:
                login_response = requests.post('http://localhost:8001/auth/login',
                                             headers={'Content-Type': 'application/json'},
                                             json={
                                                 'identifier': new_email,
                                                 'password': 'Test@1234'
                                             })
                print(f'登录状态码: {login_response.status_code}')
                print(f'登录响应内容: {json.dumps(login_response.json(), ensure_ascii=False, indent=2)}')
                
                if login_response.status_code == 200:
                    print('\n✓ 登录成功! 注册功能完整正常工作')
                else:
                    print('\n✗ 登录失败')
            except Exception as e:
                print(f'登录请求失败: {e}')
        else:
            print('\n✗ 注册失败')
    except Exception as e:
        print(f'注册请求失败: {e}')

if __name__ == '__main__':
    test_full_register()
