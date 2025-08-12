# -*- coding: utf-8 -*-

"""
Enhanced OpenAI Compatible API for ClickHouse Agent

完全兼容 OpenAI API 协议的 ClickHouse Agent 服务
支持流式和非流式响应，保持gradio中的回答生成方法
"""

import os
import time
import uuid
import json
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ch_agent import CHAgent


# 加载 .env 文件
load_dotenv()


# LLM 配置
DASHSCOPE_LLM_CFG = {
    'model': 'qwen3-coder-plus',  # qwen-plus / qwen-turbo
    'model_server': os.getenv("DASHSCOPE_BASE_URL"),
    'api_key': os.getenv("DASHSCOPE_API_KEY")
}

DEEPSEEK_LLM_CFG = {
    'model': 'deepseek-reasoner',  # deepseek-chat / deepseek-reasoner
    'model_server': os.getenv("DEEPSEEK_BASE_URL"),
    'api_key': os.getenv("DEEPSEEK_API_KEY")
}


# 数据库配置
DB_CONFIG = {
    "host": os.getenv("CLICKHOUSE_HOST"),
    "port": os.getenv("CLICKHOUSE_PORT"),
    "user": os.getenv("CLICKHOUSE_USER"),
    "password": os.getenv("CLICKHOUSE_PASSWORD"),
}


# Pydantic 模型定义
class Message(BaseModel):
    role: str = Field(..., description="消息角色: user, assistant, system")
    content: str = Field(..., description="消息内容")


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="clickhouse-agent", description="模型名称")
    messages: List[Message] = Field(..., description="对话消息列表")
    stream: bool = Field(default=False, description="是否流式响应")
    temperature: Optional[float] = Field(default=0.7, description="温度参数")
    max_tokens: Optional[int] = Field(default=None, description="最大token数")
    top_p: Optional[float] = Field(default=1.0, description="top_p参数")
    frequency_penalty: Optional[float] = Field(default=0.0, description="频率惩罚")
    presence_penalty: Optional[float] = Field(default=0.0, description="存在惩罚")
    stop: Optional[Union[str, List[str]]] = Field(default=None, description="停止词")


class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class ChatCompletionStreamChoice(BaseModel):
    index: int
    delta: Dict[str, Any]
    finish_reason: Optional[str] = None


class ChatCompletionStreamResponse(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[ChatCompletionStreamChoice]


class ModelInfo(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str = "clickhouse-agent"
    permission: List[Dict] = []
    root: str = "clickhouse-agent"
    parent: Optional[str] = None


class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[ModelInfo]


class ErrorResponse(BaseModel):
    error: Dict[str, Any]


# 创建 FastAPI 应用
app = FastAPI(
    title="Enhanced ClickHouse Agent OpenAI Compatible API",
    description="完全兼容 OpenAI API 协议的 ClickHouse Agent 服务",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 创建 Agent 实例
def create_react_agent(llm_cfg, db_config):
    """创建 React Agent 实例"""
    cha = CHAgent(llm_cfg, db_config)
    react_agent = cha.create_react_agent()
    return react_agent


# 全局 Agent 实例
agent = create_react_agent(DASHSCOPE_LLM_CFG, DB_CONFIG)


def generate_response_gradio_style(messages: List[Dict], max_history: int = 6):
    """
    使用与gradio相同的回答生成方法
    保持与gradio_ch_agent.py中generate_response函数相同的逻辑
    """
    # 保留最后 max_history 条历史记录
    if len(messages) > max_history:
        messages = messages[-max_history:]
    
    # 使用 Agent 生成响应
    for chunk in agent.run(messages):
        content = chunk[-1].get("content", "")
        yield content


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Enhanced ClickHouse Agent OpenAI Compatible API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "models": "/v1/models",
            "chat_completions": "/v1/chat/completions",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/v1/models")
async def list_models():
    """获取可用模型列表"""
    return ModelsResponse(
        data=[
            ModelInfo(
                id="clickhouse-agent",
                created=int(time.time()),
                owned_by="clickhouse-agent",
                permission=[{
                    "id": "modelperm-clickhouse-agent",
                    "object": "model_permission",
                    "created": int(time.time()),
                    "allow_create_engine": False,
                    "allow_sampling": True,
                    "allow_logprobs": True,
                    "allow_search_indices": False,
                    "allow_view": True,
                    "allow_fine_tuning": False,
                    "organization": "*",
                    "group": None,
                    "is_blocking": False
                }],
                root="clickhouse-agent"
            )
        ]
    )


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    """创建聊天完成"""
    try:
        # 转换消息格式
        messages = []
        for msg in request.messages:
            messages.append({
                'role': msg.role,
                'content': msg.content
            })
        
        # 生成唯一ID
        completion_id = f"chatcmpl-{uuid.uuid4().hex[:29]}"
        created = int(time.time())
        
        if request.stream:
            # 流式响应
            return StreamingResponse(
                generate_stream_response(completion_id, created, request.model, messages),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/plain; charset=utf-8"
                }
            )
        else:
            # 非流式响应
            response_content = ""
            token_count = 0
            
            # 使用gradio风格的响应生成方法
            for content in generate_response_gradio_style(messages):
                response_content = content
                token_count += len(content.split())  # 简单的token计数
            
            return ChatCompletionResponse(
                id=completion_id,
                created=created,
                model=request.model,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        message=Message(role="assistant", content=response_content),
                        finish_reason="stop"
                    )
                ],
                usage=Usage(
                    prompt_tokens=sum(len(msg['content'].split()) for msg in messages),
                    completion_tokens=token_count,
                    total_tokens=sum(len(msg['content'].split()) for msg in messages) + token_count
                )
            )
            
    except Exception as e:
        error_response = ErrorResponse(
            error={
                "message": str(e),
                "type": "internal_server_error",
                "param": None,
                "code": "internal_error"
            }
        )
        raise HTTPException(status_code=500, detail=error_response.dict())


