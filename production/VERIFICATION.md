# 定稿验证记录 · 2026-11-20

当前交付为[正式1080P版](exports/FY27-Kickoff-FINAL-1080P.mp4)与[微信720P版](exports/FY27-Kickoff-WeChat-720P.mp4)。用户已通过v05；正式文件直接复制该版，没有新增编码。

| 检查 | 结果与证据 |
| --- | --- |
| 正式版身份 | 54,542,732字节；SHA256与用户通过的v05一致，见[正式manifest](exports/FY27-Kickoff-FINAL-manifest.json) |
| 时间线 | 1663帧／30fps＝55.433333秒；详见[交付记录](25-FINAL-DELIVERY-v01.md) |
| 高清基础合成 | 源片对齐抽查、尺寸、完整解码与黑色末帧，见[HD验证](exports/HD-full-v01-manifest.json) |
| 定稿声音精修 | 视频压缩流与v04一致、完整解码通过、混音无削波，见[v05验证](exports/HD-intro-a-bridge-v05-manifest.json) |
| 微信压缩版 | 1280×720／30fps／1663帧，8,941,492字节；完整解码通过，见[微信manifest](exports/FY27-Kickoff-WeChat-manifest.json) |
| 画布 | 高清7条、片尾4项分别归组，采用／部分采用／历史对比名称明确，布局已保存，见[整理后清单](canvas-after-final-tidy-20261120.json)与[截图](previews/FINAL-canvas-organized-20261120.png) |

原始生成的动作或轻微姿态问题不会因高清增强自动消失；用户已回看并接受本片。微信客户端二次压缩与收件端播放本轮未实测。活动上传、许可及Prompt交付口径不属于本地文件验证结果。

[历史准备包验证](VERIFICATION-HISTORY-20261120.md)记录各阶段当时状态；其中“尚未生成”“60秒／1800帧”等不适用于当前定稿。文档与JSON链接校验结果见[整理校验清单](delivery-tidy-verification-20261120.json)。
