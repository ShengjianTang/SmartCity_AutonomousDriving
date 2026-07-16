# 配置策略

## 来源

配置值只能来自：官方规则/手册、官方 SDK 示例、真实硬件探测、留档标定或真实测试。每份实例配置应记录 `source`、`source_hash`、`measured_at`（如适用）和 `status`。

## Schema 与实例分离

- `config/schemas/` 定义字段、类型、必填条件和来源要求，不填经验值。
- `config/host/` 只保存主机运行配置模板。
- `config/vehicle/`、`perception/`、`planning/`、`control/` 等待真实资料后保存实例。
- 未知字段为 `null`，状态为 `BLOCKED`，并提供 `source_required`。
- `config/host/offline_replay.yaml` 保持 `maximum_frame_age_ms: null`、`motion_configuration_complete: false`，因此可运行回放但不能获得运动授权。

## 验证规则

1. 未知字段、类型错误、缺少来源或 source hash 不匹配时拒绝相关后端启动。
2. 官方规则给出的范围只用于合规验证，不自动选择范围内的任一值。
3. 标定值必须带单位、设备标识、测量方法、日期和原始记录路径。
4. 控制参数必须说明适用车辆、软件版本和验证场景。
5. 第三方配置值禁止导入正式实例。

## 变更

参数变更须同时更新事实登记/标定记录、验证记录、`PROJECT_STATE.md` 和 `CHANGELOG.md`。没有来源的变更不得合并。
