# Phase 回归清单

## Phase 0/1 最小回归
- [ ] `POST /api/v1/auth/login` 获取 token 成功
- [ ] `GET /api/v1/auth/me` 返回角色/部门/权限
- [ ] `GET /api/v1/kb/list` 能看到本部门知识库
- [ ] `POST /api/v1/kb/{id}/documents/upload` 上传成功
- [ ] `POST /api/v1/chat/ask` 返回 `trace_id + answer + sources + token_total`
- [ ] `GET /api/v1/files/source/{doc_id}` 可下载来源文件
- [ ] `GET /api/v1/chat/history` 可按 `session_id` 查询
- [ ] `GET/PUT /api/v1/settings/chat` 配置可读取/写入

## Phase 2 回归
- [ ] 非 super_admin 无法跨部门访问知识库
- [ ] 缺少权限点时接口返回 403
- [ ] `GET /api/v1/audit/logs` 可按部门/用户过滤
- [ ] `GET /api/v1/usage/tokens/daily|weekly|monthly` 返回聚合结果

## Phase 3 回归
- [ ] `GET /metrics` 暴露 Prometheus 指标
- [ ] Prometheus 可抓取 `migration_api:8100`
- [ ] Grafana 能使用预置数据源查看指标
- [ ] 审计留存策略脚本可执行

