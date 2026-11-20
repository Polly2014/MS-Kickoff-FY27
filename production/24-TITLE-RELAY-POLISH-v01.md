> **当前状态：2026-11-20 已正式定稿v05。** 下文待回看字样属于阶段记录，交付以[最终交付记录](25-FINAL-DELIVERY-v01.md)为准。

# 片头文字与转场轻量精修 · 2026-11-20

用户已完整回看并通过HuoShan高清v01。随后要求按讨论优化片头文字，并说明希望补充的是正片几个转场的光束音效，片头原生音效已很好。

本轮全部本地完成，0积分，未调用LibTV生成。

## 待回看的精修版

- [55.43秒完整精修版：文字＋三处接力音效](exports/FY27-CG-intro-A-F-55p43s-1080P-v03-title-relay-sfx-music.mp4)
- [片头前9秒预览](previews/INTRO-polish-v02-first9s-music.mp4)
- [三处转场音效6秒合集](previews/HD-three-relays-v03-sfx-review.mp4)
- [仅文字精修＋原音轨完整版](exports/FY27-CG-intro-A-F-55p43s-1080P-v02-title-polish-music.mp4)
- [验证数据](exports/HD-polish-v03-manifest.json) · [本地脚本](scripts/polish_title_transition_sfx_v02.py)

片头第一行由91px改为100px（约+10%），第二行保持66px。保留原淡入淡出，0.97–1.62秒增加一次沿文字笔画移动的蓝青高光，不穿过背景，不新增片头音效。

正片只补三处光束：A→B（13.22–14.10秒）、B→C（25.39–26.22秒）、C→D（33.22–33.84秒）。根据可见光束出现位置对齐，使用本地合成的轻空气掠过声和很弱的短脉冲，并有克制左右声像；没有每个切镜都添加。D→E原本是连续舞蹈，没有补音效。

原混音不做全局增益或闪避，片头和片尾不添加音效。试听版混合后AAC重编码，片头输入PCM未改；仅文字版直接复制原压缩音轨，便于选择。

保留原1080P已通过版本及精修候选，待用户决定采用哪版。时长仍为55.433秒、1663帧、1920×1080／30fps。

## Scott 旋转音效 v04

用户对文字与转场精修反馈“非常好”，并同意为Scott独舞转圈补一声轻掠过。已在D段独舞地板旋转的34.30–37.12秒加入一次温和的空气旋转声：低中频较暖，随动作渐强再退去，有轻微左右声像，没有撞击或电子脉冲。

[5.5秒局部试听](previews/Scott-spin-v04-sfx-5p5s-review.mp4) · [完整v04](exports/FY27-CG-intro-A-F-55p43s-1080P-v04-scott-spin-sfx-music.mp4) · [验证记录](exports/HD-scott-spin-v04-manifest.json) · [脚本](scripts/add_scott_spin_sfx_v04.py)。

从v03编码前的无损混音WAV增加该声，再编码AAC256k，避免累计AAC压缩。视频流逐字节与v03一致；完整解码通过；仍为1663帧、30fps、55.433秒。音效平均电平比同期音乐约低23.5dB。片头、三处光束、片尾的混音输入保持原有内容。本轮0积分，v04待用户试听。

## 片头→A声音衔接 v05

用户反馈Scott转圈音效“可以的”，并同意柔化片头到A的声音接点。原片头在3.96–4.00秒做40ms淡出，本轮使用原CG音效最后0.5秒生成一层柔和、削弱高频的扩散立体声余响，在3.72秒渐入、延续到A的4.28秒归零。没有改变音乐入场位置、拍点、音乐音量或画面剪辑。

[6秒先前后新版对比（Before／After各3秒）](previews/INTRO-A-v04-v05-audio-bridge-before-after-6s.mp4) · [新版局部预览](previews/INTRO-A-v05-audio-bridge-6s-review.mp4) · [完整v05](exports/FY27-CG-intro-A-F-55p43s-1080P-v05-intro-a-audio-bridge-music.mp4) · [验证记录](exports/HD-intro-a-bridge-v05-manifest.json) · [脚本](scripts/smooth_intro_a_audio_v05.py)。

使用v04编码前混音WAV处理，余响区间外的PCM不变；AAC256k重新编码。视频压缩流与v04逐字节一致，全片完整解码通过，仍为55.433秒、1663帧、1920×1080／30fps；混音无削波。本轮0积分，v05待用户试听，旧版保留。


## 正式定稿 · 2026-11-20

用户确认“完美，定稿！！！”；最终采用v05，前述待审状态均为历史记录。[正式成片](exports/FY27-Kickoff-FINAL-1080P.mp4)为v05原文件复制，SHA256一致，没有再次渲染或编码；55.433秒、1920×1080、30fps，所有已通过音画效果保留。[定稿清单](exports/FY27-Kickoff-FINAL-manifest.json)。本次归档0积分。
