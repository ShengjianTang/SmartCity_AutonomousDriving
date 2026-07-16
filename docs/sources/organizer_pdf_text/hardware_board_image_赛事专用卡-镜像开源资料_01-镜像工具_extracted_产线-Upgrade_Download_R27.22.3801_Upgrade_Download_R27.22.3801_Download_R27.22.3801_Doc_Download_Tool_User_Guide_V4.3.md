# PDF 逐页文本：hardware/board_image/赛事专用卡-镜像开源资料/01-镜像工具/extracted/产线-Upgrade_Download_R27.22.3801/Upgrade_Download_R27.22.3801/Download_R27.22.3801/Doc/Download Tool User Guide V4.3.pdf

- SHA-256：`1b5fb35c518a2a44b8f0728f0fab42dc566462ccd4410babeb46046d12c3c9a7`

## 第 1 页



Download Tool User Guide


Issue             V4.3
 Date             10-Sep -2021

 UNISOC (Shanghai) Technologies Co., Ltd.



## 第 2 页


Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies
Co., Ltd.
i

Copyright © UNISOC (Shanghai) Technologies Co., Ltd.  All rights reserved.
All data and information contained in or disclosed by this document is confidential and proprietary information
of UNISOC (Shanghai) Technologies Co., Ltd. (hereafter referred as UNISOC) and all rights therein are
expressly reserved . This document is provided for reference purpose, no license (express or implied, by estoppel
or otherwise) to any intellectual property rights i s granted by this document , and no express and implied
warranties, including but without limitation, the implied warranties of fitness for a ny particular purpose, and
non-infringement, as well as any performance. By accepting this material, the recipient a grees that the material
and the information contained therein is to be held in confidence and in trust and will not be used, copied,
reproduced in whole or in part, nor its contents revealed in any manner to others without the express written
permission of  UNISOC. UNISOC may make any changes at any time without prior notice. Although every
reasonable effort is made to present current and accurate information, UNISOC makes no guarantees of any
kind with respect to the matters addressed in this document. In n o event shall UNISOC be responsible or liable,
directly or indirectly, for any damage or loss caused or alleged to be caused by or in connection with the use of
or reliance on any such content.
Please refer to the UNISOC Documents in the UNISOC Deliverable s for the use of the Deliverables. Any loss
caused by the modification, customization or use of the UNISOC Deliverables in violation of the instructi ons
in the UNISOC Documents shall be undertaken by those who conduct so. The performance indicators, test
results and parameters in the UNISOC Deliverables are all obtained in the internal development and test system
of UNISOC and are only for the reference. Before using UNISOC Deliverables commercially or conducti ng
mass production of the Deliverables, compreh ensive testing and debugging in combination with its own
software and hardware test environment are pre -requisite.













UNISOC (Shanghai) Technologies Co., Ltd.


## 第 3 页


About this document

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. i

About this document
Purpose
This document aims to describe how to use the download tools of UNISOC and how to conduct factory testing.
Intended audience
This document is intended primarily for technical personnel of production line testing and developers and testing
personnel of UNISOC.

Symbol conventions
Symbol Description
 Calls attention to important information, best practices and tips.
NOTE is used to address information not related to personal injury, equipment damage,
and environment deterioration.

Calls attention  to error-prone operations.
CAUTION is used to address information not related to personal injury, equipment
damage, and environment deterioration.
 Calls attention  to irreversible operations.
WARNING is used to address information not related to personal i njury and environment
deterioration.

Acronyms and abbreviations
Acronym and Abbreviation Full Name
MMI Man Machine Interface
PCBA Printed Circuit Board Assembly

## 第 4 页


About this document

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. ii

Revision history
Issue Date Description
V1.0 28-Sep-2017 This issue is the first official release.
V2.0 01-Apr-2018 Update Logo.
V2.1 25-Jul-2019  Add  content in FAQ.
 Update some contents.
V3.0 23-Sep-2020  Update the screenshot of new -version tool interface.
 Add function description of some interfaces.
 Add FAQ, and sup plement log level configuration.
 Add function description for the first entry of the mode after boot .
 Add configuration description of Sparse2Raw.
 Add introduction of Inproduction Flag.
V4.0 26-Jan-2021  Add description of  the entry method 1.4.3 Keyless triggering  download
mode.
 Add  6 Command line download.
V4.1 01-Mar-2021  Update UI interface description of  2 Tool introduction.
 Update description of 8.6 Set tool Log level
V4.2 13-Apr-2021  Add  content in FAQ.
 Add introduction of the function Download Img file.
V4.3 10-Sep-2021  Modify the document name from UNISOC Download User Guide to
Download Tool User Guide .
 Modify the content structure, and optimize the content.
− Delete the introduction of the function Download Img file.
− Divide FAQ into 7 Interface error message and 8 F AQ and
supplementary information.

Keywords
FactoryDownload,  UpgradeDownload,  ResearchDownloa d

## 第 5 页


Contents

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. iii

Contents
1 Overview ................................ ................................ ................................ ................................ .. 1
1.1 Function introduction ....................................................................................................................................................... 1
1.2 Runtime environment ....................................................................................................................................................... 1
1.2.1 Hardware requirement .............................................................................................................................................. 1
1.2.2 Software requirement................................................................................................................................................ 2
1.3 Download environment setup .......................................................................................................................................... 2
1.4 Entry methods of download mode................................................................................................................................... 3
1.4.1 Pin pull-down or pull-up........................................................................................................................................... 3
1.4.2 Key triggering............................................................................................................................................................ 3
1.4.3 Keyless triggering ..................................................................................................................................................... 4
1.5 Watchdog........................................................................................................................................................................... 4
2 Tool introduction ................................ ................................ ................................ .......................  5
2.1 Main interface ................................................................................................................................................................... 5
2.2 Tool bar.............................................................................................................................................................................. 6
2.3 Status bar ........................................................................................................................................................................... 6
3 FactoryDownload user guide................................ ................................ ................................ ...... 9
3.1 Download settings ............................................................................................................................................................ 9
3.1.1 Main Page .................................................................................................................................................................. 9
3.1.2 Options..................................................................................................................................................................... 10
3.1.3 Multi Languages...................................................................................................................................................... 12
3.1.4 LCD Configure........................................................................................................................................................ 12
3.1.5 Customization.......................................................................................................................................................... 12
3.2 Operati ng instruction ...................................................................................................................................................... 13
3.2.1 Load a file ................................................................................................................................................................ 13
3.2.2 Set download parameters ........................................................................................................................................ 13
3.2.3 Start downl oad......................................................................................................................................................... 13
3.2.4 Complete downl oad ................................................................................................................................................ 14
3.2.5 Exit download.......................................................................................................................................................... 15
4 UpgradeDownload user guide ................................ ................................ ................................ .. 16
4.1 Download settings .......................................................................................................................................................... 16
4.1.1 Main Page ................................................................................................................................................................ 16
4.1.2 Options..................................................................................................................................................................... 17
4.1.3 Multi Languages...................................................................................................................................................... 18
4.1.4 LCD Configure........................................................................................................................................................ 18
4.1.5 Customization.......................................................................................................................................................... 18
4.2 Operati ng instruction ...................................................................................................................................................... 19
4.2.1 Load a file ................................................................................................................................................................ 19
4.2.2 Set download parameters ........................................................................................................................................ 19

## 第 6 页


Contents

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. iv

