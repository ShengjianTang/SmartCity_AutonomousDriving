# PDF 逐页文本：hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/DRIVER_R4.19.5001/DRIVER_R4.19.5001/Doc/Driver Install and Uninstall Guide.pdf

- SHA-256：`3c6ae0a5f997bb693b33918fc1b1caa8155da55c82fedb08e5b1f693a468367b`

## 第 1 页

Driver Install And
Uninstall Guide

## 第 2 页

Revision History
2
Version Date Notes
V1.0 2019/11/4 Create
V1.1 2019/11/11 Modified after review

## 第 3 页

Document Information
3
Chip Platform OS Version Keyword
Common Win7(32/64)/Win8(32/64)/Win10(32/64) ADB Driver, USB to serial port driver,Modem Driver

## 第 4 页

Contents
Introduce Driver Package1
Uninstall Driver2
Install Driver3
Q&A44

## 第 5 页

Introduce Driver Package
5
 Driver_Release_Notes.xlsx:
This document shows the changes of driver releases
 DriversForWin10:
This folder include all driver files for Win10 OS platform
DriverSetup.exe: main installer
config.reg:  configure for ignore HW serial number by modify system register
dpinst.xml: installer configure file
DPInst32/64.exe: installer using dpinst.xml
Drivers: driver inf/cat/bin files
*.inf:      driver install files
*.cat:     digital signed files
amd64: bin files folder for Win64 platform
i386: bin files folder for Win32 platform
DriverUninstall32/64.exe: uninstall drivers for Win32 / Win64 platform
 DriversForWin78:
Drivers for Win7 and Win8 OS platform
It is same as the folder “DriversForWin10”
│  Driver_Release_Notes.xlsx
│
├─DriversForWin10
│  │  config.reg
│  │  dpinst.xml
│  │  DPInst32.exe
│  │  DPInst64.exe
│  │  DriverSetup.exe
│  │  DriverUninstall32.exe
│  │  DriverUninstall64.exe
│  │
│  └─Drivers
│      │  *.cat
│      │  *.inf
│      │
│      ├─amd64
│      │      *.sys
│      │      WdfCoInstaller01009.dll
│      │      winusbcoinstaller2.dll
│      │
│      └─i386
│              *.sys
│              WdfCoInstaller01009.dll
│              winusbcoinstaller2.dll
│
└─DriversForWin78
│  config.reg
│  dpinst.xml
│  DPInst32.exe
│  DPInst64.exe
│  DriverSetup.exe
│  DriverUninstall32.exe
│  DriverUninstall64.exe
│
└─Drivers
├─amd64
└─i386

## 第 6 页

Uninstall Driver
6
 How to uninstall drivers:
 For Win32 platform
Run DriverUninstall32.exe with administrator privilege
 For Win64 platform
Run DriverUninstall64.exe with administrator privilege

## 第 7 页

Install Driver
7
 Uninstall drivers before install new drivers
 How to install drivers:
 Fully Install (Recommend)
1. Remove the USB connection for all UNISOC products
2. For Win10, enter the folder “DriversForWin10” then
For Win7 or Win8, enter the folder “DriversForWin78” then
3. Run DriverSetup.exe with administrator privilege
4. Follow install wizard until all steps complete
5. Connect the UNISOC device by USB cable and the system will install the driver automatically
 Upgrade Install
1. Close all programs ( such as Download or Logel tool) that will use ports or adb
2. Open Device Manager (Right click my computer and select “Manager”, and the select the Device Manager node)
3. Connect the UNISOC device to the PC by USB cable
4. New devices will show in the Device Manager
5. Follow the steps in next  page

## 第 8 页

 Step1. Select the device and right click to Upgrade Driver Software…
 Step2. Click “Brows my computer for driver software”
 Step3. Click “Let me pick from a list of device drivers on my computer”
 Step4. Click “Install from disk”
Then click “Brows” to select the inf
file which locate the driver package
DriversForWin10/Drivers for Win10
or DriverForWin78/Driver for Win7
and Win8
 Step5. Click “Next”
If there is not only one item
listed, please select new one
and then click “Next”
 Step6. Wait until complete
 Step7. Repeat 1-6 for other devices
 Notice:
There is a simple way:
In step3, you can click “Brows” to
locate to DriversForWin10 folder
for Win10 or DriversForWin78
folder for Win7 and Win8, and then
go to step 5.
Driver Install – Update Install
8
1 2 3
4 5 6
Locate to inf
file folder

## 第 9 页

Q&A
9
 Q: Why windows system gives the warning of Windows Security when installing?
 A: It is normal because UNISOC provides drivers with only UNISOC signature and no WHQL verification.
Just ignore by clicking “Install this driver software anyway" to skip the warning and continue to install.

## 第 10 页

Q&A
10
 Q: How to check the driver system version?
 A: There are two version information in release notes
 Driver Package Version
Identify unique driver package
 Driver INF and Binary File Version and Date
Usually binary files will not be recompiled, and only modify the INF files, so INF and Binary Files are not
changed in different driver package. But INF file will update date information, so after install completely
please check device property in device manage to check the date and version if same as this.
Driver Package Verison
Driver INF & Binary File
Verison

## 第 11 页

Q&A
11
 Q: How to collect log information if install failed?
 A: 1. Setup log:
Windows system will log the setup information for driver installing, and this file is stored at
C:\Windows\inf\setupapi.dev.log
2. Device status: get the screen shot as bellow:
Click property of device in Device Manager, and device status is
displayed in the “General” tab. If device got any error, the error
information will be listed in this view.

## 第 12 页

Q&A
12
 Q: How to check device vid and pid?
 A: Click property of device in device manager and then click “Details” tab
Select “Hardware ID” in property combo box, then value list will show VID and PID, like below screen shot.

## 第 13 页

THANKS
本文件所含数据和信息都属于紫光展锐所有的机密信
息，紫光展锐保留所有相关权利。本文件仅为信息参
考之目的提供，不包含任何明示或默示的知识产权许
可，也不表示有任何明示或默示的保证，包括但不限
于满足任何特殊目的、不侵权或性能。当您接受这份
文件时，即表示您同意本文件中内容和信息属于紫光
展锐机密信息，且同意在未获得紫光展锐书面同意前
，不使用或复制本文件的整体或部分，也不向任何其
他方披露本文件内容。紫光展锐有权在未经事先通知
的情况下，在任何时候对本文件做任何修改。紫光展
锐对本文件所含数据和信息不做任何保证，在任何情
况下，紫光展锐均不负责任何与本文件相关的直接或
间接的、任何伤害或损失。
请参照交付物中说明文档对紫光展锐交付物进行使用
，任何人对紫光展锐交付物的修改、定制化或违反说
明文档的指引对紫光展锐交付物进行使用造成的任何
损失由其自行承担。紫光展锐交付物中的性能指标、
测试结果和参数等，均为在紫光展锐内部研发和测试
系统中获得的，仅供参考，若任何人需要对交付物进
行商用或量产，需要结合自身的软硬件测试环境进行
全面的测试和调试。
