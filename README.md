# Chat2Anything（迁移版主线）

本仓库默认技术栈已切换为：
- API：FastAPI（`/api/v1/*`）
- 鉴权：JWT + RBAC
- 数据：PostgreSQL + pgvector
- 观测：Prometheus + Grafana（预置）
- 部署：Docker Compose

旧的 FastChat/Flask 运行链路保留为 legacy 参考，不再作为默认启动路径。

## 快速启动（推荐）

### 方式一：Docker Compose
1. 准备环境变量
   - 复制 `api/.env.example` 为 `api/.env`
2. 启动
   - `docker compose -f docker-compose.migration.yml up -d`
3. 访问
   - API 文档：`http://127.0.0.1:8100/docs`
   - Prometheus：`http://127.0.0.1:9090`
   - Grafana：`http://127.0.0.1:3000`

### 方式二：本地运行
1. 进入 `api` 目录并创建虚拟环境
2. 安装依赖：`python -m pip install -r requirements-modern.txt`
3. 启动：`python -m uvicorn app.main:app --reload --port 8100`

## 关键接口
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/kb/list`
- `POST /api/v1/kb/{id}/documents/upload`
- `POST /api/v1/chat/ask`
- `GET /api/v1/files/source/{doc_id}`
- `GET /api/v1/audit/logs`
- `GET /api/v1/usage/tokens/{daily|weekly|monthly}`
- `GET /api/v1/settings/chat`
- `PUT /api/v1/settings/chat`

## 迁移资料
- 模块映射：`docs/migration/module-mapping.md`
- 回归清单：`docs/migration/regression-checklist.md`
- 安全基线：`docs/migration/security-baseline.md`

## Legacy 说明
- `Chat2Anything/fastchat/*` 与 `Chat2Anything-admin/*` 作为历史实现保留。
- 默认入口已切到迁移 API 主线；如需 legacy 调试，请在隔离分支中进行。






