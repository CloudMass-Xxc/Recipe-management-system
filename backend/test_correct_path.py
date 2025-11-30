import requests

try:
    print('=== 测试正确路径的食谱详情API ===')
    # 使用正确的路径：http://localhost:8000/recipes/1
    response = requests.get('http://localhost:8000/recipes/1')
    print('状态码:', response.status_code)
    print('响应文本:', response.text)
except Exception as e:
    print('错误:', repr(e))
