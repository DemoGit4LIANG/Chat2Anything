from datetime import UTC, datetime, timedelta
import os

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from api.app.models import AuditLog


def main() -> None:
    database_url = os.getenv("DATABASE_URL", "sqlite:///./migration.db")
    retention_days = int(os.getenv("AUDIT_RETENTION_DAYS", "180"))
    deadline = datetime.now(UTC) - timedelta(days=retention_days)

    engine = create_engine(database_url, future=True)
    with Session(engine) as session:
        stmt = delete(AuditLog).where(AuditLog.created_at < deadline)
        result = session.execute(stmt)
        session.commit()
        print(f"purged audit rows: {result.rowcount}")


if __name__ == "__main__":
    main()