4.2.3 Start downl oad......................................................................................................................................................... 20
4.2.4 Complete downl oad ................................................................................................................................................ 20
4.2.5 Exit download.......................................................................................................................................................... 21
5 ResearchDownload user guide ................................ ................................ ................................ . 22
5.1 Download settings .......................................................................................................................................................... 22
5.1.1 Main Page ................................................................................................................................................................ 22
5.1.2 Options..................................................................................................................................................................... 23
5.1.3 Backup ..................................................................................................................................................................... 25
5.1.4 Flash Operations...................................................................................................................................................... 27
5.1.5 Multi Languages...................................................................................................................................................... 29
5.1.6 LCD Configure........................................................................................................................................................ 29
5.1.7 MCP Type ................................................................................................................................................................ 29
5.1.8 V ol-Freq Tuni ng ...................................................................................................................................................... 30
5.1.9 Uart Port Switch ...................................................................................................................................................... 31
5.2 Operati ng instruction ...................................................................................................................................................... 32
5.2.1 Load a file ................................................................................................................................................................ 32
5.2.2 Set download parameters ........................................................................................................................................ 32
5.2.3 Start downl oad......................................................................................................................................................... 33
5.2.4 Complete downl oad ................................................................................................................................................ 33
5.2.5 Exit download.......................................................................................................................................................... 34
6 Command line download ................................ ................................ ................................ .........  35
6.1 Parameter format ............................................................................................................................................................ 35
6.2 Download example ......................................................................................................................................................... 35
7 Interface error message analysis and solution ................................ ................................ ...........  37
7.1 [DL1150] Incompati ble partition................................................................................................................................... 37
7.2 [UB1142] Wait input time out........................................................................................................................................ 37
7.3 [DL1138] Image size is over its partition...................................................................................................................... 37
7.4 [PS2262] User cancel ..................................................................................................................................................... 38
7.5 [UB1254] Software has not supported thi s feature ...................................................................................................... 38
7.6 [PS2257] Uart send error ............................................................................................................................................... 38
7.7 [UB1132] Operation failed ............................................................................................................................................ 39
7.8 [SW2020] NV data read in phone i s crashed................................................................................................................ 39
7.9 [SW2021] NV data in nvitem.bin i s crashed ................................................................................................................ 39
8 FAQ and supplementary information ................................ ................................ ........................  40
8.1 Unrecognize the port ...................................................................................................................................................... 40
8.2 Fail to capture the port after modifying the port name ................................................................................................ 40
8.3 Local file has a .flag suffix after decompressi ng Pac ................................................................................................... 40
8.4 Modify required or opti onal attributes of files in the partition list.............................................................................. 41
8.5 Record ID information of the module ........................................................................................................................... 41
8.6 Set tool Log level............................................................................................................................................................ 42

## 第 7 页


Contents

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. v

8.7 Check MCP (DDR or EMMC) ...................................................................................................................................... 42
8.8 Set password for downl oad tool .................................................................................................................................... 43
8.9 Inproduction Flag function............................................................................................................................................. 44
8.10 Set the writing length of FactoryDownload SN ......................................................................................................... 44
8.11 Set the prefix of the SN written in by FactoryDownload........................................................................................... 44
8.12 Set the entry mode of the first booti ng after FactoryDownload download............................................................... 45
8.13 Configure Sparse2Raw in FactoryDownload.i ni........................................................................................................ 46
8.14 Upgrade software usi ng UpgradeDownload............................................................................................................... 46
8.15 Packet usi ng ResearchDownload ................................................................................................................................ 46
8.16 Erase Flash using ResearchDownl oad ........................................................................................................................ 47
8.17 Prompt message (Size is too large) occurs when ResearchDownload reads FixNV write-back............................. 48
8.18 Set ResearchDownload Debug Level.......................................................................................................................... 48


## 第 8 页


List of figures

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. vi

List of figures
Figure 1-1 Download environment of the PCBA stage of production line ................................ ...... 2
Figure 2-1 Main interface of FactoryDownload ................................ ................................ ............  5
Figure 2-2 Status bar................................ ................................ ................................ ....................  7
Figure 2-3 Successful download with mobile phone connected ................................ .....................  7
Figure 2-4 Successful download with mobile phone disconnected ................................ .................  8
Figure 2-5 Failed download ................................ ................................ ................................ .........  8
Figure 3-1 FactoryDownload Main Page ................................ ................................ ......................  9
Figure 3-2 FactoryDownload Options................................ ................................ .......................... 11
Figure 3-3 FactoryDownload Customization................................ ................................ ...............  12
Figure 3-4 FactoryDownload in download status ................................ ................................ ........  14
Figure 3-5 FactoryDownload Input SN input box................................ ................................ ........  14
Figure 3-6 Suspend FactoryDownload download ................................ ................................ ........  14
Figure 3-7 FactoryDownload download completed ................................ ................................ ..... 14
Figure 3-8 FactoryDownload waits for download again ................................ ..............................  14
Figure 4-1 UpgradeDownload Main Page ................................ ................................ ...................  16
Figure 4-2 UpgradeDownload Options ................................ ................................ .......................  17
Figure 4-3 UpgradeDownload Customization ................................ ................................ .............  19
Figure 4-4 UpgradeDownload in download status ................................ ................................ ....... 20
Figure 4-5 UpgradeDownload download completed................................ ................................ .... 20
Figure 4-6 UpgradeDownload waits for download again ................................ .............................  20
Figure 5-1 ResearchDownload Main Page ................................ ................................ ..................  22
Figure 5-2 ResearchDownload Options ................................ ................................ ......................  24
Figure 5-3 ResearchDownload Backup................................ ................................ .......................  26
Figure 5-4 ResearchDownload Flash Operations................................ ................................ .........  27
Figure 5-5 ResearchDownload MCP Type ................................ ................................ ..................  30
Figure 5-6 ResearchDownload V ol-Freq Tuning ................................ ................................ .........  31
Figure 5-7 ResearchDownload Uart Port Switch ................................ ................................ .........  32
Figure 5-8 ResearchDownload in download status ................................ ................................ ...... 33

## 第 9 页


List of figures

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. vii

Figure 5-9 ResearchDownload download completed ................................ ................................ ... 33
Figure 5-10 ResearchDownload waits for download again ................................ ..........................  33
Figure 6-1 Successful CmdDloader download ................................ ................................ ............  36
Figure 6-2 Failed CmdDloader download ................................ ................................ ...................  36
Figure 8-1 Enter password ................................ ................................ ................................ .........  43
Figure 8-2 Reset password ................................ ................................ ................................ .........  44
Figure 8-3 Packet setting................................ ................................ ................................ ............  47
Figure 8-4 Packeting complete prompt ................................ ................................ .......................  47
Figure 8-5 Erase Memory using ResearchDownload ................................ ................................ ... 48


## 第 10 页


List of tables

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. viii

List of tables
Table 1-1 Hardware requirement ................................ ................................ ................................ .. 1
Table 1-2 Software requirement................................ ................................ ................................ .... 2
Table 1-3 Hardware resource ................................ ................................ ................................ ........  3
Table 2-1 Description of the main interface................................ ................................ ...................  5
Table 2-2 Description of Tool bar ................................ ................................ ................................ . 6
Table 2-3 Description of Status bar ................................ ................................ ...............................  7
Table 3-1 Description of FactoryDownload Main Page................................ ................................ .. 9
Table 3-2 Description of FactoryDownload Options ................................ ................................ .....11
Table 4-1 Description of UpgradeDownload Main Page ................................ ..............................  17
Table 4-2 Description of UpgradeDownload Options ................................ ................................ .. 18
Table 5-1 Description of ResearchDownload Main Page ................................ .............................  23
Table 5-2 Description of ResearchDownload Options................................ ................................ .. 24
Table 5-3 Read Flash configuration item................................ ................................ .....................  27
Table 5-4 Erase Flash configuration item ................................ ................................ ....................  28
Table 5-5 Write Flash configuration item ................................ ................................ ....................  28

## 第 11 页


1 Overview

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 1

1 Overview
1.1 Function introduction
Download means to write mobile software into hardware module through a download tool. The UNISOC
download tools support  simultaneous download  of a software for multiple modules in a relatively efficient and
simple way. Once the module is connected to the port correctly and the co rrect mode is set, the program detect s it
and start s the download process automatically. After downloading a software, you need to replace the module
manually. Then, the program repeat s the process.
UNISOC provides three download tools for different scenarios.
 FactoryDownload
This tool is commonly used for production download in Printed Circuit Board Assembly (PCBA) stage. It
can erase the production parameters in production line, such as ProdNV and Fix NV partitions, while
initializing PhaseCheck. It supports SN number pre-writing.
 UpgradeDownload
This tool is commonly used for software upgrade in PCBA stage or complete machine stage of a mobile
phone. The calibration flag bit is checked before the upgrade, and the upgrade cannot be performed if the
calibration flag bit is not set. The main feature of this tool is that it back s up NV parameters compulsively
before upgrade, and dose  not initialize PhaseCheck and ProdNV partitions.
 ResearchDownload
The tool is commonly used for R&D debugging. It supports  many functions, including Flash partition
reading and writing, NV parameters, PhaseCheck and ProdNV partitions back up, and downloaded file
packing. The tool does not initialize ProdNV and PhaseCheck partitions by default.
1.2 Runtime environment
1.2.1 Hardware requirement
The basic requirement of hardware is shown in T able 1-1.
Table 1-1 Hardware requirement
Hardware Basic requirement
PC  CPU: i5 or later version s
 Internal memory: 8GB or larger
USB cable No special requirement.
USB expansion card USB expansion card is necessary for downloading a software for multiple modules
simultaneously .

## 第 12 页


1 Overview

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 2

