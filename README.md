# MAA 外部通知

## 简介
MAA目前自带外部通知,但是通知的内容仅限运行完成. 

MAA_*_send 读取gui.log里面的内容,并提取摘要.
check_MAA_emulator 检查 MAA或者模拟器状态。如果是关闭的（例如手动打关后忘记打开），则发送提醒，并不直接自动开启。

## 用法
1. git clone 并把bat文件里的路径指向py文件.
2. MAA设置 "运行后" 指向bat文件.

当前只对TG发送消息,需要自行创建bot和获取chat_id

