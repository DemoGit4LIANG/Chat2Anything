# Chat2Anything 迁移模块映射（Phase 0）

## 目标
- 保持原仓可运行，采用“保留/改造/替换”渐进迁移。
- 新增能力落在原仓新增目录，不创建独立交付仓库。

## 映射表

| 原模块 | 策略 | 迁移落点 | 说明 |
|---|---|---|---|
| `Chat2Anything/fastchat/serve/chat2anything_web_server.py` | 保留+改造 | `Chat2Anything/fastchat/serve/` + `api/app/main.py` | 保留现有 Gradio 入口，新增 `/api/v1/*` 标准接口用于管理端/第三方前台接入 |
| `Chat2Anything/chains/local_vector_stroe.py` | 保留 | `Chat2Anything/chains/local_vector_stroe.py` | 一期不替换原 RAG 链路，迁移 API 中以占位回答保留接口契约 |
| `Chat2Anything/chains/database/*` | 保留+配置化 | `Chat2Anything/chains/database/` | 后续逐步剥离硬编码，统一环境变量 |
| `Chat2Anything-admin/applications/models/*` | 保留+增强 | `Chat2Anything-admin/applications/models/` + `api/app/models.py` | 管理端继续使用原模型；迁移 API 独立补齐审计/用量聚合模型 |
| `Chat2Anything-admin/applications/view/*` | 保留 | `Chat2Anything-admin/applications/view/` | 避免一期大规模 UI 重写 |
| 旧依赖配置 | 并行替换 | `api/requirements-modern.txt` | 在不破坏原环境前提下引入现代栈依赖窗口 |

## 阶段落地清单

### Phase 1
- API：`/api/v1/auth/*`、`/api/v1/chat/*`、`/api/v1/kb/*`、`/api/v1/files/source/{doc_id}`、`/api/v1/settings/chat`
- 回归：登录、上传、问答、来源下载

### Phase 2
- RBAC：权限点 `chat.ask`、`kb.upload`、`kb.manage`、`audit.read`、`usage.read`
- 审计：`audit_logs` 全链路记录 `trace_id/user/department/action/result`
- 用量：`token_usage_daily` 聚合统计（daily/weekly/monthly）

### Phase 3
- 可观测：`/metrics`、Prometheus 抓取、Grafana 数据源与仪表盘目录
- 合规预留：审计留存策略、最小权限角色策略、配置与密钥分离

