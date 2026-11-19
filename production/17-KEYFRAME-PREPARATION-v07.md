# 关键构图准备单 v07

2026-11-19。完成目标构图定义、现有来源检查与图像Prompt，尚未生成新关键帧。四类P0＋一个P1可选；不是五段各做一对首尾帧，也不是需要十张新图。

## 检查结论

本轮实际查看了CORE3_MASTER-v02与GROUP_LOCAL-v03预览：三人图为暖色静态站姿，与B段蓝紫03不一致；六人图有正确队形来源，但仍为静态站姿。它们可以提供身份与站位，不证明动态间距、05局部或连续升镜已匹配。

所有新目标统一16:9；若后续真用首尾帧模式，先核对图片尺寸是否覆盖输出比例，以及当前Wan面板是否支持该组合。不可从Agent描述推断所有模型能力相同。

| 构图 | 优先级 | 用途 | 本轮状态 |
| --- | --- | --- | --- |
| KF_AB_FENG | P0 | A出点与B起点：局部02的Feng全身蓄力 | 目标已定义，旧Demo帧不是匹配02的正式素材 |
| KF_B_CORE3 | P0 | B后4秒：03蓝紫区三人完整共舞构图 | 三人来源已存在，需改场景匹配与动作间距 |
| KF_DE_GROUP | P0 | D后4秒与E起点：05六人齐舞构图 | 六人来源已存在，需核对05与全景空间关系 |
| KF_E_LOGO | P0 | E约4秒到达的全景与结束构图 | Logo与六人全景来源已存在，需统一观察方向与尺度 |
| KF_A_SHOE | P1可选 | A开场半秒鞋部首帧 | 仅当构图需要精控时补 |

## 首尾帧使用表

| 段 | 起点策略 | 段内／终点策略 |
| --- | --- | --- |
| A | 可选鞋部首帧；模型不支持时用参考与文字控制 | KF_AB_FENG用于后2秒参考，不把它当开场 |
| B | A选定实际出点帧，前期以KF_AB_FENG设计 | KF_B_CORE3仅后4秒参考；换人由剪切建立，不默认锁全段双帧 |
| C | Song在新机位地板动作的起势；沿用04场景参考 | Amy在右侧交接；不硬套三人出点帧作首帧 |
| D | Renwei新机位低位起势 | KF_DE_GROUP用于后4秒，明确切六人，不瞬移 |
| E | D选定实际六人出点帧；前期以KF_DE_GROUP设计 | KF_E_LOGO为第4秒到达目标，尾帧能力实测支持时才启用；尾帧不能把揭示拖到末尾 |

实际抽帧要记录源片、时间戳、人物、舞台编号和图像尺寸，不能把AI设计图标成视频抽帧。只有前段已选用后才确定正式交接帧；不依赖Demo决定蓝图。

## 图像任务卡与完整Prompt

图片按需用dream-painter／GPT Image 2。单人身份以画布最新确认版为准，下列本地文件是可追溯来源候选，补图前核对与画布一致，不拿旧图替换新版。下面planned_output只是计划路径，当前没有这些生成输出。

### KF_AB_FENG｜A后2秒构图／B首帧目标

缺口：已有Demo抽帧来自01旧舞台，不能当作02正式交接帧；目标图未生成。

来源（相对production）：

- ../assets/characters/production-pack/feng/feng-front-v01.png：存在，1024×1536
- frames/stage-locals/STAGE-LOCAL-06-Feng-cyan-violet-4K-v01.png：存在，3840×2160

完整图像Prompt：[KF_AB_FENG](prompts/keyframes-v07/KF_AB_FENG.txt)

生成16:9横屏电影级3D卡通舞蹈MV关键构图。参考Feng单人身份图锁定脸型、发际线、眼镜、比例、深蓝队服和白鞋；参考局部02锁定青蓝过渡台面与远处暗紫折叠，不能用01替代。只出现一个Feng，完整全身居中，头顶、双手、双鞋留边，前方与身体两侧留足地板动作空间。Feng面朝镜头略偏画面右，双脚分开，右脚略前、左脚略后，两脚掌贴地，膝盖弯曲、重心下沉、双手低位打开，像正在接下一拍而不是站定合照。机位为略低斜前方，看清面部和地面接触，光从画面左方抵达，青蓝环境与柔和脸部主光，鞋底阴影清楚。只展示局部Logo实面，不展示全貌、不改变台面几何、不新增底座，无文字水印。