async def generate_stream_response(completion_id: str, created: int, model: str, messages: List[Dict]):
    """生成流式响应"""
    try:
        # 发送开始标记
        start_response = ChatCompletionStreamResponse(
            id=completion_id,
            created=created,
            model=model,
            choices=[
                ChatCompletionStreamChoice(
                    index=0,
                    delta={"role": "assistant", "content": ""},
                    finish_reason=None
                )
            ]
        )
        yield f"data: {start_response.model_dump_json()}\n\n"
        
        # 流式生成内容 - 使用gradio风格的响应生成方法
        previous_content = ""
        for current_content in generate_response_gradio_style(messages):
            # 计算增量内容
            if current_content.startswith(previous_content):
                delta_content = current_content[len(previous_content):]
            else:
                delta_content = current_content
            
            if delta_content:
                # 发送内容块
                content_response = ChatCompletionStreamResponse(
                    id=completion_id,
                    created=created,
                    model=model,
                    choices=[
                        ChatCompletionStreamChoice(
                            index=0,
                            delta={"content": delta_content},
                            finish_reason=None
                        )
                    ]
                )
                yield f"data: {content_response.model_dump_json()}\n\n"
            
            previous_content = current_content
        
        # 发送结束标记
        end_response = ChatCompletionStreamResponse(
            id=completion_id,
            created=created,
            model=model,
            choices=[
                ChatCompletionStreamChoice(
                    index=0,
                    delta={},
                    finish_reason="stop"
                )
            ]
        )
        yield f"data: {end_response.model_dump_json()}\n\n"
        
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        # 发送错误信息
        error_data = {
            "error": {
                "message": str(e),
                "type": "internal_server_error",
                "param": None,
                "code": "internal_error"
            }
        }
        yield f'data: {json.dumps(error_data)}\n\n'
        yield "data: [DONE]\n\n"


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 简单的健康检查，可以扩展为检查数据库连接等
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "service": "clickhouse-agent",
            "database": "connected" if DB_CONFIG.get("host") else "not_configured"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )


@app.get("/v1/models/{model_id}")
async def get_model(model_id: str):
    """获取特定模型信息"""
    if model_id == "clickhouse-agent":
        return ModelInfo(
            id="clickhouse-agent",
            created=int(time.time()),
            owned_by="clickhouse-agent",
            permission=[{
                "id": "modelperm-clickhouse-agent",
                "object": "model_permission",
                "created": int(time.time()),
                "allow_create_engine": False,
                "allow_sampling": True,
                "allow_logprobs": True,
                "allow_search_indices": False,
                "allow_view": True,
                "allow_fine_tuning": False,
                "organization": "*",
                "group": None,
                "is_blocking": False
            }],
            root="clickhouse-agent"
        )
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "message": f"The model '{model_id}' does not exist",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "model_not_found"
                }
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动 Enhanced ClickHouse Agent OpenAI Compatible API")
    print("📖 API文档: http://localhost:8001/docs")
    print("🔍 ReDoc文档: http://localhost:8001/redoc")
    print("💚 健康检查: http://localhost:8001/health")
    print("🤖 模型列表: http://localhost:8001/v1/models")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # 使用不同的端口避免冲突
        log_level="info",
        reload=False
    )