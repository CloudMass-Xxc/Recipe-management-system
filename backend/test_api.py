import http.client
import json

def test_get_endpoint(endpoint, parse_json=True):
    conn = http.client.HTTPConnection("localhost", 8000)
    try:
        conn.request("GET", endpoint)
        response = conn.getresponse()
        status = response.status
        data = response.read().decode()
        
        print(f"状态码: {status}")
        if parse_json and status == 200:
            try:
                json_data = json.loads(data)
                print(f"响应内容: {json_data}")
                return True
            except json.JSONDecodeError:
                print(f"响应不是有效的JSON: {data[:100]}...")
                return False
        else:
            print(f"响应长度: {len(data)} 字符")
            return status == 200
    except Exception as e:
        print(f"请求失败: {e}")
        return False
    finally:
        conn.close()

def test_api_endpoints():
    print("开始测试API功能...")
    
    # 测试根路径
    print("\n根路径测试 (GET /):")
    test_get_endpoint("/")
    
    # 测试健康检查
    print("\n健康检查测试 (GET /health):")
    test_get_endpoint("/health")
    
    # 测试API文档访问
    print("\nAPI文档测试 (GET /docs):")
    test_get_endpoint("/docs", parse_json=False)
    
    print("\nAPI功能测试完成!")

if __name__ == "__main__":
    test_api_endpoints()