Hardware Basic requirement
Power supply   Common DC power supply requires UNISOC voltage stabilizer.
 Precision DC power supply outputs stably.

1.2.2 Software requirement
The basic requirement of software is shown in T able 1-2.
Table 1-2 Software requirement
Software Version requirement
OS version  Windows7, Windows10

1.3 Download environment setup
Download using FactoryDownload or UpgrageDownload
When using FactoryDownload  or UpgradeDownload  to download in the PCBA stage of production line, an
example of environment setup is shown in Figure 1-1.
Figure 1-1 Download environment of the PCBA stage of production line



## 第 13 页


1 Overview

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 3

Table 1-3 Hardware resource
Device Description

 PC meets the requirement of 1.2 Runtime environment.
 PC is connected to the testing module through a USB cable.
 USB_Hub is equipped with a powered USB Hub or a USB expansion card.

DC power supply  uses precision DC power supply or uses common DC power supply with
UNISOC voltage stabilizer.

Voltage stabilizer.

Download fixture.

Download using ResearchDownload
ResearchDownload is not commonly used in the scenario of downloading a software simultaneously for multiple
modules. Therefore, it does not need USB Hub, USB expansion card, and voltage stabilizer, and its download
environment setup is very simple.
 When do wnloading a module through the USB cable, a USB cable is needed to connect the PC and the
module directly, and a common regulated  power supply or a battery is needed  to supply power to the module.
 When downloading a module through the Uart port, a USB Uart board and flat cables are needed
additionally.
1.4 Entry methods of download mode
1.4.1 Pin pull-down or pull-up
When Flash is not empty, the PCBA stage uses fixture to download. The module enters the download mode by
detecting the pull-down or pull-up state of a specific pin when the mobile phone is  powered on. It depends on the
specific project to use the pin pull-down or pull -up to enter the download mode. For example, UIS8910DM pulls
up the U1TXD pin. The specific method of pin pull-down or pull-up is as follows.
 Pin pull-down
− The nBoot pin is ground -connected.
− The U1TXD pin is connected to a 1 kΩ pull-down resistor.
 Pin pull-up: pull up the U1TXD pin.
Click
  on Tool bar (such as the Tool bar of FactoryDownload) and power on the mobile phone , and wait the
module to enter the download mode.
1.4.2 Key triggering
In complete machine stage, key triggering method is commonly used to enter the download  mode.

## 第 14 页


1 Overview

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 4

 On UNISOC smartphone platforms, press and hold  Volume (KE YIN0) and power on the mobile phone at
the same time, the mobile phone enter s the download mode.
 On UNISOC feature phone platforms, press and hold KE YIN0 or KE YOUT0 and power on the mobile
phone at the same time, the mobile phone enter s the download mode. Different programs may define its own
triggering keys of entering  the download mode.
1.4.3 Keyless triggering
Before using this functi on when the mobile phone is power off, assign  the value of DownloadByPoweroff in
BMFileType.ini to 1. When this function is enabled, connect the USB cable directly af ter clicking Start
Downloading on Tool bar, and the mobile phone enters the download mode.

 The precondition of keyless triggering is that the Flash of the mobile phone must be empty, or the previous
download of the mobile phone is in Pass status.
 Failed download  disables keyless triggering. Follow the methods below to solve this problem.
− Enter the download mode forcibly through key triggering method  (see 1.4.2 Key triggering ).
− Refer to 1.5 Watchdog to make the mobile phone reboot automatically.
− Reboot the mobile phone forcibly.
1.5 Watchdog
The prerequisite to enable this function is that the mobile phone supports Watchdog commands ( OpenWatchDog
and CloseWatchDog). To enable the function, assign the value of WatchDog field in BMFileType.ini to 1. The
WatchDogTime field is used to set the watchdog  timeout. The default value is 150000 ms.
After enabling the function, the download tool send s the command OpenWatchDog after FDL2 starts , and send
the command CloseWatchDog before Poweroff. If the download fails, the mobile phone performs a reboot action
after the timeout of Watchdog.

Set WatchDogTime according to the actual situation. It should at least exceed the whole packet download
time.

## 第 15 页


2 Tool introduction

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 5

2 T ool introduction
2.1 Main interface
Apart from the tool name displayed at the top -left corner the prompt message at the button -right corner, the main
interfaces of FactoryDownload,  UpgrageDownload and ResearchDownload  are almost the same.
The main interface of FactoryDownload is taken as an example to  introduce its basic operations.
Figure 2-1 Main interface of FactoryDownload
2
1
2 3
4
5
6


Table 2-1 Description of the main interface
No. Item Description
1 Title bar It displays the name and version of the tool.
2 Tool bar It contains Load packet, Settings , Start downloading, Stop
downloading, and About buttons .
3 Packet information It shows the name, version, size and load time of the packet.
4 Status bar It shows status information, including the download device number,
download port number, current ope ration file name or operation
description, current operation status, download progress, download
time, download rate.
5 Tool log setting  It can open the tool log path and set tool log level.

## 第 16 页


2 Tool introduction

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 6

No. Item Description
6 Prompt message  It can be replaced through bin/rdl_bkmark.bmp file.

2.2 Tool bar
Table 2-2 Description of Tool bar
Button
icon
Meaning Description

Load packet This button is to select the packet and configuration file to download, where
configuration file is optional. This button is disabled when the download  starts, and be
available when the download stops.

Settings  This button is to set the download parameters. Click it to open the dialog box for setting.
This button is disabled when the download  starts, and be available when the download
stops.

Start
downloading
This button is to detect and open the available ports, an d to prepare for the download
process. There are two download modes.
 Automatic mode: The program automatically detects if there is a module connected
to the port. If yes, the download  process starts automatically. When th e download
finishes, the program automatically detects again if there is a module connected to
the port.
 Manual mode: The  program reports the dow nload result after the module is
download ed, and pauses. The download starts again only when you click Start.
This button is disabled when running the program for the first time, and yo u can only
start the download  process after setting it first.

Stop
downloading
This button is to stop the download process. This button is available only when you
click Start and the program opens the available ports.
In order to protect NV files, the Stop button is unavailable when entering the process
to avoid clicking. In any other cases, you can click thi s button to stop the download
process.
Only after the download  process stops can the program be exited.

About  This button is to open the tool Doc directory quickly. You can check the meaning of
error message on the interface or open the User Guide.

2.3 Status bar
The Status bar is to display status information, including port status, download status and download result, as
shown in Figure 2-2.

## 第 17 页


2 Tool introduction

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 7

Figure 2-2 Status bar


Table 2-3 Description of Status bar
Item  Description
No Number the downloading devices in order. If restarted, the tool bind s to the port numbers
according to the new connection order, and you need to pay attention to the insertion
order.
Port Available port number, and X means that this port cannot be opened.
Step The current operation document name or operation description.
Status  The current operation status.
Progress  The progress bar.
 Waiting means that an operation is in progress.
 Passed means that the download  succeeds, and the mobile phone is connected.
 Ready means that the download  succeeds, and the mobile phone is disconnected.
 Failed means that the download  fails.
Time[s] Time of a single download . The unit is s.
MCP Type  The MCP Type (Flash size) information of the current download device.
Rate[MB/s] Download rate.
 Actual download: the current ly downloaded data. The unit is MB.
 Average rate: the current average download rate. The unit is MB/s. The actual
download data determines the average rate. And the actual download data may differ
from the Pac size.
 Peak rate: the maximum download rate. The unit is MB/s.

 When the download  succeeds, and the mobile phone is connected, the interface information is shown in
Figure 2-3.
Figure 2-3 Successful download with mobile phone connected


 When the download succeeds, and the mobile phone is disconnected, the interface information is shown in
Figure 2-4

## 第 18 页


2 Tool introduction

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 8

Figure 2-4 Successful download with mobile phone disconnected


 When the download  fails, the interface information is shown in Figure 2-5.
Figure 2-5 Failed download


## 第 19 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 9

3 FactoryDownload user guide
FactoryDownload is applicable for production dow nload in PCBA stage. The tool can initialize PhaseCheck,
divide ProdNV , erase NV parameters, and pre-write SN number. It erase s Running NV forcibly, and writes in Fix
Nv. Therefore, you need to backup NV as needed before using this tool.
3.1 Download settings
Click
  to enter the setting interface of FactoryDownload, as shown in  Figure 3-1. The interface contains
five tabs: Main Page, Options, Multi Language s, LCD Configure, and Customization.
Figure 3-1 FactoryDownload Main Page


