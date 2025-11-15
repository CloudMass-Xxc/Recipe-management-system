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
    AI客户端类，负责与LLM API交互
    """
    
    def __init__(self):
        self.settings = get_ai_settings()
        self.api_key = self.settings.OPENAI_API_KEY
        self.api_base_url = self.settings.OPENAI_API_BASE_URL
        self.model = self.settings.OPENAI_MODEL
        self.timeout = httpx.Timeout(30.0)
    
    def _prepare_request_headers(self) -> Dict[str, str]:
        """
        准备请求头
        
        Returns:
            请求头字典
        """
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
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.settings.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens or self.settings.OPENAI_MAX_TOKENS,
            "temperature": temperature or self.settings.OPENAI_TEMPERATURE,
            "response_format": {"type": "json_object"}  # 要求JSON响应
        }
    
    async def _make_async_request(
        self,
        endpoint: str,
        request_body: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        发送异步HTTP请求
        
        Args:
            endpoint: API端点
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
        url = f"{self.api_base_url}{endpoint}"
        headers = self._prepare_request_headers()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url=url,
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
            response = await self._make_async_request("/chat/completions", request_body)
            
            # 提取和解析响应
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not content:
                raise InvalidResponseError("Empty response from AI API")
            
            # 解析JSON响应
            recipe_data = json.loads(content)
            
            # 验证必要字段
            required_fields = ["title", "ingredients", "instructions"]
            for field in required_fields:
                if field not in recipe_data:
                    raise InvalidResponseError(f"Missing required field: {field}")
            
            return recipe_data
            
        except json.JSONDecodeError:
            # 如果响应不是有效的JSON，记录原始响应并抛出异常
            logger.error(f"Invalid JSON response from AI API: {content}")
            raise InvalidResponseError("AI API returned invalid JSON")
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

请以相同的JSON格式返回修改后的食谱。
"""
        
        request_body = self._prepare_chat_completion_request(prompt)
        
        try:
            response = await self._make_async_request("/chat/completions", request_body)
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error enhancing recipe: {str(e)}")
            if isinstance(e, AIServiceError):
                raise
            raise AIServiceError(f"Failed to enhance recipe: {str(e)}")


# 创建全局AI客户端实例
ai_client = AIClient()