# LT 角色定稿

状态：**2026-11-17 用户已确认定稿**。用户原话：“完美，定稿吧，中间过程可以删掉，保留这版！”以下三张图片为后续视频制作的人物基准，保留已认可文件原名及原始像素，不重新生成或改脸。

| 定稿素材 | 人物顺序 | 尺寸 |
| --- | --- | --- |
| [六人总览](lt-six-style-review-v03.png) | 上排 Jessica、Feng、Song；下排 Amy、Scott、Wei | 1536×2144 |
| [Jessica／Feng／Song](style-calibration-trio-fresh-feng-v02.png) | 从左到右 | 1536×1024 |
| [Amy／Scott／Wei](style-calibration-amy-scott-wei-v04.png) | 从左到右 | 1536×1024 |

六人总览是两张完整三人图的原尺寸排版，不是六人再次联合重绘。图中原有 “NEW CANDIDATE” 为制作时的图内标题；整版现已获认可，无需继续等待造型确认。[定稿清单与 SHA-256](FINALIZATION.json)用于检查后续素材是否仍是这版。

## 制作来源

- 工具：既有 `dream-painter` / Azure 部署 `gpt-image-1.5` 图生图，两组各一次联合生成人物；对应日志均未触发文生图回退。
- Jessica／Feng／Song：Feng 身份来自原照，Jessica、Song 来自此前认可的卡通参考。保留完整[实际输入板](../../references/lt/style-calibration-trio-fresh-feng-input-v02.png)、[原始 Prompt](../../prompts/style-calibration-trio-fresh-feng-v02.txt)及[执行日志](style-calibration-trio-fresh-feng-v02.log)。
- Amy／Scott／Wei：三人原照提供身份，已认可的上一组三人图提供统一画风、比例、队服、背景和灯光。保留[实际输入板](../../references/lt/style-calibration-amy-scott-wei-input-v01.png)、[原始 Prompt](../../prompts/style-calibration-amy-scott-wei-v01.txt)及[执行日志](style-calibration-amy-scott-wei-v01.log)。
- 新三人定稿图在联合输出基础上，仅对六个袖口添加窄渐变织物饰边；没有更换或合成头部。总计修改 902 个像素，差异仅限六处袖口；脸、体型、腰边、裤子、鞋子与背景均未改变。[验证记录](style-calibration-amy-scott-wei-v04-verification.json)保留为制作说明，记录中的旧源图已按用户要求清理。
- 六份原始照片仍保存在 `references/lt/`，不属于本次中间图清理范围。两份完整输入板与实际 Prompt 保留，供片尾制作信息与来源说明使用。

## 后续使用

以这版的脸型、卡通程度、比例、深蓝队服与渐变饰边为共同基准；后续单人高清图、舞台合成或舞蹈样段均须保持人物身份。不再使用被否定的 Feng B 头像、写实修正版或贴头方案。

本次定稿覆盖六位现有角色。Wei 与名单 Renwei 的对应仍待确认，Zhuoying、Michael 的照片仍待补充；正式名单仍按八人方案处理。高清单人资产、音乐与视频尚未制作，舞蹈脚本仍为讨论稿。

已按用户要求清理 101 个旧候选、对照试验、临时裁图、弃用 Prompt／参考板与角色试验脚本，从项目移除约 68.73 MiB；文件移入 Windows 回收站，必要时可恢复。舞台概念图、原始照片、创意与剧本讨论、V1 快照均保留。定稿图片校验值与全部项目 Markdown 本地链接均已检查通过。
