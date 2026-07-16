# 组委会资料集成架构

```text
原始投放/石墨索引
        │ SHA-256、解压、PDF/视频/模型/许可证审计
        v
证据层（manifest / fact registry / source lock / blockers）
        │ 只允许已登记且用途匹配的事实
        ├──────────────> 2025 工程/模型：REFERENCE_ONLY
        v
Host 离线层
配置校验 -> ReplayCameraBackend -> Frame/时效 -> DisabledDetectorBackend
                                           │
                                           v
                               MissionStateMachine/SafetySupervisor
                                           │
                                           v
                           RecordingTransport + TelemetryLogger
                               drives_vehicle=false
```

离线层已经 `IMPLEMENTED_UNVERIFIED`，用于验证输入、状态、安全拒绝与退出路径。真实相机、目标板推理、运动规划/控制和实车传输仍位于未实现边界之外。
