# 资产名称与现有舞台素材索引

> 最新编号已按播放顺序调整：01 Jessica → 02 Feng → 03 Scott → 04 暖色接力 → 05 群舞；06为备用。下文早期06 Feng／02备用是历史命名，以文末“按播放顺序重编号”表及stage-canvas-name-map-20261118.json为准。

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

## Song／Amy／Renwei画布命名更新（2026-11-18）

用户完成正面图上传及多视图准备后，本次仅修改以下6个已有节点的显示名称，保留图片、节点ID与连线。多视图来自用户当前画布的3808×1632结果，不等同于本地1536×1024三视图文件；本次未触发生成。

| 节点ID | 当前名称 |
| --- | --- |
| i-FJj0jSYnVL | CHAR-Song-正面全身-v01 |
| i-PHayPm84M6 | CHAR-Song-多视图设定-v01 |
| i-5EaLZTHFnc | CHAR-Amy-正面全身-v01 |
| i-jMeEQyh1bC | CHAR-Amy-多视图设定-v01 |
| i-Rdk6hADvE5 | CHAR-Renwei-正面全身-v01 |
| i-P9XvulU7pU | CHAR-Renwei-多视图设定-v01 |

Renwei对应原wei-front-v01.png。已通过节点标题和资产管理列表核对名称。证据截图：previews/CHAR-Song-Amy-Renwei-renamed-20261118.jpg。

## Feng专用4K局部舞台

[STAGE-LOCAL-06-Feng-cyan-violet-4K-v01](frames/stage-locals/STAGE-LOCAL-06-Feng-cyan-violet-4K-v01.png)：3840×2160 PNG，dream-painter / GPT Image 2，单次生成。青蓝舞面连接右侧蓝紫高大折带，供Jessica与Scott之间的Feng段使用。静态画面已检查，无人物、无文字、未露全Logo；运动／段间接缝尚未验证，未上传、未生成新视频。旧素材保留。

主线按01→06→03→04→05→全景母版，02为备用；素材库6张局部，主线仍5张。正式采用须先看低成本衔接样片，其他局部当前为2K，不声称已全部4K。详见[连续性方案](13-STAGE-CONTINUITY-LOCK.md)、[生成记录](STAGE-LOCAL-06-Feng-cyan-violet-4K-v01-generation.json)、[静态顺序对照](previews/stage-continuity-route-v02.jpg)。

## 局部舞台画布统一名称（最新，2026-11-18）

已核对用户上传的5张新图并统一命名，原有蓝青局部编为01。本次仅修改6个现有节点显示名，不移动节点、不修改图片和连线、不触发生成。下表覆盖前文旧显示名，本地文件名保持原样。

| 节点ID | 旧显示名 | 当前显示名 |
| --- | --- | --- |
| i-rT6OBZqneE | STAGE-Copilot-蓝青局部空景-v01 | STAGE-Copilot-局部01-蓝青开场-2K-v01 |
| i-Fb9Mu0iXWH | STAGE-LOCAL-02-blue-side-v01 | STAGE-Copilot-局部02-蓝青拱折-2K-v01 |
| i-2otVSX966A | STAGE-LOCAL-03-violet-match-v01 | STAGE-Copilot-局部03-蓝紫接棒-2K-v01 |
| i-4cmaW64j1o | STAGE-LOCAL-04-warm-duo-v01 | STAGE-Copilot-局部04-暖色双人-2K-v01 |
| i-kzsIrmfBdI | STAGE-LOCAL-05-warm-ensemble-v01 | STAGE-Copilot-局部05-暖色群舞-2K-v01 |
| i-dgQOPwWiXd | STAGE-LOCAL-06-Feng-cyan-violet-4K-v01 | STAGE-Copilot-局部06-青蓝过渡-4K-v01 |

主线建议：01 Jessica → 06 Feng → 03 Scott → 04 暖色接力 → 05 群舞；02保留为备用。01–05为2048×1152，06为3840×2160；标题2K／4K只描述背景图片，不代表生成视频分辨率。核对截图：previews/STAGE-local-names-unified-20261118.jpg。

## 按播放顺序重编号（当前唯一有效编号）

按用户要求，Feng青蓝过渡从06改为02；原蓝青拱折从02改为06并明确备用。01、03、04、05不变。

| 编号 | 用途 | 当前画布名称 | 节点ID |
| --- | --- | --- | --- |
| 01 | Jessica | STAGE-Copilot-局部01-蓝青开场-2K-v01 | i-rT6OBZqneE |
| 02 | Feng | STAGE-Copilot-局部02-青蓝过渡-4K-v01 | i-dgQOPwWiXd |
| 03 | Scott | STAGE-Copilot-局部03-蓝紫接棒-2K-v01 | i-2otVSX966A |
| 04 | 后续接力 | STAGE-Copilot-局部04-暖色双人-2K-v01 | i-4cmaW64j1o |
| 05 | 六人群舞 | STAGE-Copilot-局部05-暖色群舞-2K-v01 | i-kzsIrmfBdI |
| 06 备用 | 备用 | STAGE-Copilot-局部06-蓝青拱折-备用-2K-v01 | i-Fb9Mu0iXWH |

本地原始生成文件名保留以确保提示词、日志及视频历史可追溯；当前素材编号按画布名执行。仅修改显示名称，未生成内容。截图：previews/STAGE-playback-order-renumbered-20261118.jpg。
