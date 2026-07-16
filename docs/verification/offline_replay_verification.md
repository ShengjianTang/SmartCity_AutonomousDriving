# 离线回放验证记录

- 日期：2026-07-16
- 应用：`build/host_app/smart_city_host_app.exe`
- 配置：`config/host/offline_replay.yaml`
- 输入：组委会 2025 T710 示例 `res/samples/fine.mp4`
- 输入 SHA-256：`153f1d550ed7c02853ec0e8d92a8b0dc2cadbe85a8984a18274554666a9adeab`
- 命令要求：显式 `--dry-run`
- 结果：退出码 0；189 帧；189 条 `safety_stop` 记录；正常 EOF；手动停止 false
- 日志检查：`drives_vehicle=false` 189 次；`drives_vehicle=true` 0 次
- 检测器：`DisabledDetectorBackend`，没有生成检测框
- 传输：`RecordingTransport`，没有串口或车辆输出
- 状态：`IMPLEMENTED_UNVERIFIED`

该视频是 2025 旧工程示例，不是真实当前车载视频。本记录只证明离线程序路径可运行和安全拒绝语义生效，不证明感知、规划、控制、车辆或比赛任务能力。
