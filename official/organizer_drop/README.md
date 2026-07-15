# 组委会资料投放说明

请保留原始文件名和内容，不要先行转换或覆盖。投放位置：

```text
official/organizer_drop/maps/        最终地图和赛道图纸
official/organizer_drop/hardware/    赛具硬件手册、接线图
official/organizer_drop/sdk/         官方 SDK 和工具链
official/organizer_drop/examples/    官方样例工程
official/organizer_drop/datasets/    官方数据集和标签
official/organizer_drop/models/      官方模型和权重
official/organizer_drop/notices/     QQ 群通知、赛区通知、补充规则
mcu/official/                        官方 MCU 工程
```

投放后运行：

```powershell
.\.venv\Scripts\python.exe tools\audit\audit_new_official_materials.py
```

审计脚本只生成清单，不修改原资料，也不会把未知资料自动认定为官方事实。
