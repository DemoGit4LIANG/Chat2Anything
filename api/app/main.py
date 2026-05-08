from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app.deps import get_current_user, require_permission
from app.models import AuditLog, ChatLog, Department, Document, KnowledgeBase, Role, User
from app.schemas import (
    AskRequest,
    AskResponse,
    AuditItem,
    AuditLogsResponse,
    ChatHistoryResponse,
    ChatLogItem,
    ChatSettings,
    DocumentOut,
    KnowledgeBaseIn,
    KnowledgeBaseOut,
    LoginRequest,
    LoginResponse,
    MeResponse,
    SourceItem,
    UsageItem,
    UsageResponse,
)
from app.security import create_access_token, hash_password, verify_password
from app.services import (
    aggregate_usage,
    append_chat_log,
    generate_trace_id,
    get_chat_settings,
    update_chat_settings,
    upsert_usage_daily,
    write_audit,
)

REQUEST_COUNTER = Counter("chat2anything_api_requests_total", "Total api request count", ["endpoint"])
GPU_USAGE_PLACEHOLDER = Gauge("chat2anything_gpu_usage_ratio", "GPU usage placeholder ratio")


def bootstrap(db: Session) -> None:
    dept = db.scalar(select(Department).where(Department.code == settings.bootstrap_admin_department))
    if dept is None:
        dept = Department(name="Platform", code=settings.bootstrap_admin_department)
        db.add(dept)
        db.flush()

    super_role = db.scalar(select(Role).where(Role.name == "super_admin"))
    if super_role is None:
        super_role = Role(name="super_admin", permissions=["*"])
        db.add(super_role)
        db.flush()

    user = db.scalar(select(User).where(User.username == settings.bootstrap_admin_username))
    if user is None:
        user = User(
            username=settings.bootstrap_admin_username,
            password_hash=hash_password(settings.bootstrap_admin_password),
            role_id=super_role.id,
            department_id=dept.id,
            status=1,
        )
        db.add(user)

    operator = db.scalar(select(Role).where(Role.name == "operator"))
    if operator is None:
        db.add(
            Role(
                name="operator",
                permissions=[
                    "chat.ask",
                    "kb.read",
                    "kb.upload",
                    "audit.read",
                    "usage.read",
                    "chat.settings.read",
                ],
            )
        )

    db.commit()


app = FastAPI(title=settings.app_name, version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    settings.storage_path
    with Session(engine) as db:
        bootstrap(db)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "env": settings.app_env}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/v1/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    REQUEST_COUNTER.labels(endpoint="auth_login").inc()
    user = db.scalar(select(User).where(User.username == payload.username, User.status == 1))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    return LoginResponse(access_token=create_access_token(user.id))


