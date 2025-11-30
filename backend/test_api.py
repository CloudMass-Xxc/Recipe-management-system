import requests

try:
    # 测试食谱详情API
    response = requests.get('http://localhost:8000/api/recipes/1')
    print('状态码:', response.status_code)
    
    if response.status_code == 200:
        data = response.json()
        print('\n完整响应数据:')
        print(data)
        print('\ninstructions字段信息:')
        print('类型:', type(data.get('instructions')))
        print('内容:', data.get('instructions'))
        print('是否为数组:', isinstance(data.get('instructions'), list))
except Exception as e:
    print('错误:', e)
