import requests

try:
    print('=== 测试获取所有食谱API ===')
    response = requests.get('http://localhost:8000/api/recipes')
    print('状态码:', response.status_code)
    print('响应数据:', response.json())
except Exception as e:
    print('错误:', repr(e))
