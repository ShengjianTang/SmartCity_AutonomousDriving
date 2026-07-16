# 组委会压缩包验证与解压记录

- 扫描到的原始压缩包：12
- 原始压缩包保持不变；目标目录为压缩包相邻的 `extracted/<archive-name>/`。
- 解压使用新建暂存目录并在成功后原子改名，不覆盖已有文件。
- ZIP 使用 CRC 检查；TAR/TGZ 检查头和成员路径；RAR/7z 使用系统 bsdtar 3.8.4 列表验证。

| 压缩包 | SHA-256 | 验证 | 解压 | 成员 | 文件 | 解压字节 | 目标/说明 |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `examples/开源工程/icar_autopilot_2025th.zip` | `54f0c38151b5844b0108754d3917b2bfcab983e8a8a79f03d0bea8d5eacf69c7` | VALID | SKIPPED_EXISTING | 426 | 361 | 121723907 | `examples/开源工程/extracted/icar_autopilot_2025th`; matching completion marker; no files overwritten |
| `examples/开源工程/icar_autopilot_2025th_FZ3B.zip` | `c03a6a6b74ba0ba18a8f6ff673ea5548201ea55373d1e2a520427111ea7517a4` | VALID | SKIPPED_EXISTING | 375 | 317 | 74811809 | `examples/开源工程/extracted/icar_autopilot_2025th_FZ3B`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/DRIVER_R4.19.5001.zip` | `76b8c13127835ba636935961a78f83a63d92cf9b2d9f563d61530be5a10dfc42` | VALID | SKIPPED_EXISTING | 126 | 117 | 24641132 | `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/DRIVER_R4.19.5001`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/USB Image Tool.rar` | `e6c7c401969d0240e75792d26612a51f2f5a538a1a08bf2c5d2f71016a53f8b8` | VALID | SKIPPED_EXISTING | 7 | 7 | 437399 | `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/USB Image Tool`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/产线-Upgrade_Download_R27.22.3801.7z` | `258cc0c6ef45619ab12ab3bd39c97576e8e6c33a2e19292527ff959f9b98bb57` | VALID | SKIPPED_EXISTING | 388 | 341 | 32620572 | `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/产线-Upgrade_Download_R27.22.3801`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/格式内存卡.rar` | `4d6bb5879d611416d6ece24a57237cd3d5e0ec8deec90dbf89265867b69ac268` | VALID | SKIPPED_EXISTING | 8 | 8 | 3809343 | `hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/格式内存卡`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/02-EMMC镜像/t710sys-230222.pac.tgz` | `f18730e6ba3080aecf0214263634d5ffc22bf3c73101f0d917619f3fa9abb6c9` | VALID | SKIPPED_EXISTING | 1 | 2 | 11251956144 | `hardware/board_image/赛事专用卡-镜像开源资料/02-EMMC镜像/extracted/t710sys-230222.pac`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/t710-boot-sd.pac.zip` | `10eb52596ae98cae03509936f65d023fb50a68c32b0c2c22f9096d6a9b98bcd2` | VALID | SKIPPED_EXISTING | 1 | 2 | 94323233 | `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/extracted/t710-boot-sd.pac`; matching completion marker; no files overwritten |
| `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/赛事开源-EB新板卡-IP254 V1.1.zip` | `045acaa161085ae94fa50782f91b36a5c8e0d779ab8b19186458ee218fbd1e93` | VALID | EXTRACTED | 1 | 1 | 31266439168 | `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/extracted/赛事开源-EB新板卡-IP254 V1.1`; ZIP central directory and CRC validation passed |
| `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/赛事开源-EB新板卡-IP254-29.12G.rar` | `bd69c0ea61e84f32aee4b267b3586b65aff5956dcff36ee849bd000df44761b5` | VALID | EXTRACTED | 1 | 1 | 31266439168 | `hardware/board_image/赛事专用卡-镜像开源资料/03-赛事定制镜像-SD卡-推荐/extracted/赛事开源-EB新板卡-IP254-29.12G`; bsdtar listing and member path validation passed |
| `hardware/remote_access/赛事专用卡-远程操作资料/MobaXterm_Installer_v23.0.zip` | `668550319b08dbc690290b13d129d337b3d82383b7def31afaecff4e793b5c1d` | VALID | EXTRACTED | 2 | 2 | 31674209 | `hardware/remote_access/赛事专用卡-远程操作资料/extracted/MobaXterm_Installer_v23.0`; ZIP central directory and CRC validation passed |
| `sdk/model_compiler/赛事专用卡-模型编译教程/ppnc2.0_v1.0.2.tar` | `655db72cf5d8f34f6a28007160396e1c16eb763bb10e2566a98b3fedce57abf3` | VALID | EXTRACTED | 15 | 12 | 10656587731 | `sdk/model_compiler/赛事专用卡-模型编译教程/extracted/ppnc2.0_v1.0.2`; TAR headers and member paths validated |