3.1.1 Main Page
As shown in Figure 3-1, Main Page is used to configure the port and its baud rate, and display information
including downloaded file version and Product. For more details, see T able 3-1.
Table 3-1 Description of FactoryDownload Main Page
Item name Description
Input SN When this check box is cleared, the tool write s in SN randomly. When selected , you
need to input SN.

## 第 20 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 10

Item name Description
Port Port setting.
You can select a certain port to download or select All. When selecting All, the tool
automatically detects available ports for downloading. A module corresponds to an
available port. When downloading a software for multiple modules simultaneously,
there are multiple available ports.
Baudrate Baud rate setting .
This is necessary only when downloading through U art.
Information bar Displays version and Product information above the file list.
Downloaded file list  FileID indicates the name of downloaded file.
 FileName displays the path to download the file.
 Base1 indicates the download address.
 Size1  indicates the file size (0x0 indicates that the file size is automatically
calculated by the download tool during download ).

3.1.2 Options
Options interface requires the support of FDL or Uboot module. As shown in Figure 3-2, only Reset to Normal,
PowerOff (selected  by default) and Dump Uboot Log can be selected . Other options can be implemented only by
modifying the configurations in FactoryDownload.ini.


## 第 21 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 11

Figure 3-2 FactoryDownload Options


Table 3-2 Description of FactoryDownload Options
Item name Description
Repartition It is selected  by default and indicates whether to repartition during download, which is
valid only for Nand or EMMC Flash products.
Keep Charge It is unavailable by default and indicates whether to enable charging during download,
which requires software support.
Uart Download It is unavailable by default and indicates whether to download over the serial port.
Reset to Normal It is cleared by default . It indicates that the tool sends a command to restart the mobile
phone in the last step of download.
Power Off It is selected by default and indicates that the tool sends a command to shut down the
mobile phone, which takes effect after unplugging the US B. This function requires
software support, and it needs to be selected  for built-in battery download.
Dump Uboot Log It is not commonly used and requires the software support of FDL2. If the downloa d fails,
the tool saves the log  in Uboot.
Read MCP Type  It is unavailable by default and requires software support.
Read Chip UID It is unavailable by default and requires software support.
Check Match  It is unavailable by default and requires software support.
DDR Check It is unavailable by default and req uires software support.

## 第 22 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 12

Item name Description
EMMC Check It is unavailable by default and requires software support.
Self Refresh It is unavailable by default and requires software support.
Check 2nd Hand
Mem
It is unavailable by default and requires software support.
Vpac Check It is unavailable by default and requires software support.

3.1.3 Multi Languages
Multi Languages is used to set multiple languages in NV . If the NV files selected on Main Page does not contain
multilingual information, the interface is empty. Selecting a language indicates that the mobile phone ’s Man
Machine Interface (MMI) enable s functions in this language.
3.1.4 LCD Configure
LCD Configure is used to configure LCD-related drivers in PS or User Img files.

Only when the downloaded file list contains  PS or UserImg file, LCD-related configuration information is
displayed on LCD Configure.
3.1.5 Customization
As shown in Figure 3-3, select Customization, and enter Customization.
Figure 3-3 FactoryDownload Customization



## 第 23 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 13

Bad Flash Rate
Select Check bad flash rate to set the maximum allowable value of bad flash rate. Enable Factory Download to
check the Flash bad flash rate of the mobile phone  that is waiting for software download (only supports Nand
Flash bad flash rate checking currently).
The precondition of enabling the Flash bad flash rate check ing function: The software  of the mobile phone  that is
waiting for software download  has the function of checking the bad flash rate of Flash.
After enabling the function, FactoryDownload check s the bad flash rate of the mobile phone ’s Nand Flash before
download. When the bad flash rate exceeds the maximum allowable value, the download is cancelled.
Inproduction Flag
The Inproduction Flag function is used infrequently. It is to write in the specified content, and then back them up
to the mobile phone when backing up Miscdata partiti on.
3.2 Operating instruction
Before download , set up the download environment according to 1.3 Download environment setup.
3.2.1 Load a file
Open the download tool and click
  to load a file that requires download.
3.2.2 Set download parameters
After the file is loaded successfully, click  to enter the setting interface, and set download parameters on
Main Page and Options.
 Set the port and Baud rate on Main Page. If you need to input SN manually, select Input SN.
 Check Reset to Normal or Power Off option according to the test requirements on Options.

 To set download parameters for mobile phone with built-in battery, it is recommended to select Reset to
Normal or Power Off option .
 The precondition of checking Power Off: The mobile software supports the Power Off function after the
download  is completed.
3.2.3 Start download
1. After the tool is set, click
  on Tool bar. The program automatically detects available ports and prepares
to download.
2. Set up the test environment, and trigger the download mode of mobile phone. The tool auto matically detects
the available ports and starts the download, as shown in  Figure 3-4.

## 第 24 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 14

Figure 3-4 FactoryDownload in download status


If Input SN is selected , the dialogue box prompts after FDL file is downloaded, as shown in Figure 3-5. Input SN
and click OK, the tool will continue to download.
Figure 3-5 FactoryDownload Input SN input box


If you click Suspend in Figure 3-5, the tool suspends download  as shown in Figure 3-6. Click
  in Figure
3-6 to resume download ing.
Figure 3-6 Suspend FactoryDownload download


3.2.4 Complete download
If the download succeeds and the module is connected, a green Passed is displayed on Tool bar, as shown in
Figure 3-7.
Figure 3-7 FactoryDownload download completed


If the download  succeeds and the module is disconnected, a blue Ready is displayed on Tool bar, as shown in
Figure 3-8. If you need to download again, replace the module and enter the download mode, the t ool
automatically start s the download without clicking
  in Tool bar again.
Figure 3-8 FactoryDownload waits for download again



## 第 25 页


3 FactoryDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 15

3.2.5 Exit download
If FactoryDownload is in automatic download status, other buttons on Tool bar are unavailable. Click  to
exit the automatic download status. In this case, other buttons on Tool bar are available. Y ou can click
  to
reload other files or close the tool directly.
.

## 第 26 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 16

4 UpgradeDownload user guide
UpgradeDownload is applicable for software upgrad e in PCBA stage or complete machine stage of mobile phone .
The main feature of the tool is the  compulsive backup for NV parameters (read back and then write in the mobile
phone) . It does not  operate  the PhaseCheck and ProdNV partitions. Before upgrading, the tool checks the
calibration flag bit. If the calibration fails, the upgrade cannot be performed.
4.1 Download settings
Click
  to enter the setting interface of UpgradeDownload , as shown in Figure 4-1. The interface contains
five tabs: Main Page , Options , Multi Language s, LCD Configure, and Customization.
Figure 4-1 UpgradeDownload Main Page


4.1.1 Main Page
As shown in Figure 4-1, Main Page is used to configure the port and its baud rate and display information
including downloaded file version and Product . For more details, see T able 4-1.

## 第 27 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 17

Table 4-1 Description of UpgradeDownload Main Page
Item name Description
Port Port setting .
You can select a certain port to download or select All. When selecting All, the tool
automatically detects available ports for download. A module corresponds to an
available port. When downloading  a software for multiple modules simultaneously,
there are multiple available ports.
Baudrate Baud rate setting .
Information bar Displays version and Product information above the file list.
Downloaded file list  FileID indicates the name of downloaded file.
 FileName displays the path to download the file.
 Base1 indicates the download address .
 Size1  indicates the file size (0x0 indicates that the file size is automatically
calculated by the download tool during download ).

4.1.2 Options
Options interface requires the support of FDL or Uboot module. As shown in Figure 4-2, only Reset to Normal,
PowerOff (selected  by default) and Dump Uboot Log can be selected . Other options can be implemented only by
modifying the configurations in UpgradeDownload.ini.
Figure 4-2 UpgradeDownload Options



## 第 28 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 18

Table 4-2 Description of UpgradeDownload Options
Item name Description
Repartition It is selected  by default and indicates whether to repartition during download , which is
valid only for Nand or EMMC Flash products.
Keep Charge It is unavailable by default and indicates whether to enable charging during download,
which requires software support.
Uart Download It is unavailable by default and indicates whether to download over the serial port.
Reset to Normal It is cleared by default . It indicates that  the tool sends a command to restart the mobile
phone in the last step of download .
Power Off It is selected  by default and indicates that the tool sends a command to shut down the
mobile phone, which takes effect after unplugging the USB. This function requires
software support , and it needs to be selected  for built-in battery download.
Dump Uboot Log It is not commonly used . It requires the software support of FDL2. If the download fails,
the tool saves the log in Uboot.
Read MCP Type  It is unavailable by default and requires software support.
Read Chip UID It is unavailable by default and requires software support.
Check Match  It is unavailable by default and requires software support.
DDR Check It is unavailable by default and requires software support.
EMMC Check It is unavailable by default and requires software support.
Self Refresh It is unavailable by default and requires software support.
Check 2nd Hand
Mem
It is unavailable by default and requires software support.

