# 资产名称与现有舞台素材索引

更新：2026-11-18。此表整理名称与来源，不代表新增生成或最终采用。

## LibTV 手工试片画布：已执行重命名

画布：<https://www.liblib.tv/canvas?guideSource=home-feature-grid&spaceId=16349996&projectId=a955aae8171f4a67b8bc47f6142d931d>

| 原节点名 | 当前节点名 |
| --- | --- |
| 图片节点 1 | CHAR-Jessica-正面全身-v01 |
| 角色设定图 | CHAR-Jessica-多视图设定-v01 |
| feng-front-v01.png | CHAR-Feng-正面全身-v01 |
| 角色三视图 | CHAR-Feng-多视图设定-v01 |
| copilot-logo-stage-overview-v01.png | STAGE-Copilot-全景概念-v01 |
| 多机位九宫格 | STAGE-Copilot-多机位九宫格-v01 |
| 视频节点 10 | TEST-A-Jessica到Feng-15s-Wan3-480P-v01 |

仅修改显示名称，原节点、连线、参考图片、提示词与视频保留。视频名称中的模型依据节点当前可见配置；本次未查询独立账单。画布中的原始概念图为1200×800，区别于下列4K全景。九宫格为用户当前画布资产，不冒称本地生成文件。

## 本地既有舞台素材：统一检索别名

以下为索引别名，原始文件不改名，保留已有Prompt、manifest和上传包的引用。

| 检索别名 | 来源 | 内容及复用注意 |
| --- | --- | --- |
| STAGE-Copilot-全景母版-v02 | [STAGE_MASTER](frames/STAGE_MASTER-gpt-image-2-v02.png) | 3840×2160空舞台，完整Logo；适合最终揭示及美术母版 |
| STAGE-Copilot-蓝青局部空景-v01 | [HANDOFF-stage](frames/HANDOFF-stage-gpt-image-2-v01.png) | 2048×1152，局部空舞台；优先检查是否适合当前舞段 |
| SCENE-Jessica-蓝青局部-v01 | [HANDOFF-jessica](frames/HANDOFF-jessica-gpt-image-2-v01.png) | 同机位含Jessica，可参考人物与台面的尺度 |
| SCENE-Feng-蓝青局部-v01 | [HANDOFF-feng](frames/HANDOFF-feng-gpt-image-2-v01.png) | 同机位含Feng，可参考人物与台面的尺度 |
| SCENE-核心三人-暖色局部-v02 | [CORE3_MASTER](frames/CORE3_MASTER-gpt-image-2-v02.png) | Jessica/Feng/Scott；含人物，不是纯背景 |
| SCENE-Song-Amy-暖色局部-v01 | [DUO_MASTER](frames/DUO_MASTER-gpt-image-2-v01.png) | 双人场景；含人物，不是纯背景 |
| SCENE-六人-暖色局部-v03 | [GROUP_LOCAL](frames/GROUP_LOCAL-gpt-image-2-v03.png) | 六人局部；含人物，不是纯背景 |
| SCENE-六人-全景-v03 | [GROUP_MASTER](frames/GROUP_MASTER-gpt-image-2-v03.png) | 4K六人全景，Scott已修正；前两版不作为当前推荐 |

[八张素材总览](previews/stage-asset-index-20261118.jpg)

## 复用顺序

先检查蓝青局部空景与两张同机位人物图；不需要重复生成这些已有素材。暖色区域目前列出的可用图均含人物，若确实需要暖色空景，再按当前舞段构图去人物或补图。现有图片在设计上相关，但没有经过三维相机标定，不能保证模型运镜时完全保持几何连续。

CHAR表示白底人物身份素材，STAGE表示空舞台或舞台设计图，SCENE表示含人物的场景图，TEST表示技术试片。版本沿用来源版本，避免把旧候选误认成新版本。

## 第二段工作资产（2026-11-18）

