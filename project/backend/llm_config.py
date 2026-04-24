"""
LLM 配置模块
支持本地模型（Ollama、llama.cpp）和云端模型（OpenAI、国产API）
"""
import os
import json
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import time

# 尝试导入 langchain 相关库
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

# 尝试导入 requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class LLMProvider(Enum):
    """LLM提供商枚举"""
    OLLAMA = "ollama"          # 本地模型（推荐）
    LLAMACPP = "llamacpp"      # llama.cpp
    OPENAI = "openai"          # OpenAI GPT
    DASHSCOPE = "dashscope"    # 阿里通义千问
    ERNIE = "ernie"            # 百度文心
    MOONSHOT = "moonshot"      # 月之暗面 Kimi

@dataclass
class LLMConfig:
    """LLM配置"""
    provider: LLMProvider
    model_name: str
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = False
    timeout: int = 60

class LLMManager:
    """LLM管理器"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        初始化LLM管理器
        
        Args:
            config: LLM配置，如果为None则从环境变量加载
        """
        self.config = config or self._load_config_from_env()
        self._initialize_client()
    
    def _load_config_from_env(self) -> LLMConfig:
        """从环境变量加载配置"""
        provider_str = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        # 解析 provider
        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            print(f"未知的 LLM provider: {provider_str}，使用 ollama")
            provider = LLMProvider.OLLAMA
        
        # 根据 provider 确定默认模型
        default_model = {
            LLMProvider.OLLAMA: "qwen2:7b",
            LLMProvider.LLAMACPP: "qwen2-7b-instruct-q4_k_m.gguf",
            LLMProvider.OPENAI: "gpt-4-turbo",
            LLMProvider.DASHSCOPE: "qwen-max",
            LLMProvider.ERNIE: "ernie-4.0",
            LLMProvider.MOONSHOT: "moonshot-v1-8k"
        }.get(provider, "qwen2:7b")
        
        return LLMConfig(
            provider=provider,
            model_name=os.getenv("LLM_MODEL", default_model),
            api_key=os.getenv(f"{provider_str.upper()}_API_KEY"),
            api_base=os.getenv(f"{provider_str.upper()}_API_BASE"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
            stream=os.getenv("LLM_STREAM", "false").lower() == "true",
            timeout=int(os.getenv("LLM_TIMEOUT", "60"))
        )
    
    def _initialize_client(self):
        """初始化 LLM 客户端"""
        if self.config.provider == LLMProvider.OLLAMA:
            # Ollama 配置
            self.api_base = self.config.api_base or "http://localhost:11434"
            print(f"✅ 使用 Ollama 本地模型: {self.config.model_name}")
            print(f"   Ollama API 地址: {self.api_base}")
            
        elif self.config.provider == LLMProvider.LLAMACPP:
            # llama.cpp 配置
            self.api_base = self.config.api_base or "http://localhost:8080"
            print(f"✅ 使用 llama.cpp 本地模型: {self.config.model_name}")
            print(f"   llama.cpp API 地址: {self.api_base}")
            
        elif self.config.provider == LLMProvider.OPENAI:
            if not LANGCHAIN_AVAILABLE:
                raise ImportError("需要安装 langchain: pip install langchain openai")
            self._openai_client = ChatOpenAI(
                model=self.config.model_name,
                api_key=self.config.api_key,
                base_url=self.config.api_base,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                streaming=self.config.stream
            )
            print(f"✅ 使用 OpenAI API: {self.config.model_name}")
            
        elif self.config.provider == LLMProvider.DASHSCOPE:
            self.api_base = self.config.api_base or "https://dashscope.aliyuncs.com/api/v1"
            print(f"✅ 使用阿里通义千问: {self.config.model_name}")
            
        elif self.config.provider == LLMProvider.ERNIE:
            print(f"✅ 使用百度文心一言: {self.config.model_name}")
            
        elif self.config.provider == LLMProvider.MOONSHOT:
            self.api_base = self.config.api_base or "https://api.moonshot.cn/v1"
            print(f"✅ 使用月之暗面 Kimi: {self.config.model_name}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        对话接口
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            **kwargs: 其他参数
        
        Returns:
            LLM 响应内容
        """
        # 重试逻辑
        max_retries = kwargs.get("max_retries", 3)
        
        for attempt in range(max_retries):
            try:
                if self.config.provider == LLMProvider.OLLAMA:
                    return self._chat_ollama(messages, **kwargs)
                elif self.config.provider == LLMProvider.LLAMACPP:
                    return self._chat_llamacpp(messages, **kwargs)
                elif self.config.provider == LLMProvider.OPENAI:
                    return self._chat_openai(messages, **kwargs)
                elif self.config.provider == LLMProvider.DASHSCOPE:
                    return self._chat_dashscope(messages, **kwargs)
                elif self.config.provider == LLMProvider.ERNIE:
                    return self._chat_ernie(messages, **kwargs)
                elif self.config.provider == LLMProvider.MOONSHOT:
                    return self._chat_moonshot(messages, **kwargs)
                else:
                    raise ValueError(f"不支持的 provider: {self.config.provider}")
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ LLM 调用失败 (已重试 {max_retries} 次): {str(e)}")
                    return "抱歉，我现在无法回答您的问题，请稍后再试。"
                print(f"⚠️  LLM 调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                time.sleep(2 ** attempt)  # 指数退避
    
    def _chat_ollama(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Ollama对话实现"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("需要安装 requests: pip install requests")
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "num_predict": kwargs.get("max_tokens", self.config.max_tokens)
            }
        }
        
        response = requests.post(
            f"{self.api_base}/api/chat",
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "")
    
    def _chat_llamacpp(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """llama.cpp对话实现"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("需要安装 requests: pip install requests")
        
        # 将消息转换为提示词格式
        prompt = self._format_prompt(messages)
        
        payload = {
            "prompt": prompt,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "n_predict": kwargs.get("max_tokens", self.config.max_tokens),
            "stop": ["</s>", "Human:", "Assistant:"],
            "stream": False
        }
        
        response = requests.post(
            f"{self.api_base}/completion",
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("content", "")
    
    def _chat_openai(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """OpenAI对话实现"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("需要安装 langchain")
        
        # 转换消息格式
        lc_messages = []
        for msg in messages:
            if msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
        
        response = self._openai_client.invoke(lc_messages)
        return response.content
    
    def _chat_dashscope(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """阿里通义千问对话实现"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("需要安装 requests: pip install requests")
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "parameters": {
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens)
            }
        }
        
        response = requests.post(
            f"{self.api_base}/services/aigc/text-generation/generation",
            headers=headers,
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("output", {}).get("text", "")
    
    def _chat_ernie(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """百度文心一言对话实现（占位）"""
        # 具体实现需要百度 API
        raise NotImplementedError("文心一言 API 实现待完善")
    
    def _chat_moonshot(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """月之暗面 Kimi 对话实现"""
        if not REQUESTS_AVAILABLE:
            raise ImportError("需要安装 requests: pip install requests")
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": kwargs.get("temperature", self.config.temperature),
            "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            "stream": False
        }
        
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    def _format_prompt(self, messages: List[Dict[str, str]]) -> str:
        """格式化消息为llama.cpp提示词"""
        # Qwen2 聊天格式
        formatted = ""
        for msg in messages:
            if msg["role"] == "system":
                formatted += f"<|im_start|>system\n{msg['content']}<|im_end|>\n"
            elif msg["role"] == "user":
                formatted += f"<|im_start|>user\n{msg['content']}<|im_end|>\n"
            elif msg["role"] == "assistant":
                formatted += f"<|im_start|>assistant\n{msg['content']}<|im_end|>\n"
        
        # 添加最后一个assistant开始标记
        if not formatted.endswith("<|im_start|>assistant\n"):
            formatted += "<|im_start|>assistant\n"
        
        return formatted
    
    def check_connection(self) -> bool:
        """检查LLM连接是否可用"""
        try:
            test_messages = [{"role": "user", "content": "Hi"}]
            # 使用简化请求避免token消耗
            if self.config.provider == LLMProvider.OLLAMA:
                if not REQUESTS_AVAILABLE:
                    return False
                response = requests.get(f"{self.api_base}/api/tags", timeout=5)
                return response.status_code == 200
            elif self.config.provider == LLMProvider.LLAMACPP:
                if not REQUESTS_AVAILABLE:
                    return False
                response = requests.get(f"{self.api_base}/health", timeout=5)
                return response.status_code == 200
            else:
                # 对于云服务，尝试一个简化调用
                return True
        except Exception as e:
            print(f"❌ LLM 连接检查失败: {str(e)}")
            return False

# 全局 LLM 管理器实例
_llm_manager: Optional[LLMManager] = None

def get_llm_manager() -> LLMManager:
    """获取全局LLM管理器"""
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager

def set_llm_manager(config: LLMConfig) -> None:
    """设置全局LLM管理器"""
    global _llm_manager
    _llm_manager = LLMManager(config)