4.1.3 Multi Languages
Multi Languages is used  to set multiple languages in NV . If the NV file selected on Main Page does not contain
multilingual information, the interface is empty. Selecting a language indicates that the mobile phone ’s MMI
enables functions in this language.
4.1.4 LCD Configure
LCD Configure is used to configure LCD-related drivers in PS or UserImg files.

Only when the downloaded file list con tains PS or UserImg file, LCD-related configuration information is
displayed on LCD Configure.
4.1.5 Customization
As shown in Figure 4-3, select Customization, and  enter Customization.

## 第 29 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 19

Figure 4-3 UpgradeDownload Customization


Bad Flash Rate
Select Check bad flash rate to set the maximum allowable value of bad flash rate. Enable UpgradeDownload to
check the Flash bad flash rate of the mobile phone that is waiting for software download (only supports Nand
Flash bad flash rate checking currently).
The precondition of enabling the Flash bad flash rate checking function: The software of the mobile phone that is
waiting for software download has the function of checking the bad flash rate of Flash.
After enabling the function, UpgradeDownload check s the bad flash rate of the mobile phone ’s Nand Flash before
downloading. When the bad flash rate exceeds the maximum allowable value, the download is cancelled.
Inproduction Flag
The Inproduction Flag function is used infrequently. It is to write in the specified content, and then back them up
to the mobile phone when ba cking up Miscdata partition.
4.2 Operating instruction
Before downloading, set up the download environment according to 1.3 Download environment setup.
4.2.1 Load a file
Open the download tool and click
  to load the file that requires downloading.
4.2.2 Set download parameters
After the file is loaded successfully, click  to enter the setting interface, and set download parameters on
Main Page and Option s.

## 第 30 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 20

 Set the port and baud  rate on Main Page.
 Check Reset to Normal or Power Off option according to the test requirements on Options.

 To set download parameters for mobile phone with built -in battery, it is recommended to select Reset to
Normal or Power Off option.
 The precondition of  selecting Power Off: The  mobile software supports the Power Off function after the
download is completed.
4.2.3 Start download
1. After the tool is set, click
  on Tool bar. The program automatically detects available ports and prepares
to download.
2. Set up the test environment, and trigger the download mode  of the mobile phone . The tool automatically
detects the available port s and starts the download.
Figure 4-4 UpgradeDownload in download status


4.2.4 Complete download
If the download succeeds and the module is connected, a green Passed is displayed on Tool bar, as shown in
Figure 4-5.
Figure 4-5 UpgradeDownload download completed


If the download succeeds  and the module is disconnected, a blue Ready is displayed on Tool bar, as shown in
Figure 4-6. If you need to download again, replace the module and enter the download mode,  and the tool
automatically start s the download without clicking
  in Tool bar again.
Figure 4-6 UpgradeDownload waits for download again



## 第 31 页


4 UpgradeDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 21

4.2.5 Exit download
If UpgrageDownload is in automatic download status, other buttons on Tool bar are unavailable, click  to
exit the automatic download status. In this case, other buttons on Tool bar are available. Y ou can click
  to
reload other files or close the tool directly.


## 第 32 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 22

5 ResearchDownload user guide
ReserchDownload  is mainly used for R&D debugging. It can read and write Flash partition , backup NV
parameters, PhaseCheck, and ProdNV partitions (read back and then write in the mobile phone), and package
downloaded files. This tool does not initialize ProdNV and PhaseCheck partitions by default , and it is not
recommended to be use d as a production testing  tool.
5.1 Download settings
The setting window is used to set the download process, including the port rate and the files to be downloaded.
Click
  on Tool bar to enter the tool setting interface.
5.1.1 Main Page
Main Page is used for port selection, baud  rate configuratio n, file download selection, Product information
selection, and file download path customization , as shown in Figure 5-1.
Figure 5-1 ResearchDownload Main Page



## 第 33 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 23

Table 5-1 Description of ResearchDownload Main Page
Item name Description
Port Port setting .
You can select a certain port to download or select All. When selecting All, the tool
automatically detects available ports for downloading. A module corresponds to an
available port. When downloading a software for multiple modules simultaneously,
there are multiple available ports.
Baudrate Baud rate setting .
Information bar Displays version and Product information above the file list.
Downloaded file list  FileID indicates the name of downloaded file.
 The FileName column is an editable item. After double -clicking, you can enter the
file path or open the file selection dialog box to select the file.
 Base1 indicates the logical address or partition name of the downloaded partition.
 Size1  indicates the size of the downloaded partition. If it is displayed as
0xFFFFFFFF, the partition is an adaptive size.

5.1.2 Options
As shown in Figure 5-2, options interface requires the support of FDL or Uboot module .

## 第 34 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 24

Figure 5-2 ResearchDownload Options


Table 5-2 Description of ResearchDownload Options
Item name Description
Repartition It is selected  by default and indicates whether to repartition during download, which is valid
only for Nand or EMMC Flash products. Clear this item to ensure the integrity of mobile
phone content when reading Flash.
Keep Charge It is unavailable by default and indicates whether to enable charging during download,
which requires software support.
Uart Download It is unavailable by default and indicates whether to download over the serial port.
Download by using USB if cleared.
Debug Level It is used to enable or disable the kernel log and requires the support of FDL2.
 The default value is 0: disable the kernel log and select PhaseCheck on Main Page to
download.
 Enable the kernel log: set the kernel log level to 7 in general settings to capture  the most
complete log.
Reset to Normal It is cleared by default . It indicates that the tool sends a command to restart the mobile
phone in the last step of download.
Power Off It is selected  by default and indicates that the tool sends a command to shut down the
mobile phone, which takes effect after unplugging the USB. This function requires software
support, and it needs to be selected  for built-in battery download.

## 第 35 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 25

Item name Description
Dump Uboot
Log
It is not commonly used and requires the software support of FDL2. If the downloa d fails,
the tool saves  the log in Uboot.
Read MCP Type  It is cleared by default . It requires software support for reading the MCP Type (Flash size)
information.
Read Chip UID It is cleared by default. It requires software support for downloading UID functions for
reading.
Check Match  It is cleared by default. It requires the support of customized FDL2 for version fool-
proofing.
DDR Check It is cleared by default. It requires the software support of FDL1 for checking DDR.
EMMC Check It is cleared by default. It requires the software support of FDL2 for checking the download
integrity under EMMC.
Self Refresh It is cleared by default. It requires the software support of FDL1 for self -refreshing.
Check 2nd Hand
Mem
It is cleared by default. It requires software support for checking second hand memory.
Auto
Comparison
It automatically compares the read -back partition data with the original data of the
corresponding partition in Pac, which needs to be used with the Read  Flash function in
Flash Operations.  If a third-party comparison software is configured, it is called at the same
time to implement the comparison function.

5.1.3 Backup
As shown in Figure 5-3, Backup is used for set ting the items to be backed up for download. During download,
you can choose whether to backup NV , ProdNV , and PhaseCheck based on actual need.

## 第 36 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 26

Figure 5-3 ResearchDownload Backup


Backup NV Item
Backup NVItem lists NV ID items to be backed up. For example, if the backup NV is set in File Backup, you
can first read the NV in the mobile phone back to the PC, backup the IDs one by one according to the selected NV
ID items in Backup NVItem, and then  download them to the mobile phone. These backu p items are only valid for
NV partition. If a non -NV item is selected in File Backup, the configuration information of the backup item is not
displayed on the interface.
Save NV to local
For example, if Save NV to local is selected  and the backup function is set in File Backup, the backup partition
file that is named after the SN information is save d in the Backup directory under the tool directory after
downloading .
File Backup
The File Backup list box lists the partitions that need to be backed up by default. The partitions are backed up if
the item is selected . If not selected , the partitions are not backed up and the original download files in Pac are
directly downloaded to the corresponding partition.  If the corresponding downlo ad item is not selected on the
setting interface of Main Page, these partitions are not operated during download.

Each time you reopen the download program, the above options  in 5.1.3 Backup are restored to default
values.

## 第 37 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 27

