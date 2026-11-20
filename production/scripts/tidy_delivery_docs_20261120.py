"""Archive outdated entry points and write the approved final delivery index."""
from pathlib import Path
import json
import shutil

P = Path(__file__).resolve().parents[1]
R = P.parent

def archive(path):
    dest = path.with_name(path.stem + '-HISTORY-20261120' + path.suffix)
    if not dest.exists():
        shutil.copy2(path, dest)
    return dest.name

def write(path, text):
    path.write_text(text.strip() + '\n', encoding='utf-8')

for path in [R/'README.md', P/'00-START-HERE.md', P/'04-DELIVERY-CHECKLIST.md', P/'VERIFICATION.md']:
    archive(path)

write(R/'README.md', '''
# MS Kickoff FY27 · AI Dance Challenge

**2026-11-20 正式定稿，用户确认“完美，定稿！！！”；最终采用 v05。**

团队：**STCA M365 Copilot Foundation & Platform Team**。六位卡通伙伴在光束接力中依次起舞，最终汇合，拉远揭示并共同点亮 Copilot Logo；以 Baoli、Yun 两小只探头挥手合影谢幕。

| 用途 | 文件 | 规格 |
| --- | --- | --- |
| 正式播放／交付 | [正式版](production/exports/FY27-Kickoff-FINAL-1080P.mp4) | 1080P，30fps，55.43秒，54.54MB |
| 微信分享预览 | [微信压缩版](production/exports/FY27-Kickoff-WeChat-720P.mp4) | 720P，30fps，55.43秒，8.94MB |
| 交付与复现说明 | [最终交付记录](production/25-FINAL-DELIVERY-v01.md) | 实际时间线、源片、画布分组、验证 |

主创署名：**Created by Baoli Wang · Yun Gu**。

[制作总入口](production/00-START-HERE.md) · [交付验收](production/04-DELIVERY-CHECKLIST.md) · [验证记录](production/VERIFICATION.md) · [素材索引](production/10-ASSET-NAME-INDEX.md)

视频通过 LibTV 的 Wan 3.0 生成，选用源片经 HuoShan 高清增强；图片使用 Dream-Painter／GPT Image 2 与 LibTV；音乐为 ElevenMusic V3。本地 Python／FFmpeg 完成精剪、字幕、合成和声音精修。片尾完整展示已确认的模型与工具信息。

视频和音频保留本地，仓库中的媒体链接需要本机素材齐全才能打开。本轮未提交或推送 Git，也未执行活动平台上传。

## 历史与原始素材

[原 README 与活动要求](README-HISTORY-20261120.md)保留当时背景、原始方案和待办；其中“尚未生成”“60秒方案”等不代表当前成片状态。

[角色定稿](assets/characters/README.md) · [舞台概念](assets/stage/README.md) · [早期创意](V2-LT-DANCE.md) · [早期剧本讨论](V2-SCRIPT-DRAFT.md)。历史文档用于追溯，交付以当前最终记录为准。
''')

write(P/'00-START-HERE.md', '''
# FY27 Kickoff · 定稿交付入口

**2026-11-20 已定稿：v05，55.433秒／1663帧／30fps。**

| 入口 | 用途 |
| --- | --- |
| [正式版 1080P／54.54MB](exports/FY27-Kickoff-FINAL-1080P.mp4) | 正式播放与交付；与用户通过的 v05 逐字节一致 |
| [微信版 720P／8.94MB](exports/FY27-Kickoff-WeChat-720P.mp4) | 完整内容分享预览；体积减少83.6% |
| [最终交付与复现说明](25-FINAL-DELIVERY-v01.md) | 时间线、源片、制作信息、画布整理、校验 |

正式团队名：**STCA M365 Copilot Foundation & Platform Team**。主创：**Baoli Wang · Yun Gu**。

## 当前采用结构

CG片头4秒 → A Jessica追光9.933秒 → B Feng／Scott／三人12秒 → C Song／Amy 8秒 → D v08前4秒独舞＋v13后4秒群舞 → E Logo揭示8秒 → F 合影片尾5.5秒。

A在追光过程中结束，B前8帧补余光；不采用新A v08。片尾单次挥手后保留合影，最后0.3秒音画共同淡出。片头标题100／66px、一次蓝青扫光；三处转场光束、Scott旋转和片头跨A余响均已纳入正式版。

## 制作记录

- [验收表](04-DELIVERY-CHECKLIST.md) · [验证记录](VERIFICATION.md)
- [高清升级](23-HD-FULL-FILM-v01.md) · [片头与声音精修、最终确认](24-TITLE-RELAY-POLISH-v01.md)
- [片尾制作](19-F-ENDING-PLAN-v01.md) · [片头制作](20-INTRO-COMPARISON-v01.md)
- [素材命名索引](10-ASSET-NAME-INDEX.md) · [画布整理后清单](canvas-after-final-tidy-20261120.json)
- [正式版校验清单](exports/FY27-Kickoff-FINAL-manifest.json) · [微信版校验清单](exports/FY27-Kickoff-WeChat-manifest.json)
- [片尾文字与制作信息](credits-info.json)

## 历史规划与执行材料

[v07五段导演蓝图](16-FIVE-SEGMENT-DIRECTOR-BLUEPRINT-v07.md)、[关键帧准备](17-KEYFRAME-PREPARATION-v07.md)、prompts／actual-prompts／各段提交JSON保留规划和实际生成参数。原始生成时长、Prompt与最终取段不同是正常的，剪辑请遵循最终交付记录。

早期60秒／1800帧、48秒故事＋12秒片尾和旧音乐切分均为历史规划，不再作为当前时间线。[原首页完整历史](00-START-HERE-HISTORY-20261120.md)。

本轮压缩、文档和画布整理0积分，未重新生成，未删除历史素材，未执行Git提交／推送或活动平台上传。
''')

