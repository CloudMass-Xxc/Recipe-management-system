import os
from typing import Dict, Any
from pydantic_settings import BaseSettings
from functools import lru_cache


class AIServiceSettings(BaseSettings):
    """
    AI服务配置类
    """
    # API提供商配置
    API_PROVIDER: str = "alipan"  # 默认使用通义千问
    
    # OpenAI配置
    OPENAI_API_KEY: str = ""  # 从环境变量读取
    OPENAI_API_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo-1106"  # 使用支持JSON响应的模型
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7
    
    # 通义千问配置
    QWEN_API_KEY: str = ""  # 从环境变量读取
    QWEN_API_SECRET: str = ""  # 从环境变量读取
    QWEN_API_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"  # 通义千问API基础URL
    QWEN_MODEL: str = "qwen-turbo"  # 通义千问模型
    QWEN_MAX_TOKENS: int = 2000
    QWEN_TEMPERATURE: float = 0.7
    
    # 系统提示词
    SYSTEM_PROMPT: str = """
你是一个专业的营养师和厨师，擅长根据用户的饮食偏好、健康状况和目标生成个性化食谱。
请根据用户提供的信息，生成详细、可行且符合营养均衡的食谱建议。
"""
    
    # 食谱生成提示词模板
    RECIPE_GENERATION_PROMPT_TEMPLATE: str = """
请为我生成一个个性化食谱，满足以下条件：

饮食偏好：{dietary_preferences}
食物喜好：{food_likes}
食物禁忌：{food_dislikes}
健康状况：{health_conditions}
营养目标：{nutrition_goals}
烹饪时间限制：{cooking_time_limit}
难度级别：{difficulty}

请以JSON格式输出，包含以下字段：
- title: 食谱标题
- description: 简短描述
- prep_time: 准备时间（分钟）
- cooking_time: 烹饪时间（分钟）
- servings: 份量
- difficulty: 难度级别（easy/medium/hard）
- ingredients: 食材列表，每项包含name, quantity, unit, note
- instructions: 烹饪步骤
- nutrition_info: 营养信息，包含calories, protein, carbs, fat, fiber
- tips: 烹饪小贴士
"""
    
    class Config:
        env_file = ".env"
        extra = "allow"  # 允许额外的环境变量


@lru_cache()
def get_ai_settings() -> AIServiceSettings:
    """
    获取AI服务配置实例（单例模式）
    
    Returns:
        AIServiceSettings实例
    """
    return AIServiceSettings()