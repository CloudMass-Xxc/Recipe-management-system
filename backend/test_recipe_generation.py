#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食谱生成功能测试脚本
用于验证AI食谱生成功能是否正常工作
"""

import os
import sys
import asyncio
import httpx
import json
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """加载配置信息"""
    # 加载.env文件
    load_dotenv()
    
    # 获取后端服务配置
    config = {
        "backend_url": os.getenv("BACKEND_URL", "http://localhost:8000"),
        "api_endpoint": f"{os.getenv('BACKEND_URL', 'http://localhost:8000')}/ai/generate-recipe"
    }
    
    return config

async def test_recipe_generation_api(config):
    """测试食谱生成API"""
    logger.info("开始测试食谱生成API...")
    
    # 准备测试数据
    test_recipe_params = {
        "dietary_preferences": ["vegetarian"],
        "food_likes": ["蔬菜", "豆类", "坚果"],
        "food_dislikes": ["肉类", "海鲜"],
        "health_conditions": [],
        "nutrition_goals": ["高蛋白", "低脂肪"],
        "cooking_time_limit": 30,
        "difficulty": "easy",
        "cuisine": "chinese"
    }
    
    logger.info(f"正在调用API端点: {config['api_endpoint']}")
    logger.info(f"测试参数: {json.dumps(test_recipe_params, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送API请求
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url=config["api_endpoint"],
                json=test_recipe_params,
                headers={"Content-Type": "application/json"}
            )
            
            logger.info(f"响应状态码: {response.status_code}")
            
            # 检查响应
            if response.status_code == 200:
                try:
                    recipe_data = response.json()
                    logger.info("食谱生成成功！")
                    logger.info(f"生成的食谱标题: {recipe_data.get('title', '未找到标题')}")
                    
                    # 验证食谱数据结构
                    required_fields = ["title", "ingredients", "instructions"]
                    missing_fields = []
                    for field in required_fields:
                        if field not in recipe_data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        logger.warning(f"食谱数据缺少必要字段: {missing_fields}")
                    else:
                        logger.info("食谱数据结构验证通过")
                    
                    # 打印食谱摘要
                    print_recipe_summary(recipe_data)
                    return True
                    
                except json.JSONDecodeError:
                    logger.error(f"无法解析响应为JSON: {response.text}")
                    return False
            elif response.status_code == 429:
                logger.error("API请求频率限制，稍后再试")
                logger.error(f"响应内容: {response.text}")
                return False
            elif response.status_code >= 500:
                logger.error(f"服务器错误: {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return False
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                return False
                
    except httpx.ConnectError as e:
        logger.error(f"无法连接到后端服务: {str(e)}")
        return False
    except httpx.TimeoutException:
        logger.error("API请求超时")
        return False
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return False

def print_recipe_summary(recipe_data):
    """打印食谱摘要信息"""
    print("\n===== 食谱生成结果摘要 =====")
    print(f"标题: {recipe_data.get('title', 'N/A')}")
    print(f"描述: {recipe_data.get('description', 'N/A')}")
    print(f"准备时间: {recipe_data.get('prep_time', 'N/A')} 分钟")
    print(f"烹饪时间: {recipe_data.get('cooking_time', 'N/A')} 分钟")
    print(f"难度: {recipe_data.get('difficulty', 'N/A')}")
    
    ingredients = recipe_data.get('ingredients', [])
    print(f"\n食材数量: {len(ingredients)}")
    if ingredients:
        print("主要食材:")
        for i, ing in enumerate(ingredients[:3], 1):
            name = ing.get('name', '未知')
            quantity = ing.get('quantity', '')
            unit = ing.get('unit', '')
            print(f"  {i}. {name} - {quantity} {unit}")
    
    instructions = recipe_data.get('instructions', [])
    print(f"\n烹饪步骤数量: {len(instructions) if isinstance(instructions, list) else 1}")
    
    nutrition = recipe_data.get('nutrition_info', {})
    if nutrition:
        print("\n营养信息:")
        print(f"  热量: {nutrition.get('calories', 'N/A')} 千卡")
        print(f"  蛋白质: {nutrition.get('protein', 'N/A')} 克")
        print(f"  碳水化合物: {nutrition.get('carbs', 'N/A')} 克")
        print(f"  脂肪: {nutrition.get('fat', 'N/A')} 克")
    print("============================\n")

def check_backend_status(config):
    """检查后端服务状态"""
    logger.info("检查后端服务状态...")
    status_url = f"{config['backend_url']}/ai/status"
    
    try:
        response = httpx.get(status_url, timeout=10.0)
        
        if response.status_code == 200:
            status_data = response.json()
            logger.info(f"后端服务状态: {status_data.get('status', '未知')}")
            logger.info(f"AI服务提供商: {status_data.get('provider', '未知')}")
            logger.info(f"消息: {status_data.get('message', '')}")
            return status_data.get('status') == 'available'
        else:
            logger.error(f"无法获取后端服务状态，状态码: {response.status_code}")
            return False
            
    except httpx.ConnectError:
        logger.error(f"无法连接到后端服务: {config['backend_url']}")
        return False
    except Exception as e:
        logger.error(f"检查后端服务状态时出错: {str(e)}")
        return False

async def main():
    """主函数"""
    print("===== 食谱生成功能测试 =====")
    
    # 加载配置
    config = load_config()
    
    # 检查后端服务状态
    if not check_backend_status(config):
        print("错误: 后端服务不可用，请先启动后端服务")
        return 1
    
    # 测试食谱生成API
    success = await test_recipe_generation_api(config)
    
    if success:
        print("测试结果: ✓ 食谱生成功能正常工作！")
        return 0
    else:
        print("测试结果: ✗ 食谱生成功能测试失败")
        return 1

if __name__ == "__main__":
    asyncio.run(main())
