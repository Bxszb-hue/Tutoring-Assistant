#!/usr/bin/env python3
"""
大模型客户端
支持多种大模型的连接和调用
"""
import os
import logging
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    """大模型客户端基类"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话"""
        pass

class DeepSeekClient(BaseLLMClient):
    """DeepSeek大模型客户端"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        if not self.api_key or self.api_key == "your-deepseek-api-key-here":
            logger.warning("DeepSeek API key not configured, using fallback mode")
            self.client = None
            return

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info("DeepSeek client initialized successfully")
        except ImportError:
            logger.warning("OpenAI package not installed, DeepSeek client will use HTTP requests")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.client:
            logger.warning("DeepSeek client not initialized, using fallback")
            return self._generate_fallback(prompt, **kwargs)
        
        try:
            logger.info(f"Calling DeepSeek API with prompt length: {len(prompt)}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            logger.info(f"DeepSeek API returned content length: {len(content)}")
            # 移除emoji表情符号（保留中文字符）
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            logger.info(f"After cleaning, content length: {len(content)}")
            return content
        except Exception as e:
            logger.error(f"DeepSeek generate error: {e}")
            return self._generate_fallback(prompt, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话"""
        if not self.client:
            return self._chat_fallback(messages, **kwargs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            # 移除emoji表情符号
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            return content
        except Exception as e:
            logger.error(f"DeepSeek chat error: {e}")
            return self._chat_fallback(messages, **kwargs)
    
    def _generate_fallback(self, prompt: str, **kwargs) -> str:
        """降级方案"""
        return f"[DeepSeek API未配置] 根据您的输入：{prompt[:50]}...，我暂时无法生成完整回答。请配置DeepSeek API密钥。"
    
    def _chat_fallback(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话降级方案"""
        last_message = messages[-1]["content"] if messages else ""
        return f"[DeepSeek API未配置] 您说：{last_message[:50]}...，我暂时无法生成完整回答。请配置DeepSeek API密钥。"

class QwenClient(BaseLLMClient):
    """通义千问大模型客户端"""
    
    def __init__(self, api_key: str, model: str = "qwen-turbo"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        if not self.api_key or self.api_key.startswith("your-"):
            logger.warning("Qwen API key not configured, using fallback mode")
            self.client = None
            return

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info("Qwen client initialized successfully")
        except ImportError:
            logger.warning("OpenAI package not installed, Qwen client will use HTTP requests")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.client:
            return self._generate_fallback(prompt, **kwargs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            # 移除emoji表情符号
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            return content
        except Exception as e:
            logger.error(f"Qwen generate error: {e}")
            return self._generate_fallback(prompt, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话"""
        if not self.client:
            return self._chat_fallback(messages, **kwargs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            # 移除emoji表情符号
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            return content
        except Exception as e:
            logger.error(f"Qwen chat error: {e}")
            return self._chat_fallback(messages, **kwargs)
    
    def _generate_fallback(self, prompt: str, **kwargs) -> str:
        """降级方案"""
        return f"[Qwen API未配置] 根据您的输入：{prompt[:50]}...，我暂时无法生成完整回答。请配置Qwen API密钥。"
    
    def _chat_fallback(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话降级方案"""
        last_message = messages[-1]["content"] if messages else ""
        return f"[Qwen API未配置] 您说：{last_message[:50]}...，我暂时无法生成完整回答。请配置Qwen API密钥。"

class OpenAIClient(BaseLLMClient):
    """OpenAI大模型客户端"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """初始化客户端"""
        if not self.api_key or self.api_key.startswith("your-"):
            logger.warning("OpenAI API key not configured, using fallback mode")
            self.client = None
            return

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI client initialized successfully")
        except ImportError:
            logger.warning("OpenAI package not installed")
            self.client = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        if not self.client:
            return self._generate_fallback(prompt, **kwargs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            # 移除emoji表情符号
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            return content
        except Exception as e:
            logger.error(f"OpenAI generate error: {e}")
            return self._generate_fallback(prompt, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话"""
        if not self.client:
            return self._chat_fallback(messages, **kwargs)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                stream=False
            )
            content = response.choices[0].message.content
            # 移除emoji表情符号
            content = ''.join(c for c in content if not (0x1F600 <= ord(c) <= 0x1F64F) and not (0x1F300 <= ord(c) <= 0x1F5FF) and not (0x1F680 <= ord(c) <= 0x1F6FF) and not (0x2600 <= ord(c) <= 0x26FF) and not (0x2700 <= ord(c) <= 0x27BF))
            return content
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            return self._chat_fallback(messages, **kwargs)
    
    def _generate_fallback(self, prompt: str, **kwargs) -> str:
        """降级方案"""
        return f"[OpenAI API未配置] 根据您的输入：{prompt[:50]}...，我暂时无法生成完整回答。请配置OpenAI API密钥。"
    
    def _chat_fallback(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """对话降级方案"""
        last_message = messages[-1]["content"] if messages else ""
        return f"[OpenAI API未配置] 您说：{last_message[:50]}...，我暂时无法生成完整回答。请配置OpenAI API密钥。"

class LLMFactory:
    """大模型工厂类"""
    
    _clients: Dict[str, BaseLLMClient] = {}
    
    @classmethod
    def get_client(cls, provider: str = None, api_key: str = None, **kwargs) -> BaseLLMClient:
        """
        获取大模型客户端
        
        Args:
            provider: 模型提供商 (deepseek, qwen, openai)
            api_key: API密钥
            **kwargs: 其他参数
        
        Returns:
            BaseLLMClient: 大模型客户端实例
        """
        # 如果已存在，直接返回
        if provider in cls._clients:
            return cls._clients[provider]
        
        # 根据provider创建客户端
        if provider == "deepseek":
            api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("LLM_API_KEY")
            model = kwargs.get("model", "deepseek-chat")
            base_url = kwargs.get("base_url", "https://api.deepseek.com")
            client = DeepSeekClient(api_key=api_key, model=model, base_url=base_url)
        elif provider == "qwen":
            api_key = api_key or os.getenv("DASHSCOPE_API_KEY") or os.getenv("LLM_API_KEY")
            model = kwargs.get("model", "qwen-turbo")
            client = QwenClient(api_key=api_key, model=model)
        elif provider == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            model = kwargs.get("model", "gpt-4o-mini")
            client = OpenAIClient(api_key=api_key, model=model)
        else:
            # 默认使用DeepSeek
            api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("LLM_API_KEY")
            model = kwargs.get("model", "deepseek-chat")
            base_url = kwargs.get("base_url", "https://api.deepseek.com")
            client = DeepSeekClient(api_key=api_key, model=model, base_url=base_url)
        
        # 缓存客户端
        cls._clients[provider or "default"] = client
        return client
    
    @classmethod
    def create_completion(cls, prompt: str, provider: str = None, **kwargs) -> str:
        """创建文本补全"""
        client = cls.get_client(provider)
        return client.generate(prompt, **kwargs)
    
    @classmethod
    def create_chat(cls, messages: List[Dict[str, str]], provider: str = None, **kwargs) -> str:
        """创建对话"""
        client = cls.get_client(provider)
        return client.chat(messages, **kwargs)
    
    @classmethod
    def reset(cls):
        """重置所有客户端"""
        cls._clients = {}

# 全局函数
def get_llm_client(provider: str = None) -> BaseLLMClient:
    """获取大模型客户端"""
    return LLMFactory.get_client(provider)

def llm_complete(prompt: str, provider: str = None, **kwargs) -> str:
    """文本补全"""
    return LLMFactory.create_completion(prompt, provider, **kwargs)

def llm_chat(messages: List[Dict[str, str]], provider: str = None, **kwargs) -> str:
    """对话"""
    return LLMFactory.create_chat(messages, provider, **kwargs)
