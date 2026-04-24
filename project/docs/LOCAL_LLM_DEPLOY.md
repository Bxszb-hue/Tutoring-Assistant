# 本地大模型部署指南

本指南将帮助你在本地部署大模型，无需任何API调用费用。

---

## 一、快速开始（推荐方案：Ollama）

### 1. 安装 Ollama

**Windows:**
1. 访问 https://ollama.ai/download
2. 下载并安装 Windows 版本
3. 安装完成后，重启终端/命令行

**验证安装:**
```bash
ollama --version
```

### 2. 下载并运行模型

**推荐模型（中文效果好）:**

| 模型 | 显存要求 | 下载命令 | 推荐使用场景 |
|------|---------|---------|-------------|
| Qwen2:7B | 8GB+ | `ollama run qwen2:7b` | 日常开发测试 |
| Qwen2:14B | 12GB+ | `ollama run qwen2:14b` | 生产环境，更好效果 |
| DeepSeek-V3:8B | 8GB+ | `ollama run deepseek-v3:8b` | 代码和推理场景 |
| Llama3.1:8B | 8GB+ | `ollama run llama3.1:8b` | 多语言通用 |

**第一次运行会自动下载模型:**
```bash
ollama run qwen2:7b
```

### 3. 测试模型

运行后你可以在终端直接对话：
```
>>> 你好，你是谁？
你好！我是Qwen，由阿里巴巴开发的人工智能助手。
>>>
```

输入 `/bye` 退出交互模式。

---

## 二、项目配置

### 1. 配置环境变量

复制 `.env.example` 为 `.env`：
```bash
# Windows PowerShell
cp .env.example .env
```

编辑 `.env` 文件，确保使用 Ollama 配置：
```env
# 选择 Ollama 作为提供商
LLM_PROVIDER=ollama

# 使用 Qwen2 7B 模型
LLM_MODEL=qwen2:7b

# 其他配置保持默认
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 验证 LLM 连接

在项目根目录运行：
```python
from backend.llm_config import get_llm_manager

llm = get_llm_manager()

# 测试连接
print("连接状态:", llm.check_connection())

# 测试对话
response = llm.chat([
    {"role": "user", "content": "你好！"}
])

print("AI 回复:", response)
```

---

## 三、高级选项：使用 llama.cpp（性能更好）

如果需要更好的性能，可以使用 llama.cpp。

### 1. 编译 llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# Windows 使用 CMake
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

### 2. 下载 GGUF 模型

从以下渠道下载 GGUF 格式的模型：
- ModelScope (推荐国内使用): https://modelscope.cn/models
- HuggingFace: https://huggingface.co/models

**推荐模型:**
- Qwen2-7B-Instruct-GGUF: https://modelscope.cn/models/qwen/Qwen2-7B-Instruct-GGUF

下载 `qwen2-7b-instruct-q4_k_m.gguf`（推荐）

### 3. 启动 llama.cpp 服务

```bash
cd llama.cpp

# 使用 server 模式启动
./build/bin/server -m ../qwen2-7b-instruct-q4_k_m.gguf -c 4096
```

访问 http://localhost:8080 可以看到 llama.cpp 界面。

### 4. 修改环境配置

在 `.env` 中设置：
```env
LLM_PROVIDER=llamacpp
LLAMACPP_API_BASE=http://localhost:8080
LLM_MODEL=qwen2-7b-instruct-q4_k_m.gguf
```

---

## 四、模型选择指南

### 根据显存大小选择模型

| 显存大小 | 最佳模型选择 | 推荐量化 | 预计速度 |
|---------|-------------|---------|---------|
| **8GB** | Qwen2-7B | Q4_K_M | ~15-30 tokens/s |
| **12GB** | Qwen2-14B | Q4_K_M | ~10-20 tokens/s |
| **16GB** | Qwen2-14B | Q8_0 | ~8-15 tokens/s |
| **24GB+** | Qwen2-72B | Q4_K_M | ~5-10 tokens/s |

### 常用模型列表

**Ollama 上可用的热门模型:**

```bash
# 通义千问（阿里开源，中文最佳）
ollama pull qwen2:7b
ollama pull qwen2:14b
ollama pull qwen2:72b

# DeepSeek (代码和推理强)
ollama pull deepseek-v3:8b
ollama pull deepseek-v3:32b

# Llama (Meta 开源，通用)
ollama pull llama3.1:8b
ollama pull llama3.1:70b

# 中文优化模型
ollama pull yi:6b
ollama pull yi:34b
```

---

## 五、常见问题

### Q: Ollama 下载速度慢怎么办？

**A:** 设置国内镜像：
```bash
# Windows PowerShell
$env:OLLAMA_HOST="https://mirror.sjtu.edu.cn/ollama"

# 或者手动下载模型文件放到模型目录
# Windows: C:\Users\你的用户名\.ollama\models
```

### Q: 显存不足怎么办？

**A:** 尝试以下方案：
1. 使用更小的模型（7B 代替 14B）
2. 使用更高量化程度的版本（Q3_K_M 代替 Q4_K_M）
3. 关闭其他占用显存的程序（浏览器、视频等）
4. 使用 CPU 模式运行（会慢很多，不推荐）

### Q: 如何让模型更快？

**A:** 优化建议：
1. 使用更高量化程度（Q4_K_M 足够好，速度快）
2. 减小上下文长度（4096 通常足够）
3. 使用 CUDA 加速（需要 NVIDIA 显卡）
4. 增加 `LLM_MAX_TOKENS` 不影响速度，但会影响单次输出长度

### Q: 如何切换到云端 API？

**A:** 只需修改 `.env` 配置，代码无需改动：
```env
# 例如切换到通义千问
LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=你的API密钥
LLM_MODEL=qwen-plus
```

---

## 六、下一步

配置好本地模型后，你可以：

1. **重构智能体** - 将硬编码逻辑替换为 LLM 调用
2. **优化提示词** - 为每个智能体设计专业的系统提示词
3. **添加对话历史管理** - 智能截断过长的对话历史
4. **实现工具调用** - 让 LLM 能调用数据库等工具

详细的代码示例请参考项目中的其他文档。
