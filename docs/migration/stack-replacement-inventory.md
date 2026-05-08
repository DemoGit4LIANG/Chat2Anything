# 旧技术栈替换清点（执行结果）

## 已替换为新主线（默认路径）

| 维度 | 旧栈 | 新栈 | 现状 |
|---|---|---|---|
| API 服务 | FastChat/自定义脚本 | FastAPI (`api/app/main.py`) | 已替换 |
| 鉴权 | Flask 体系分散实现 | JWT + RBAC | 已替换 |
| 数据库 | MySQL | PostgreSQL + pgvector | 已替换 |
| 部署编排 | `Chat2Anything-admin/dockercompose.yaml` (flask/mysql/redis) | 根目录 `docker-compose.yml` + `docker-compose.migration.yml` | 已替换 |
| 监控 | 无统一指标入口 | `/metrics` + Prometheus + Grafana | 已替换 |
| 启动脚本 | `Chat2Anything-admin/run.bat|run.sh` 启动 Flask | 改为启动 `uvicorn app.main:app` | 已替换 |

## 关键替换点
- 根目录 `README.md` 已改为迁移版主线说明。
- `Chat2Anything-admin/requirements.txt` 与 `dockerdata/requirements.txt` 已切到 FastAPI 依赖集合。
- `Chat2Anything-admin/dockercompose.yaml` 与 `dockerdata/docker-compose.yml` 已切到 PostgreSQL + migration_api。
- 新增根目录 `run.bat`、`run.sh`，统一启动迁移 API。
- `Chat2Anything/fastchat/serve/chat2anything_web_server.py` 默认禁用，需显式设置 `CHAT2ANYTHING_ALLOW_LEGACY_WEB=1` 才能临时回退。

## 保留但降级为 legacy（非默认）
- `Chat2Anything/fastchat/*`
- `Chat2Anything-admin/applications/*`

说明：以上目录保留用于对照迁移与应急回退，不作为默认运行主线。

