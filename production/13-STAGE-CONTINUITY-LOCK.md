# 舞台局部与颜色连续性方案 v02

2026-11-18，按用户要求直接将画布素材编号改为播放顺序。本页与stage-canvas-name-map-20261118.json为当前依据。

## 当前编号与主线

| 编号 | 用途 | 当前画布名称 | 节点ID |
| --- | --- | --- | --- |
| 01 | Jessica | STAGE-Copilot-局部01-蓝青开场-2K-v01 | i-rT6OBZqneE |
| 02 | Feng | STAGE-Copilot-局部02-青蓝过渡-4K-v01 | i-dgQOPwWiXd |
| 03 | Scott | STAGE-Copilot-局部03-蓝紫接棒-2K-v01 | i-2otVSX966A |
| 04 | 后续接力 | STAGE-Copilot-局部04-暖色双人-2K-v01 | i-4cmaW64j1o |
| 05 | 六人群舞 | STAGE-Copilot-局部05-暖色群舞-2K-v01 | i-kzsIrmfBdI |
| 06 备用 | 备用 | STAGE-Copilot-局部06-蓝青拱折-备用-2K-v01 | i-Fb9Mu0iXWH |

主线直接按01→02→03→04→05→完整Logo母版。06仅备用，不作为暖色群舞后的下一镜。

## 原始文件映射

- 01：frames/HANDOFF-stage-gpt-image-2-v01.png。
- 02 Feng：frames/stage-locals/STAGE-LOCAL-06-Feng-cyan-violet-4K-v01.png（原生成编号06，现在播放编号02）。
- 03：frames/stage-locals/STAGE-LOCAL-03-violet-match-v01.png。
- 04：frames/stage-locals/STAGE-LOCAL-04-warm-duo-v01.png。
- 05：frames/stage-locals/STAGE-LOCAL-05-warm-ensemble-v01.png。
- 06备用：frames/stage-locals/STAGE-LOCAL-02-blue-side-v01.png（原生成编号02）。
- 全景：frames/STAGE_MASTER-gpt-image-2-v02.png。

原始生成文件名、提示词与日志作为来源记录保留；LibTV引用与播放编号使用当前画布名称，不能再从源文件名推断播放顺序。

## 舞台和颜色关系

青蓝→蓝紫→紫红／珊瑚暖色逐步推进，保留统一的深蓝环境与蓝色主光。颜色来自彩带不同物理区域，避免整体滤镜把人物肤色、白衣随背景一起染色。01到03保持左向右的视觉接力方向，切点仍需检查人物朝向、支撑脚、前进方向、带缘及阴影。

单镜头锁定对应局部图；跨区域用踩拍切镜、前景遮挡或同向甩镜，不要求两张图连续融化。03到04的冷暖变化较明显，利用共同紫色结构及蓝色环境光衔接，并检查04较亮暖色舞面的曝光。全身动作保留头、手、鞋及地面回旋范围。

## 高分辨率前的验证

02与全景母版为3840×2160，其他局部为2048×1152；标题2K／4K只描述图像。先以低成本样片验证动作力度、身份、构图、方向及曝光接缝，再锁定采用图和真实@绑定，按最终视频实际规格决定是否补高分辨率图。不得把放大480P片当作原生高清；高分辨率模型、时长与积分报价须提交前核对。

图像均为AI参考派生而非标定三维相机输出，静态图不能证明空间几何或动作无缝。已有A/B视频保持不变；这轮仅重编号，未触发生成。

## 当前证据

- previews/STAGE-playback-order-renumbered-20261118.jpg：画布当前编号截图。
- previews/stage-continuity-route-v02.jpg：既有静态颜色顺序对照，人物区域顺序不变。
- STAGE-LOCAL-06-Feng-cyan-violet-4K-v01-generation.json：播放编号02的原始生成记录。
