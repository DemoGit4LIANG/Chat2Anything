from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models import AppSetting, AuditLog, ChatLog, TokenUsageDaily


def generate_trace_id() -> str:
    return uuid4().hex


def write_audit(
    db: Session,
    *,
    trace_id: str,
    action: str,
    user_id: int | None,
    department_id: int | None,
    payload: dict,
    result: str = "success",
) -> None:
    db.add(
        AuditLog(
            trace_id=trace_id,
            action=action,
            user_id=user_id,
            department_id=department_id,
            payload=payload,
            result=result,
        )
    )


def upsert_usage_daily(db: Session, *, department_id: int, user_id: int, token_total: int) -> None:
    today = datetime.now(UTC).date()
    row = db.scalar(
        select(TokenUsageDaily).where(
            and_(
                TokenUsageDaily.dt == today,
                TokenUsageDaily.department_id == department_id,
                TokenUsageDaily.user_id == user_id,
            )
        )
    )
    if row is None:
        row = TokenUsageDaily(
            dt=today,
            department_id=department_id,
            user_id=user_id,
            token_total=token_total,
            request_count=1,
        )
        db.add(row)
    else:
        row.token_total += token_total
        row.request_count += 1


def get_chat_settings(db: Session, context_window_default: int, rag_top_k_default: int) -> dict:
    row = db.get(AppSetting, "chat")
    if row is None:
        value = {"context_window": context_window_default, "rag_top_k": rag_top_k_default}
        db.add(AppSetting(key="chat", value=value))
        db.commit()
        return value
    return row.value


def update_chat_settings(db: Session, payload: dict) -> dict:
    row = db.get(AppSetting, "chat")
    if row is None:
        row = AppSetting(key="chat", value=payload)
        db.add(row)
    else:
        row.value = payload
    db.commit()
    return row.value


def usage_range_filter(range_name: str) -> datetime.date:
    today = datetime.now(UTC).date()
    if range_name == "daily":
        return today
    if range_name == "weekly":
        return today - timedelta(days=6)
    return today.replace(day=1)


def aggregate_usage(db: Session, range_name: str):
    date_from = usage_range_filter(range_name)
    stmt = (
        select(
            TokenUsageDaily.department_id,
            TokenUsageDaily.user_id,
            func.sum(TokenUsageDaily.token_total),
            func.sum(TokenUsageDaily.request_count),
        )
        .where(TokenUsageDaily.dt >= date_from)
        .group_by(TokenUsageDaily.department_id, TokenUsageDaily.user_id)
    )
    return db.execute(stmt).all()


def append_chat_log(
    db: Session,
    *,
    trace_id: str,
    session_id: str,
    user_id: int,
    department_id: int,
    kb_id: int | None,
    question: str,
    answer: str,
    sources: list[dict],
    token_total: int,
) -> ChatLog:
    row = ChatLog(
        trace_id=trace_id,
        session_id=session_id,
        user_id=user_id,
        department_id=department_id,
        kb_id=kb_id,
        question=question,
        answer=answer,
        sources=sources,
        token_total=token_total,
    )
    db.add(row)
    return row

