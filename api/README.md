# Chat2Anything Migration API

## 启动（本地）
1. 复制环境变量模板：
   - `copy .env.example .env`
2. 安装依赖：
   - `python -m venv .venv`
   - `.\.venv\Scripts\python.exe -m pip install -r requirements-modern.txt`
3. 启动服务：
   - `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8100`

## 启动（Docker Compose）
在仓库根目录执行：
- `docker compose -f docker-compose.migration.yml up -d`

## 已实现接口
- `/api/v1/auth/login`
- `/api/v1/auth/me`
- `/api/v1/kb/list`
- `/api/v1/kb/create`
- `/api/v1/kb/{id}/documents/upload`
- `/api/v1/kb/{id}/documents`
- `/api/v1/files/source/{doc_id}`
- `/api/v1/chat/ask`
- `/api/v1/chat/history`
- `/api/v1/settings/chat`
- `/api/v1/audit/logs`
- `/api/v1/usage/tokens/{daily|weekly|monthly}`
- `/metrics`

