import json
import logging
from typing import Dict, Any, Optional
import httpx
from app.ai_service.config import get_ai_settings
from app.ai_service.exceptions import (
    AIServiceError,
    APIConnectionError,
    InvalidResponseError,
    RateLimitError,
    AuthenticationError
)

logger = logging.getLogger(__name__)


class AIClient:
    """
    AI客户端类，负责与LLM API交互，支持通义千问和OpenAI
    """
    
    def __init__(self):
        self.settings = get_ai_settings()
        self.api_provider = self.settings.API_PROVIDER
        self.timeout = httpx.Timeout(30.0)
        
        # 初始化API配置
        if self.api_provider == "alipan":
            # 通义千问配置
            self.api_key = self.settings.QWEN_API_KEY
            self.api_secret = self.settings.QWEN_API_SECRET
            self.api_base_url = self.settings.QWEN_API_BASE_URL
            self.model = self.settings.QWEN_MODEL
            self.max_tokens = self.settings.QWEN_MAX_TOKENS
            self.temperature = self.settings.QWEN_TEMPERATURE
        else:
            # OpenAI配置
            self.api_key = self.settings.OPENAI_API_KEY
            self.api_base_url = self.settings.OPENAI_API_BASE_URL
            self.model = self.settings.OPENAI_MODEL
            self.max_tokens = self.settings.OPENAI_MAX_TOKENS
            self.temperature = self.settings.OPENAI_TEMPERATURE
    
    def _prepare_request_headers(self) -> Dict[str, str]:
        """
        准备请求头
        
        Returns:
            请求头字典
        """
        if self.api_provider == "alipan":
            # 通义千问请求头
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            # OpenAI请求头
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
    
    def _prepare_chat_completion_request(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        准备聊天完成请求
        
        Args:
            prompt: 用户提示词
            max_tokens: 最大令牌数
            temperature: 温度参数
        
        Returns:
            请求体字典
        """
        if self.api_provider == "alipan":
            # 通义千问请求格式
            system_prompt = self.settings.SYSTEM_PROMPT
            full_prompt = f"{system_prompt}\n\n{prompt}\n\n请严格按照JSON格式输出，不要添加任何额外的解释或文本。"
            
            return {
                "model": self.model,
                "input": {
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ]
                },
                "parameters": {
                    "max_tokens": max_tokens or self.max_tokens,
                    "temperature": temperature or self.temperature,
                    "result_format": "text"
                }
            }
        else:
            # OpenAI请求格式
            return {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.settings.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature or self.temperature,
                "response_format": {"type": "json_object"}  # 要求JSON响应
            }
    
    async def _make_async_request(
        self,
        request_body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        发送异步HTTP请求
        
        Args:
            request_body: 请求体
        
        Returns:
            API响应
        
        Raises:
            AIServiceError: AI服务错误
            APIConnectionError: API连接错误
            InvalidResponseError: 无效响应错误
            RateLimitError: 速率限制错误
            AuthenticationError: 认证错误
        """
        headers = self._prepare_request_headers()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url=self.api_base_url,
                    headers=headers,
                    json=request_body
                )
                
                # 检查响应状态码
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 429:
                    raise RateLimitError("API rate limit exceeded")
                elif response.status_code >= 500:
                    raise APIConnectionError(f"API server error: {response.status_code}")
                elif response.status_code != 200:
                    raise AIServiceError(f"API request failed: {response.status_code}")
                
                # 解析响应
                return response.json()
                
        except httpx.ConnectError:
            raise APIConnectionError("Failed to connect to AI API")
        except httpx.TimeoutException:
            raise APIConnectionError("API request timed out")
        except (ValueError, json.JSONDecodeError):
            raise InvalidResponseError("Failed to parse API response")
    
    async def generate_recipe(
        self,
        recipe_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成个性化食谱
        
        Args:
            recipe_params: 食谱生成参数
        
        Returns:
            生成的食谱数据
        
        Raises:
            AIServiceError: AI服务错误
        """
        # 格式化提示词
        prompt = self.settings.RECIPE_GENERATION_PROMPT_TEMPLATE.format(**recipe_params)
        
        # 准备请求
        request_body = self._prepare_chat_completion_request(prompt)
        
        try:
            # 调用API
            response = await self._make_async_request(request_body)
            
            # 根据不同的API提供商解析响应
            if self.api_provider == "alipan":
                # 通义千问响应格式
                content = response.get("output", {}).get("text", "")
            else:
                # OpenAI响应格式
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                raise InvalidResponseError("Empty response from AI API")
            
            logger.info(f"Raw AI response: {content}")
            
            # 尝试提取JSON部分（如果响应包含额外文本）
            try:
                # 尝试直接解析
                recipe_data = json.loads(content)
            except json.JSONDecodeError:
                # 尝试提取JSON格式的部分
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    recipe_data = json.loads(json_match.group())
                else:
                    raise InvalidResponseError("Could not find valid JSON in AI response")
            
            # 验证必要字段
            required_fields = ["title", "ingredients", "instructions"]
            for field in required_fields:
                if field not in recipe_data:
                    raise InvalidResponseError(f"Missing required field: {field}")
            
            return recipe_data
            
        except json.JSONDecodeError as e:
            # 如果响应不是有效的JSON，记录原始响应并抛出异常
            logger.error(f"Invalid JSON response from AI API: {content}")
            raise InvalidResponseError(f"AI API returned invalid JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}")
            if isinstance(e, AIServiceError):
                raise
            raise AIServiceError(f"Failed to generate recipe: {str(e)}")
    
    async def enhance_recipe(
        self,
        recipe_data: Dict[str, Any],
        enhancement_request: str
    ) -> Dict[str, Any]:
        """
        增强或修改现有食谱
        
        Args:
            recipe_data: 现有食谱数据
            enhancement_request: 增强请求描述
        
        Returns:
            增强后的食谱数据
        """
        prompt = f"""
请对以下食谱进行修改或增强：

{json.dumps(recipe_data, ensure_ascii=False)}

修改要求：{enhancement_request}

请严格按照JSON格式返回修改后的食谱，不要添加任何额外的解释或文本。
"""
        
        request_body = self._prepare_chat_completion_request(prompt)
        
        try:
            response = await self._make_async_request(request_body)
            
            # 根据不同的API提供商解析响应
            if self.api_provider == "alipan":
                content = response.get("output", {}).get("text", "")
            else:
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            logger.info(f"Raw AI enhancement response: {content}")
            
            # 尝试提取JSON部分
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    raise InvalidResponseError("Could not find valid JSON in AI response")
            
        except Exception as e:
            logger.error(f"Error enhancing recipe: {str(e)}")
            if isinstance(e, AIServiceError):
                raise
            raise AIServiceError(f"Failed to enhance recipe: {str(e)}")


# 创建全局AI客户端实例
ai_client = AIClient()