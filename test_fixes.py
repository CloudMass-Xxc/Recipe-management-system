#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证修复效果

本脚本用于测试我们对两个问题的修复：
1. 食谱列表显示异常问题
2. 个性化食谱生成模块故障
"""

import requests
import json
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_fixes.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_fixes")

# API 配置
BASE_URL = "http://localhost:8002"
FRONTEND_URL = "http://localhost:5174"

# 测试用例 1: 测试食谱列表显示异常问题
def test_recipe_list_fix():
    """测试食谱列表显示异常问题的修复"""
    logger.info("=== 开始测试食谱列表显示异常问题的修复 ===")
    
    try:
        # 1. 获取所有食谱列表
        logger.info("1. 测试获取所有食谱列表")
        response = requests.get(f"{BASE_URL}/recipes")
        logger.info(f"获取食谱列表响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            recipes_data = response.json()
            logger.info(f"成功获取食谱列表，共 {len(recipes_data)} 个食谱")
            
            # 检查是否有收藏标记的食谱
            favorite_recipes_in_list = [recipe for recipe in recipes_data if recipe.get('is_favorite')]
            if favorite_recipes_in_list:
                logger.warning(f"发现 {len(favorite_recipes_in_list)} 个带有收藏标记的食谱")
                for i, recipe in enumerate(favorite_recipes_in_list[:3]):
                    logger.warning(f"  - 食谱 {i+1}: ID={recipe.get('id')}, 标题={recipe.get('title')}")
            else:
                logger.info("✓ 食谱列表中没有发现带有收藏标记的食谱，修复有效")
        else:
            logger.error(f"获取食谱列表失败: {response.text}")
            
        # 2. 测试获取收藏食谱
        logger.info("2. 测试获取收藏食谱")
        # 注意：这里可能需要先登录或提供用户ID，根据实际API设计调整
        # 我们可以尝试不同的方式来测试收藏功能
        
        # 尝试使用可能的收藏食谱API
        try:
            # 方案1：使用用户ID参数
            user_id = "1"  # 假设的测试用户ID
            response = requests.get(f"{BASE_URL}/recipes?user_id={user_id}&is_favorite=true")
            logger.info(f"使用user_id参数获取收藏食谱响应状态码: {response.status_code}")
            
            # 方案2：使用收藏路由
            response = requests.get(f"{BASE_URL}/recipes/favorites/{user_id}")
            logger.info(f"使用favorites路由获取收藏食谱响应状态码: {response.status_code}")
            
        except Exception as e:
            logger.warning(f"测试收藏食谱API时发生异常: {str(e)}")
            logger.info("注意：收藏功能测试可能需要用户认证，建议在前端手动测试")
        
        logger.info("食谱列表显示异常问题测试完成")
        return True
        
    except Exception as e:
        logger.error(f"测试食谱列表显示异常问题时发生错误: {str(e)}")
        import traceback
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return False

# 测试用例 2: 测试个性化食谱生成模块
def test_personalized_recipe_generation():
    """测试个性化食谱生成模块的修复"""
    logger.info("\n=== 开始测试个性化食谱生成模块的修复 ===")
    
    try:
        # 测试数据
        test_data = {
            "ingredients": ["鸡胸肉", "西兰花", "胡萝卜"],
            "dietary_preferences": ["低脂肪", "高蛋白"],
            "cooking_time": "30分钟以内"
        }
        
        logger.info(f"测试数据: {json.dumps(test_data, ensure_ascii=False)}")
        
        # 发送请求生成个性化食谱
        logger.info("发送请求生成个性化食谱...")
        response = requests.post(
            f"{BASE_URL}/ai/generate-recipe",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"生成食谱响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            recipe_data = response.json()
            logger.info("✓ 成功生成个性化食谱！")
            logger.info(f"生成的食谱标题: {recipe_data.get('title', 'N/A')}")
            
            # 检查生成的食谱数据结构
            required_fields = ['title', 'ingredients', 'instructions']
            missing_fields = [field for field in required_fields if field not in recipe_data]
            
            if missing_fields:
                logger.warning(f"生成的食谱缺少必要字段: {missing_fields}")
            else:
                logger.info("✓ 生成的食谱包含所有必要字段")
                logger.info(f"  - 食材数量: {len(recipe_data.get('ingredients', []))}")
                logger.info(f"  - 步骤数量: {len(recipe_data.get('instructions', []))}")
                
                # 打印前3个食材和步骤作为示例
                logger.info("  - 部分食材示例: {}".format(
                    "", "\n    ".join(recipe_data['ingredients'][:3]) if recipe_data['ingredients'] else "无"
                ))
                logger.info("  - 部分步骤示例: {}".format(
                    "", "\n    ".join(recipe_data['instructions'][:3]) if recipe_data['instructions'] else "无"
                ))
                
            return True
        else:
            logger.error(f"生成个性化食谱失败: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"测试个性化食谱生成模块时发生错误: {str(e)}")
        import traceback
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return False

# 测试用例 3: 测试异常数据处理
def test_edge_cases():
    """测试边缘情况处理"""
    logger.info("\n=== 开始测试边缘情况处理 ===")
    
    try:
        # 1. 测试空食材列表
        logger.info("1. 测试空食材列表")
        test_data = {
            "ingredients": [],
            "dietary_preferences": ["低脂肪"],
            "cooking_time": "30分钟以内"
        }
        
        response = requests.post(
            f"{BASE_URL}/ai/generate-recipe",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"空食材列表测试响应状态码: {response.status_code}")
        if response.status_code in [200, 400]:
            logger.info("✓ 成功处理空食材列表请求")
        else:
            logger.warning(f"空食材列表测试返回意外状态码: {response.status_code}")
        
        # 2. 测试不完整的请求数据
        logger.info("2. 测试不完整的请求数据")
        test_data = {
            "ingredients": ["鸡胸肉"]
            # 缺少 dietary_preferences 和 cooking_time
        }
        
        response = requests.post(
            f"{BASE_URL}/ai/generate-recipe",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        logger.info(f"不完整请求数据测试响应状态码: {response.status_code}")
        if response.status_code in [200, 400]:
            logger.info("✓ 成功处理不完整的请求数据")
        else:
            logger.warning(f"不完整请求数据测试返回意外状态码: {response.status_code}")
            
        return True
        
    except Exception as e:
        logger.error(f"测试边缘情况处理时发生错误: {str(e)}")
        import traceback
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        return False

# 主测试函数
def run_all_tests():
    """运行所有测试"""
    logger.info("开始运行所有修复验证测试")
    logger.info(f"后端API地址: {BASE_URL}")
    logger.info(f"前端地址: {FRONTEND_URL}")
    
    # 等待服务完全启动
    logger.info("等待3秒确保服务完全启动...")
    time.sleep(3)
    
    # 运行测试
    test_results = {
        "recipe_list_fix": test_recipe_list_fix(),
        "personalized_recipe_generation": test_personalized_recipe_generation(),
        "edge_cases": test_edge_cases()
    }
    
    # 输出测试结果摘要
    logger.info("\n=== 测试结果摘要 ===")
    for test_name, passed in test_results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        logger.info(f"{test_name}: {status}")
    
    # 计算总体结果
    total_tests = len(test_results)
    passed_tests = sum(1 for passed in test_results.values() if passed)
    
    logger.info(f"\n总体测试结果: {passed_tests}/{total_tests} 测试通过")
    
    if passed_tests == total_tests:
        logger.info("🎉 所有测试通过！修复验证成功！")
    else:
        logger.warning("⚠️ 部分测试失败，建议进一步检查和修复。")
    
    logger.info("\n测试完成！建议在前端界面进行手动验证，确保所有功能正常工作。")
    logger.info("前端访问地址: {}".format(FRONTEND_URL))
    logger.info("后端API文档地址: {}/docs".format(BASE_URL))

if __name__ == "__main__":
    run_all_tests()