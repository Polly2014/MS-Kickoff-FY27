# Focus Kickoff · v05 电影级CG制作包

更新：2026-11-18。用户确认“一人踏出节拍，伙伴接住光，六人汇合共同点亮Copilot”的CG方向，会员已开通。已有4秒Mini试片和三张GPT Image2局部参考图；v05的Seedance2.5长段、六人群舞、音乐和最终成片仍待生成。不将计划或提示词当成效果保证。

先看[生成前准备包](07-PREPARATION-READY.md)：五种空间与群像参考已备，Scott已修正，并已整理[分段上传包](upload-pack/README.md)。C/E正式包仅待B/D采用后的真实出点帧；空间关系与动态身份仍需视频试制验收。[审计历史](06-ASSET-PROMPT-AUDIT.md)保留补图前的判断。

## 按这个顺序读和操作

1. [分段生成计划](05-GENERATION-PLAN.md)：12镜分为A4/B8/C12/D12/E12秒五段，包含可插入@素材的Prompt模板。
2. [完整剧本](01-FULL-SCRIPT.md)：48 秒故事 + 12 秒制作信息，共 60 秒。
3. [逐镜分镜](02-STORYBOARD.md)：12 镜，包含构图、参考素材、动作、转场、逐镜验收。
4. [v05操作指南](03-LIBTV-GUIDE-v05.md)：先B段8秒 → 六人/Logo验证 → 音乐 → 补其余段 → 终剪。
5. [段落时间线](generation-timeline.csv)、[12镜剪辑边界](edit-timeline.csv)与[计划提示词](prompts)：SEG-*为主路线，Sxx-*为拆镜补救。模板别名须换成页面插入的真实@标签。
6. [提交验收](04-DELIVERY-CHECKLIST.md)：逐项检查后再交付。

## 先看这三点

- 主路线是 **dream-painter / GPT Image2按需补图＋LibTV Seedance2.5分段视频＋后期精确终剪**。只在段落失败时拆镜，人物交接允许遮挡或动作匹配切镜，不让人变形成下一位。第一拍与最终点亮是两个视觉重点，中间克制留白。
- 正式锁定 **6人版**：Jessica、Feng、Scott、Song、Amy、Renwei。Zhuoying、Michael不纳入本片，不再等待照片。Wei＝Renwei已确认，源文件名保留Wei。前三位依次独立亮相，S07核心三人同框；S08为Song＋Amy，S09为Renwei，S10–S12六人群舞。Feng前排中央，Jessica／Scott第二排，其余三人第三排。正式团队名已确认：**STCA M365 Copilot Foundation & Platform Team**。
- 12 秒片尾无法让观众按正常语速读完所有原始 Prompt。本包安排“制作信息正常播放可读，全部原始 Prompt 分页暂停可读”，另交完整文本附件。**是否接受暂停阅读需按活动要求核对**；如果要求正常播放逐字读完，必须获准延长附录或改用附件，否则一分钟限制与全文阅读不能同时满足。不能把二维码或提示词摘要冒充全部原始 Prompt。

用户已确认会员开通；此前Mini试片实际花费94积分，开通前余额6积分，不能作为开通后当前余额。新会员各模型报价、分辨率和下载权益仍按实际面板核对。图片API费用独立于LibTV，实际账单未查询。

## 文件状态

`prompts/` 是计划提交的提示词。实际生成前如有改字，必须保存实际版本到 `run-log.csv` 所指文件，记录模型、参数、输入、结果。片尾从实际采用素材的生成记录制作，不能直接把本包计划文本标为已经使用。

分镜图仅为构图示意，不是正式美术资产；六位现有角色沿用，不重新设计。Mini视频与三张GPT Image2图的实际提示词、输出和run-log保留。v05本轮仅更新文档与生成计划，没有追加收费调用，也未提交活动作品。旧版在`../versions/v04-before-cinematic/`。公开能力研究见[调研](00-LIBTV-RESEARCH.md)，实测分别见[Mini记录](LIBTV-TRIAL-20261118.md)和[图像流程](DREAM-PAINTER-WORKFLOW.md)。
