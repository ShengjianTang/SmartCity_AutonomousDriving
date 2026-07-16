# PDF 逐页文本：hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/产线-Upgrade_Download_R27.22.3801/Upgrade_Download_R27.22.3801/Download_R27.22.3801/Doc/Customized/鉴权/Download_AUTH_客制化动态库使用说明.pdf

- SHA-256：`a536da99b663602b7368e723bd969f1dca8667806a1c12548e5615fe03a39109`

## 第 1 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
1 / 6
Download_ Authentication_动态库使用说明











Document Number:  Document Version: 1.0
Owner: Leiming.sun Date: 2021-10-18
Document Type:
NOTE: ALL MATERIALS INCLUDED HEREIN ARE COPYRIGHTED AND CONFIDENTIAL
UNLESS OTHERWISE IN DICATED. The information is intended only for the person or
entity to which it is addressed and may contain confidential and/or privileged material. Any
review, retransmission, dissemination, or other use of or taking of any action in reliance
upon this information by persons or entities other than the intended recipient is prohibited.

This document is subject to change without notice. Please verify that your company has the
most recent specification.

Copyright © 2019  UNISOC Communications Inc.


www.UNISOC.com

## 第 2 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
2 / 6
修订记录

版本  日期 作者 说明
V1.0 2021-10-18  草稿


## 第 3 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
3 / 6
目录
Download_ Authentication_动态库使用说明 ............................................................................... 1
修订记录......................................................................................................................................... 2
目录................................................................................................................................................. 3
1. 目的............................................................................................................................................. 4
1.1. 缩略词说明...................................................................................................................... 4
1.2. 参考文档.......................................................................................................................... 4
2. 环境配置..................................................................................................................................... 5
2.1. 生成 Auth.dll 动态库 ...................................................................................................... 5
2.2. 添加 AUTH.dll ................................................................................................................ 5
3. 动态库接口说明......................................................................................................................... 6
3.1. 功能开关.......................................................................................................................... 6
3.2. 服务器交互接口.............................................................................................................. 6


## 第 4 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
4 / 6

1. 目的
本文介绍 Download 工具客制化鉴权功能 Authentication 动态库的方法，适用于所有 PC 上
位机程序开发人员和对外合作开发人员。

1.1. 缩略词说明
名称 全称 定义
AUTH Authentication 鉴权
M1  UE 侧返回鉴权数据
M2  服务器返回鉴权数据

1.2. 参考文档



## 第 5 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
5 / 6

2. 环境配置
2.1. 生成 Auth.dll 动态库
根据第 3 章接口说明内容，填充和配置接口实现，工具将根据接口的具体实现完成
鉴权功能流程。
2.2. 添加 AUTH.dll
将编译出的鉴权动态库放到工具包/Bin/App/Auth/Auth.dll 路径上。

 结构说明：
——Bin
|——Download.exe
 |——Customized
  |——Auth
   |——Auth.dll
  |——其余客制化模块


## 第 6 页


 Copyright 2019 UNISOC Communications Inc.                               Confidential and Proprietary.
6 / 6
3. 动态库接口说明
3.1. 功能开关
【语法】
 AUTH_API int EnableAuth();
【说明】
              返回鉴权功能是否打开
【参数】
 null
【返回值】
 0  ：不打开鉴权功能
 1 ： 打开鉴权功能

3.2. 服务器交互接口
【语法】
AUTH_API AUTH_ID ServerAuth(AUTH_DUT_T* lpInBuff, AUTH_SECURE_T* lpOutBuff, unsigned long*
nOutLen);
【说明】
              与服务器交互，返回 M2 数据流
【参数】

参数 IN/OUT 说明
AUTH_DUT_T* lpInBuff IN 输入从 CE 侧返回的 M1 数据
AUTH_SECURE_T* lpOutBuff OUT 输出从服务器返回的 M2 数据
unsigned long* nOutLen OUT 输出 M2 数据的 Size
【返回值】
typedef enum AUTH_ID {
 APP_AUTH_SUCCESS = 0x200,
 APP_AUTH_DUT_FAIL = 0x201,
 APP_AUTH_SURVER_FAIL = 0x202,
 APP_AUTH_SURVER_SIZE_IS_ZEOR = 0x203,
};