5.1.4 Flash Operations
As shown in Figure 5-4, Flash Operations is used to control the  functions of Flash reading and erasing . The
configuration items on Flash Operations are processed  only after download items on Main Page are processed.
Figure 5-4 ResearchDownload Flash Operations


Read Flash
This function  is used to read partition data from the Flash of a mobile phone and save  it to a file on PC.
 After the Pac file is loaded, the tool automat ically generates the default read back configurations based on the
download items in Pac.
 Select Active Read Flash, and  select the read-back configuration item of the partition to be read, then
customize the Base, Size , and File of the partition to be read. For details about the configuration information,
see T able 5-3.
 To ensure the integrity of read-back data, do not  select Repartition on Options if you only need to read back
the content of Flash partition.
Table 5-3 Read Flash configuration item
Item name Description
SN It is used to select or cancel a specified read -back configuration item.
Base The information about the Base or ID of the read-back partition is the same as Base1 bar on
Main Page.
Size It indicates the size (Byte) of the partition to be read back, which must be smaller than or
equal to the size of the entire partition .
The hexadecimal value starts with 0x.

## 第 38 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 28

Item name Description
File It is used  to save the contents of read -back partition to the local file path.
Active Read
Flash
It indicates the switch of read -back function, which needs to be selected to operate the
contents in the list.
Select All It is used to select or cancel all read -back configuration items
Clear It is used to clear the configuration of all read -back configuration items.

Erase Flash
This function is used to erase a download partition.  After selecting Active E rase Flash, you can configure the
partition information to be erased. For details about the configuration i tems, see  T able 5-4.
Table 5-4 Erase Flash configuration item
Item name Description
SN It is used  to select or cancel a specified Erase Flash configuration item.
Base The information about the Base or ID of the parts to be erased in the partition is the same as
Base1 bar on Main Page.
Size It indicates the size (Byte) of the partition to be erased , which must be smaller than or equal to
the size of the entire partition.
The hexadecimal value starts with 0x. Erase the entire partition if Size is 0.
Active Erase
Flash
It indicates the switch of Erase Flash , which needs to be selected to operate the co ntents in the
list.
Clear It is used to clear the configuration of all Erase Flash configuration items.

Write Flash
This function is used  to write a specified download file to a download partition, which is same as the function of
the download item on Main Page.  After selecting Active Write Flash, you can configure the partition information
that needs to be written to . For details about the  configuration items, see T able 5-5.
Table 5-5 Write Flash configuration item
Item name Description
SN It is used to select or cancel a specified Write Flash configuration item.
Base The information about the Base or ID of the Flash partition that needs to write a specified file
is the same as Base1 bar on Main Page.
File It indicates the local file path that needs to write in the Flash partition.
Active Erase
Flash
It indicates the switch of Write Flash, which needs to be selected to operate the contents in the
list.

## 第 39 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 29

Item name Description
Clear It is used to clear the configuration of all Write Flash configuration items.

Erase All Flash
Select E rase All Flash if you need to erase the entire Flash. If E rase All Flash is configured, this tool firstly reads
back the backup partition and erases the entire Flash, then completes the download items on Main Page, and
finally executes the reading, writing and erasing configuration items in the setting.

Not all products support E rase All Flash.
5.1.5 Multi Languages
Multi Languages is used to set multiple languages in NV . If the NV file selected on Main Page does not contain
multilingual information, the interface is empty. Selecting a language indicates that the mobile phone ’s MMI
enables functions in this language.
5.1.6 LCD Configure
LCD Configure is used to configure LCD-related drivers in PS or UserImg files.

Only when the downloaded file list con tains PS or UserImg file, LCD-related configuration information is
displayed on LCD Configure.
5.1.7 MCP Type
As shown in Figure 5-5, select MCP T ype on the setting interface to enter MCP Type.

## 第 40 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 30

Figure 5-5 ResearchDownload MCP Type


Select Check MCP T ype and the tool c hecks whether MCP Type matches the selected  item after downloading
FDL1 (FDL2). If the match fails, an error is reported. MCP Type is set in the configuration file MCPType.ini. If
you want to add MCP Type, add it in this file.
5.1.8 Vol-Freq Tuning
As shown in Figure 5-6, V ol-Freq Tuning is used to set voltage and frequency.

## 第 41 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 31

Figure 5-6 ResearchDownload V ol-Freq Tuning


On Download setting s, select Vol-Freq T uning to enter the V ol-Freq Tuning. Double -click the Value column to
set the voltage or frequency and the setting results  are directly saved to the SPLLoader file. Therefore, it is
recommended to backup this file before changing the settings. Whether the V ol-Freq Tuning can be modified
depends on the special tags in the SPLLoader file. If no special tags or SPLLoader download items are available,
the V ol-Freq Tuning cannot be modified. The rendering of detailed interface depends on the data format of the tag
block.
5.1.9 Uart Port Switch
As shown in Figure 5-7, Uart Port Switch is used to configure Uart ports.

## 第 42 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 32

Figure 5-7 ResearchDownload Uart Port Switch


On Download settings , select Uart Port Switch to enter the Uart Port Switch. Double -click the Value column to
modify related parameters, which are directly saved to the UBOOTLoader file. Therefore, it is recommended to
backup this file before modifying. Whether the Uart Port Switch can be modified depends on the special tags in
the UBOOTLoader file. If no sp ecial tags or UBOOTLoader download items are available, this interface cannot
be modified.
5.2 Operating instruction
Before downloading, set up the download environment according to  1.3 Download environment setup.
5.2.1 Load a file
Open the download tool and click
  to load the file that requires downloading.
5.2.2 Set download parameters
After the file is loaded successfully, click  to enter the setting interface , and set download parameters.
 Main Page: set the port and baudrate and select the file that requires downloading .
 Options: select KeepCharge, Reset to Normal or Power Off option according to the test requirements .
 Backup: set whether to back up NV , PhaseCheck, and ProdNV item.

## 第 43 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 33


 FDL1 is compulsory when selecting download files (FDL2 is also compulsory if exists). Select other files
based on requirements.
 To set download parameters for mobile phone with built -in battery, it is recommended to  select Reset to
Normal or Power Off option.
 The precondition of  selecting Power Off: The mobile software supports the  Power Off function after the
download is completed.

5.2.3 Start download
1. After the tool is set, click
  on Tool bar. The program automatically detects available ports and prepares
to download.
2. Set up the test environment, and trigger the download mode of mobile phone . The tool automatically detects
the available ports and starts the download, as shown in Figure 5-8.
Figure 5-8 ResearchDownload in download status


5.2.4 Complete download
If the download succeeds , a green Passed is displayed on Tool bar, as shown in Figure 5-9.
Figure 5-9 ResearchDownload download completed


If the module is disconnected, a blue Ready is displayed on Tool bar, as shown in Figure 5-10. If you need to
download again, replace the module and enter the download mode,  the tool automatically start s the download
without clicking
  again.
Figure 5-10 ResearchDownload waits for download again



## 第 44 页


5 ResearchDownload user guide

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 34

5.2.5 Exit download
If ResearchDownload is in automatic download status, other buttons on Tool bar are unavailable, click  to
exit the automatic download status. In this case, other buttons on Tool bar are available. Y ou can click
  to
reload other files or close the tool directly.


## 第 45 页


6 Command line download

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 35

6 Command line download
FatoryDownload, UpgrageDownload and ResearchDownload not only support the graphical interface download
described previously, but also command line download. Command line download is implemented by CmdDloader
application, and the whole download process is handled in the background. The CmdDloader application is
responsible for starting the download tool s and monitoring the download progress and results.
6.1 Parameter format
The parameter format for the command line to start the CmdDloader application is as follows.
CmdDloader.exe <-pac PacFile>  [ -port ComPort] [-c] [-WriteSN SN1] [ -WriteSN2 SN2] [-timeout t][-cout n]
For example,
CmdDloader.exe -pac D:\SC7702_sc7701.pac -port 195

 -pac PacFile: enter the Pac file.
 -port ComPort: enter the port number of download  devices.
 -c: this command is optional. When you enter this parameter, the CmdDloader application clear s the
download progress before executing the download.
 -WriteSN XXXXXX and -WriteSN2 YYYYYY: these two parameters are used only when
FactoryDownload_Cmd writes SN number.
 -timeout xx: the unit is in seconds. The timeout in waiting for port connection ends the download process.
This parameter is not commonly used.
 - count x: number of modules in simultaneous software download  without entering the port number. This
parameter is not commonly used.
 If no port information is specified, the application automatically searches for an appropriate port for
