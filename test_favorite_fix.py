# 测试收藏功能修复的Python脚本
import requests
import json

# 测试用户凭据
login_data = {
    "identifier": "xuxiaochang@qq.com",
    "password": "Xxc20001018"
}

try:
    # 登录获取token
    print("正在登录...")
    login_response = requests.post(
        "http://localhost:8001/auth/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    login_response.raise_for_status()
    login_result = login_response.json()
    token = login_result["access_token"]
    
    print(f"登录成功，获取到令牌: {token}")
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 选择一个存在的食谱ID进行测试（这里使用ID为1的食谱）
    recipe_id = "1"
    
    # 测试添加收藏
    print("\n测试添加收藏...")
    add_response = requests.post(
        f"http://localhost:8001/recipes/{recipe_id}/favorite",
        headers=headers
    )
    add_response.raise_for_status()
    print(f"添加收藏成功! 状态码: {add_response.status_code}")
    print(f"响应内容: {add_response.text}")
    
    # 测试取消收藏
    print("\n测试取消收藏...")
    remove_response = requests.delete(
        f"http://localhost:8001/recipes/{recipe_id}/favorite",
        headers=headers
    )
    remove_response.raise_for_status()
    print(f"取消收藏成功! 状态码: {remove_response.status_code}")
    
    print("\n🎉 测试完成！收藏功能修复成功！")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
