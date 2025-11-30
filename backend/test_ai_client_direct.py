#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试AI客户端生成食谱
不通过API接口，直接调用AIClient类生成食谱
用于验证AI客户端是否能正确生成包含图片URL的食谱
"""

import sys
import os
import asyncio
import json
from app.ai_service.ai_client import AIClient
from app.ai_service.config import get_ai_settings

async def main():
    """
    主函数，测试AI客户端生成食谱
    """
    print("=== 直接测试AI客户端 ===")
    
    # 获取AI设置
    settings = get_ai_settings()
    print(f"API提供商: {settings.API_PROVIDER}")
    print(f"模型: {settings.QWEN_MODEL}")
    print(f"API密钥配置: {'✅ 已配置' if settings.QWEN_API_KEY else '❌ 未配置'}")
    
    # 打印提示词模板
    print("\n=== 提示词模板内容 ===")
    print(settings.RECIPE_GENERATION_PROMPT_TEMPLATE)
    
    # 创建AI客户端实例
    ai_client = AIClient()
    
    # 测试数据 - 按照AIClient.generate_recipe方法的要求格式
    recipe_params = {
        "dietary_preferences": "素食",
        "food_likes": "西红柿,鸡蛋,米饭",
        "food_dislikes": "香菜",
        "health_conditions": "无",
        "nutrition_goals": "均衡营养",
        "cooking_time_limit": 20,
        "difficulty": "简单",
        "cuisine": "中式",
        "ingredients": "西红柿,鸡蛋,米饭"
    }
    
    print("\n=== 开始生成食谱 ===")
    
    try:
        # 正确调用AI客户端生成食谱 - 传递一个包含所有参数的字典
        recipe = await ai_client.generate_recipe(recipe_params)
        
        print("\n✅ 食谱生成成功！")
        print(f"\n=== 食谱详情 ===")
        print(f"标题: {recipe.get('title')}")
        print(f"描述: {recipe.get('description')}")
        print(f"烹饪时间: {recipe.get('cooking_time')} 分钟")
        print(f"难度: {recipe.get('difficulty')}")
        print(f"菜系: {recipe.get('cuisine')}")
        
        # 检查是否包含图片URL
        if 'image_url' in recipe:
            print(f"\n📷 图片URL: {recipe.get('image_url')}")
            print("✅ 食谱包含图片URL！")
        else:
            print("\n❌ 食谱不包含图片URL！")
        
        # 打印食谱完整内容（可选）
        print("\n=== 完整食谱数据 ===")
        print(json.dumps(recipe, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"\n❌ 生成食谱时发生错误: {e}")
        import traceback
        print(f"错误详情: {traceback.format_exc()}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())
