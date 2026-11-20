# FY27 Kickoff · 最终交付记录

日期：2026-11-20。用户确认“完美，定稿！！！”；正式版为精修 v05。本文记录实际交付，替代早期60秒规划。

## 文件

| 用途 | 文件 | 分辨率／帧率 | 时长 | 体积 |
| --- | --- | --- | --- | --- |
| 正式播放与交付 | [FINAL-1080P](exports/FY27-Kickoff-FINAL-1080P.mp4) | 1920×1080／30fps | 55.433秒 | 54,542,732字节 |
| 微信分享预览 | [WeChat-720P](exports/FY27-Kickoff-WeChat-720P.mp4) | 1280×720／30fps | 55.433秒 | 8,941,492字节 |

两版均为MP4／H.264／AAC、16:9、1663帧。微信版保留完整内容、音乐与字幕，双遍1200kbps视频＋96kbps立体声音频，yuv420p／High Level3.1／faststart，体积减少83.6%。720P用于分享预览，正式提交使用1080P。微信客户端仍可能再次压缩；未在收件端实测。

[正式版manifest](exports/FY27-Kickoff-FINAL-manifest.json) · [微信版manifest](exports/FY27-Kickoff-WeChat-manifest.json)

## 实际剪辑时间线

以下采用30fps、左闭右开区间；秒数显示为近似值，帧数为准。[可复用剪辑时间表CSV](final-edit-timeline-20261120.csv)。

| 段落 | 成片时间／秒 | 全局帧区间 | 采用内容 |
| --- | --- | --- | --- |
| INTRO | 0–4 | 0–120 | CG追光、脉冲、团队标题 |
| A | 4–13.933 | 120–418 | A v07源12秒，取前298帧；追光过程结束 |
| B | 13.933–25.933 | 418–778 | B v08完整12秒；前8帧补蓝青余光 |
| C | 25.933–33.933 | 778–1018 | C v08完整8秒 |
| D1 | 33.933–37.933 | 1018–1138 | D v08源8秒取前4秒独舞 |
| D2 | 37.933–41.933 | 1138–1258 | D v13源8秒取后4秒六人群舞 |
| E | 41.933–49.933 | 1258–1498 | E v08完整8秒，拉远揭示Logo |
| F | 49.933–55.433 | 1498–1663 | 双人探头单次挥手后合影、英文制作信息；最后0.3秒音画共同淡出 |

D原始节点名含Renwei，用户在选取独舞时称Scott；本次统一用D1“独舞”标明取段，保留原始记录，不依据旧名更改人物资产。

## 高清源片与画布

LibTV中Wan 3.0／480P源片保留，采用源片经HuoShan画质增强至1080P／30fps。下载实测1922×1080，本地合成为1920×1080；这属于高清增强，不是原生1080P重新生成。F复用E高清末帧与既有双人动画本地合成。

| 段落 | 高清节点 | 本地 videos/ 下文件 |
| --- | --- | --- |
| INTRO | v-6e7QwOGXOe | INTRO-CG-HuoShan-1080P30-HD-v01.mp4 |
| A | v-002YZjAFcl | SEG-A-v07-HuoShan-1080P30-HD-v01.mp4 |
| B | v-VWxQswHYvB | SEG-B-v08-HuoShan-1080P30-HD-v01.mp4 |
| C | v-y4mbwea2xS | SEG-C-v08-HuoShan-1080P30-HD-v01.mp4 |
| D1 | v-uyUL58uqhL | SEG-D-v08-HuoShan-1080P30-HD-v01.mp4 |
| D2 | v-Oq5pR9teGw | SEG-D-v13-HuoShan-1080P30-HD-v01.mp4 |
| E | v-52Hb9y4LAR | SEG-E-v08-HuoShan-1080P30-HD-v01.mp4 |

[LibTV制作画布](https://www.liblib.tv/canvas?guideSource=home-feature-grid&spaceId=16349996&projectId=a955aae8171f4a67b8bc47f6142d931d)已整理：

- `00-FINAL-HD-定稿采用源片-按00至06顺序`：7条高清采用源，编号表达剪辑顺序。
- `01-FINAL-F-片尾双人形象与动画源片`：统一画风图、左右透明人物图、6秒动画源，共4项。
- 角色、舞台母版、局部01–06、关键帧和历史测试原有分组保留；自动整理布局已保留。
- A及D源片名称注明实际取段，F改为采用，Topaz对比标明未采用；早期音乐切片组标为`ARCHIVE-MUSIC-早期分段-非定稿时间线`。

未删除源片或历史候选，原引用连线保留。画布中的采用视频是源片，完整字幕、精剪、混音与分享压缩在本地完成，不应将单个画布源节点当成最终成片。

[整理前清单](canvas-before-final-tidy-20261120.json) · [整理后节点／重命名／分组记录](canvas-after-final-tidy-20261120.json) · [画布截图](previews/FINAL-canvas-organized-20261120.png)

## 画面、声音与片尾

片头第一行100px、第二行66px，一次蓝青扫光。保留CG原生音效；A→B、B→C、C→D补轻量光束声，Scott旋转34.30–37.12秒补一次轻掠过；片头余响延续进入A段0.28秒。音乐沿用已通过的ElevenMusic V3主曲统一剪辑，不使用早期按60秒规划的分段直接拼接。

片尾按以下顺序居中排版，创意句突出、主创正常字重、技术信息较小：

> Passing the spark, bringing Copilot to life together.
>
> Created by Baoli Wang · Yun Gu
>
> AI Models: Seedance 2.5 · Wan 3.0 · GPT Image 2 · Lib Image 2.5 Pro · ElevenMusic V3
>
> Tools: Copilot · Codex · LibTV · Dream-Painter · CapCut

技术署名按用户确认的制作信息保留；实际定稿舞蹈采用Wan 3.0。未把Seedance测试或其他历史候选误写为最终采用视频模型。

## 复现与校验

正式版是用户通过的[精修v05](exports/FY27-CG-intro-A-F-55p43s-1080P-v05-intro-a-audio-bridge-music.mp4)逐字节复制，SHA256：`52ea529519aef33922f1186292a0a2d54103b4d803f4a5c4e1db765018ef2a0d`。

微信版SHA256：`d207fe894308dc91c9bad8f94b05e22048c291cf9d60e0c1f3bd137b8eade07c`。尺寸、帧率、帧数与完整解码通过。

复现链为[高清合成](scripts/assemble_full_hd_v01.py) → [标题和转场声音](scripts/polish_title_transition_sfx_v02.py) → [旋转音效](scripts/add_scott_spin_sfx_v04.py) → [片头声音接点](scripts/smooth_intro_a_audio_v05.py)。需要本地源媒体和中间混音文件；旧文件保留，不必为本次交付再次渲染。

微信版由[压缩脚本](scripts/make_wechat_share_v01.py)输出；现有目标存在时只校验，不覆盖重编码。运行环境为Python 3.10，使用既有OpenCV、NumPy、Pillow、FFmpeg依赖。

压缩、文档更新和画布整理均0积分，未重新生成媒体。随后仓库同步图片、文档、脚本和制作记录，视频音频保留本地；未向微信收件人发送或向活动平台提交。活动上传路径、截止时刻及原始Prompt交付口径仍以主办方最新通知为准。当前成片有制作信息，没有另附全文Prompt滚屏；历史Prompt与日志保留为附件材料。
