import os
import sys
import json
import httpx

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ai_service.config import get_ai_settings
from app.ai_service.ai_client import AIClient

async def test_lingguang_config():
    """测试灵光AI配置"""
    print("=== 测试灵光AI配置 ===")
    
    # 获取配置
    settings = get_ai_settings()
    print(f"当前API提供商: {settings.API_PROVIDER}")
    print(f"灵光AI API密钥: {settings.LINGGUANG_API_KEY}")
    print(f"灵光AI API基础URL: {settings.LINGGUANG_API_BASE_URL}")
    print(f"灵光AI模型: {settings.LINGGUANG_MODEL}")
    
    # 测试AI客户端初始化
    print("\n=== 测试AI客户端初始化 ===")
    ai_client = AIClient()
    print(f"AI客户端API提供商: {ai_client.api_provider}")
    print(f"AI客户端模型: {ai_client.model}")
    print(f"AI客户端API基础URL: {ai_client.api_base_url}")
    
    # 测试请求头
    headers = ai_client._prepare_request_headers()
    print(f"请求头: {headers}")
    
    # 测试请求体准备
    prompt = "测试提示词"
    request_body = ai_client._prepare_chat_completion_request(prompt)
    print(f"请求体: {json.dumps(request_body, indent=2)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_lingguang_config())
