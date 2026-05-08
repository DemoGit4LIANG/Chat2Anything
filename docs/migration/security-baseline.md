# 安全与合规预留基线（Phase 3）

## 最小权限
- `super_admin`：全量权限，仅平台管理员使用。
- `operator`：`chat.ask`、`kb.upload`、`kb.read`、`audit.read`、`usage.read`、`chat.settings.read`。
- 生产环境禁止为业务账号分配 `super_admin`。

## 审计留存
- 审计表：`audit_logs`，必须记录 `trace_id/action/user_id/department_id/payload/result`。
- 默认留存：180 天（可通过 `AUDIT_RETENTION_DAYS` 调整）。
- 清理方式：执行 `scripts/purge_audit_logs.py` 定期归档与删除。

## 配置分离
- 机密项（JWT 密钥、数据库密码）必须经 `.env` 注入，禁止硬编码。
- 建议分离配置：
  - `.env.dev`：开发环境
  - `.env.staging`：联调环境
  - `.env.prod`：生产环境（仅运维持有）

## 可观测性
- API 指标由 `/metrics` 暴露，Prometheus 抓取。
- Grafana 仅作为展示层，不直接写生产数据库。
- GPU 指标先预留占位，二期接入实际 exporter（NVIDIA DCGM 或等效方案）。