@app.get("/api/v1/auth/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user)) -> MeResponse:
    REQUEST_COUNTER.labels(endpoint="auth_me").inc()
    return MeResponse(
        id=user.id,
        username=user.username,
        role=user.role.name,
        department_id=user.department_id,
        permissions=user.role.permissions or [],
    )


@app.get("/api/v1/kb/list", response_model=list[KnowledgeBaseOut])
def kb_list(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    REQUEST_COUNTER.labels(endpoint="kb_list").inc()
    stmt = select(KnowledgeBase)
    if user.role.name != "super_admin":
        stmt = stmt.where(KnowledgeBase.department_id == user.department_id)
    return [
        KnowledgeBaseOut(id=x.id, name=x.name, department_id=x.department_id, visibility=x.visibility)
        for x in db.scalars(stmt.order_by(KnowledgeBase.id.desc())).all()
    ]


@app.post("/api/v1/kb/create", response_model=KnowledgeBaseOut)
def kb_create(
    payload: KnowledgeBaseIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    REQUEST_COUNTER.labels(endpoint="kb_create").inc()
    require_permission(user, "kb.manage")
    department_id = payload.department_id if user.role.name == "super_admin" and payload.department_id else user.department_id
    kb = KnowledgeBase(name=payload.name, department_id=department_id, visibility="department", created_by=user.id)
    db.add(kb)
    db.commit()
    db.refresh(kb)
    return KnowledgeBaseOut(id=kb.id, name=kb.name, department_id=kb.department_id, visibility=kb.visibility)


def ensure_kb_access(db: Session, user: User, kb_id: int) -> KnowledgeBase:
    kb = db.get(KnowledgeBase, kb_id)
    if kb is None:
        raise HTTPException(status_code=404, detail="kb not found")
    if user.role.name != "super_admin" and kb.department_id != user.department_id:
        raise HTTPException(status_code=403, detail="cross department access denied")
    return kb


@app.post("/api/v1/kb/{kb_id}/documents/upload", response_model=DocumentOut)
async def kb_upload(
    kb_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DocumentOut:
    REQUEST_COUNTER.labels(endpoint="kb_upload").inc()
    require_permission(user, "kb.upload")
    ensure_kb_access(db, user, kb_id)

    file_token = f"{uuid4().hex}_{file.filename}"
    target_dir = settings.storage_path / str(kb_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / file_token
    target_path.write_bytes(await file.read())

    doc = Document(kb_id=kb_id, filename=file.filename, storage_path=str(target_path), uploader_id=user.id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return DocumentOut(id=doc.id, kb_id=doc.kb_id, filename=doc.filename, created_at=doc.created_at)


@app.get("/api/v1/kb/{kb_id}/documents", response_model=list[DocumentOut])
def kb_documents(kb_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    REQUEST_COUNTER.labels(endpoint="kb_documents").inc()
    ensure_kb_access(db, user, kb_id)
    rows = db.scalars(select(Document).where(Document.kb_id == kb_id).order_by(desc(Document.id))).all()
    return [DocumentOut(id=x.id, kb_id=x.kb_id, filename=x.filename, created_at=x.created_at) for x in rows]


@app.get("/api/v1/files/source/{doc_id}")
def source_download(doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    REQUEST_COUNTER.labels(endpoint="files_source").inc()
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="document not found")
    ensure_kb_access(db, user, doc.kb_id)
    path = Path(doc.storage_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="file missing")
    return FileResponse(path=str(path), filename=doc.filename)


@app.post("/api/v1/chat/ask", response_model=AskResponse)
def ask(payload: AskRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> AskResponse:
    REQUEST_COUNTER.labels(endpoint="chat_ask").inc()
    require_permission(user, "chat.ask")
    trace_id = generate_trace_id()

    sources: list[dict] = []
    if payload.kb_id is not None:
        ensure_kb_access(db, user, payload.kb_id)
        latest_doc = db.scalar(
            select(Document).where(Document.kb_id == payload.kb_id).order_by(desc(Document.id)).limit(1)
        )
        if latest_doc is not None:
            sources.append(
                {
                    "doc_id": latest_doc.id,
                    "filename": latest_doc.filename,
                    "download_url": f"/api/v1/files/source/{latest_doc.id}",
                }
            )

    answer = f"迁移版回答：已接收问题“{payload.question}”，请接入真实 RAG/LLM 管线替换此占位实现。"
    token_total = max(32, len(payload.question) * 2)

    append_chat_log(
        db,
        trace_id=trace_id,
        session_id=payload.session_id,
        user_id=user.id,
        department_id=user.department_id,
        kb_id=payload.kb_id,
        question=payload.question,
        answer=answer,
        sources=sources,
        token_total=token_total,
    )
    upsert_usage_daily(db, department_id=user.department_id, user_id=user.id, token_total=token_total)
    write_audit(
        db,
        trace_id=trace_id,
        action="chat.ask",
        user_id=user.id,
        department_id=user.department_id,
        payload={"question": payload.question, "kb_id": payload.kb_id, "session_id": payload.session_id},
        result="success",
    )
    db.commit()
    GPU_USAGE_PLACEHOLDER.set(0.0)
    return AskResponse(
        trace_id=trace_id,
        answer=answer,
        token_total=token_total,
        sources=[SourceItem(**x) for x in sources],
    )


@app.get("/api/v1/chat/history", response_model=ChatHistoryResponse)
def history(
    session_id: str = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChatHistoryResponse:
    REQUEST_COUNTER.labels(endpoint="chat_history").inc()
    stmt = select(ChatLog).where(ChatLog.session_id == session_id)
    if user.role.name != "super_admin":
        stmt = stmt.where(ChatLog.department_id == user.department_id)
    rows = db.scalars(stmt.order_by(desc(ChatLog.id)).limit(50)).all()
    return ChatHistoryResponse(
        items=[
            ChatLogItem(
                trace_id=r.trace_id,
                session_id=r.session_id,
                question=r.question,
                answer=r.answer,
                token_total=r.token_total,
                created_at=r.created_at,
            )
            for r in rows
        ]
    )


@app.get("/api/v1/settings/chat", response_model=ChatSettings)
def read_chat_settings(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> ChatSettings:
    REQUEST_COUNTER.labels(endpoint="settings_read").inc()
    require_permission(user, "chat.settings.read")
    data = get_chat_settings(db, settings.context_window_default, settings.rag_top_k)
    return ChatSettings(**data)


@app.put("/api/v1/settings/chat", response_model=ChatSettings)
def write_chat_settings(
    payload: ChatSettings,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChatSettings:
    REQUEST_COUNTER.labels(endpoint="settings_write").inc()
    require_permission(user, "chat.settings.write")
    data = update_chat_settings(db, payload.model_dump())
    return ChatSettings(**data)


@app.get("/api/v1/audit/logs", response_model=AuditLogsResponse)
def audit_logs(
    department_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AuditLogsResponse:
    REQUEST_COUNTER.labels(endpoint="audit_logs").inc()
    require_permission(user, "audit.read")
    stmt = select(AuditLog)
    if user.role.name != "super_admin":
        stmt = stmt.where(AuditLog.department_id == user.department_id)
    if department_id:
        stmt = stmt.where(AuditLog.department_id == department_id)
    if user_id:
        stmt = stmt.where(AuditLog.user_id == user_id)
    rows = db.scalars(stmt.order_by(desc(AuditLog.id)).limit(200)).all()
    return AuditLogsResponse(
        items=[
            AuditItem(
                trace_id=x.trace_id,
                action=x.action,
                user_id=x.user_id,
                department_id=x.department_id,
                result=x.result,
                created_at=x.created_at,
            )
            for x in rows
        ]
    )


@app.get("/api/v1/usage/tokens/{range_name}", response_model=UsageResponse)
def usage(
    range_name: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UsageResponse:
    REQUEST_COUNTER.labels(endpoint="usage_tokens").inc()
    if range_name not in {"daily", "weekly", "monthly"}:
        raise HTTPException(status_code=400, detail="range must be daily/weekly/monthly")
    require_permission(user, "usage.read")
    rows = aggregate_usage(db, range_name)
    items = [
        UsageItem(
            period=range_name,
            department_id=department_id,
            user_id=user_id,
            token_total=int(token_total or 0),
            request_count=int(request_count or 0),
        )
        for department_id, user_id, token_total, request_count in rows
        if user.role.name == "super_admin" or department_id == user.department_id
    ]
    return UsageResponse(range=range_name, items=items)

