import requests

# 测试API连接
url = 'http://127.0.0.1:8001/recipes/9384ea78-29a7-4d5c-bbaa-d0fd26ff93cb'
print(f'测试API连接: {url}')

# 发送GET请求
try:
    response = requests.get(url)
    print(f'HTTP状态码: {response.status_code}')
    print(f'响应内容类型: {response.headers.get("Content-Type")}')
    print('响应内容:')
    print(response.text[:1000] + '...' if len(response.text) > 1000 else response.text)
except Exception as e:
    print(f'请求失败: {e}')