### KF_B_CORE3｜B段8–12秒段内三人构图参考

缺口：本轮查看的既有三人母图是暖色台面、静态站姿；需适配03蓝紫区域及舞蹈间距，不能直接作为已经匹配的首尾帧。

来源（相对production）：

- frames/CORE3_MASTER-gpt-image-2-v02.png：存在，2048×1152
- ../assets/characters/production-pack/jessica/jessica-front-v01.png：存在，1024×1536
- ../assets/characters/production-pack/feng/feng-front-v01.png：存在，1024×1536
- ../assets/characters/production-pack/scott/scott-front-v01.png：存在，1024×1536
- frames/stage-locals/STAGE-LOCAL-03-violet-match-v01.png：存在，2048×1152

完整图像Prompt：[KF_B_CORE3](prompts/keyframes-v07/KF_B_CORE3.txt)

生成16:9横屏电影级3D卡通街舞关键构图。三人母图仅参考Jessica、Feng、Scott身份关系与前后站位，三张单人图用于身份核对；场景必须以局部03蓝紫台面为准，不能复制三人母图的橙红暖色地面。Feng前中央，Jessica左后、Scott右后，正面完整全身同框，六只鞋与双臂均有活动空间，不互相挡脸或挡脚。三人正在同拍屈膝回弹、手臂半展开，呈现蓄力中的舞蹈状态，不做合照。服装、比例沿用身份，Scott浓密侧分头发和黑色矩形眼镜，与Feng明显不同。前景蓝紫带缘、中景人物、远景暗折带形成纵深，面部清楚。人物站在同一已有平缓实面，避开留白与陡坡，不新增平台，不完整曝光Logo，无文字水印。

### KF_DE_GROUP｜D段后4秒六人构图／E首帧目标

缺口：本轮查看的既有六人图身份队形可作来源，但仍是静态站姿；须核对05几何、动作间距，并与完整Logo母版建立可解释的相机关系。

来源（相对production）：

- frames/GROUP_LOCAL-gpt-image-2-v03.png：存在，2048×1152
- frames/stage-locals/STAGE-LOCAL-05-warm-ensemble-v01.png：存在，2048×1152
- frames/STAGE_MASTER-gpt-image-2-v02.png：存在，3840×2160

完整图像Prompt：[KF_DE_GROUP](prompts/keyframes-v07/KF_DE_GROUP.txt)

生成16:9横屏电影级3D卡通六人街舞关键构图。参考修正Scott后的六人图逐一保留身份：Feng前中央；Jessica第二排画面左、Scott第二排画面右；Song、Amy、Renwei第三排从左到右错位展开。Renwei保持不透明墨镜，Scott不能变成第二个Feng。用局部05及完整Logo母版共同确定同一舞台的暖色平缓实面与远处折叠关系，局部机位不展示完整Logo。正面中全景保留六人完整头手鞋，各排留够横向开臂和短交叉步空间，视线与地平线关系统一，避开中心空洞。六人处于同拍落脚后的膝部回弹，双手正由胸前打开，姿态有力且自然，不站定合照。光来自既定蓝色环境与柔和面部主光，暖色地面不过曝，脚底阴影方向一致，不新增台阶或独立底座。此图应能沿同一观察方向升高后退到完整Logo构图，无文字水印。

### KF_E_LOGO｜E约4秒到达的全景／结束构图

缺口：完整舞台与修正Scott后的群像来源已存在，仍需匹配局部05、观察方向、六人位置和最终尺度；不要求原图已具备相机标定。

来源（相对production）：

- frames/STAGE_MASTER-gpt-image-2-v02.png：存在，3840×2160
- frames/GROUP_MASTER-gpt-image-2-v03.png：存在，3840×2160

