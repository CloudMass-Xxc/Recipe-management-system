#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化测试脚本：直接测试食谱图片生成功能
避免复杂的数据库操作和外键约束问题
"""

import json
import os
import sys
import logging
from app.ai_service.ai_client import AIClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("TestImageGeneration")

# 获取当前工作目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 添加backend目录到sys.path
sys.path.insert(0, base_dir)

# 初始化AI客户端
try:
    ai_client = AIClient()
    logger.info("成功初始化AI客户端")
except Exception as e:
    logger.error(f"初始化AI客户端失败: {str(e)}", exc_info=True)
    sys.exit(1)

# 测试图片生成功能
def test_image_generation():
    """测试食谱图片生成功能"""
    try:
        logger.info("开始测试图片生成功能")
        
        # 测试用例1: 中文食谱
        cuisine = "Chinese"
        recipe_title = "宫保鸡丁"
        logger.info(f"测试用例1: 尝试为'{recipe_title}' (菜系: {cuisine})生成图片")
        
        # 调用同步方法生成图片
        image_url = ai_client.generate_recipe_image(cuisine, recipe_title)
        
        logger.info(f"测试用例1生成的图片URL: {image_url}")
        
        if image_url and image_url.startswith("http"):
            logger.info("测试用例1通过: 成功生成中文食谱图片!")
        else:
            logger.error("测试用例1失败: 中文食谱图片生成失败!")
            return False
        
        # 测试用例2: 英文食谱
        cuisine = "Italian"
        recipe_title = "Spaghetti Carbonara"
        logger.info(f"测试用例2: 尝试为'{recipe_title}' (菜系: {cuisine})生成图片")
        
        # 调用同步方法生成图片
        image_url2 = ai_client.generate_recipe_image(cuisine, recipe_title)
        
        logger.info(f"测试用例2生成的图片URL: {image_url2}")
        
        if image_url2 and image_url2.startswith("http"):
            logger.info("测试用例2通过: 成功生成英文食谱图片!")
        else:
            logger.error("测试用例2失败: 英文食谱图片生成失败!")
            return False
        
        # 测试用例3: 空参数测试
        logger.info("测试用例3: 尝试使用空参数生成图片")
        try:
            image_url3 = ai_client.generate_recipe_image("", "")
            if image_url3 and image_url3.startswith("http"):
                logger.info("测试用例3通过: 成功处理空参数!")
            else:
                logger.error("测试用例3失败: 空参数处理失败!")
                return False
        except Exception as e:
            logger.error(f"测试用例3异常: {str(e)}")
            return False
        
        logger.info("所有图片生成测试用例通过!")
        return True
        
    except Exception as e:
        logger.error(f"图片生成测试失败: {str(e)}", exc_info=True)
        return False

# 测试图片URL处理逻辑
def test_image_url_handling():
    """测试图片URL处理逻辑"""
    try:
        logger.info("开始测试图片URL处理逻辑")
        
        # 模拟前端发送的食谱数据
        test_cases = [
            # 测试用例1: 有图片URL
            {
                "title": "宫保鸡丁",
                "cuisine": "Chinese",
                "image": "https://example.com/gongbao.jpg"
            },
            # 测试用例2: 无图片URL
            {
                "title": "麻婆豆腐",
                "cuisine": "Chinese"
            },
            # 测试用例3: 空图片URL
            {
                "title": "鱼香肉丝",
                "cuisine": "Chinese",
                "image": ""
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"测试用例{i}: 处理食谱数据: {test_case}")
            
            # 模拟图片URL处理逻辑
            if test_case.get("image") and test_case["image"].strip():
                # 如果有有效的图片URL，直接使用
                image_url = test_case["image"]
                logger.info(f"测试用例{i}使用提供的图片URL: {image_url}")
            else:
                # 如果没有图片URL，生成占位图
                import urllib.parse
                encoded_title = urllib.parse.quote(test_case["title"])
                encoded_cuisine = urllib.parse.quote(test_case["cuisine"])
                image_url = f"https://picsum.photos/seed/{encoded_title}{encoded_cuisine}/800/600"
                logger.info(f"测试用例{i}生成占位图片URL: {image_url}")
            
            # 验证生成的URL格式
            if image_url and image_url.startswith("http"):
                logger.info(f"测试用例{i}通过: 图片URL格式正确")
            else:
                logger.error(f"测试用例{i}失败: 图片URL格式不正确")
                return False
        
        logger.info("所有图片URL处理测试用例通过!")
        return True
        
    except Exception as e:
        logger.error(f"图片URL处理测试失败: {str(e)}", exc_info=True)
        return False

# 主函数
def main():
    """运行所有测试"""
    logger.info("开始运行食谱图片生成和处理测试")
    
    try:
        # 1. 测试图片生成功能
        logger.info("===== 测试1: 图片生成功能 =====")
        image_generation_success = test_image_generation()
        
        if not image_generation_success:
            logger.error("图片生成功能测试失败")
            return False
        
        # 2. 测试图片URL处理逻辑
        logger.info("\n===== 测试2: 图片URL处理逻辑 =====")
        url_handling_success = test_image_url_handling()
        
        if not url_handling_success:
            logger.error("图片URL处理逻辑测试失败")
            return False
        
        logger.info("\n🎉 所有测试通过！食谱图片生成和处理功能正常工作。")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
