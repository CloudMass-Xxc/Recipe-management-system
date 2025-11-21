#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问API连接测试脚本
用于验证通义千问API密钥是否有效以及连接状态
"""

import os
import sys
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
    
    # 获取通义千问配置
    config = {
        "api_key": os.getenv("QWEN_API_KEY", ""),
        "api_secret": os.getenv("QWEN_API_SECRET", ""),
        "api_base_url": os.getenv(
            "QWEN_API_BASE_URL",
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        ),
        "model": "qwen-turbo"
    }
    
    # 验证必要的配置
    if not config["api_key"]:
        logger.error("未配置QWEN_API_KEY")
        return None
    
    return config

def test_qwen_api_connection(config):
    """测试通义千问API连接"""
    logger.info("开始测试通义千问API连接...")
    
    # 准备测试请求
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    # 简单的测试提示词
    test_prompt = "请输出一个简单的JSON对象，包含字段'hello'，值为'world'。"
    
    request_body = {
        "model": config["model"],
        "input": {
            "messages": [
                {"role": "user", "content": test_prompt}
            ]
        },
        "parameters": {
            "max_tokens": 100,
            "temperature": 0.0,
            "result_format": "text"
        }
    }
    
    try:
        logger.info(f"正在连接到: {config['api_base_url']}")
        logger.info(f"使用API密钥: {config['api_key'][:8]}...")
        
        # 发送测试请求
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                url=config["api_base_url"],
                headers=headers,
                json=request_body
            )
            
            logger.info(f"响应状态码: {response.status_code}")
            
            # 检查响应
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    logger.info("API连接成功！")
                    logger.info(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
                    return True
                except json.JSONDecodeError:
                    logger.error(f"无法解析响应为JSON: {response.text}")
                    return False
            elif response.status_code == 401:
                logger.error("认证失败！API密钥可能无效或已过期")
                logger.error(f"响应内容: {response.text}")
                return False
            elif response.status_code == 429:
                logger.error("请求过于频繁，API速率限制已触发")
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
        logger.error(f"网络连接错误: {str(e)}")
        return False
    except httpx.TimeoutException:
        logger.error("请求超时")
        return False
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        return False

def validate_api_key_format(api_key):
    """验证API密钥格式是否正确"""
    # 通义千问API密钥通常是固定长度的字符串
    # 检查是否是有效的格式
    if not api_key or len(api_key) < 30:
        logger.warning("API密钥格式可能不正确，长度过短")
        return False
    
    # 检查是否是sk-开头（通常的模式）
    if not api_key.startswith("sk-"):
        logger.warning("API密钥可能不是正确的格式，应以sk-开头")
        return False
    
    return True

def main():
    """主函数"""
    print("===== 通义千问API连接测试 =====")
    
    # 加载配置
    config = load_config()
    if not config:
        print("错误: 配置加载失败，请检查.env文件")
        return 1
    
    # 验证API密钥格式
    if not validate_api_key_format(config["api_key"]):
        print("警告: API密钥格式可能不正确")
    else:
        print("API密钥格式检查通过")
    
    # 测试API连接
    success = test_qwen_api_connection(config)
    
    if success:
        print("\n测试结果: ✓ 通义千问API连接成功！")
        return 0
    else:
        print("\n测试结果: ✗ 通义千问API连接失败，请检查配置和网络连接")
        return 1

if __name__ == "__main__":
    sys.exit(main())
