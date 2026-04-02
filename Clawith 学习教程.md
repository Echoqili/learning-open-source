# 🦞 Clawith 学习教程

> 基于 Clawith 项目的多智能体协作平台完整学习路径

---

## 📚 目录

- [模块一：AI 大模型基础认知](#模块一 ai 大模型基础认知)
- [模块二：Spring AI 实战](#模块二 spring-ai 实战)
- [模块三：Prompt 工程实战](#模块三 prompt 工程实战)
- [模块四：LangChain4j 核心框架](#模块四 langchain4j 核心框架)
- [模块五：RAG 检索增强生成](#模块五 rag 检索增强生成)
- [模块六：Agent 系统开发](#模块六 agent 系统开发)
- [模块七：MCP 协议开发](#模块七 mcp 协议开发)
- [模块八：A2A 协议与 Agent Skill](#模块八 a2a 协议与 agent-skill)
- [模块九：AgentScope 多 Agent 框架](#模块九 agentscope 多 agent 框架)
- [模块十：Vibe Coding](#模块十 vibe-coding)
- [模块十一：生产级工程实践](#模块十一生产级工程实践)
- [项目实战](#项目实战)

---

## 模块一：AI 大模型基础认知

### 学习目标
- 理解大模型的工作原理和核心概念
- 掌握大模型选型方法
- 完成开发环境搭建

### 理论内容

#### 1.1 大模型原理
- Transformer 架构基础
- 预训练与微调
- Token 与上下文窗口
- 温度值与采样策略

#### 1.2 核心概念
- **LLM Provider**: OpenAI, Anthropic, 智谱，通义千问等
- **API 调用模式**: RESTful API, Streaming
- **Token 计费**: 输入/输出 Token 计算
- **上下文管理**: 对话历史、系统提示词

#### 1.3 选型指南
| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 通用对话 | GPT-4o / Claude-3.5 | 综合能力强 |
| 代码生成 | Claude-3.5-Sonnet | 代码能力突出 |
| 中文场景 | 通义千问 / Kimi | 中文优化好 |
| 成本控制 | GPT-3.5-Turbo | 性价比高 |

### Clawith 实践

#### 1.4 开发环境搭建

**步骤 1: 克隆项目**
```bash
git clone https://github.com/dataelement/Clawith.git
cd Clawith
```

**步骤 2: 一键安装**
```bash
# 生产/测试环境
bash setup.sh

# 开发环境（包含测试工具）
bash setup.sh --dev
```

**步骤 3: 配置 LLM API**
编辑 `.env` 文件：
```bash
# OpenAI
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key
LLM_MODEL=gpt-4o

# 或使用国内模型
LLM_PROVIDER=deepseek
LLM_API_KEY=your-deepseek-key
LLM_MODEL=deepseek-chat
```

**步骤 4: 启动服务**
```bash
bash restart.sh
# 前端：http://localhost:3008
# 后端：http://localhost:8008
```

#### 1.5 Clawith 中的 LLM 配置管理

查看后端配置：[backend/app/config.py](file:///d:/pyworkplace/github/Clawith/backend/app/config.py)

```python
# 关键配置项
LLM_PROVIDER: str = "openai"
LLM_API_KEY: str
LLM_MODEL: str = "gpt-4o"
LLM_BASE_URL: Optional[str] = None  # 自定义 API 端点
```

**企业级模型池管理**：
- 支持多模型配置
- 按 Agent 分配不同模型
- 主备模型自动切换

### 实践任务
1. ✅ 完成 Clawith 本地部署
2. ✅ 配置至少一个 LLM Provider
3. ✅ 创建一个简单的 Agent 并测试对话

---

## 模块二：Spring AI 实战

> **说明**: Clawith 使用 FastAPI (Python)，但 Spring AI 的设计理念相通

### 学习目标
- 理解 AI 应用的核心组件
- 掌握对话管理、记忆机制
- 实现流式输出和多模态

### 核心概念映射

| Spring AI | Clawith (FastAPI) | 说明 |
|-----------|------------------|------|
| ChatClient | LLM Service | LLM 调用封装 |
| Prompt | System/User Message | 提示词管理 |
| Memory | Agent Memory | 对话记忆 |
| Streaming | WebSocket | 流式输出 |
| Multi-modal | Image/File Upload | 多模态支持 |

### Clawith 实践

#### 2.1 ChatClient 模式 - LLM 服务封装

查看实现：[backend/app/services/llm_service.py](file:///d:/pyworkplace/github/Clawith/backend/app/services/llm_service.py)

```python
class LLMService:
    """统一的 LLM 调用服务"""
    
    async def chat(
        self,
        messages: List[Message],
        model: str,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Union[ChatResponse, AsyncGenerator]:
        """发送对话请求"""
        # 1. 构建 API 请求
        # 2. 处理认证
        # 3. 调用 LLM API
        # 4. 解析响应
```

**关键特性**：
- 统一不同 Provider 的 API 差异
- 自动重试和错误处理
- Token 使用统计

#### 2.2 Prompt 管理

**系统提示词结构**：
```python
system_prompt = f"""你是{agent.name}，{agent.role_description}。

## 你的身份
{agent.soul.personality}

## 你的能力
- 可用的工具：{tool_list}
- 工作空间：{workspace_path}

## 行为准则
{agent.boundaries}
"""
```

**动态构建 Prompt**：
- 根据 Agent 角色定制
- 注入可用工具列表
- 包含上下文记忆

#### 2.3 Memory 对话记忆

**记忆类型**：
1. **短期记忆**: 当前对话历史
2. **长期记忆**: `memory.md` 文件持久化
3. **工作记忆**: Focus Items（关注点）

**记忆管理策略**：
```python
# 对话历史截断
def truncate_history(messages, max_tokens=4000):
    """保持上下文在 Token 限制内"""
    while count_tokens(messages) > max_tokens:
        # 移除最早的对话
        messages.pop(0)
```

#### 2.4 流式输出

**WebSocket 实时推送**：
```python
@app.websocket("/ws/{agent_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: int):
    await websocket.accept()
    
    async for chunk in llm_service.stream_chat(messages):
        # 实时推送每个 token
        await websocket.send_json({
            "type": "token",
            "content": chunk
        })
```

**前端流式渲染**：
```typescript
// 使用 TanStack Query 订阅 WebSocket
const { data } = useWebSocket(`/ws/${agentId}`, {
  onMessage: (event) => {
    if (event.type === 'token') {
      setStreamingContent(prev => prev + event.content);
    }
  }
});
```

#### 2.5 多模态支持

**图片上传与识别**：
```python
# 上传图片
POST /api/files/upload
Content-Type: multipart/form-data

# 在对话中引用图片
{
  "content": "分析这张图片",
  "image_urls": ["https://.../image.png"]
}
```

**文件处理**：
- PDF 解析：`pdfplumber`
- Word 文档：`python-docx`
- Excel 表格：`openpyxl`
- PPT 演示：`python-pptx`

### 实践任务
1. ✅ 实现一个自定义的 LLM Provider 适配器
2. ✅ 为 Agent 添加长期记忆功能
3. ✅ 测试流式对话体验
4. ✅ 实现图片上传和识别功能

---

## 模块三：Prompt 工程实战

### 学习目标
- 掌握 Prompt 设计原则
- 实现结构化输出
- 动态构建 Prompt

### 3.1 Prompt 设计原则

#### CLEAR 原则
- **Concise**: 简洁清晰，避免冗余
- **Logical**: 逻辑结构化
- **Explicit**: 明确具体
- **Adaptive**: 适应场景
- **Robust**: 抗干扰

#### Clawith 中的最佳实践

**1. 角色定义**：
```markdown
你是 {name}，{role_description}。

## 核心职责
- 职责 1
- 职责 2

## 行为边界
- 可以做的：...
- 不能做的：...
```

**2. 上下文注入**：
```markdown
## 当前任务
{current_task}

## 历史对话摘要
{memory_summary}

## 可用工具
{tools_with_schemas}
```

**3. 输出格式规范**：
```markdown
请按以下 JSON 格式输出：
{
  "thought": "你的思考过程",
  "action": "工具名称",
  "parameters": {...}
}
```

### 3.2 结构化输出

**使用 Pydantic 定义输出 Schema**：
```python
from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    thought: str = Field(description="推理过程")
    tool_name: str = Field(description="工具名称")
    parameters: dict = Field(description="工具参数")
    confidence: float = Field(ge=0, le=1, description="置信度")
```

**在 Prompt 中指定格式**：
```python
prompt = f"""
{context}

请严格按照以下 JSON Schema 输出：
{ToolCall.model_json_schema()}

示例：
{example_json}
"""
```

### 3.3 动态构建 Prompt

**根据场景动态组装**：
```python
class PromptBuilder:
    def __init__(self, agent):
        self.agent = agent
        self.components = []
    
    def add_system_role(self):
        self.components.append(self._build_system_prompt())
        return self
    
    def add_context(self, messages):
        self.components.append(self._format_context(messages))
        return self
    
    def add_tools(self, tools):
        self.components.append(self._format_tools(tools))
        return self
    
    def add_memory(self, memory_items):
        self.components.append(self._inject_memory(memory_items))
        return self
    
    def build(self):
        return "\n\n".join(self.components)
```

### 3.4 Few-Shot Learning

**在 Prompt 中提供示例**：
```markdown
## 示例 1
用户：查询今天的天气
助手：{"action": "weather_query", "params": {"date": "today"}}

## 示例 2
用户：帮我写一封邮件
助手：{"action": "email_compose", "params": {"subject": "...", "body": "..."}}

## 现在请处理：
用户：{user_input}
```

### 实践任务
1. ✅ 为 Clawith Agent 设计一个完整的系统 Prompt
2. ✅ 实现结构化输出的 JSON Schema
3. ✅ 创建一个 Prompt 模板库（至少 5 个场景）
4. ✅ 测试不同 Prompt 对输出质量的影响

---

## 模块四：LangChain4j 核心框架

> **说明**: 对应 Clawith 中的 Agent 核心框架

### 学习目标
- 理解 AI Service 架构
- 掌握对话记忆管理
- 实现 Tool 工具调用

### 4.1 AI Service 架构

**Clawith 的 Agent 服务层**：

```
┌─────────────────────────────────────┐
│         Agent Service Layer          │
├─────────────────────────────────────┤
│  Agent Orchestrator (编排器)         │
│  ├─ Message Router                  │
│  ├─ Tool Executor                   │
│  └─ Response Generator              │
├─────────────────────────────────────┤
│  Memory Manager (记忆管理)           │
│  ├─ Short-term (对话历史)            │
│  ├─ Long-term (memory.md)           │
│  └─ Focus Items (工作记忆)          │
├─────────────────────────────────────┤
│  Tool Registry (工具注册)            │
│  ├─ Built-in Tools                  │
│  ├─ MCP Tools                       │
│  └─ Custom Skills                   │
└─────────────────────────────────────┘
```

### 4.2 对话记忆实现

**记忆层级**：

```python
class AgentMemory:
    """Agent 记忆系统"""
    
    async def add_short_term(self, message: Message):
        """添加到短期记忆（对话历史）"""
        self.conversation_history.append(message)
    
    async def add_long_term(self, insight: str):
        """提炼并添加到长期记忆"""
        # 1. 使用 LLM 提炼关键信息
        # 2. 追加到 memory.md
        # 3. 定期合并相似记忆
    
    async def get_focus_items(self) -> List[FocusItem]:
        """获取当前关注点"""
        # Focus Items 是结构化的工作记忆
        # [ ] 待办  [/] 进行中  [x] 已完成
```

**Focus Items 管理**：
```python
class FocusItem(BaseModel):
    id: str
    title: str
    status: Literal["pending", "in_progress", "completed"]
    created_at: datetime
    related_trigger_id: Optional[int] = None
```

### 4.3 Tool 工具调用

#### 工具定义规范

```python
from pydantic import BaseModel, Field

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict  # JSON Schema
    handler: Callable  # 处理函数

# 示例：搜索工具
search_tool = ToolDefinition(
    name="web_search",
    description="搜索互联网获取最新信息",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "num_results": {"type": "integer", "description": "返回结果数", "default": 5}
        },
        "required": ["query"]
    },
    handler=jina_search
)
```

#### 工具执行流程

```python
async def execute_tool(agent, tool_name: str, params: dict):
    """执行工具调用"""
    # 1. 从注册表获取工具定义
    tool = tool_registry.get(tool_name)
    
    # 2. 参数验证
    validated_params = validate_parameters(tool.parameters, params)
    
    # 3. 执行工具
    try:
        result = await tool.handler(**validated_params)
        
        # 4. 记录活动日志
        await log_tool_execution(agent.id, tool_name, params, result)
        
        # 5. 检查是否需要审批
        if tool.requires_approval:
            await request_approval(agent.creator_id, tool_name, params)
        
        return result
        
    except Exception as e:
        # 6. 错误处理
        await handle_tool_error(agent.id, tool_name, e)
        raise
```

#### 内置工具列表

Clawith 提供的内置工具：

| 工具 | 描述 | 配置 |
|------|------|------|
| `web_search` | 网络搜索 | Jina AI |
| `web_read` | 网页转 Markdown | Jina AI |
| `file_read` | 读取文件 | 本地文件系统 |
| `file_write` | 写入文件 | 本地文件系统 |
| `code_execute` | 代码执行 | Docker 沙箱 |
| `send_email` | 发送邮件 | IMAP/SMTP |
| `send_message_to_agent` | Agent 间通信 | 内部 API |

### 4.4 ReAct 模式实现

**ReAct (Reasoning + Acting)**：

```python
async def agent_loop(user_input: str):
    """Agent 执行循环"""
    messages = [SystemMessage(system_prompt), UserMessage(user_input)]
    
    max_iterations = 10
    for i in range(max_iterations):
        # 1. 调用 LLM
        response = await llm.chat(messages)
        
        # 2. 解析响应
        if is_final_answer(response):
            return response.content
        
        # 3. 提取工具调用
        tool_call = parse_tool_call(response)
        
        # 4. 执行工具
        tool_result = await execute_tool(tool_call)
        
        # 5. 将结果添加到对话历史
        messages.extend([
            AssistantMessage(response.content),
            ToolMessage(tool_call, tool_result)
        ])
    
    raise Exception("超过最大迭代次数")
```

### 实践任务
1. ✅ 实现一个自定义 Tool（如天气查询）
2. ✅ 为 Agent 添加 Focus Items 管理
3. ✅ 实现完整的 ReAct 执行循环
4. ✅ 测试工具调用的错误处理

---

## 模块五：RAG 检索增强生成

### 学习目标
- 理解向量数据库原理
- 掌握文档处理方法
- 构建知识库并优化效果

### 5.1 向量数据库

**Clawith 的知识库架构**：

```
┌──────────────────────────────────────┐
│         Enterprise Knowledge Base     │
├──────────────────────────────────────┤
│  Document Processing Pipeline          │
│  ├─ PDF/DOCX/XLSX 解析                │
│  ├─ 文本分块 (Chunking)               │
│  └─ 向量化 (Embedding)                │
├──────────────────────────────────────┤
│  Vector Store                          │
│  ├─ PostgreSQL (pgvector)             │
│  └─ 可选：Redis / Milvus              │
├──────────────────────────────────────┤
│  Retrieval Engine                      │
│  ├─ 语义检索                          │
│  ├─ 关键词检索                        │
│  └─ 混合检索 + Rerank                 │
└──────────────────────────────────────┘
```

### 5.2 文档处理

#### 文档解析

```python
from parsers import parse_pdf, parse_docx, parse_txt

async def parse_document(file_path: str) -> str:
    """统一文档解析接口"""
    if file_path.endswith('.pdf'):
        return await parse_pdf(file_path)
    elif file_path.endswith('.docx'):
        return await parse_docx(file_path)
    elif file_path.endswith('.txt'):
        return await parse_txt(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{file_path}")
```

#### 文本分块策略

```python
def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: List[str] = None
) -> List[str]:
    """智能分块"""
    separators = separators or ["\n\n", "\n", "。", "！", "？", ".", "!", "?"]
    
    chunks = []
    start = 0
    while start < len(text):
        # 找到合适的分割点
        end = start + chunk_size
        if end < len(text):
            # 在分隔符处截断
            for sep in separators:
                sep_pos = text.rfind(sep, start, end)
                if sep_pos > start:
                    end = sep_pos + len(sep)
                    break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - chunk_overlap
    
    return chunks
```

### 5.3 向量化与存储

#### Embedding 模型选择

| 模型 | 维度 | 语言 | 场景 |
|------|------|------|------|
| text-embedding-3-small | 1536 | 多语言 | 通用 |
| bge-large-zh | 1024 | 中文 | 中文优化 |
| m3e-base | 768 | 中文 | 轻量级 |

#### 向量存储实现

```python
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import VECTOR

class KnowledgeChunk(Base):
    """知识库向量存储"""
    __tablename__ = "knowledge_chunks"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, nullable=False)
    document_id = Column(Integer)
    content = Column(Text)
    embedding = Column(VECTOR(1536))  # pgvector
    metadata = Column(JSON)
    
    @classmethod
    async def search(cls, query_embedding, tenant_id, top_k=5):
        """语义检索"""
        # 使用余弦相似度
        similarity = cls.embedding.cosine_distance(query_embedding)
        
        results = await db.execute(
            select(cls, similarity.label("score"))
            .where(cls.tenant_id == tenant_id)
            .order_by(similarity)
            .limit(top_k)
        )
        return results.all()
```

### 5.4 检索增强生成

#### RAG 流程

```python
async def rag_query(agent_id: int, query: str) -> str:
    """RAG 检索增强查询"""
    # 1. 生成查询向量
    query_embedding = await embedding_model.encode(query)
    
    # 2. 检索相关文档
    chunks = await KnowledgeChunk.search(
        query_embedding,
        tenant_id=agent.tenant_id,
        top_k=5
    )
    
    # 3. 构建增强 Prompt
    context = "\n\n".join([chunk.content for chunk in chunks])
    
    prompt = f"""基于以下参考资料回答问题：

## 参考资料
{context}

## 问题
{query}

请根据参考资料提供准确的回答。如果资料中没有相关信息，请说明。
"""
    
    # 4. 调用 LLM 生成回答
    response = await llm.chat([UserMessage(prompt)])
    return response.content
```

#### 混合检索优化

```python
async def hybrid_search(query: str, top_k: int = 10) -> List[Chunk]:
    """混合检索：语义 + 关键词"""
    # 1. 语义检索
    embedding = await encode(query)
    semantic_results = await vector_search(embedding, top_k=top_k * 2)
    
    # 2. 关键词检索 (BM25)
    keyword_results = await bm25_search(query, top_k=top_k * 2)
    
    # 3. 合并结果 (RRF - Reciprocal Rank Fusion)
    merged = rrf_fusion(semantic_results, keyword_results, k=60)
    
    # 4. 重排序 (可选)
    if USE_RERANKER:
        merged = await rerank(query, merged, top_k=top_k)
    
    return merged[:top_k]
```

### 5.5 效果优化技巧

1. **分块大小调优**: 根据文档类型调整 chunk_size
2. **元数据过滤**: 按文档类型、时间范围等过滤
3. **查询重写**: 使用 LLM 优化用户查询
4. **结果重排序**: 使用 Cross-Encoder 精排
5. **缓存策略**: 对热门查询缓存结果

### 实践任务
1. ✅ 实现文档解析和分块功能
2. ✅ 搭建向量数据库（使用 pgvector）
3. ✅ 完成 RAG 检索流程
4. ✅ 测试不同分块策略的效果

---

## 模块六：Agent 系统开发

### 学习目标
- 理解 ReAct 框架
- 实现业务 Agent
- 掌握多 Agent 协作

### 6.1 ReAct 框架详解

**ReAct 核心循环**：

```
┌─────────────┐
│   Thought   │  分析当前状态，推理下一步
└────────────┘
       │
       v
┌─────────────┐
│   Action    │  选择并执行工具
└──────┬──────┘
       │
       v
┌─────────────┐
│  Observation│  观察工具执行结果
└────────────┘
       │
       v
    循环直到得出结论
```

**Clawith 中的实现**：

```python
async def react_agent_loop(agent, user_message: str):
    """ReAct Agent 执行循环"""
    
    # 初始化对话历史
    messages = build_initial_messages(agent, user_message)
    
    # 创建 Focus Item
    focus = await FocusItem.create(
        title=f"处理：{user_message[:50]}...",
        status="in_progress"
    )
    
    max_turns = 15
    for turn in range(max_turns):
        # 1. 思考 (Thought)
        prompt = build_react_prompt(agent, messages, focus)
        response = await llm.chat(messages + [UserMessage(prompt)])
        
        # 2. 解析响应
        if has_final_answer(response):
            # 完成任务
            await focus.update(status="completed")
            return extract_answer(response)
        
        # 3. 行动 (Action)
        tool_call = parse_tool_call(response)
        trigger_id = await Trigger.create(
            agent_id=agent.id,
            type="once",
            action=tool_call,
            focus_item_id=focus.id
        )
        
        # 4. 执行工具
        result = await execute_tool_with_trigger(agent, tool_call, trigger_id)
        
        # 5. 观察 (Observation)
        messages.extend([
            AssistantMessage(response.content),
            ToolMessage(tool_call, result)
        ])
        
        # 6. 记录内心独白
        await Monologue.create(
            agent_id=agent.id,
            content=response.thought,
            tool_call=tool_call,
            result=result
        )
    
    raise TimeoutError("Agent 执行超时")
```

### 6.2 业务 Agent 实现

#### Agent 类型

**1. 客服 Agent**：
```python
customer_service_agent = AgentConfig(
    name="小客服",
    role="处理客户咨询和投诉",
    tools=["knowledge_base_search", "ticket_create", "send_email"],
    personality="耐心、专业、友善",
    boundaries=[
        "不承诺无法实现的功能",
        "遇到技术问题升级给工程师",
        "记录所有客户反馈"
    ]
)
```

**2. 数据分析 Agent**：
```python
data_analyst_agent = AgentConfig(
    name="数据分析师",
    role="分析业务数据并生成报告",
    tools=["sql_query", "chart_generate", "report_export"],
    personality="严谨、数据驱动、善于发现规律",
    boundaries=[
        "不访问敏感数据",
        "所有查询需要审批",
        "报告需要人工审核"
    ]
)
```

**3. 研发 Agent**：
```python
dev_agent = AgentConfig(
    name="研发助手",
    role="代码审查、Bug 修复、功能开发",
    tools=["code_read", "code_write", "test_run", "git_commit"],
    personality="追求代码质量、注重细节",
    boundaries=[
        "不直接部署到生产环境",
        "重大重构需要审批",
        "所有代码需要测试覆盖"
    ]
)
```

### 6.3 多 Agent 协作

#### 组织架构

```
CEO Agent (总协调)
    │
    ├─ 产品 Agent
    │   └─ 设计 Agent
    │
    ├─ 研发 Agent
    │   ├─ 前端 Agent
    │   └─ 后端 Agent
    │
    └─ 运营 Agent
        ├─ 客服 Agent
        └─ 市场 Agent
```

#### Agent 间通信

```python
async def send_message_to_agent(
    from_agent: int,
    to_agent: int,
    content: str,
    priority: str = "normal"
):
    """Agent 发送消息"""
    # 1. 创建消息记录
    message = await Message.create(
        sender_id=from_agent,
        receiver_id=to_agent,
        content=content,
        priority=priority
    )
    
    # 2. 通知接收方 Agent
    await Notification.send(
        agent_id=to_agent,
        type="new_message",
        data={"message_id": message.id}
    )
    
    # 3. 可选：触发接收方 Agent 的自主响应
    if priority == "urgent":
        await Trigger.create(
            agent_id=to_agent,
            type="on_message",
            action="respond_to_message",
            params={"message_id": message.id}
        )
```

#### 协作模式

**1. 任务委派**：
```python
# CEO Agent 委派任务给研发 Agent
await send_message_to_agent(
    from_agent=ceo_agent.id,
    to_agent=dev_agent.id,
    content="""
    【任务委派】开发新用户注册功能
    
    需求：
    1. 支持邮箱注册
    2. 发送验证邮件
    3. 密码强度校验
    
    请在 2 小时内完成并测试
    """
)
```

**2. 信息查询**：
```python
# 运营 Agent 向数据 Agent 查询
await send_message_to_agent(
    from_agent=ops_agent.id,
    to_agent=data_agent.id,
    content="请提供上周的用户活跃数据报告"
)
```

**3. 协同决策**：
```python
# 多个 Agent 讨论方案
async def collaborative_decision(agents: List[int], topic: str):
    # 1. 创建讨论主题
    discussion = await Discussion.create(topic=topic)
    
    # 2. 邀请所有 Agent 参与
    for agent_id in agents:
        await send_message_to_agent(
            from_agent=current_agent.id,
            to_agent=agent_id,
            content=f"邀请参与讨论：{topic}"
        )
    
    # 3. 收集意见
    opinions = []
    for agent_id in agents:
        opinion = await get_agent_opinion(agent_id, topic)
        opinions.append(opinion)
    
    # 4. 汇总决策
    decision = await summarize_and_decide(opinions)
    return decision
```

### 6.4 Pulse Engine - 自主触发

**触发器类型**：

```python
class TriggerType(str, Enum):
    CRON = "cron"          # 定时执行 (如每天 9 点)
    INTERVAL = "interval"  # 固定间隔 (如每 30 分钟)
    ONCE = "once"          # 单次定时 (如 10 分钟后)
    POLL = "poll"          # HTTP 端点监控
    ON_MESSAGE = "on_message"  # 等待特定消息
    WEBHOOK = "webhook"    # 外部 HTTP 回调
```

**触发器管理**：

```python
async def set_trigger(
    agent_id: int,
    trigger_type: TriggerType,
    config: dict,
    action: str,
    focus_item_id: int
):
    """设置触发器"""
    trigger = await Trigger.create(
        agent_id=agent_id,
        type=trigger_type,
        config=config,  # 如 {"cron": "0 9 * * *"}
        action=action,
        focus_item_id=focus_item_id
    )
    return trigger

async def cancel_trigger(trigger_id: int):
    """取消触发器"""
    await Trigger.delete(trigger_id)
```

**触发器守护进程**：

```python
async def trigger_daemon():
    """后台运行，检查并触发"""
    while True:
        now = datetime.now()
        
        # 检查 CRON 触发器
        cron_triggers = await Trigger.get_due_cron(now)
        for trigger in cron_triggers:
            await execute_trigger(trigger)
        
        # 检查 INTERVAL 触发器
        interval_triggers = await Trigger.get_due_interval(now)
        for trigger in interval_triggers:
            await execute_trigger(trigger)
        
        # 检查 ONCE 触发器
        once_triggers = await Trigger.get_due_once(now)
        for trigger in once_triggers:
            await execute_trigger(trigger)
            await cancel_trigger(trigger.id)  # 单次触发后删除
        
        await asyncio.sleep(60)  # 每分钟检查一次
```

### 实践任务
1. ✅ 实现一个完整的 ReAct Agent
2. ✅ 创建 3 个不同角色的业务 Agent
3. ✅ 实现 Agent 间通信功能
4. ✅ 设置自主触发器（CRON + INTERVAL）
5. ✅ 测试多 Agent 协作场景

---

## 模块七：MCP 协议开发

### 学习目标
- 理解 MCP 协议原理
- 实现 MCP Server/Client
- 掌握 Spring AI MCP 集成

### 7.1 MCP 协议基础

**什么是 MCP (Model Context Protocol)**？

MCP 是一个标准化的协议，用于 AI 模型与外部工具/数据源的交互。它定义了：
- 工具描述规范
- 参数传递格式
- 结果返回结构
- 错误处理机制

**MCP 架构**：

```
┌─────────────────┐      MCP       ┌─────────────────┐
│   AI Agent      │ ◄────────────► │   MCP Server    │
│   (Clawith)     │   JSON-RPC     │   (Tool Provider)│
└─────────────────┘                └─────────────────┘
```

### 7.2 MCP Server 实现

#### 使用 Python 实现 MCP Server

```python
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.types as types

# 创建 MCP Server
server = Server("example-tool-server")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """返回可用工具列表"""
    return [
        types.Tool(
            name="get_weather",
            description="获取指定城市的天气",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        ),
        types.Tool(
            name="calculate",
            description="执行数学计算",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required": ["expression"]
            }
        )
    ]

@server.call_tool()
async def call_tool(
    name: str, 
    arguments: dict
) -> list[types.TextContent | types.ImageContent]:
    """执行工具调用"""
    if name == "get_weather":
        city = arguments["city"]
        # 调用天气 API
        weather_data = await fetch_weather(city)
        return [types.TextContent(text=f"{city}天气：{weather_data}")]
    
    elif name == "calculate":
        expression = arguments["expression"]
        # 安全计算
        result = safe_eval(expression)
        return [types.TextContent(text=f"计算结果：{result}")]
    
    else:
        raise ValueError(f"未知工具：{name}")

# 启动 Server
if __name__ == "__main__":
    server.run()
```

### 7.3 MCP Client 集成

#### Clawith 中的 MCP Client

```python
from mcp.client import Client
import mcp.types as types

class MCPClient:
    """MCP 客户端"""
    
    def __init__(self, server_url: str):
        self.client = Client(server_url)
        self.tools = []
    
    async def connect(self):
        """连接到 MCP Server"""
        await self.client.initialize()
        self.tools = await self.client.list_tools()
    
    async def call_tool(self, tool_name: str, args: dict) -> str:
        """调用远程工具"""
        result = await self.client.call_tool(tool_name, args)
        return self._parse_result(result)
    
    def _parse_result(self, result: list[types.Content]) -> str:
        """解析结果"""
        texts = []
        for content in result:
            if isinstance(content, types.TextContent):
                texts.append(content.text)
            elif isinstance(content, types.ImageContent):
                texts.append(f"[图片：{content.data[:50]}...]")
        return "\n".join(texts)
```

### 7.4 Smithery 集成

**Smithery** 是一个 MCP 工具市场，Clawith 支持自动发现和安装 Smithery 上的工具。

#### 工具发现

```python
async def discover_smithery_tools(query: str = None) -> List[Tool]:
    """从 Smithery 发现工具"""
    url = "https://smithery.ai/api/tools"
    if query:
        url += f"?q={query}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        tools_data = response.json()
        
        return [
            Tool(
                name=tool["name"],
                description=tool["description"],
                mcp_server=tool["server_url"],
                install_count=tool["installs"]
            )
            for tool in tools_data
        ]
```

#### 工具安装

```python
async def install_mcp_tool(agent_id: int, tool_name: str, server_url: str):
    """为 Agent 安装 MCP 工具"""
    # 1. 创建客户端连接
    client = MCPClient(server_url)
    await client.connect()
    
    # 2. 验证工具存在
    tools = await client.list_tools()
    if tool_name not in [t.name for t in tools]:
        raise ValueError(f"工具 {tool_name} 不存在")
    
    # 3. 保存到数据库
    await AgentTool.create(
        agent_id=agent_id,
        name=tool_name,
        type="mcp",
        config={"server_url": server_url},
        enabled=True
    )
    
    # 4. 更新 Agent 的工具列表
    await update_agent_tools_cache(agent_id)
```

### 7.5 ModelScope MCP 集成

**ModelScope** 是阿里的模型开放平台，也提供 MCP 工具。

```python
async def discover_modelscope_tools() -> List[Tool]:
    """从 ModelScope 发现工具"""
    url = "https://modelscope.cn/api/mcp/tools"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        tools_data = response.json()["tools"]
        
        return [
            Tool(
                name=tool["name"],
                description=tool["description"],
                mcp_server=tool["endpoint"],
                provider="ModelScope"
            )
            for tool in tools_data
        ]
```

### 7.6 自定义 MCP 工具

#### 创建自定义工具

```python
# 定义工具处理函数
async def custom_data_export_tool(format: str, output_path: str):
    """自定义数据导出工具"""
    # 1. 查询数据
    data = await db.query("SELECT * FROM ...")
    
    # 2. 格式化
    if format == "csv":
        content = format_as_csv(data)
    elif format == "json":
        content = format_as_json(data)
    else:
        raise ValueError(f"不支持的格式：{format}")
    
    # 3. 写入文件
    with open(output_path, "w") as f:
        f.write(content)
    
    return f"数据已导出到：{output_path}"

# 注册为 MCP 工具
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "data_export":
        return await custom_data_export_tool(
            format=arguments["format"],
            output_path=arguments["output_path"]
        )
```

### 7.7 Spring AI MCP 集成（参考）

虽然 Clawith 使用 Python，但 Spring AI 的 MCP 集成原理相同：

```java
// Spring AI MCP Client 配置
@Configuration
public class McpConfig {
    
    @Bean
    public McpClient mcpClient() {
        return McpClient.builder()
            .serverUrl("http://localhost:8080/mcp")
            .build();
    }
    
    @Bean
    public AgentService agentService(McpClient mcpClient) {
        return new AgentService(mcpClient);
    }
}

// 使用 MCP 工具
@Service
public class AgentService {
    
    @Autowired
    private McpClient mcpClient;
    
    public String executeTool(String toolName, Map<String, Object> args) {
        return mcpClient.callTool(toolName, args);
    }
}
```

### 实践任务
1. ✅ 实现一个简单的 MCP Server（提供 2-3 个工具）
2. ✅ 在 Clawith 中集成 MCP Client
3. ✅ 从 Smithery 安装一个现成工具
4. ✅ 创建一个自定义 MCP 工具
5. ✅ 测试 MCP 工具的调用和错误处理

---

## 模块八：A2A 协议与 Agent Skill

### 学习目标
- 理解 Agent2Agent 通信协议
- 掌握多 Agent 协作模式
- 实现 Agent Skill 系统

### 8.1 Agent2Agent 协议

**A2A (Agent to Agent)** 协议定义了 Agent 之间的标准通信方式。

#### 消息格式

```python
class A2AMessage(BaseModel):
    """A2A 消息格式"""
    id: str = Field(default_factory=generate_uuid)
    from_agent: int
    to_agent: int
    type: Literal["request", "response", "notification"]
    priority: Literal["low", "normal", "urgent"] = "normal"
    
    # 内容
    subject: str  # 主题
    content: str  # 正文
    attachments: List[Attachment] = []  # 附件
    
    # 元数据
    created_at: datetime
    expires_at: Optional[datetime] = None
    in_reply_to: Optional[str] = None  # 回复的消息 ID
    conversation_id: Optional[str] = None  # 会话 ID
```

#### 通信模式

**1. 请求 - 响应模式**：
```python
async def request_response_pattern(
    requester: int,
    responder: int,
    request: str,
    timeout: int = 300
) -> str:
    """请求 - 响应模式"""
    # 1. 发送请求
    message_id = await send_a2a_message(
        from_agent=requester,
        to_agent=responder,
        type="request",
        subject="数据查询请求",
        content=request
    )
    
    # 2. 等待响应
    response = await wait_for_response(
        message_id,
        timeout=timeout
    )
    
    if response is None:
        raise TimeoutError("等待响应超时")
    
    return response.content
```

**2. 发布 - 订阅模式**：
```python
async def publish_subscribe_pattern(
    publisher: int,
    topic: str,
    content: str,
    subscribers: List[int]
):
    """发布 - 订阅模式"""
    # 1. 发布到主题
    await publish_to_topic(
        agent_id=publisher,
        topic=topic,
        content=content
    )
    
    # 2. 通知所有订阅者
    for subscriber in subscribers:
        await send_a2a_message(
            from_agent=publisher,
            to_agent=subscriber,
            type="notification",
            subject=f"新消息：{topic}",
            content=content
        )
```

**3. 广播模式**：
```python
async def broadcast_pattern(
    sender: int,
    content: str,
    recipients: List[int]
):
    """广播模式"""
    tasks = [
        send_a2a_message(
            from_agent=sender,
            to_agent=recipient,
            type="notification",
            subject="广播通知",
            content=content
        )
        for recipient in recipients
    ]
    await asyncio.gather(*tasks)
```

### 8.2 多 Agent 协作

#### 协作场景

**场景 1: 任务链**
```python
async def task_chain_workflow():
    """任务链：产品 -> 研发 -> 测试"""
    
    # 1. 产品 Agent 设计功能
    product_result = await request_response_pattern(
        requester=current_agent.id,
        responder=product_agent.id,
        request="设计用户登录功能的需求文档"
    )
    
    # 2. 研发 Agent 实现功能
    dev_result = await request_response_pattern(
        requester=current_agent.id,
        responder=dev_agent.id,
        request=f"根据需求实现功能：{product_result.content}"
    )
    
    # 3. 测试 Agent 验证功能
    test_result = await request_response_pattern(
        requester=current_agent.id,
        responder=test_agent.id,
        request=f"测试功能：{dev_result.content}"
    )
    
    return test_result
```

**场景 2: 集体决策**
```python
async def collective_decision(agents: List[int], topic: str):
    """集体决策"""
    # 1. 发起讨论
    discussion_id = await create_discussion(topic)
    
    # 2. 收集意见
    opinions = []
    for agent in agents:
        opinion = await request_response_pattern(
            requester=current_agent.id,
            responder=agent,
            request=f"请对以下议题发表意见：{topic}"
        )
        opinions.append(opinion.content)
    
    # 3. 汇总决策
    summary = await llm.summarize(opinions)
    decision = await llm.decide(summary)
    
    # 4. 通知所有参与者
    await broadcast_pattern(
        sender=current_agent.id,
        content=f"决策结果：{decision}",
        recipients=agents
    )
    
    return decision
```

**场景 3: 知识共享**
```python
async def knowledge_sharing(teacher: int, students: List[int], topic: str):
    """知识共享"""
    # 1. 教师 Agent 准备内容
    content = await get_knowledge_content(teacher, topic)
    
    # 2. 发布到知识库
    await publish_to_knowledge_base(
        agent_id=teacher,
        topic=topic,
        content=content
    )
    
    # 3. 通知学生
    for student in students:
        await send_a2a_message(
            from_agent=teacher,
            to_agent=student,
            type="notification",
            subject=f"新知识：{topic}",
            content=content
        )
```

### 8.3 Agent Skill 系统

#### Skill 定义

```python
class AgentSkill(BaseModel):
    """Agent 技能定义"""
    id: str
    name: str
    description: str
    version: str
    
    # 技能文件
    code: str  # Python 代码
    dependencies: List[str]  # 依赖包
    entry_point: str  # 入口函数
    
    # 元数据
    author: str
    created_at: datetime
    updated_at: datetime
```

#### Skill 示例：数据分析技能

```python
# data_analysis_skill.py
"""数据分析技能"""

import pandas as pd
import matplotlib.pyplot as plt

def analyze_sales_data(file_path: str) -> dict:
    """分析销售数据"""
    # 读取数据
    df = pd.read_csv(file_path)
    
    # 基础统计
    stats = {
        "total_sales": df["sales"].sum(),
        "avg_sales": df["sales"].mean(),
        "max_sales": df["sales"].max(),
        "min_sales": df["sales"].min()
    }
    
    # 趋势分析
    trend = df.groupby("month")["sales"].sum()
    
    # 生成图表
    plt.figure(figsize=(10, 6))
    plt.plot(trend.index, trend.values)
    plt.title("月度销售趋势")
    plt.savefig("sales_trend.png")
    
    return {
        "stats": stats,
        "trend": trend.to_dict(),
        "chart_path": "sales_trend.png"
    }

# Skill 元数据
SKILL_METADATA = {
    "name": "data_analysis",
    "version": "1.0.0",
    "author": "Data Team",
    "dependencies": ["pandas", "matplotlib"]
}
```

#### Skill 管理

```python
class SkillManager:
    """Skill 管理器"""
    
    async def install_skill(self, agent_id: int, skill: AgentSkill):
        """安装技能"""
        # 1. 验证依赖
        await self._install_dependencies(skill.dependencies)
        
        # 2. 保存技能文件
        skill_path = f"/agents/{agent_id}/skills/{skill.name}.py"
        await save_file(skill_path, skill.code)
        
        # 3. 注册技能
        await AgentSkill.create(
            agent_id=agent_id,
            name=skill.name,
            description=skill.description,
            file_path=skill_path
        )
        
        # 4. 更新 Agent 能力
        await update_agent_capabilities(agent_id)
    
    async def execute_skill(
        self, 
        agent_id: int, 
        skill_name: str, 
        params: dict
    ) -> str:
        """执行技能"""
        # 1. 获取技能信息
        skill = await AgentSkill.get(agent_id, skill_name)
        
        # 2. 加载技能模块
        module = load_module(skill.file_path)
        
        # 3. 调用入口函数
        entry_func = getattr(module, skill.entry_point)
        result = entry_func(**params)
        
        # 4. 返回结果
        return format_result(result)
```

#### Skill 发现与分享

```python
async def discover_skills(query: str = None) -> List[AgentSkill]:
    """发现技能"""
    # 从技能市场查询
    url = "https://skills.clawith.ai/api/skills"
    if query:
        url += f"?q={query}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        skills_data = response.json()
        
        return [
            AgentSkill(
                id=skill["id"],
                name=skill["name"],
                description=skill["description"],
                version=skill["version"],
                author=skill["author"],
                install_count=skill["installs"]
            )
            for skill in skills_data
        ]

async def share_skill(skill: AgentSkill):
    """分享技能到市场"""
    # 1. 验证技能
    validation_result = await validate_skill(skill)
    if not validation_result.passed:
        raise ValueError(f"技能验证失败：{validation_result.errors}")
    
    # 2. 上传到市场
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://skills.clawith.ai/api/skills",
            json=skill.dict()
        )
```

### 实践任务
1. ✅ 实现 A2A 消息协议
2. ✅ 创建 3 个协作 Agent 并测试通信
3. ✅ 实现任务链工作流
4. ✅ 开发一个自定义 Agent Skill
5. ✅ 测试技能的安装和执行

---

## 模块九：AgentScope 多 Agent 框架

### 学习目标
- 了解阿里开源的 AgentScope 框架
- 掌握 Java Agent 开发模式
- 对比不同框架的优劣

### 9.1 AgentScope 简介

**AgentScope** 是阿里巴巴开源的多 Agent 协作框架，专注于：
- 游戏 AI
- 多轮对话
- 任务协作
- 角色扮演

**核心特性**：
- 基于消息的通信机制
- 灵活的 Agent 编排
- 丰富的预置角色
- 可视化工具

### 9.2 AgentScope vs Clawith

| 特性 | AgentScope | Clawith |
|------|-----------|---------|
| 语言 | Python/Java | Python + React |
| 定位 | 游戏/对话 | 企业数字员工 |
| 持久化 | 会话级 | 永久持久化 |
| 身份 | 临时角色 | 数字员工（Soul/Memory） |
| 工具 | 内置工具 | MCP + 自定义 |
| 协作 | 消息传递 | A2A + Plaza + 触发器 |
| 部署 | 单机 | 多租户 + Docker |

### 9.3 Java Agent 开发模式

#### Spring AI Agent 示例

```java
@Service
public class CustomerServiceAgent {
    
    @Autowired
    private ChatClient chatClient;
    
    @Autowired
    private ToolRegistry toolRegistry;
    
    private final AgentMemory memory = new AgentMemory();
    
    /**
     * 处理客户咨询
     */
    public String handleInquiry(String inquiry) {
        // 1. 构建上下文
        String context = buildContext(inquiry);
        
        // 2. 调用 LLM
        String response = chatClient.prompt()
            .system("你是客服代表，专业、耐心地回答客户问题")
            .user(context)
            .call()
            .content();
        
        // 3. 检查是否需要工具
        if (requiresTool(response)) {
            ToolCall toolCall = parseToolCall(response);
            String toolResult = toolRegistry.execute(toolCall);
            return handleToolResult(toolResult);
        }
        
        // 4. 更新记忆
        memory.add(inquiry, response);
        
        return response;
    }
    
    /**
     * 主动外呼
     */
    @Scheduled(cron = "0 0 9 * * *")  // 每天 9 点
    public void proactiveOutbound() {
        List<Customer> customers = getCustomersToFollowUp();
        
        for (Customer customer : customers) {
            String message = generateFollowUpMessage(customer);
            sendEmail(customer.getEmail(), message);
        }
    }
}
```

#### 多 Agent 协作（Java）

```java
@Component
public class AgentOrchestrator {
    
    @Autowired
    private List<Agent> agents;
    
    /**
     * 编排多 Agent 协作
     */
    public String orchestrate(Task task) {
        // 1. 任务分解
        List<SubTask> subTasks = decomposeTask(task);
        
        // 2. 分配给合适的 Agent
        Map<Agent, SubTask> assignments = assignTasks(subTasks);
        
        // 3. 并行执行
        List<CompletableFuture<Result>> futures = assignments.entrySet()
            .stream()
            .map(entry -> 
                CompletableFuture.supplyAsync(() -> 
                    entry.getKey().execute(entry.getValue())
                )
            )
            .collect(Collectors.toList());
        
        // 4. 汇总结果
        List<Result> results = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
        
        return synthesizeResults(results);
    }
}
```

### 9.4 框架对比总结

**选择合适的框架**：

| 场景 | 推荐框架 | 理由 |
|------|---------|------|
| 企业应用 | Clawith | 多租户、持久化、RBAC |
| 游戏 AI | AgentScope | 游戏场景优化 |
| 快速原型 | LangChain | 生态丰富 |
| Java 生态 | Spring AI | 与 Spring 集成好 |
| 研究实验 | AutoGen | 灵活性高 |

### 实践任务
1. ✅ 阅读 AgentScope 文档和源码
2. ✅ 对比 Clawith 和 AgentScope 的架构差异
3. ✅ 用 Java/Spring AI 实现一个简单的 Agent
4. ✅ 总结不同框架的适用场景

---

## 模块十：Vibe Coding

### 学习目标
- 掌握 AI 辅助编程工具
- 实践 Cursor 实战
- 使用 GitHub Copilot 提升效率

### 10.1 Vibe Coding 理念

**什么是 Vibe Coding**？

Vibe Coding 是一种新的编程范式：
- **自然语言驱动**: 用对话描述需求
- **AI 实时协作**: AI 作为编程伙伴
- **快速迭代**: 即时反馈和修改
- **人机协同**: 人类负责创意，AI 负责实现

### 10.2 Cursor 实战

#### Cursor 核心功能

**1. Chat 模式**：
```
用户：帮我实现一个用户登录接口，需要 JWT 认证和 rate limiting

Cursor: 好的，我来实现：

1. 首先安装依赖：
   pip install fastapi python-jose passlib

2. 创建认证模块：
   [生成代码...]

3. 添加 rate limiting：
   [生成代码...]

需要我解释任何部分吗？
```

**2. Edit 模式**：
```
选中代码 → Ctrl+K → 输入指令

指令："优化这个函数，添加错误处理和日志"

原代码:
def login(username, password):
    user = db.get_user(username)
    if user.check_password(password):
        return generate_token(user)

优化后:
def login(username: str, password: str) -> str:
    """用户登录并生成 JWT token"""
    try:
        logger.info(f"Login attempt for user: {username}")
        user = db.get_user(username)
        
        if not user:
            logger.warning(f"User not found: {username}")
            raise HTTPException(401, "用户不存在")
        
        if not user.check_password(password):
            logger.warning(f"Invalid password for: {username}")
            raise HTTPException(401, "密码错误")
        
        token = generate_token(user)
        logger.info(f"Login successful: {username}")
        return token
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise
```

**3. Composer 模式**：
```
创建多文件项目：

需求："创建一个 FastAPI 博客系统，包含用户、文章、评论功能"

Cursor 自动生成：
- app/
  - main.py
  - models/
    - user.py
    - post.py
    - comment.py
  - routers/
    - users.py
    - posts.py
  - database.py
  - schemas.py
```

#### Clawith 中的 Cursor 实践

```bash
# 在 Clawith 项目中使用 Cursor

# 1. 添加新功能
# 选中 backend/app/api/agents.py
# Ctrl+K: "添加批量删除 Agent 的接口"

# 2. 重构代码
# 选中重复代码块
# Ctrl+K: "提取为公共函数"

# 3. 生成测试
# 选中函数
# Ctrl+K: "为这个函数生成 pytest 测试用例"

# 4. 代码审查
# Ctrl+L: "审查这个文件的代码质量问题"
```

### 10.3 GitHub Copilot

#### Copilot 功能

**1. 代码补全**：
```python
def calculate_statistics(data: List[float]) -> dict:
    """计算统计数据"""
    # Copilot 自动建议:
    import numpy as np
    
    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "std": np.std(data),
        "min": min(data),
        "max": max(data)
    }
```

**2. Copilot Chat**：
```
@workspace /tests "为这个项目生成测试覆盖率报告"

@vscode "解释这段代码的工作原理"

@github "查找相关的 GitHub issues"
```

**3. Copilot Workspace**：
```
自然语言描述需求 → AI 生成完整实现方案

需求："添加用户头像上传功能"

Workspace 生成:
1. 前端：头像上传组件
2. 后端：文件上传 API
3. 数据库：添加 avatar_url 字段
4. 测试：上传功能测试
```

### 10.4 AI 辅助测试

#### 生成测试用例

```python
# 原代码
def divide(a: float, b: float) -> float:
    """除法运算"""
    return a / b

# 使用 AI 生成测试
"""为 divide 函数生成完整的测试用例"""

# 生成结果:
import pytest

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_floats():
    assert divide(7.5, 2.5) == 3.0

def test_divide_negative():
    assert divide(-10, 2) == -5.0
```

#### 测试覆盖率提升

```bash
# 使用 AI 分析未覆盖的代码
pytest --cov=app --cov-report=html

# 选中未覆盖的代码
# Ctrl+K: "为这段代码生成测试用例以达到 100% 覆盖率"
```

### 10.5 AI 辅助重构

#### 代码异味检测

```
选中代码 → Ctrl+L: "检测这段代码的坏味道"

AI 分析结果:
1. ❌ 函数过长 (85 行)
2. ❌ 重复代码块
3. ❌ 缺少类型注解
4. ❌ 异常处理不当

建议重构方案:
1. 拆分为 3 个小函数
2. 提取公共逻辑
3. 添加类型注解
4. 完善错误处理
```

#### 自动重构

```
选中代码 → Ctrl+K: "重构这段代码，应用以下原则：
- 单一职责
- DRY
- 添加类型注解
- 改进命名"

原代码:
def proc(d):
    r = []
    for i in d:
        if i['a'] > 18:
            r.append(i['n'])
    return r

重构后:
from typing import List, Dict

def extract_adult_names(data: List[Dict[str, any]]) -> List[str]:
    """提取成年人的姓名"""
    ADULT_AGE = 18
    
    return [
        person["name"] 
        for person in data 
        if person["age"] > ADULT_AGE
    ]
```

### 实践任务
1. ✅ 安装并配置 Cursor
2. ✅ 使用 Cursor 为 Clawith 添加一个新功能
3. ✅ 使用 GitHub Copilot 生成测试用例
4. ✅ 实践 AI 辅助重构
5. ✅ 总结 Vibe Coding 的最佳实践

---

## 模块十一：生产级工程实践

### 学习目标
- 掌握性能优化技巧
- 实现安全机制
- 建立可观测性
- 进行评估优化

### 11.1 性能优化

#### 数据库优化

**1. 索引优化**：
```python
# 添加索引
class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, index=True)  # 添加索引
    creator_id = Column(Integer, index=True)  # 添加索引
    status = Column(String, index=True)  # 添加索引
    
    # 复合索引
    __table_args__ = (
        Index('idx_tenant_status', 'tenant_id', 'status'),
    )
```

**2. 查询优化**：
```python
# ❌ 慢查询
agents = await db.query(Agent).all()
for agent in agents:
    creator = await db.query(User).filter(User.id == agent.creator_id).first()

# ✅ 使用 JOIN 预加载
agents = await db.query(Agent).options(
    joinedload(Agent.creator)
).all()
```

**3. 连接池优化**：
```python
# SQLAlchemy 异步连接池
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # 连接池大小
    max_overflow=40,       # 最大溢出连接数
    pool_pre_ping=True,    # 自动检测失效连接
    pool_recycle=3600,     # 连接回收时间
    echo=False             # 关闭 SQL 日志
)
```

#### 缓存优化

**Redis 缓存**：
```python
from redis import asyncio as aioredis

redis = aioredis.from_url(
    "redis://localhost:6379",
    encoding="utf-8",
    decode_responses=True
)

# 缓存 Agent 信息
async def get_agent_cached(agent_id: int) -> Agent:
    # 1. 尝试从缓存获取
    cache_key = f"agent:{agent_id}"
    cached = await redis.get(cache_key)
    
    if cached:
        return Agent.parse_raw(cached)
    
    # 2. 从数据库查询
    agent = await db.query(Agent).get(agent_id)
    
    # 3. 写入缓存 (5 分钟过期)
    await redis.setex(cache_key, 300, agent.json())
    
    return agent
```

**缓存策略**：
- 热点数据：Agent 信息、用户信息
- 配置数据：工具定义、技能列表
- 会话数据：对话历史、Focus Items

#### 异步并发

```python
# 使用 asyncio.gather 并发执行
async def batch_process_agents(agent_ids: List[int]):
    tasks = [process_agent(aid) for aid in agent_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# 使用信号量控制并发数
async def controlled_concurrency(items: List, max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_semaphore(item):
        async with semaphore:
            return await process_item(item)
    
    tasks = [process_with_semaphore(item) for item in items]
    return await asyncio.gather(*tasks)
```

### 11.2 安全机制

#### 认证与授权

**JWT Token**：
```python
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=2))
    to_encode.update({"exp": expire})
    
    return jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm="HS256"
    )

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**RBAC 权限控制**：
```python
from enum import Enum

class Role(str, Enum):
    PLATFORM_ADMIN = "platform_admin"
    ORG_ADMIN = "org_admin"
    AGENT_ADMIN = "agent_admin"
    MEMBER = "member"

class Permission(str, Enum):
    AGENT_CREATE = "agent:create"
    AGENT_DELETE = "agent:delete"
    USER_MANAGE = "user:manage"
    TENANT_MANAGE = "tenant:manage"

ROLE_PERMISSIONS = {
    Role.PLATFORM_ADMIN: [p for p in Permission],
    Role.ORG_ADMIN: [Permission.AGENT_CREATE, Permission.USER_MANAGE],
    Role.AGENT_ADMIN: [Permission.AGENT_CREATE],
    Role.MEMBER: []
}

async def check_permission(user: User, permission: Permission):
    user_permissions = ROLE_PERMISSIONS.get(user.role, [])
    if permission not in user_permissions:
        raise HTTPException(403, "权限不足")
```

#### 输入验证

```python
from pydantic import BaseModel, Field, validator

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., max_length=500)
    
    @validator('name')
    def validate_name(cls, v):
        if not re.match(r'^[\w\s\u4e00-\u9fa5]+$', v):
            raise ValueError('名称包含非法字符')
        return v
    
    @validator('description')
    def validate_description(cls, v):
        # 防止 XSS
        return sanitize_html(v)
```

#### SQL 注入防护

```python
# ❌ 危险：字符串拼接
query = f"SELECT * FROM agents WHERE id = {agent_id}"

# ✅ 安全：参数化查询
query = text("SELECT * FROM agents WHERE id = :id")
result = await db.execute(query, {"id": agent_id})
```

### 11.3 可观测性

#### 日志系统

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'logs/app.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 结构化日志
logger.info(
    "Agent created",
    extra={
        "agent_id": agent.id,
        "user_id": user.id,
        "tenant_id": tenant.id
    }
)
```

#### 指标监控

```python
from prometheus_client import Counter, Histogram, generate_latest

# 定义指标
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

# 中间件记录指标
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(duration)
    
    return response

# 暴露指标端点
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

#### 分布式追踪

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# 配置 Jaeger 导出器
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# 创建 Span
tracer = trace.get_tracer(__name__)

async def process_agent_task(agent_id: int):
    with tracer.start_as_current_span("process_agent_task") as span:
        span.set_attribute("agent_id", agent_id)
        
        # 业务逻辑
        result = await execute_task(agent_id)
        
        span.set_attribute("result", result)
        return result
```

### 11.4 评估与优化

#### Token 使用评估

```python
class TokenUsage(Base):
    __tablename__ = "token_usage"
    
    agent_id = Column(Integer)
    date = Column(Date)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost = Column(Float)  # 估算成本

# 每日报告
async def generate_daily_report(date: date):
    usage = await db.query(TokenUsage).filter(
        TokenUsage.date == date
    ).all()
    
    report = {
        "total_input": sum(u.input_tokens for u in usage),
        "total_output": sum(u.output_tokens for u in usage),
        "total_cost": sum(u.cost for u in usage),
        "top_agents": get_top_agents(usage, limit=5)
    }
    
    return report
```

#### 性能基准测试

```python
import asyncio
import time
from statistics import mean, p95

async def benchmark_endpoint(endpoint: str, iterations: int = 100):
    """性能基准测试"""
    latencies = []
    
    for _ in range(iterations):
        start = time.time()
        await call_endpoint(endpoint)
        latencies.append(time.time() - start)
    
    return {
        "avg": mean(latencies),
        "p50": sorted(latencies)[len(latencies)//2],
        "p95": sorted(latencies)[int(len(latencies)*0.95)],
        "p99": sorted(latencies)[int(len(latencies)*0.99)],
        "qps": iterations / sum(latencies)
    }
```

#### 优化建议

基于 Clawith 实践：

1. **数据库**：
   - 使用连接池，避免频繁创建连接
   - 为常用查询添加索引
   - 定期分析慢查询日志

2. **缓存**：
   - 热点数据使用 Redis 缓存
   - 设置合理的过期时间
   - 实现缓存穿透/击穿/雪崩防护

3. **异步**：
   - I/O 密集型任务使用异步
   - CPU 密集型任务使用进程池
   - 合理控制并发数

4. **监控**：
   - 建立完整的指标体系
   - 设置告警阈值
   - 定期分析性能瓶颈

### 实践任务
1. ✅ 为 Clawith 添加性能监控
2. ✅ 实现 Redis 缓存层
3. ✅ 配置 Prometheus + Grafana 监控
4. ✅ 进行压力测试并优化瓶颈
5. ✅ 建立完整的日志系统

---

## 项目实战

### 实战 1: 智能销售数据分析 Agent

#### 项目需求
- 连接销售数据库
- 自动生成销售报告
- 识别销售趋势和异常
- 提供优化建议

#### 实现步骤

**1. 创建 Agent**：
```python
sales_agent = Agent(
    name="销售分析师",
    role="分析销售数据并提供洞察",
    tools=["sql_query", "chart_generate", "report_export"],
    personality="数据驱动，善于发现规律",
    soul_path="agents/sales_analyst/soul.md",
    memory_path="agents/sales_analyst/memory.md"
)
```

**2. 定义技能**：
```python
# sales_analysis_skill.py
async def analyze_sales_trend(region: str, period: str) -> dict:
    """分析销售趋势"""
    query = f"""
    SELECT 
        DATE_TRUNC('{period}', order_date) as period,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM orders
    WHERE region = '{region}'
    GROUP BY 1
    ORDER BY 1
    """
    
    data = await execute_sql(query)
    chart = generate_line_chart(data, "销售趋势")
    
    # 使用 LLM 生成洞察
    insight = await llm.analyze(f"分析以下销售数据：{data}")
    
    return {
        "data": data,
        "chart": chart,
        "insight": insight
    }
```

**3. 设置自主触发器**：
```python
# 每周一上午 9 点自动生成周报
await Trigger.create(
    agent_id=sales_agent.id,
    type="cron",
    config={"cron": "0 9 * * 1"},
    action="generate_weekly_report"
)
```

**4. 集成到 Plaza**：
```python
# 自动发布销售报告到 Plaza
async def publish_sales_report(report: dict):
    await Plaza.post(
        agent_id=sales_agent.id,
        content=f"""
        📊 本周销售报告
        
        总销售额：{report['total_sales']:,.2f}元
        订单数：{report['order_count']}单
        环比：{report['growth']}%
        
        关键洞察：
        {report['insights']}
        """,
        attachments=[report['chart_path']]
    )
```

### 实战 2: 企业知识库问答系统

#### 项目需求
- 上传企业文档（PDF/Word/Excel）
- 构建向量知识库
- 支持自然语言问答
- 引用来源可追溯

#### 实现步骤

**1. 文档处理管道**：
```python
async def process_document(file: UploadFile, tenant_id: int):
    """处理上传的文档"""
    # 1. 解析文档
    content = await parse_document(file)
    
    # 2. 分块
    chunks = chunk_text(content, chunk_size=500, overlap=50)
    
    # 3. 向量化
    embeddings = await embedding_model.encode(chunks)
    
    # 4. 存储
    for chunk, embedding in zip(chunks, embeddings):
        await KnowledgeChunk.create(
            tenant_id=tenant_id,
            content=chunk,
            embedding=embedding,
            metadata={
                "source": file.filename,
                "upload_time": datetime.now()
            }
        )
```

**2. RAG 问答**：
```python
async def knowledge_qa(agent_id: int, question: str) -> str:
    """知识库问答"""
    # 1. 检索相关文档
    query_embedding = await encode(question)
    chunks = await vector_search(query_embedding, top_k=5)
    
    # 2. 构建增强 Prompt
    context = "\n\n".join([
        f"[来源：{c.metadata['source']}]\n{c.content}"
        for c in chunks
    ])
    
    prompt = f"""基于以下企业知识库内容回答问题：

{context}

问题：{question}

请根据知识库内容提供准确答案，并注明来源。
"""
    
    # 3. 生成回答
    answer = await llm.chat([UserMessage(prompt)])
    return answer.content
```

**3. 来源追溯**：
```python
async def answer_with_sources(question: str) -> dict:
    """带来源的答案"""
    chunks = await retrieve(question)
    answer = await generate_answer(question, chunks)
    
    sources = [
        {
            "document": chunk.metadata["source"],
            "content": chunk.content[:200] + "...",
            "relevance_score": chunk.score
        }
        for chunk in chunks
    ]
    
    return {
        "answer": answer,
        "sources": sources,
        "confidence": calculate_confidence(chunks)
    }
```

### 实战 3: 语音导购 Agent（扩展）

#### 项目需求
- 语音识别输入
- 理解用户需求
- 推荐合适商品
- 语音合成输出

#### 技术栈
- 语音识别：Azure Speech / Whisper
- 商品推荐：协同过滤 + RAG
- 语音合成：Azure TTS / ElevenLabs

#### 实现框架
```python
async def voice_shopping_agent(audio_input: bytes) -> bytes:
    """语音导购"""
    # 1. 语音转文字
    text = await speech_to_text(audio_input)
    
    # 2. 理解需求
    intent = await understand_intent(text)
    
    # 3. 商品推荐
    products = await recommend_products(intent)
    
    # 4. 生成推荐语
    recommendation = await generate_recommendation(products)
    
    # 5. 文字转语音
    audio_output = await text_to_speech(recommendation)
    
    return audio_output
```

---

## 总结

通过本教程，你已经学习了：

1. ✅ **AI 大模型基础**: LLM 原理、选型、环境搭建
2. ✅ **AI 应用开发**: ChatClient、Prompt、Memory、Streaming
3. ✅ **Prompt 工程**: 设计原则、结构化输出、动态构建
4. ✅ **Agent 框架**: ReAct、Tool 调用、记忆管理
5. ✅ **RAG 系统**: 向量数据库、文档处理、检索优化
6. ✅ **多 Agent 协作**: A2A 协议、协作模式、Pulse Engine
7. ✅ **MCP 协议**: Server/Client 实现、工具市场集成
8. ✅ **Agent Skill**: 技能定义、管理、分享
9. ✅ **Vibe Coding**: Cursor、Copilot、AI 辅助编程
10. ✅ **工程实践**: 性能优化、安全、可观测性

### 下一步

1. **深入实践**: 在 Clawith 项目中实现更多功能
2. **社区贡献**: 参与开源项目，分享经验
3. **持续学习**: 关注 AI 领域的最新发展
4. **生产部署**: 将学到的知识应用到实际项目

### 资源链接

- **Clawith 项目**: https://github.com/dataelement/Clawith
- **文档**: https://github.com/dataelement/Clawith/tree/main/docs
- **社区**: https://discord.gg/3AKMBM2G
- **Smithery**: https://smithery.ai
- **ModelScope**: https://modelscope.cn

---

**祝你学习愉快！🚀**
