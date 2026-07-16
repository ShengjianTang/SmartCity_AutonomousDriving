# PDF 逐页文本：hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/产线-Upgrade_Download_R27.22.3801/Upgrade_Download_R27.22.3801/Download_R27.22.3801/Doc/Customized/鉴权/下载模式鉴权交互说明-CN.pdf

- SHA-256：`a4e54df2d3058cc48d8e51e1d5b8b30ab52d9a84d7e4ea7cd4f3520b307fc8c4`

## 第 1 页

Download 鉴权指令交互说明

Document Number:  Document Version: V0.1
Owner: leiming.sun Date: 2020-11-10
Document Type:
NOTE: ALL MATERIALS INCLUDED HEREIN ARE COPYRIGHTED AND
CONFIDENTIAL UNLESS OTHERWISE INDICATED. The information
is intended only for the person or entity to which it is addressed and may
contain confidential and/or privileged material. Any review, retransmission,
dissemination, or other use of or taking of any action in re liance upon this
information by persons or entities other than the intended recipient is
prohibited.

This document is subject to change without notice. Please verify that your
company has the most recent specification.

Copyright © 2019  UNISOC Communications Inc.


www.UNISOC.com



## 第 2 页

修订记录

Revision  Date Author Description
V0.1 2020.11.10 leiming.sun Initial draft



















## 第 3 页

目录

修订记录........................................................................................................................................... 2
第 1 章 简介..................................................................................................................................... 4
1.1 目的 .................................................................................................................................... 4
1.2 目标读者 ............................................................................................................................ 4
1.3 缩略语 ................................................................................................................................ 4
1.4 参考文献 ............................................................................................................................ 4
第 2 章 需求描述 ............................................................................................................................. 5
2.1 需求描述 ............................................................................................................................ 5
第 3 章 鉴权交互 ............................................................................................................................. 6
3.1 uboot 指令说明 ................................................................................................................. 6
3.2 uboot 交互说明 ................................................................................................................. 6
3.3 交互实现 ............................................................................................ 错误!未定义书签。

















## 第 4 页

第 1 章 简介
1.1 目的
本文档主要说明 Download 下载工具鉴权指令交互说明。
1.2 目标读者
本文档的目标读者是相关功能的研发工程师，测试工程师，用户和项目管理人员。
1.3 缩略语
本文档使用的缩略语如下：
缩略语 含义








1.4 参考文献










## 第 5 页

第 2 章 需求描述
2.1 需求描述
Download 下载工具通过和 uboot 交互鉴权指令，接收鉴权数据 M1，并与 Server 交互
将鉴权数据 M2 返回给 uboot.























## 第 6 页

第 3 章 鉴权交互
3.1 uboot 指令说明
在uboot 回复96 命令后，工具将与UBOOT 进行下列交互：
 扩展现有发送命令，增加两个CMD，分别用于两次握手：
BSL_CMD_AUTH_BEGIN  = 0x41,
BSL_CMD_AUTH_END   = 0x42,
 扩展现有响应命令，用于接收M1 和应答
BSL_REP_AUTH_M1_DATA    = 0xBD
3.2 uboot 交互说明
1． 发送鉴权开始命令，并等待 UBOOT 返回 M1 数据
 PC->UBOOT 命令 BSL_CMD_AUTH_BEGIN (0x41)：
命令含义：发送鉴权开始指令。
命令格式：无数据区。
HEADER CMD TYPE DATA LENGTH DATA CRC TAIL
7E 00 41 00 00 NULL XX XX 7E

 UBOOT->PC 命令：
命令应答： 成功返回 BSL_REP_AUTH_M1_DATA（0xBD）。
失败返回 BSL_REP_OPERATION_FAILED（0x84）
HEADER CMD TYPE DATA LENGTH DATA CRC TAIL
7E 00 BD LENGTH(M1) M1 XX XX 7E


2． 发送 M2 数据，并等待 UBOOT 返回鉴权成功与否的结果返回
 PC->UBOOT 命令 BSL_CMD_AUTH_END(0x42)：
命令含义：发送 M2。
命令格式：含数据区 M2。
HEADER CMD TYPE DATA LENGTH DATA CRC TAIL
7E 00 42 LENGTH (M2) M2 XX XX 7E

 UBOOT->PC 命令：
命令应答： 成功返回 BSL_REP_ACK（0x80）。
验证失败返回 BSL_REP_OPERATION_FAILED（0x84）
HEADER CMD TYPE DATA LENGTH DATA CRC TAIL
7E 00 80 00 00 NULL XX XX 7E
