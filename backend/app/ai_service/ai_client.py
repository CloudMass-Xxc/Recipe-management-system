import json
import logging
import re
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
        logger.info(f"准备发送HTTP请求，API提供商: {self.api_provider}")
        logger.info(f"请求URL: {self.api_base_url}")
        logger.info(f"请求超时设置: {self.timeout}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("开始发送POST请求到AI服务API")
                response = await client.post(
                    url=self.api_base_url,
                    headers=headers,
                    json=request_body
                )
                
                logger.info(f"API请求完成，状态码: {response.status_code}")
                
                # 检查响应状态码
                if response.status_code == 401:
                    logger.error("API认证失败，可能是API密钥无效")
                    raise AuthenticationError("Invalid API key or authentication failed")
                elif response.status_code == 429:
                    logger.error("API速率限制被触发")
                    raise RateLimitError("API rate limit exceeded")
                elif response.status_code >= 500:
                    logger.error(f"API服务器错误，状态码: {response.status_code}")
                    raise APIConnectionError(f"API server error: {response.status_code}")
                elif response.status_code != 200:
                    logger.error(f"API请求失败，状态码: {response.status_code}")
                    raise AIServiceError(f"API request failed: {response.status_code}")
                
                # 解析响应
                logger.info("开始解析API响应")
                response_json = response.json()
                logger.info(f"成功获取API响应，响应结构: {list(response_json.keys())}")
                return response_json
                
        except httpx.ConnectError as e:
            logger.error(f"连接AI API失败: {str(e)}")
            raise APIConnectionError("Failed to connect to AI API")
        except httpx.TimeoutException as e:
            logger.error(f"API请求超时: {str(e)}")
            raise APIConnectionError("API request timed out")
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"解析API响应失败: {str(e)}")
            raise InvalidResponseError("Failed to parse API response")
        except Exception as e:
            logger.error(f"API请求处理异常: {str(e)}", exc_info=True)
            raise
    
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
        logger.info(f"开始生成食谱，API提供商: {self.api_provider}")
        logger.info(f"食谱参数详情: {recipe_params}")
        
        # 格式化提示词
        prompt = self.settings.RECIPE_GENERATION_PROMPT_TEMPLATE.format(**recipe_params)
        logger.info(f"构建提示词完成，提示词长度: {len(prompt)} 字符")
        
        # 准备请求
        request_body = self._prepare_chat_completion_request(prompt)
        logger.info(f"准备请求体完成，请求体结构: {list(request_body.keys())}")
        
        try:
            # 调用API
            logger.info("开始发送API请求到AI服务")
            response = await self._make_async_request(request_body)
            logger.info(f"API请求完成，响应状态: {'成功' if response else '失败'}")
            
            # 使用统一的解析方法处理响应
            recipe_data = self._parse_response(response)
            logger.info(f"响应解析完成，获取到的食谱数据结构: {list(recipe_data.keys())}")
          
            # 验证食谱数据
            self._validate_recipe_data(recipe_data)
            
            logger.info(f"食谱生成成功，标题: {recipe_data.get('title', '未命名')}")
            return recipe_data
            
        except json.JSONDecodeError as e:
            # 如果响应不是有效的JSON，记录原始响应并抛出异常
            raw_content = response.text if hasattr(response, 'text') else str(response)
            logger.error(f"Invalid JSON response from AI API: {raw_content[:300]}...")
            raise InvalidResponseError(f"AI API returned invalid JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating recipe: {str(e)}", exc_info=True)
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
            
            # 使用统一的解析方法处理响应
            return self._parse_response(response)
            
        except Exception as e:
            logger.error(f"Error enhancing recipe: {str(e)}")
            if isinstance(e, AIServiceError):
                raise
            raise AIServiceError(f"Failed to enhance recipe: {str(e)}")


    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析API响应
        
        Args:
            response: API响应
        
        Returns:
            解析后的响应
        
        Raises:
            InvalidResponseError: 无效响应错误
        """
        logger.info(f"开始解析{self.api_provider} API响应")
        logger.info(f"原始响应内容预览: {str(response)[:300]}...")
        
        # 获取响应内容
        if self.api_provider == "alipan":
            # 通义千问响应格式
            content = response.get("output", {}).get("text", "")
            logger.info(f"通义千问响应解析: output存在={bool(response.get('output'))}, text长度={len(content)} 字符")
        else:
            # OpenAI响应格式
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            logger.info(f"OpenAI响应解析: choices数量={len(response.get('choices', []))}, text长度={len(content)} 字符")
        
        if not content:
            logger.error("AI API返回空响应")
            raise InvalidResponseError("Empty response from AI API")
        
        logger.info(f"原始AI响应内容: {content[:200]}...")  # 只记录前200个字符
        
        # 尝试提取JSON部分（如果响应包含额外文本）
        try:
            # 尝试直接解析
            logger.info("尝试直接解析JSON格式")
            result = json.loads(content)
            logger.info(f"JSON解析成功，数据结构: {list(result.keys())}")
            return result
        except json.JSONDecodeError:
            # 尝试提取JSON格式的部分
            logger.warning("直接解析失败，尝试提取JSON部分")
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                logger.info(f"提取JSON成功，数据结构: {list(result.keys())}")
                return result
            else:
                logger.error(f"响应内容不是有效的JSON格式: {content[:100]}...")
                raise InvalidResponseError("Could not find valid JSON in AI response")
    
    def _validate_recipe_data(self, recipe_data: Dict[str, Any]) -> bool:
        """
        验证食谱数据是否包含所有必需字段
        
        Args:
            recipe_data: 食谱数据
        
        Returns:
            是否有效
        
        Raises:
            InvalidResponseError: 无效响应错误
        """
        logger.info("开始验证食谱数据结构")
        logger.info(f"食谱数据包含的字段: {list(recipe_data.keys())}")
        
        # 必需字段
        required_fields = ["title", "ingredients", "instructions"]
        
        # 检查是否包含所有必需字段
        missing_fields = [field for field in required_fields if field not in recipe_data]
        if missing_fields:
            logger.error(f"食谱数据缺少必需字段: {', '.join(missing_fields)}")
            raise InvalidResponseError(f"Missing required recipe fields: {', '.join(missing_fields)}")
        
        logger.info("所有必需字段均存在")
        
        # 检查字段类型
        if not isinstance(recipe_data["title"], str):
            logger.error(f"字段'title'类型错误，应为字符串，实际为: {type(recipe_data['title']).__name__}")
            raise InvalidResponseError("Field 'title' must be a string")
        logger.info(f"字段'title'验证通过，内容: {recipe_data['title'][:50]}...")
        
        if not isinstance(recipe_data["ingredients"], list):
            logger.error(f"字段'ingredients'类型错误，应为列表，实际为: {type(recipe_data['ingredients']).__name__}")
            raise InvalidResponseError("Field 'ingredients' must be a list")
        logger.info(f"字段'ingredients'验证通过，包含 {len(recipe_data['ingredients'])} 个食材")
        
        if not isinstance(recipe_data["instructions"], list):
            logger.error(f"字段'instructions'类型错误，应为列表，实际为: {type(recipe_data['instructions']).__name__}")
            raise InvalidResponseError("Field 'instructions' must be a list")
        logger.info(f"字段'instructions'验证通过，包含 {len(recipe_data['instructions'])} 个步骤")
        
        logger.info("食谱数据验证完成，所有必需字段和类型检查均通过")
        return True

# 创建全局AI客户端实例
ai_client = AIClient()