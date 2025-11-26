#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用FastAPI TestClient测试保存食谱API
使用依赖注入模拟用户认证，确保instructions是字符串格式
"""

from fastapi.testclient import TestClient
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

# 导入应用和数据库模型
try:
    from backend.main import app
    from backend.app.core.database import get_db
    from backend.app.auth.dependencies import get_current_user as original_get_current_user
    from backend.app.models.user import User
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

# 测试配置
TEST_USER_ID = "b9c9b23f-0fb9-4422-8ee2-3f0eb19d4e21"  # 从测试脚本中获取的有效用户ID

# 创建测试客户端
client = TestClient(app)

print("===== 使用TestClient测试保存食谱API =====")

# 读取测试数据
try:
    with open("test_recipe_data.json", "r", encoding="utf-8") as f:
        test_data = json.load(f)
    print(f"✅ 成功读取测试数据: {test_data['recipe_data'].get('title')}")
except Exception as e:
    print(f"❌ 读取测试数据失败: {e}")
    sys.exit(1)

# 确保instructions是字符串格式
if isinstance(test_data['recipe_data'].get('instructions'), list):
    print("⚠️  测试数据中instructions是数组格式，将自动转换为字符串")
    test_data['recipe_data']['instructions'] = '\n'.join(test_data['recipe_data']['instructions'])

print(f"\n测试数据详情:")
print(f"- 食谱标题: {test_data['recipe_data'].get('title')}")
print(f"- 食谱描述: {test_data['recipe_data'].get('description')}")
print(f"- 烹饪步骤类型: {type(test_data['recipe_data'].get('instructions'))}")
print(f"- 烹饪步骤内容(前100字符): {test_data['recipe_data'].get('instructions')[:100]}...")

# 测试函数
def test_save_recipe():
    """使用TestClient测试保存食谱API"""
    print("\n🚀 开始测试保存食谱API...")
    
    # 获取数据库会话以查找测试用户
    try:
        db = next(get_db())
        test_user = db.query(User).filter(User.user_id == TEST_USER_ID).first()
        
        if not test_user:
            print(f"❌ 未找到测试用户: {TEST_USER_ID}")
            return False
        
        print(f"✅ 找到测试用户: {test_user.username}")
        
        # 重写get_current_user依赖，直接返回测试用户
        def override_get_current_user():
            return test_user
        
        # 应用依赖重写
        app.dependency_overrides[original_get_current_user] = override_get_current_user
        
        try:
            # 发送API请求
            response = client.post(
                "/ai/save-generated-recipe",
                json=test_data,
                headers={"Authorization": "Bearer test_token"}  # 令牌不重要，因为我们重写了认证
            )
            
            print(f"\n📊 API响应:")
            print(f"- 状态码: {response.status_code}")
            print(f"- 响应内容: {response.text}")
            
            if response.status_code == 200:
                print("\n🎉 API调用成功！")
                return True
            else:
                print(f"\n❌ API调用失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"\n💥 API请求异常: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清除依赖重写
            app.dependency_overrides.clear()
            
    except Exception as e:
        print(f"\n💥 测试过程异常: {e}")
        import traceback
        traceback.print_exc()
        return False

# 运行测试
if __name__ == "__main__":
    success = test_save_recipe()
    
    print("\n===== 测试结果 =====")
    if success:
        print("🎉 测试通过！保存食谱API功能正常工作。")
        sys.exit(0)
    else:
        print("💥 测试失败！保存食谱API功能仍有问题。")
        sys.exit(1)