downloading.  The con figuration item WaitDUTTimeout in CmdDloader.ini sets the time to wait to find a
valid device.  When the value is 0, it indicate s an infinite wait until an appropriate  download port is found.
6.2 Download example
Figure 6-1 shows an example of suc cessful command line download, and DownLoad Passed indicates the
download succeeds .

## 第 46 页


6 Command line download

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 36

Figure 6-1 Successful CmdDloader download


Figure 6-2 shows an  example of failed command line download , and displays the error message for failed
download.
Figure 6-2 Failed CmdDloader download




## 第 47 页


7 Interface error message analysis and solution

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 37

7 Interface error message analysis and solution
This chapter describes the causes of interface error message  and corresponding solutions.
7.1 [DL1150] Incompatible partition
Cause
 The partition table in XML or FDL2 is incompatible with the partition on Flash.
 The partition does not exist or  is damaged.
Solution
1. Check Options on the setting interface and select Repartition.
2. Check whether the File list correspond s to the partition table in the software XML.
3. Check FLASH Hardware.
4. If Nand project is second hand m emory, it needs to be all erased to download .
5. Check software according to log.
7.2 [UB1142] Wait input time out
Cause
The device -side response returns timeout .
Solution
Provide tool log (T able 2-1 describes how to set tool log.) and serial port log for Uboot -side analysis.
7.3 [DL1138] Image size is over its partition
Cause
The size of downloaded Image file is inconsistent with the partition size of the mobile phone.
Solution
1. Check whether Pac corresponds to the mobile phone and check whether the XML configuration is consistent
with the actual partition size of the mobile phone.
2. Modify the partition size or modify the XML definition about the partition size in the product Pac to make it
consistent.

## 第 48 页


7 Interface error message analysis and solution

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 38

For example,
If an error is reported after using Read FixNV to write back again , you can find the solutions i n 8.17 Prompt
message (Size is too large ) occurs when ResearchDownload reads FixNV write-back.
7.4 [PS2262] User cancel
Cause
 The device is unplugged manually.
 The device is unplugged due to environmental causes, such as poor contact.
 The port enumeration on UE-side is stopped
Solution
 The problems that are not sure to come may be associated with environment, which can troubleshoot t he
mismatches between USB cables, computer USB ports, battery capacity, or P ac with the devices.
 The problems that are sure to come need to provide Uboot software colleagues with serial port log to analyze
and solve the specific problems.
7.5 [UB1254] Software has not supported this feature
Cause
The software does not support the command.
Solution
Provide tool log (T able 2-1 describes how to set tool log.) for Uboot -side analysis  and add corresponding
command support .
7.6 [PS2257] Uart send error
Cause
The possible causes  that the data cannot be written on the port during download :
 If the FDL1 download  has not started, the hardware and download environment need to be checked.
 If the FDL1 download has finished, FDL1 is not running or DDR fails to initialize.
Solution
 The problems that are not sure to come may be associated with environment, which can troubleshoot the
mismatches between USB cables, computer USB ports, battery capacity, or P ac with the devices.
 The problems that are sure to come need to provide Uboot engineers with serial port log to analyze and solve
the specific problems.

## 第 49 页


7 Interface error message analysis and solution

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 39

7.7 [UB1132] Operation failed
Cause
The Uboot -side returns the response of Operation fails.
Solution
Provide tool log (T able 2-1 des cribes how to set tool log.) and serial port log for Uboot  personnel  to do recurrence
analysis.
7.8 [SW2020] NV data read in phone is crashed
Cause
The end identifier ID = FFFF is not found by the tool due to an NV data structure error within the device.
Solution
 Modify the MaxReadLength field in BMFileType.ini after NV capacity expansion .
[DownloadNV]
MaxReadLength = 0x100000

The default value of the MaxReadLength  field is 0x100000, that is, the maximum length of the NV read b y
the tool from the device is 1 MB by default.
 Provide read-back NV files and tool log (set the log level to 5) for UNISOC NV personnel to analyze.
The operations about reading the NV files ba ck are as follows.
ResearchDownload  Setting button  only select FDL1 and FDL2 on Main Page  No backup on
Backup  Read Fix NV partition back on Flash Operations.
7.9 [SW2021] NV data in nvitem.bin is crashed
Cause
The NV file in Pac is not valid NV data, o r the NV file is not 4 Byte aligned .
Solution
Use the Pac file with correct NV file and provide nvitem.bin file for UNISOC NV personnel to analyze .


## 第 50 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 40

8 FAQ and supplementary information
8.1 Unrecognize the port
If the module is connected and the device manager can enumerate ports, but the download fails, the possible
causes are as follows.
 The power supply to the module is abnormal, for example, there is no external power supply .
 The port is occupied by another application.
 The module is not  in the download mode. See 1.4 Entry methods of download mode to ensure the module
is under the download mode.
8.2 Fail to capture the port after modifying the port name
After modifying the port name in device manager, you need to modify the [AT_REBOOT_SETTING] part in
BMFileType.ini file and add the port name. The added  port name must be consistent with the modified port name
in device manager.
8.3 Local file has a .flag suffix after decompressing Pac
Cause
To prevent large temporary files after decompression, the download tool has a decompression strategy  when
decompressing Pac. If the size of the decompressed file is greater than the set value, the compression is not
required. Only a temporary file with a  .flag suffix is generated, and the data is still s aved in Pac.
Solution
Modify the BinPac.ini file by setting LoadPolicy and MaxReadLength in Settings to 0 as follows.
[Setting]
LoadPolicy = 0
MaxDataLength = 0 ;  the unit is MB

The modification takes effect only after you restart the download tool .

## 第 51 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 41

8.4 Modify required or optional attributes of files in the
partition list
In the XML file of Pac, <File> has Flag and CheckFlag definitions, and each downloaded file has corresponding
Flag and CheckFlag definitions in the XML file. Y ou can modify the required or optional  attributes of the
downloaded file by modifying the CheckFlag definition of the downloaded file.
Flag
 0: Y ou have no need to enter the file path.
 1: Y ou must enter the file path if 1 is selected.
CheckFlag
 0: The file is optional.
 1: The file is required.
 2: The file is not checked.
8.5 Record ID information of the module
The download tool records the ID information of the module that downloads a software,  and saves it as a CSV or
TXT file. This function is disabled by default. Y ou can enable this function by modifying the xxDownload.ini file.
The related fields and descriptions are as follows.
[Report]
;report file name is download_result.txt under the tool folder.
enable= 0                 //function switch , 0: disabled, 1: enabled.
;0, Normal; 1, Press
Type = 0                  // saved file type, 0: txt, 1: csv.
;DUTID: 0, IMEI; 1, SN; 2, ChipUID;3, SN_IMEI
DUTID=1                 // type of recorded data , 0 and 3 are only valid for UpgradeDownload and
ResearchDownload .
The fields in [Report] in the xxdownload.ini file are modified as follows.
 Turn on the switch of recording ID information (set the enable field to 1)
 Specify the format of file saving  to save the ID information of downloaded module
− Type = 0: txt
− Type = 1: csv
 Specify the ID information type of download module to be recorded
− 0: IMEI
− 1: SN
− 2: ChipUID
− 3: SN and IMEI
Save the xxDownload.ini file and restart the download tool to make the above s ettings take effect.

## 第 52 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 42

8.6 Set tool Log level
There are two ways to set tool log level for effective capture log.
 Modify the Local Log Level field in iSpLog.ini file under the tool installation directory.
[Options]
; Text log level
; 0, No text log
; 1, Log errors,default value
; 2, Log warnings
; 3, Log runtime information
; 4, Log data only
; 5, Log everything
Local Log Level   = 5
This method barely influences the download rate.
 Adjust the tool log level in Status bar at the bottom of the tool interface.
8.7 Check MCP (DDR or EMMC)
ResearchDowload , FactoryDownload and UpgradeDownload  all support check ing MCP (DDR or EMMC)
function.

This function requires the software support of module. If the tool enables this function but the module
software does  not support it, the download  tool stop s the download process and display the prompt message
of Software has not supported this feature.
Set MCP check item
1. Convert the DDR Size and EMMC Size of the device to a hexadecimal number in MB to obtain the MCP
check item of the device.
For example, the DDR Size of the device is 4 GB and the EMMC Size is 63 GB. After converting into
hexadecimal number, its MCP check item is 1000-FC00 = TEST.

