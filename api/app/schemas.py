from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    username: str
    role: str
    department_id: int
    permissions: list[str]


class KnowledgeBaseIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    department_id: int | None = None


class KnowledgeBaseOut(BaseModel):
    id: int
    name: str
    department_id: int
    visibility: str


class DocumentOut(BaseModel):
    id: int
    kb_id: int
    filename: str
    created_at: datetime


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    kb_id: int | None = None
    session_id: str


class SourceItem(BaseModel):
    doc_id: int
    filename: str
    download_url: str


class AskResponse(BaseModel):
    trace_id: str
    answer: str
    sources: list[SourceItem]
    token_total: int


class ChatLogItem(BaseModel):
    trace_id: str
    session_id: str
    question: str
    answer: str
    token_total: int
    created_at: datetime


class ChatHistoryResponse(BaseModel):
    items: list[ChatLogItem]


class AuditItem(BaseModel):
    trace_id: str
    action: str
    user_id: int | None
    department_id: int | None
    result: str
    created_at: datetime


class AuditLogsResponse(BaseModel):
    items: list[AuditItem]


class UsageItem(BaseModel):
    period: str
    department_id: int
    user_id: int
    token_total: int
    request_count: int


class UsageResponse(BaseModel):
    range: Literal["daily", "weekly", "monthly"]
    items: list[UsageItem]


class ChatSettings(BaseModel):
    context_window: int = 5
    rag_top_k: int = 5

