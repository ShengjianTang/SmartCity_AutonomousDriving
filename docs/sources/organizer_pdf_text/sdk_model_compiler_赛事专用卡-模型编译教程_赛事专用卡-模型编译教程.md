# PDF 逐页文本：sdk/model_compiler/赛事专用卡-模型编译教程/赛事专用卡-模型编译教程.pdf

- SHA-256：`3296fd3f07c4b406449c02fc69be0a7f078f56504d15694a2040a37b08396ffa`

## 第 1 页

1 |
TEMPLATES WITH WORD FOR R&D EDU
北京赛曙科技有限公司
BEIJING SAISHU TECHNOLOGY CO.,LTD

## 第 2 页

I
目录
资料说明 ................................................................................................. 1
1.1. 下载地址 ............................................................................................................................... 1
1.2. 资料说明 ............................................................................................................................... 1
环境配置 ..................................................................................................... 1
2.1. 电脑环境配置 ....................................................................................................................... 1
2.2. DOCKER 安装 ......................................................................................................................... 4
2.3. WSL2 的安装 .........................................................................................................................4
2.4. DOCKER 环境搭建 ................................................................................................................. 6
模型编译 ..................................................................................................... 8

## 第 3 页

1
资料说明
完成模型训练后，需要使用 Docker 进行模型编译，才可以部署到机器人使
用，需要先参考模型训练教程进行模型导出，再按照此教程说明进行编译。
1.1. 下载地址
模型编译工具：点击下载模型编译工具
1.2. 资料说明
（1） Docker Desktop Installer.exe：Docker 桌面版安装包
（2） ppnc2.0_v1.0.2.tar：Docker 镜像压缩包
（3） wsl_update_x64.msi：WSL 更新安装包
环境配置
2.1. 电脑环境配置
（1） 打开任务管理器→选择性能→CPU→虚拟化，确认是否已启用。
（2） 打开控制面板→程序。
图 1-2
（3） 点击启动或关闭 windows 功能。

## 第 4 页

2
（4） 勾选 Hyper-V（找不到请看第 6 步）
（5） 勾选虚拟机平台
（6） 若找不到 Hyper-v 功能则可以在桌面建一个 Hyper-V.bat 文件，将
以下指令放入（若第 4 步执行正常无需执行此步骤，复制完成注意格式换行）
Win10 版本

## 第 5 页

3
pushd "%~dp0"
dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt
for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online
/norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
del hyper-v.txt
Dism /online /enable-feature /featurename:Microsoft-Hyper-V-All
/LimitAccess /ALL
Win11 版本
pushd "%~dp0"
dir /b %SystemRoot%\servicing\Packages\*Hyper-V*.mum >hyper-v.txt
for /f %%i in ('findstr /i . hyper-v.txt 2^>nul') do dism /online
/norestart /add-package:"%SystemRoot%\servicing\Packages\%%i"
del hyper-v.txt
Dism /online /enable-feature /featurename:Microsoft-Hyper-V-All
/LimitAccess /ALL
（7） 以管理员身份执行 Hyper-V.bat 文件（若第 4 步执行正常无需执行
此步骤）

## 第 6 页

4
（8） 重启计算机
2.2. Docker 安装
（1） 双击运行 Docker 桌面版安装包。
（2） 点击 OK
（3） 等待安装完成，点击 Close（安装过程中会提示重启计算机，安装
docker 过程中请注意保存文件）
（4） 打开 cmd 输入指令命令查看 docker 版本号，可以查询到版本号表示
安装完成
docker --version
注：此时 Docker 还未完成 Docker 的环境配置，所以无法启动桌面上的
Docker。
2.3. WSL2 的安装
（1） 以管理员身份启动 Windows PowerShell

## 第 7 页