The format of device MCP check item is DDR Size-E MMC Size = Description, where DDR Size  is the size
of DDR, E MMC Size is the size of EMMC (both of them are displayed in hexadecimal number), and
Description is the name of MCP check item.
2. Modify MCPType.ini to write device MCP check item to the MCPTypeRange field or  / and the
MCPTypeList field.
− Only one MCP check item can be added to the MCPTypeRange field, which is used as the default check
item.
− One or more MCP check items can be added to the MCPTypeList field, including the default check item
of the MCPTypeRange field and other alternative check items. Use ResearchDo wnload to check MCP
check items on MCP Type.

## 第 53 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 43


To set MCP check item quickly, use the ReadMCP function of ResearchDownload to read back the device's
MCP and copy it to the MCPTypeRange field in MCPType.ini.
Enable the MCP check ing function of the tool
 ResearchDownload
− Check Read MCP T ype on Option.
− Check Check MCP T ype on MCP T ype.
 FactoryDownload
− Modify FactoryDownload.ini, and set the value of the ShowMcpT ypePage filed to 1.
− Modify MCPType.ini file, and set the value of the CheckMCPT ype filed to 1.
 UpgrageDownload
− Modify UpgrageDownload.ini, and set the value of the ShowMcpT ypePage filed to 1.
− Modify MCPType.ini file, and set the value of the CheckMCPT ype filed to 1.
After completing the setting of MCP check item and enabling the tool ’s MCP checking function, the tool check s
the MCP according to the setting when downloading.
8.8 Set password for download tool
Y ou can set passwords for both FactoryDownload and UpgradeDownload.
Modify FactoryDownload.ini or UpgradeDownload.ini settings to enable the password mechanism.
[GUI]
NeedPassword=1
After enabling the password mechanism, reopen the download tool. When you click
  or
 , an input box
prompts for inputting password, as shown in Figure 8-1.
Figure 8-1 Enter password


Click Reset in Figure 8-1, a password reset interface prompt s as shown in Figure 8-2. Y ou can reset your
password after inputting your new password and inputting it again for confirmation.

## 第 54 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 44

Figure 8-2 Reset password



 The initial password is admin.
 The password must be letters (a-z, A-Z) or numbers (0-9), which exceeds no more than 20 characters in
length.
8.9 Inproduction Flag function
This infrequently used function is on Customization. It is to write in specific contents and back them up to mobile
phone when backing up the Miscdata partition.
8.10 Set the writing length of FactoryDownload SN
When downloading, FactoryDownload write s a SN in mobile phone, whose default length is 14. Modifying the
SN_LENGTH field in FactoryDownload.ini can reset the writing length of SN.
[SN]
SN_LENGTH = 14
8.11 Set the prefix of the SN written in by FactoryDownload
FactoryDownload.ini can customize the SN prefix wr itten in by FactoryDownload when downloading. The
example of a customized SN prefix is as follows.
[SN]
SN_LENGTH = 14
FixedSN = xxx   //xxx  indicates the SN prefix, whose length shall not exceed the length of SN.

## 第 55 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 45

8.12 Set the entry mode of the first booting after
FactoryDownload download
The fields and their configuration s description in FactoryDownload.ini to set the entry mode of the first booting is
shown as follows.
[FirstMode]
;Enable: 0:disable; 1:enable
Enable=1
SupportFeaturePhone=0
FirstMode=0x13
;0x00  normal boot mode
;0x01  GSM cal mode
;0x02  GSM Final test mode
;0x03  Wcdma cal mode
;0x04  Wcdma final test mode
;0x05  TDscdma cal mode
;0x06  TDscdma  Final test mode
;0x07  L TE TDD cal mode
;0x08  L TE TDD final test mode
;0x09  L TE FDD cal mode
;0x0A  L TE FDD final test mode
;0x0B  NR 5g sub6g cal mode
;0x0C  NR 5g sub6g final test mode
;0x0D  NR mmW
;0x0E  NR mmW final test mode
;0x0F  CDMA2k cal mode
;0x10  CDMA2k final test mode
;0x11  BBAT mode
;0x12  native MMI mode(MMI for feature phone)
;0x13  Apk MMI (apply for smartphone)
;0x14  NB -IOT cal mode
;0x15  NB -IOT final test mode
;0x16  UPT
;0x17---0xFF reserved
An example of the setting: entering APK mode of the first booting after the download  of smart phone.
1. Modify the related fields of FirstMode in FactoryDownload.ini according to the following settings, and save
the settings.
− Configure the Enable field as 1 (enable switch of the function).

## 第 56 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 46

− Reset the SupportFeaturePhone field (unsupported for feature phone).
− Configure the FirstMode field as 0x13 (first entry of APK mode).
2. Reopen FactoryDownload to download Pac.
3. Confirm if the mobile phone enters APK mode when booting for the first time after down load.
− If selected Poweroff when downloading, the mobile phone is shut down automatically after
downloading. Hold the power button for 3 seconds to reboot the  mobile phone, and confirm if the
mobile phone enters APK mode.
− If selected Reset to Normal, the mo bile phone is booted automatically after downloading. Confirm if
the mobile phone enters APK mode after the booting.

 Download is only used to verify the validity of the settings above. Therefore,  select only FDL1, FDL2 and
Uboot when setting Main Page to  save download time.
 If the mobile phone enters modes including GSM cal mode or BBAT mode, and the Device Manager
enumerates ports and does not drop them after booting, send an AT command, such as
AT+GE TTESTMODE?, to check if the current mode is consistent  with the one you set.
8.13 Configure Sparse2Raw in FactoryDownload.ini
;CheckSparse2Raw 0: not use Sparse2Raw
;CheckSparse2Raw 1: use Sparse2Raw in all partition
;CheckSparse2Raw 2: use Sparse2Raw only in super
;CheckSparse2Raw 3: use Sparse2Raw not in userdata
CheckSparse2Raw = 2
There are Sparse download format and Raw download format for files in Pac. Files in Raw format have a faster
download rate, so you should try to use the Sparse2Raw application to convert larger files in Pac from Sparse
format to Raw format to increase the download rate.
Therefore, setting CheckSparse2Raw field to 2 by default is the optimal plan, and requires no modification for
now.
8.14 Upgrade software using UpgradeDownload
UpgradeDownload  is indispensable for software upgrade, w hich forcibly backs up NV , PhaseCheck, and ProdNV
information.
8.15 Packet using ResearchDownload
The operation of ResearchDownload to packet is as follows.
Step 1 Click
  to load a Packet.
Step 2 Click  to enter Main Page to choose the file that needs to be packeted. Cleared files are not packeted.
If you need to replace a file, double -click the FileName column of the corresponding to File ID to select
another file for packeting.

## 第 57 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 47

Step 3 Click Packet, and a packet setting interface prompt s as shown in Figure 8-3. Input the product alias,
product version and saving path, and click OK to start packeting.
Figure 8-3 Packet setting


After successful packeting, the message shown in Figure 8-4 prompts.
Figure 8-4 Packeting complete prompt
OK


----E nd
8.16 Erase Flash using ResearchDownload
The operation of ResearchDownload to erase Flash is as follows.
Step 1 Click
  on Tool bar to load a Packet.
Step 2 Click  to select FDL1 and FDL2 only on Main Page and select E rash All Flash on Flash
Operations.

Do not select other options on this interface. Otherwise, the mobile phone start s downloading other
selected files after erasing.
Step 3 Back to the main interface, click , and the following dialogue box prompt s as shown in Figure 8-5.
Click Yes to confirm and start erasing.

## 第 58 页


8 FAQ and supplementary information

Issue V4.3 (10-Sep-2021) Copyright © UNISOC (Shanghai) Technologies Co., Ltd. 48

Figure 8-5 Erase Memory using ResearchDownload
Yes No


----E nd
8.17 Prompt message (Size is too large) occurs when
ResearchDownload reads FixNV write-back
The FixNV partition configured in the XML configuration in Pac is 2 MB (0x200000), but its actual size is only
about 800 KB (can be learned from the nvitem.bin file in Pac), and the remaining 1 M B is used to store Running
NV and other content.
Therefore, when using Active Read Flash to read FixNV , only 1 MB can be read. In other words, only when
changing the setting to 0x100000 can the read FixNV be written back to the mobile phone.



8.18 Set ResearchDownload Debug Level
 If the Debug level set by  the device is any level between 0 to 6, ResearchDownload can set the Debug level
to any level between 0 to 7.
 If the device has set Debug level to 7, you cannot use ResearchDownload to change Debug level to any level
from 0 to 6. The solution is to use th e E rase All Flash operation to fully erase Flash and then download Pac
again, and set the Debug level.

Debug level is saved in the Miscdata partition at 9 KB+32 Bytes offset. UpgradeDownload does not operate
the Miscdata partition in backup download, so it does not modify the Debug level.