| 用途 | 本地文件 | LibTV节点 |
| --- | --- | --- |
| A→B承接参考，A段12秒实际画面 | frames/continuity/KF-AtoB-Feng-fullbody-12s-candidate-v01.png | i-OeWdbiLoT2 |
| Scott单人身份定稿 | ../assets/characters/production-pack/scott/scott-front-v01.png | i-e1Zmtro5VV |
| Scott接棒构图，GPT Image 2派生 | frames/continuity/KF-B-Scott-blueviolet-gpt-image-2-v01.png | i-ZVD1cX5WEo |
| TEST-B-Feng到Scott-蓝紫局部-15s-Wan3-480P-v01 | 配置见TEST-B-Feng-Scott-v01-generation.json，结果以status为准 | v-mkFVjwxt8O |

Scott接棒构图使用STAGE_MASTER-gpt-image-2-v02.png作舞台设计参考，同时匹配A段实际画面的局部机位与光色。完整Logo母版未直接作为B段视频参考，避免提前全景揭示。局部图继承设计，不声称具有经过标定的三维几何。B段单次生成预算60积分，480P、15秒、无音轨；A段与旧试片保留。

## 蓝青局部舞台验证（2026-11-18）

- 上传节点 `i-rT6OBZqneE`：STAGE-Copilot-蓝青局部空景-v01，引用既有HANDOFF-stage图片。
- 结果节点 `v-qFpcETQeIX`：TEST-A-Jessica到Feng-蓝青局部-15s-Wan3-480P-v02。
- [成片](raw-video/TEST-A_blue-local_v02.mp4) / [抽帧](previews/TEST-A-blue-local-v02-contact.jpg) / [配置与评估](TEST-A-blue-local-v02-generation.json)。
- Wan 3.0全能参考，480P，15秒，1条，60积分；余额3496→3436。原始视频与引用保留。仅替换第三张舞台参考，提示词正文保持一致（原文写12秒，UI仍15秒）。局部舞台验证有效，末尾有裁头，尚未选为正式成片。

## B段试片结果归档

B段已完成，单次60积分，余额3376。原画布节点 `v-mkFVjwxt8O`；[检查记录](TEST-B-Feng-Scott-v01-REVIEW.md)与[配置](TEST-B-Feng-Scott-v01-generation.json)已保存。浏览器下载尚未返回文件，未生成本地AB拼接版。约14.5秒Scott全身截图见 `previews/TEST-B-Feng-Scott-v01-browser-14p5s.jpg`。

## 新增局部空舞台包 v01

四张已生成并目视检查的候选空背景，2048×1152，dream-painter / GPT Image 2。当前仅本地归档，未上传LibTV，未生成新视频。API费用未查询，与LibTV积分分开。

| 文件 | 用途 |
| --- | --- |
| [STAGE-LOCAL-02-blue-side-v01](frames/stage-locals/STAGE-LOCAL-02-blue-side-v01.png) | 单人快速脚步、侧向跟拍、倒立全身 |
| [STAGE-LOCAL-03-violet-match-v01](frames/stage-locals/STAGE-LOCAL-03-violet-match-v01.png) | 匹配B段Scott所在机位，供换人和后续衔接 |
| [STAGE-LOCAL-04-warm-duo-v01](frames/stage-locals/STAGE-LOCAL-04-warm-duo-v01.png) | 后续双人接力与对舞，冷区切到暖区 |
| [STAGE-LOCAL-05-warm-ensemble-v01](frames/stage-locals/STAGE-LOCAL-05-warm-ensemble-v01.png) | 三至六人队形、齐舞与最终揭示前的过渡 |

[四图总览](previews/stage-local-pack-v01-contact.jpg) / [使用说明](12-STAGE-LOCAL-SHOT-PACK.md) / [提示词路径与生成记录](stage-locals-v01-manifest.json)。这些为参考图派生背景，非三维标定的多相机输出。02实图机位偏正面斜向，不作为严格侧拍反打；03保留部分地面青色光线，去人并非像素级固定背景。
