import requests

try:
    print('=== 测试食谱详情API ===')
    response = requests.get('http://localhost:8000/api/recipes/1')
    print('状态码:', response.status_code)
    print('响应文本长度:', len(response.text))
    print('响应文本:', response.text)
except Exception as e:
    print('错误:', repr(e))
