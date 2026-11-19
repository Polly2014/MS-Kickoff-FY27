# Focus Kickoff · v07 制作包与执行记录

2026-11-19 六人参考图v05：按用户确认的7张输入（六张单人正面＋dream-painter原队形图v03），已生成[原构图肤色修复图](frames/REF-DE-group-LibTV-v05.png)，画布节点i-l45S8LnTvc，Lib Image 2.5 Pro／16:9／标准画质／2K／1张，AutoLink关闭。本次39积分，余额2773→2734。[提示词](prompts/REF-DE-group-LibTV-v05.txt)、[记录](REF-DE-group-LibTV-v05-generation.json)与[画布预览截图](previews/REF-DE-group-LibTV-v05-review.jpg)已保存。已对照完整原图：俯视角、1+2+3纵深、舞台与人物占位基本保留，脸手肤色明显减轻橙褐暗色；面部表情及少量细节有重绘，并非像素级调色。原图、v04及D段v08/v09均保留，本轮未重做视频，待用户审图。

当前目标：A12＋B12＋C8＋D8＋E8＝48秒主体，另加12秒后期片尾。Demo只作效果参考。

仓库同步说明：视频与音乐源文件保留本地，本次同步图片、文档、提示词和制作记录；相关媒体链接需在本地素材齐全时打开。

2026-11-19执行更新：A段12秒新片已生成，用户同意保留空中传光。B段采用[接势修订Prompt v08](prompts/SEG-B-video-v08.txt)，[画布配置与实际引用](SEG-B-v08-canvas-preparation.json)及[提交记录](SEG-B-v08-submission.json)已保存；B已生成，用户反馈效果不错。B提交报价48积分，余额从2956变为2908。B引用A实际尾帧、Jessica/Feng/Scott多视图及02/03舞台，共6项；尾帧仅作构图参考，当前Wan全能参考模式首尾帧选项不可用。

C段已生成并获用户通过，用户备注Amy略有驼背；[提交记录](SEG-C-v08-submission.json)保留。C花费32积分，余额从2908变为2876。

D段v08已生成，用户反馈群舞人物肤色偏暗，旧视频节点v-mJlycCOmzY和旧合照均保留。

按用户要求，LibTV已生成[六人队形参考图v04](frames/REF-DE-group-LibTV-v04.png)，使用Lib Image 2.5 Pro／2K／16:9／1张，六张人物正面图分别锁定身份、原肤色和队服，加05舞台共7张显式引用。增加柔和中性正面主光和填充，舞台暖光只作背景与边缘反射。已核查完整原图，六人脸手自然明亮；[图像生成记录](REF-DE-group-LibTV-v04-generation.json)已保存，花费39积分。

D段[肤色修订Prompt v09](prompts/SEG-D-video-v09.txt)已在新节点v-aBjKkphXQR提交生成，[配置](SEG-D-v09-canvas-preparation.json)及[提交记录](SEG-D-v09-submission.json)已保存。使用新六人队形图替换旧合照，保留04舞台、Renwei多视图、05舞台，共4项；0–4秒风车及短Freeze，4–8秒八拍齐舞不变。Wan 3.0／全能参考／480P／16:9／8秒／1条／静音，智能扩写与AutoLink关闭。本次视频32积分，本轮图加视频共71积分，余额2844→2805→2773；已生成并保存[新版视频](videos/SEG-D-Wan3-480P-v09-skin-revision.mp4)，已检查6秒群舞画面，六人脸手自然明亮；[回看截图](previews/SEG-D-v09-group-skin-review.jpg)已保存，等待用户回看确认。

1. [五段导演蓝图](16-FIVE-SEGMENT-DIRECTOR-BLUEPRINT-v07.md)：逐段叙事、景别、走位、节奏与完整Prompt。
2. [关键构图准备单](17-KEYFRAME-PREPARATION-v07.md)：四类P0构图、可选鞋部首帧、来源和图像Prompt；当前尚未生成新关键帧。
3. [五段生成时间线](generation-timeline-v07.csv)、[段内摄影时间线](edit-timeline-v07.csv)、[结构化分段](segments-v07.json)。
4. [当前舞台编号](13-STAGE-CONTINUITY-LOCK.md)：01→02→03→04→05→完整Logo，06仅备用。

