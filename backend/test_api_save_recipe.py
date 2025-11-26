# -*- coding: utf-8 -*-
"""
测试前端API调用 - 保存生成的食谱
"""

import requests
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_save_recipe_api():
    """
    测试保存生成食谱的API端点
    """
    try:
        logger.info("开始测试保存食谱API...")
        
        # 1. 登录获取令牌
        login_url = "http://localhost:8000/api/auth/login"
        login_data = {
            "identifier": "xuxiaochang@qq.com",
            "password": "Xxc20001018..."
        }
        
        logger.info("发送登录请求...")
        login_response = requests.post(
            login_url,
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code != 200:
            logger.error(f"登录失败！状态码: {login_response.status_code}")
            logger.error(f"登录响应: {login_response.text}")
            return False
        
        token = login_response.json().get("access_token")
        if not token:
            logger.error("获取令牌失败！")
            return False
        
        logger.info(f"登录成功！令牌: {token}")
        
        # 2. 保存食谱
        save_url = "http://localhost:8000/ai/save-generated-recipe"
        recipe_data = {
            "recipe_data": {
                "title": "测试食谱",
                "description": "这是一个测试用的食谱",
                "difficulty": "easy",
                "cooking_time": 30,
                "servings": 2,
                "instructions": "准备食材\n烹饪\n享用",
                "ingredients": [
                    {"name": "鸡蛋", "quantity": 2, "unit": "个"},
                    {"name": "米饭", "quantity": 1, "unit": "碗"}
                ],
                "tags": ["测试", "快速"],
                "nutrition_info": {
                    "calories": 500,
                    "protein": 20,
                    "carbs": 60,
                    "fat": 15,
                    "fiber": 5
                }
            }
        }
        
        logger.info("发送保存食谱请求...")
        save_response = requests.post(
            save_url,
            json=recipe_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        
        logger.info(f"保存食谱响应状态码: {save_response.status_code}")
        logger.info(f"保存食谱响应内容: {save_response.text}")
        
        if save_response.status_code != 200:
            logger.error("保存食谱失败！")
            return False
        
        logger.info("保存食谱成功！")
        
        # 3. 解析响应数据
        response_data = save_response.json()
        logger.info(f"响应数据: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        return True
        
    except Exception as e:
        logger.error(f"测试保存食谱API时出错: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("开始执行前端API测试脚本...")
    success = test_save_recipe_api()
    if success:
        logger.info("脚本执行成功！保存食谱API测试通过。")
    else:
        logger.error("脚本执行失败！保存食谱API测试失败。")
