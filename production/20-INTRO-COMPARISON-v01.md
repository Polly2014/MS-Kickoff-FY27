# 片头：B版节拍点火CG（已生成、拼接，待审）

用户否定A版叠字方案，要求删除；已删除该版专用试片、叠字帧、临时中间文件与脚本，旧A/B配置由当前B配置 `INTRO-B-CG-ready-v02.json` 替代。原满意正片v06与其素材不受影响。

团队名固定：STCA M365 Copilot Foundation & Platform Team，仍后期精确叠加。

B节点 `v-nkUzXaLEBh`：`INTRO-B-节拍点火CG-4s-Wan3-480P-v01-待生成`。Wan 3.0 / 全能参考 / 16:9 / 480P / 4秒 / 1条。已按用户方向开启音频，智能扩写与AutoLink仍关闭。真实@引用蓝青局部01 `i-rT6OBZqneE`，只定义材质与色彩，不露完整Logo。页面开音频后报价仍16积分（对照20），余额2467；未点击生成、0积分消耗。

画面与音效：0–0.6秒极暗舞台青光启动＋轻低频启动；0.6–1秒细光贴地疾驰、击中台面一点并扩散脉冲＋掠过声与一次紧致低频冲击；1–3.2秒中心留白给团队名＋微弱余鸣；3.2–4秒追光加速前冲、相机下压＋加速风切声。结尾不生成第二次撞击，留给原A段Jessica踩地与后期舞曲落拍。无背景音乐、旋律、鼓点、歌曲、人声或口播；避免长混响和持续轰鸣。模型能否准确对点须实际生成后判断。

实际提示词 `actual-prompts/INTRO-B-CG-ignite-Wan3-4s-sound-v02.txt`。截图 `previews/INTRO-B-CG-4s-sound-on-16credits-ready-v02.jpg`。用户此前要求付积分操作由本人点击，本轮仅配置，未生成。旧静音prompt和旧截图仅为历史配置，不是当前设置。


## B版提交记录

用户“开始吧”明确授权后，已点击16/20生成一次。提交时4秒、480P、Wan3、全能参考、原生音频开启，1121字实际提示词与蓝青局部01真实引用保留。任务已显示生成中，尚未获得结果；不自动重试。后期脚本 `scripts/assemble_intro_cg_v01.py` 已准备，须在下载实际素材并检查画面、声音后再运行。


## 当前结果：CG片头＋原A–F（待审）

本次仅生成一条，实际16积分，余额2467→2451。画布节点已改名 `INTRO-B-节拍点火CG-4s-Wan3-480P-v01-待审`。原片 `videos/INTRO-B-CG-ignite-4s-Wan3-480P-v01-source.mp4`，854×480、30fps、120帧；音轨实际存在，约4.04秒，峰值0.94685。生成截图 `previews/INTRO-B-CG-generated-16credits-v01.jpg`，抽帧联系表 `previews/INTRO-B-CG-raw-contact-v01.jpg`。

抽看贴地光弧、台面亮点、薄雾脉冲及末段前冲，未露完整Logo，画面无人物或生成字。开头比提示词设想更亮，脉冲稍晚于文字时间表；本轮没有追加生成。原生音轨有前后较强、中间较弱的声压变化；未宣称实际试听或自动音效逐点完全吻合，待用户审听。

团队名两行居中：STCA M365 Copilot / Foundation & Platform Team，字形用Segoe UI Semibold。本地以1080画布排字再缩到480预览；0.65–0.95秒渐显，3.1–3.4秒渐隐。保留完整4秒CG，直接接原正片v06第一帧白鞋踩地。CG原声音轨按峰值降约0.94dB，并只在首15ms、尾40ms做防突变淡化；4秒以后接原v06配乐，原画面与音乐整体后移4秒，不改变其内部时序。未新增音乐。

- 前9秒预览：`previews/INTRO-B-CG-to-Jessica-first9s-v01-music.mp4`
- 全片55.433秒：`exports/FY27-CG-intro-A-F-55p43s-480P-v01-music.mp4`
- 复现：`scripts/assemble_intro_cg_v01.py`
- 验证清单：`exports/INTRO-B-CG-assembled-v01-manifest.json`

全片1663帧/30fps、完整解码通过；顺序解码抽查原A–F八处画面，与原正片像素一致。原正片v06保留，当前合成为待用户审片版本。


## 标题放大v02（待审，本轮0积分）

用户已确认B片头＋正片v01效果。随后同意第一行放大约20%、第二行约15%，本轮仅做本地字形调整。1080参考画布第一行76→91px（+19.74%），第二行57→66px（+15.79%）；组中心与居中对齐保持，细调两行基准位置以保留行间距。字体仍Segoe UI Semibold、同色白字、同样淡蓝光晕；显示时段0.65–3.4秒不变，原声音轨直接复制已通过v01。

输出 `exports/FY27-CG-intro-A-F-55p43s-480P-v02-large-title-music.mp4`；预览 `previews/INTRO-B-CG-to-Jessica-first9s-v02-large-title-music.mp4`；复现 `scripts/assemble_intro_cg_large_title_v02.py`；清单 `exports/INTRO-B-CG-assembled-v02-large-title-manifest.json`。

检查通过：1663帧/30fps、完整解码、A–F八处顺序抽帧像素一致、音频ADTS压缩包与已通过v01逐字节一致。原v01保留，0积分，待用户看放大字版。