视频规划为LibTV Wan 3.0／全能参考／480P／16:9，关闭音轨，统一后期配乐；图片按需dream-painter／GPT Image 2。12秒与8秒为目标，模式兼容性及报价提交前核对。首尾帧、续写、重绘、Draft升级或导演台能力未在本轮验证，不作为已具备条件。

20–24秒三人共舞、36–40秒六人共舞各保留完整4秒；44秒共同重踏点亮Logo。关键帧按需匹配，力量技参考尚待选定。

以上蓝图为规划基线，当前执行状态和扣费以本页顶部及各段提交记录为准。旧v05/v06剧本、upload-pack、segments.json、通用旧CSV和旧构建脚本均属历史，不要按旧脚本重建覆盖本版；实际生成记录与Demo保留。






2026-11-19 D2群舞v11测试完成：使用唯一六人动势参考图v06（i-8qjdW0b56R），节点v-dqv4Tl5odC，Wan 3.0／全能参考／480P／16:9／4秒／1条／静音，智能扩写与AutoLink关闭。本次16积分，余额2663→2647。[视频](videos/SEG-D2-Wan3-480P-v11-group-only.mp4)、[提示词](prompts/SEG-D2-Wan3-480P-v11-group-only.txt)、[记录](SEG-D2-v11-submission.json)、[近尾帧预览](previews/SEG-D2-v11-review.jpg)已保存。已抽看开场、1秒、2秒、3秒、近尾帧，检查点人数均为六人，能从低位站起同步做脚步、摆臂与右转，肤色自然且未显完整Logo。局限：机位仍有拉远，模型新增圆形舞台边缘、音箱和彩纸；部分脚步像跑步式交叉步，八拍编舞未全部精准执行。待用户回看决定是否采用。v08/v10的Renwei独舞按用户要求保留，本轮未重做独舞，也未提交其他生成。

2026-11-19 D段v12升镜版已提交：按用户确认回到完整8秒（0–4秒Renwei风车及短Freeze；4–8秒六人群舞），使用局部04、Renwei多视图、局部05、六人v04共4项显式引用。群舞4–7秒由略低于胸口的机位升至15–20度轻俯视，7–8秒收稳；v04锁身份、肤色与123站位，不锁静态姿势。Wan3／480P／16:9／8秒／静音／1条，扩写及AutoLink关闭。本次32积分，余额2647→2615。节点v-WH1ZVEGDLA；[提示词](prompts/SEG-D-video-v12-v04-crane.txt)、[记录](SEG-D-v12-submission.json)。现有旧版保留；用户已在画布手动清理v06图及v11等测试节点，不恢复。

D段v12结果：已完成并保存[视频](videos/SEG-D-Wan3-480P-v12-v04-crane.mp4)。抽看约4.45秒、6秒和7.69秒群舞，均出现额外扎发人物，变为7人（后排4人），本版不通过。升镜有体现、肤色自然、未露完整Logo；结尾偏直立整齐，动作力度仍有限；2秒独舞检查帧头部触地，不完全符合提示词。保存[6秒检查截图](previews/SEG-D-v12-group-review.jpg)及[结尾截图](previews/SEG-D-v12-end-review.jpg)。仅生成1条，实际32积分，余额2615；未自动重试。

2026-11-19 用户手动生成并确认D段可用，本轮仅整理画布命名：视频v-qXYcCoJoLR由“SEG-D-Renwei到六人共舞-8s-Wan3-480P-v08-待生成 - 副本”改为“SEG-D-Renwei到六人共舞-8s-Wan3-480P-v13-采用”；其引用的上传六人图i-10GbjCzSzq由“image”改为“REF-DE-六人队形-自然肤色123-v07-采用”。视频引用局部04、Renwei多视图、局部05和这张上传图共4项。采用状态来自用户回看确认，本轮未重新生成，未花积分；画布当前显示余额2551，差额不推定为本轮操作费用。后续D段以用户认可的v13为采用版本。