5
（2） 输入指令（复制指令时请注意指令没有换行，若复制结果出现多行
请自行调整格式）
dism.exe /online /enable-feature
/featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
（3） 输入指令（复制指令时请注意指令没有换行，若复制结果出现多行
请自行调整格式）
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform
/all /norestart
（4） 双击运行 WSL 更新安装包
双击 WSL 更新包时可能会出现下列弹窗，系统为 Win11 时出现以下弹窗可
以在 终端继续执行第五步（5）指，终端会提醒按任意键进行 WSL 更新。

## 第 8 页

6
（5） 输入指令
wsl --set-default-version 2
（6） 双击桌面 Docker 图标即可正常使用
2.4. Docker 环境搭建
（1） 双击桌面图标启动 Docker 桌面版

## 第 9 页

7
（2） 在 windows 目录创建文件夹 work，将 Docker 镜像压缩包拷贝至目录
下
（3） 以管理员身份启动 Windows PowerShell
（4） 进入到 work 目录（注意路径换成自己创建的）
（5） 输入指令读取镜像（C 盘预留 20G 空间，等待约 20 分钟）
docker load -i ppnc2.0_v1.0.2.tar
（6） 读取完成后，可在 Docker 桌面端看到镜像信息

## 第 10 页

8
（7） 输入指令创建容器，其中 ppnc2.0_docker 为容器名称，可自定义；
D:\work 需要替换为自己创建的路径；/home/edgeboard/workspace 是容器中
被映射的路径（复制指令时请注意指令没有换行，若复制结果出现多行请自行
调整格式），创建完成后会自动进入容器
docker run -it --cap-add=SYS_PTRACE --name ppnc2.0_docker -v
D:\work:/home/edgeboard/workspace ppnc2.0:v1.0.2 /bin/bash
（8） 创建完成后，可在 Docker 桌面端看到容器信息
模型编译
（1） 以管理员身份启动 Windows PowerShell

## 第 11 页

9
（2） 输入指令启动容器（注意容器名称使用自己创建的）
docker start ppnc2.0_docker
（3） 输入指令进入容器（注意容器名称使用自己创建的）
docker exec -it ppnc2.0_docker /bin/bash
（4） 输入指令导入环境变量
export PPNC_HOME=/usr/local/ppnc/
（5） 输入指令导入相关路径
source /usr/local/ppnc/scripts/activate_env.sh
（6） 输入如下命令进入到 “/home/edgeboard/workspace”文件夹下 :
cd /home/edgeboard/workspace
（7） 在 work 文件夹下新建一个 yolov3 文件夹。并在该文件夹下新建
model 和 image 文件夹

## 第 12 页

10
（8） 将 Ai Studio 导出的模型文件全部放入 model 文件夹
（9） 在 image 文件夹放入 50 张以上训练使用图片，每个标签类别
（10）输入指令获取编译工具
cp -r ~/tools/ /home/edgeboard/workspace
（11）执行完成 work 文件夹自动生成 tools 文件夹

## 第 13 页

11
（12） 打开 tools/config.json 文件,按照图示修改
model_dir：“compiler/yolov3”文件夹为第 7 步所创建的文件夹
shape：模型输入尺寸，需要与模型实际尺寸保存一致。
（13）点击进入在线软件 netron
（14）点击“Open Model...”
（15）选择模型文件

## 第 14 页

12
（16）将打开的模型结构拉到最下方，确认自己的模型标签数量和输出张量
（17） 修改 tools 文件夹下 split.py⽂件的第 292⾏，将其数字修改为模
型结构上一步输出张量
（18）输入指令进入 tools 目录
cd /home/edgeboard/workspace/tools/
（19）输入指令编译模型
python3 compile.py ./config.json

## 第 15 页

13
（20）等待编译完成将编译完成模型导出
（21）将导出的模型解压，放入开源工程

## 第 16 页

14
（22）将模型训练时的最终 label_list.txt 替换到工程中

## 第 17 页

15
（23） 将 tools.hpp 中 的 宏 定 义 中 ， 将 引 号 内 的 内 容 修 改 成 与
label_list.txt 当中的标签名称一致（根据自己训练时的命名修改）

## 第 18 页

16
