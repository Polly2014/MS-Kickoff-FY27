# Jessica → Feng：首轮 4 秒小样

2026-11-18 已在登录后的 LibTV 实际生成并下载。

- 画布：[FY27_Focus_Kickoff_S03-S04_Test](https://www.liblib.tv/canvas?guideSource=home-feature-grid&starterGuide=1&spaceId=16309688&projectId=13a4ddd3ecf843018e3121871fd7bcaa)
- 两张首帧：Seedream 5.5，2K 档，实际 2816×1584，两张参考图（角色正面＋舞台），各 7 积分。
- 两段视频：Seedance 2.0 Mini，单首帧图生视频，480P 档，16:9，5 秒，1 个，关闭音频，各 40 积分。实际均为 864×496、24fps、121 帧、5.041667 秒。
- 初始 100 积分，最终 6 积分；本轮实际花费 94 积分。未充值或购买会员。Feng 首次启动被取消，随后成功生成，最终余额未多扣一次。
- Flash 的 720P／5秒界面报价 140 积分；2.5 样片模式 480P／5秒报价 100 积分，因此本轮改用 Mini。价格仅代表本次账户与参数。
- 实际提示词保存在 `actual-prompts/S03-image.txt`、`S04-image.txt`、`S03-video.txt`、`S04-video.txt`；文字与计划文件相同。来源与输出记入 `run-log.csv`，全部标记非正式成片采用。

## 文件

- `frames/S03_v01.png`、`frames/S04_v01.png`：生成首帧。
- `raw-video/S03_v01.mp4`、`raw-video/S04_v01.mp4`：平台下载原片，保留水印。
- `exports/Jessica-to-Feng_4s_v01_480p.mp4`：无声 4 秒小样，854×480、H.264、30fps、120 帧；原片略非16:9，用窄黑边补足，未裁掉人物。
- `make_handoff_sample.py`：可复现裁切及拼接。Jessica 源片 2.0–4.0 秒，Feng 0.5–2.5 秒，各 2 秒，硬切。
- `previews/S03-contact.jpg`、`S04-contact.jpg`：原片每秒接触表。
- `previews/libtv-completed.jpg`：生成完成及余额截图。

## 观察与限制

两人单独生成，未发生 Jessica 变成 Feng 的身份融合；动作方向都向右，Feng 能入场后站稳。Jessica 离场约在3秒后完成，因此本轮改用2–4秒，使切点位于空舞台。材质与配色接近，但两镜彩带几何、机位和人物大小有跳变，不能判定无缝通过。两人的运动偏跑步／跨步，未达到原定贴地侧滑，Feng 的舞蹈律动偏弱。480P 与 LibTV 水印均仅适合预演。下一轮优先收紧动作到“短距离侧滑、双鞋交替贴地、禁止跑跳”，固定首帧机位及人物尺寸，再考虑更高档模型；目前没有继续付费生成。
