# 组委会旧工程协议审计

控制板 PDF（SHA-256 `c6a48327b3f327e5f38185631f5214f7fd9d5e4e724f7ffc4016bbff27c6806e`）第 15–16 页给出 `Head/Addr/Length/Data/Check` 结构、帧头 `0x42`、地址表与前 10 字节累加校验示例。旧工程 `uart.hpp` 则暴露出以下冲突：

- PDF 表格最大帧长为 30，源码常量为 12。
- PDF 按键地址为 `0x06`，源码为 `0x10`。
- 车控/蜂鸣器/心跳分别声明 Length 10/5/4，却发送 11/6/5 字节；车控缓冲区最后一字节没有在该构造路径中明确初始化。
- PDF 原文写 USB/UART 速率“115200Kbps”，源码配置 115200、8N1；原文单位疑点不能静默修正为事实。

因此协议门禁为关闭：`OfficialSerialTransport` 未实现，旧序列化代码未复制，当前只允许 `RecordingTransport`。