完整图像Prompt：[KF_E_LOGO](prompts/keyframes-v07/KF_E_LOGO.txt)

生成16:9横屏电影级3D卡通舞蹈MV全景关键构图。STAGE_MASTER-gpt-image-2-v02唯一决定完整Copilot折叠彩带外轮廓、交叠、配色和中心留白，禁止重画成其他Logo或新造舞台。修正Scott后的六人全景仅定义身份与1＋2＋3队形：Feng前中央，Jessica与Scott第二排左右，Song、Amy、Renwei第三排从左到右。六人位于与暖色局部05对应的平缓实面，身体完整，位置支持从局部机位沿同一方向升高后退到此全景；不能跨空洞或换到另一边。优先完整Logo与全团阵势，允许人物在远景变小，不为了读脸放大人物到错误比例。全团同拍落脚开臂的收招瞬间，蓝色环境保留，现有带缘达到亮度高潮，皮肤不过曝，留白干净，无新增人物、平台、文字或水印。

### KF_A_SHOE｜A段开场0–0.5秒的可选首帧

缺口：开场微距如难以稳定可补；不作为必须新增的图像任务。

来源（相对production）：

- ../assets/characters/production-pack/jessica/jessica-front-v01.png：存在，1024×1536
- frames/HANDOFF-stage-gpt-image-2-v01.png：存在，2048×1152

完整图像Prompt：[KF_A_SHOE](prompts/keyframes-v07/KF_A_SHOE.txt)

生成16:9横屏低机位鞋部特写。Jessica既定白鞋与深蓝裤脚，从画面左侧进入蓝青局部01的平缓实面，前脚鞋底即将或刚刚接触台面，后脚部分留在画外。鞋底接触阴影清楚，画面右侧留出地面细光前进空间；不要强加完整人物或完整Logo。舞台材质、厚度、远处暗折带沿用01，光色与后续Jessica舞段一致，无文字水印。

## 准备完成的判定

蓝图、文本Prompt与来源存在性已整理，不等于图像已生成或模型能力已验证。下一制作环节先匹配三人蓝紫构图、六人局部／全景构图；必要的新图生成后逐张检查身份、站位、舞台几何与动作间距，再将目标图和正式视频抽帧分别登记。Feng Flare与Renwei Windmill完整动作参考仍待选择，不以静态力量姿势图代替运动轨迹。

机器可读来源清单：[keyframe-readiness-v07.json](keyframe-readiness-v07.json)。本轮未调用dream-painter、LibTV或音乐生成。

## 画布素材绑定对照

| 模板别名 | 应绑定的素材 |
| --- | --- |
| JESSICA／FENG／SCOTT／SONG／AMY／RENWEI | 各自当前确认的单人全身图或多视图；身份优先，不能把多视角当多人 |
| STAGE_01 | STAGE-Copilot-局部01-蓝青开场-2K-v01 |
| STAGE_02 | STAGE-Copilot-局部02-青蓝过渡-4K-v01 |
| STAGE_03 | STAGE-Copilot-局部03-蓝紫接棒-2K-v01 |
| STAGE_04 | STAGE-Copilot-局部04-暖色双人-2K-v01 |
| STAGE_05 | STAGE-Copilot-局部05-暖色群舞-2K-v01 |
| KF_AB_FENG／KF_B_CORE3／KF_DE_GROUP／KF_E_LOGO | 本准备单定义的目标构图；当前未生成，不能假装画布已有同名成品 |
| AB_CONTINUITY | 正式选定A的Feng全身出点帧；前期以KF_AB_FENG设计目标，实际绑定前写清来源 |
| DE_CONTINUITY | 正式选定D的六人全身出点帧；前期以KF_DE_GROUP设计目标，实际绑定前写清来源 |

B段三人构图与D/E六人构图已经含对应演员，不意味着模型可以省略身份核对。若引用数超过当前模式上限，先按任务职责整理经核对的组合图，不删演员、不凭空假设能传30张，也不把未支持的接口字段贴入画布。