write(P/'25-FINAL-DELIVERY-v01.md', '''
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

以下采用30fps、左闭右开区间；秒数显示为近似值，帧数为准。

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

本轮压缩、文档更新和画布整理均0积分；未重新生成媒体、未执行Git提交／推送、未向微信收件人发送或向活动平台提交。活动上传路径、截止时刻及原始Prompt交付口径仍以主办方最新通知为准。当前成片有制作信息，没有另附全文Prompt滚屏；历史Prompt与日志保留为附件材料。
''')

write(P/'04-DELIVERY-CHECKLIST.md', '''
# 最终视频交付验收 · 2026-11-20

依据用户已通过的v05与实际文件。完整说明见[最终交付记录](25-FINAL-DELIVERY-v01.md)。

- [x] 用户确认“完美，定稿！！！”；正式1080P文件与v05逐字节一致。
- [x] MP4／H.264／AAC，1920×1080、16:9、30fps、1663帧、55.433秒，少于1分钟。
- [x] CG片头团队名称、A–E舞蹈与Logo揭示、F英文制作信息均已纳入定稿。
- [x] A追光切B补余光；D采用v08前4秒＋v13后4秒。
- [x] 片头扫光、三处光束声、Scott旋转声、片头到A余响衔接均已采用。
- [x] 片尾单次挥手后合影；末0.3秒音画共同淡出。
- [x] 高清增强来源与本地合成方式已记录；不宣称原生1080P生成。
- [x] 微信720P副本8.94MB，完整时长与1663帧保持；完整解码通过。
- [x] 采用源片、历史版本、Prompt和日志保留；画布命名及分组已整理。
- [x] 正式版、微信版均有SHA256及manifest。
- [ ] 微信收件端播放实测（本轮未发送）。
- [ ] 按主办方最新通知核对上传位置、截止时刻及Prompt附件／展示要求；当前片尾没有全文Prompt滚屏。
- [ ] 核对活动使用与分发权限；本轮没有重新核实平台许可条款。
- [ ] 实际上传活动平台并确认成功；本地定稿不等于已提交。

[旧版验收规划](04-DELIVERY-CHECKLIST-HISTORY-20261120.md)保留追溯，其中60秒／1800帧等已由实际交付替代。
''')

write(P/'VERIFICATION.md', '''
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
''')

index=P/'10-ASSET-NAME-INDEX.md'
old=index.read_text(encoding='utf-8-sig')
if not old.startswith('> **2026-11-20 定稿索引'):
    write(index, '> **2026-11-20 定稿索引：** 当前采用源片、实际取段和画布分组见[最终交付记录](25-FINAL-DELIVERY-v01.md)与[整理后节点清单](canvas-after-final-tidy-20261120.json)。下文为素材命名演进历史，旧名称及早期分段不代表定稿时间线。\n\n'+old)

for name in ['23-HD-FULL-FILM-v01.md', '24-TITLE-RELAY-POLISH-v01.md']:
    path=P/name
    old=path.read_text(encoding='utf-8-sig')
    prefix='> **当前状态：2026-11-20 已正式定稿v05。** '
    if not old.startswith(prefix):
        write(path,prefix+'下文待回看字样属于阶段记录，交付以[最终交付记录](25-FINAL-DELIVERY-v01.md)为准。\n\n'+old)

credits=P/'credits-info.json'
data=json.loads(credits.read_text(encoding='utf-8-sig'))
data.update(share_file='exports/FY27-Kickoff-WeChat-720P.mp4', share_manifest='exports/FY27-Kickoff-WeChat-manifest.json', share_bytes=8941492, share_resolution='1280x720', delivery_record='25-FINAL-DELIVERY-v01.md', canvas_tidy_record='canvas-after-final-tidy-20261120.json', canvas_tidy_date='2026-11-20', delivery_tidy_credits_spent=0)
write(credits,json.dumps(data,ensure_ascii=False,indent=2))
print('Delivery documents updated; prior entry points archived in place.')
