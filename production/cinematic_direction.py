"""v05 direction overrides and grouped generation plan. No API calls.

Imported by build_pack.py so rebuilding cannot restore the old relay direction.
Shot timing remains editorial; five generation jobs may contain multiple cuts.
"""
from prompt_review import refine_segments, render_segment_prompt, write_asset_manifest

SHOT_UPDATES = {
 'S01': dict(title='第一拍，空间苏醒', camera='低位白鞋与带面材质特写，浅景深；末尾轻抬镜，完整Logo不入画',
  frame='Jessica白鞋与少量小腿落在蓝青色平缓带面，鞋边只有一小点青光；大部分空间沉在深蓝暗部。保留材质细节与后期片头安全区，无文字，不显示整体轮廓。',
  motion='0–1秒先静后动，白鞋轻抬准备；1–2秒一记明确落脚，接触点亮起青色光纹；2–4秒光沿既有带面向右传播，仅局部轮廓被唤醒，镜头轻抬；4–5秒维持光的方向，不揭示全貌。',
  cut='以光从左向右的运动衔接Jessica亮相；首个视觉重点是落脚触发空间响应。', qc='光从鞋底接触点产生，不凭空爆炸；全片最初只有Jessica的鞋，不能认出完整Logo。'),
 'S02': dict(title='Jessica 发起光的接力', camera='先用膝上中景认脸，再短距离拉至全身；运动克制，头鞋在全身阶段完整',
  frame='沿用认可的HANDOFF-jessica-gpt-image-2-v01.png作为角色与局部舞台参考；它是近全身静态构图，不是已经完成的舞步。按镜头需要派生认脸中景；保留深蓝负空间与柔和轮廓光。',
  motion='0–1秒Jessica抬眼微笑接住第一拍，脸清楚；1–3秒两次小幅左右移重心、肩部轻压，脚边光纹随落拍回应；3–4秒右手轻轻送向右侧，光纹随手势延伸；4–5秒保持重心准备短侧步。',
  cut='手势引导下一镜的光，不靠人物长距离移动；至少留2秒稳定认脸。', qc='Jessica身份和队服以定稿图为准，不凭文字重新设计眼镜；人物不跑步、不挡脸。'),
 'S03': dict(source_in=2, title='一步送光，遮挡交接', camera='同侧轴线短横移，全身可辨；仅在末尾由近景彩带扫过镜头遮挡',
  frame='与Jessica新首帧保持相机高度、人物尺度和脚底位置；右侧预留短侧步空间和近景彩带边缘，不能新建传送门或坡道。',
  motion='0–1秒Jessica面向镜头略偏右、膝盖轻弯；1–3秒向右做一次很短的贴地侧步，脚下光比人物先向右传出；3–4秒相机经过固定近景彩带边缘，前景短暂遮满画面完成遮挡，舞台自身不移动；4–5秒保持遮挡的蓝紫色调。不要追逐人物，不跑跳，不变成Feng。',
  cut='成片2秒取短侧步和完整遮挡；在遮挡最满时切Feng，同一光纹继续向右。段落B允许这一次明确切镜。', qc='交接由光与遮挡完成，不强求Jessica完全滑出画面；无人物融脸、长叠化或长距离跑动。'),
 'S04': dict(title='Feng 踩拍接光', camera='与Jessica匹配的全身机位；轻推至可认脸的中全景，结束时稳住',
  frame='沿用HANDOFF-feng-gpt-image-2-v01.png为角色和构图参考，舞台、脚底位置、人物大小匹配Jessica；这是遮挡后亮相状态，不能直接把Jessica首帧变形为Feng。',
  motion='0–1秒蓝紫前景遮挡移开，只出现Feng，光由画面左侧进入；1–2秒Feng做一次向右小幅移重心，白鞋踩稳接住光；2–4秒抬头微笑并轻压肩部；4–5秒保留脚边微光和稳定认脸。',
  cut='B段末尾的落脚与C段第一拍衔接，保持同一Feng的脸、镜头轴线和光照。', qc='只一位Feng，站稳认脸；禁止滑翔、跑步、飞跃或提前出现Scott。'),
 'S05': dict(title='Feng 推动节奏', camera='单人中全景，短促轻推后稳定；避免与Jessica重复同样的入场镜头',
  motion='0–1秒承接上一段落脚；1–3秒Feng肩部律动与短手臂波浪，光纹随两次踏步增强但不照亮全舞台；3–4秒向右开手，把光送出画外；4–5秒保持律动与清楚面部。',
  cut='在向右传出的光纹上做动作匹配切镜到Scott；使用光的方向建立因果。', qc='脸、服装、光的方向连续；亮度仍低于最终高潮，不提前泄露全景。'),
 'S06': dict(title='Scott 接光回应', camera='先给清楚认脸的中景，再小幅拉开到带有脚步的中全景，动作匹配切入',
  motion='0–1秒来自左侧的光到达Scott脚边，他轻踏回应；1–3秒左右小幅踏步和短手臂波浪，至少2秒清楚认脸；3–4秒向画面左侧开手回应已出场伙伴；4–5秒彩光在地面短暂分出呼应支线，不改变舞台几何。',
  cut='从Scott回应手势切到核心三人；镜头第一次扩大到三人，形成段落小高潮。', qc='Scott第三位首次露脸；Jessica、Feng此前不得在Scott单人画面里串脸。'),
 'S07': dict(title='三人共振，再递一棒', camera='稳定三人中全景，Feng前排中央，Jessica左后、Scott右后；短暂停稳形成呼吸',
  motion='0–1秒三人同拍落脚；1–2秒Jessica与Scott向中央开手；2–3秒Feng接住动作，脚下三股细光汇聚；3–4秒三人一起踏步，汇聚的光沿既有带面向右送出；4–5秒保持队形继续轻律动。背景其他三人不出现。',
  cut='在三人同拍后留短暂稳定画面，再沿光切Song、Amy；这是第一次汇合，不是最终全景。', qc='严格三人，不提前露完整Logo；光汇聚在带面，不盖住脸、不新增平台。'),
 'S08': dict(title='Song、Amy 接续光波', camera='双人中全景，Song左、Amy右；轻横移随手臂波浪，不重复入场特写',
  motion='0–1秒来自左侧的光先到Song脚边；1–3秒两人左右踏步，手臂波浪从Song传到Amy，地面光同步延伸；3–4秒Amy轻踏将光送往右侧；4–5秒回正，保持两张脸清楚。',
  cut='Amy落脚的光点匹配切到Renwei接光的脚边；光色逐渐增加暖色，不切换美术体系。', qc='双人身份不交换，光不过曝，人物不交叉遮脸。'),
 'S09': dict(title='Renwei 接上最后一束光', camera='Renwei中景认脸，短拉至中全景展示邻近站位；不做长距离跟跑',
  motion='0–1秒光从左侧到达，Renwei轻踏接拍；1–3秒肩部轻摆并开手，墨镜保持不透明；3–4秒向紧邻第三排右侧的位置短移一步，光随脚步延伸；4–5秒站稳，不跨越空洞和陡坡。',
  cut='沿最后一步切六人群像，其他五人已在画外到位；不给瞬移、穿越或奔跑任务。', qc='Wei素材对应Renwei；一位人物，无露眼、额外道具或身份更换。'),
 'S10': dict(title='六人蓄力，同一拍', camera='低位斜向六人群像，前景边缘、中景人物、远景暗带形成纵深；短推后稳住',
  motion='0–1秒Renwei在第三排右侧紧邻位置小步站稳，其余五人轻律动；1–2秒六人共同落脚，脚下六处光点产生回应；2–4秒同拍小幅踏步、开手，六股光只沿局部带面汇集，亮度蓄积；4–5秒保持队形，不提前露出整体Logo。',
  cut='落拍后音乐减薄，六人位置锁定，接一次连续升高后退；让揭示前出现短暂呼吸。', qc='严格六人和1＋2＋3队形；不因灯光增强提前展示全轮廓，不让人物被光效遮住。'),
 'S11': dict(title='镜头拉远，揭示共同舞台', camera='唯一一次完整空间揭示：平稳升高并后退，到同一母版高位斜俯视；不环绕、不甩镜',
  motion='0–0.5秒保持低位群像，六人原地轻律动；0.5–4.5秒镜头连续升高后退，原本隐藏在画外和暗部的折叠彩带、交叠与中心留白逐渐进入视野，环境微光只增加已有表面的可读性，边缘灯保持低亮；4.5–5秒完整Logo稳定，贯通点亮留到下一镜共同落脚。六人的相对位置不变，舞台不生长、不变形成Logo。',
  cut='最终全貌与S12同构图衔接；40秒完整轮廓已经可辨，随后强拍共同点亮。', qc='揭示靠空间与视野变化，不能用白闪、变形或另一个舞台替换；若改二维拉远须记录真实方法。'),
 'S12': dict(source_in=0, title='共同点亮 Copilot', camera='承接揭示末帧的高位斜俯视，完整Logo持续可见，稳定保持，不再无限拉远',
  motion='0–1秒六人同拍落脚，先前传递的光沿既有Logo边缘贯通一次，亮出完整轮廓；1–3秒六人左右踏步、轻压肩部；3–5秒同拍开手收回；5–6.5秒短手臂波浪；6.5–7秒小侧步回正；7–8秒共同落脚开手，最后约0.5秒定格，边缘光完成一圈首尾呼应；8–10秒保持末态，供剪辑余量。完整Logo始终可辨，人物面部不过曝，严格六人。',
  cut='成片8秒包含真实群舞和末尾短定格；48秒接信息卡，音乐延续至片尾。', qc='全片最亮最完整的视觉高潮只在此处；无激光遮脸或漫天粒子，不能用静图代替群舞。'),
}

SEGMENTS = [
 dict(id='A', start=0, end=4, shots=['S01'], cast=['Jessica'],
      title='第一拍，空间苏醒', refs=[('SHOES_JESSICA','Jessica鞋部与队服下装参考，来自认可角色图'),('STAGE_LOCAL','认可的局部空舞台，只约束材质与空间')],
      beats=[('0–1秒','白鞋与细腻带面特写，深蓝暗场中先静后动。'),('1–2秒','Jessica白鞋轻踏，接触点产生第一圈青色光纹。'),('2–4秒','光沿既有带面向右传播，轻抬镜，仍看不出完整Logo；不露脸。')]),
 dict(id='B', start=4, end=12, shots=['S02','S03','S04'], cast=['Jessica','Feng'],
      title='Jessica → Feng，光的第一棒', refs=[('JESSICA','Jessica原单人正面图，仅身份与队服'),('FENG','Feng原单人正面图，仅身份与队服'),('STAGE_LOCAL','HANDOFF-stage-gpt-image-2-v01.png，局部舞台'),('JESSICA_FRAME','HANDOFF-jessica-gpt-image-2-v01.png，Jessica起始构图'),('FENG_FRAME','HANDOFF-feng-gpt-image-2-v01.png，遮挡后Feng构图')],
      beats=[('0–2秒','只有Jessica。膝上中景清楚认脸，短拉至全身，轻压肩部和小幅踏步；脚边光纹随落拍回应。'),('2–4秒','Jessica面向镜头略偏右，右手轻送，做一次短距离贴地侧步；光先于人物向右传出。保持头鞋完整，不跑步。'),('4–6秒','Jessica完成短侧步，近景彩带边缘扫满画面，在约5.5秒遮挡最满处明确切镜；不要求她长距离滑出，不得把她变形成Feng。'),('6–8秒','遮挡移开后只见Feng，匹配机位、人物大小与脚底高度；从左进入的光抵达鞋边，他向右小幅移重心并踩拍站稳，抬头微笑，脸保持清楚。')]),
 dict(id='C', start=12, end=24, shots=['S05','S06','S07'], cast=['Jessica','Feng','Scott'],
      title='回应，核心三人共振', refs=[('JESSICA','Jessica角色身份'),('FENG','Feng角色身份'),('SCOTT','Scott角色身份'),('CORE3_MASTER','Feng前排中央、Jessica左后、Scott右后的局部三人主图'),('B_LAST','已采用B段实际末帧，只约束开头Feng与机位')],
      beats=[('0–4秒','只有Feng，承接B段末态，小幅肩部律动和手臂波浪；末尾向右开手，光沿地面传出。'),('4–8秒','在光纹上匹配切镜，只见Scott第三位首次露脸；轻踏接光，至少2秒清楚认脸，短舞后向左开手回应。'),('8–12秒','明确切到核心三人中全景，Feng前排中央，Jessica左后、Scott右后；三人同拍踏步，向中央开手再传出汇聚光；镜头短暂停稳，其他成员尚不出现。')]),
 dict(id='D', start=24, end=36, shots=['S08','S09','S10'], cast=['Jessica','Feng','Scott','Song','Amy','Renwei'],
      title='伙伴接续，六人同一拍', refs=[('SONG','Song角色身份'),('AMY','Amy角色身份'),('RENWEI','Renwei身份，使用wei-front-v01.png'),('DUO_MASTER','Song左、Amy右的局部双人主图'),('GROUP_LOCAL','固定六人主图派生的低位局部；前三人仅在8秒后出现'),('STAGE_LOCAL','同一Logo的局部材质机位参考')],
      beats=[('0–4秒','只有Song和Amy，Song左Amy右；光与手臂波浪从Song传向Amy，Amy末尾轻踏将光送出。'),('4–8秒','在光点上明确切到Renwei单人中景；他轻踏接光、开手，墨镜保持不透明，末尾向紧邻站位小移一步。'),('8–12秒','切六人局部群像，其他五人已在位置；严格1＋2＋3，Feng前排中央，Jessica和Scott第二排，Song/Amy/Renwei第三排从左到右。六人共同落脚，六处微光沿带面汇聚蓄力；完整Logo仍不入画。')]),
 dict(id='E', start=36, end=48, shots=['S11','S12'], cast=['Jessica','Feng','Scott','Song','Amy','Renwei'],
      title='共同舞台，完整点亮', refs=[('D_LAST','已采用D段实际末帧，锁定六人身份与站位'),('GROUP_MASTER','同一舞台同一站位的高位全景主图，约束完整Logo几何；是第4秒到达的构图，不是整段视频的尾帧'),('CAST_MASTER','同一六人角色校验图，仅必要时辅助身份')],
      beats=[('0–4秒','从D段末态连续升高后退，六人保持位置轻律动；暗部和画外的既有彩带进入视野，逐渐揭示完整Copilot。不可随机切景或把彩带变形成Logo；第4秒全貌稳定。'),('4–6秒','高潮强拍，六人同拍踏步，光沿已有边缘贯通，完整Logo被共同点亮；镜头稳定，左右踏步和肩压。'),('6–10秒','完整Logo持续可辨，六人统一开手收回、短手臂波浪和小幅踏步，不交换站位，不再远离人物。'),('10–12秒','六人共同落脚开手，边缘光完成一次回环呼应第一拍，最后约0.5秒定格；进入片尾。')]),
]

refine_segments(SEGMENTS)

def build_segments(base, shots):
    import csv, json
    lines=['# 分段生成计划 v05 · 光的接力', '',
           '12镜是剪辑与叙事单位，主路线为5段视频任务。所有分秒为目标，模型输出需验收，不能假定Prompt能保证精确执行。', '',
           '| 段落 | 成片位置 | 目标时长 | 镜号 | 内容 |', '| --- | --- | --- | --- | --- |']
    for seg in SEGMENTS:
        duration=seg['end']-seg['start']
        name=f"SEG-{seg['id']}-video-v05.txt"
        prompt=render_segment_prompt(seg)
        (base/'prompts'/name).write_text(prompt,encoding='utf-8')
        seg['prompt_file']='prompts/'+name
        lines.append(f"| {seg['id']} | {seg['start']}–{seg['end']}秒 | {duration}秒 | {' / '.join(seg['shots'])} | [{seg['title']}]({seg['prompt_file']}) |")
    lines += ['', '## 素材复核与提示词修订（2026-11-18）', '',
      '先读[素材与Prompt复核](06-ASSET-PROMPT-AUDIT.md)及[素材映射清单](asset-readiness.json)。当前制作参考以preparation-manifest.json的实际选用记录为准；C/E正式连续帧必须在B/D视频选定后提取，预演使用明确标记的图像参考版本。不能以设计图冒充实际视频末态。', '',
      'SEG提示词只写模型要生成的画面与声音，计费、水印、下载、原声静音和节拍精剪留在操作指南。时间戳使用整数秒，顺序与连续性优先；第40秒强拍在后期对齐。B默认只传两张在场人物图与空舞台共3张，避免同一人多份身份输入；发生身份漂移时再加单人图并显式绑定为同一人。', '',
      'D和E默认各8张图，六张单人单视图＋两张构图/连续帧。三视图拼板不进入六人任务；局部与全景里的六人需逐一对应为相同身份。E连续升镜仍为高风险提案；若需要严格首尾锁定，可直接采用4秒揭示＋8秒群舞两次生成。5段是组织方式，不是必须恰好5次付费。', '',
      '## 素材引用与平台模式', '',
      '视频主力为LibTV Seedance 2.5全能参考；Flash仅用于明确需要的预演或对照，不把上次Mini效果当成2.5效果。用户已确认会员开通，当前报价、可选时长、分辨率和下载权限仍按实际面板核对。本次只更新计划，不调用收费生成。', '',
      '【JESSICA】等为本地模板别名，不是可直接粘贴生效的@引用。先导入素材，再从LibTV的@菜单或素材旁@按钮插入平台识别的标签，逐一替换别名。核对缩略图与角色关系，再保存实际展开的完整Prompt和参数至actual-prompts及run-log.csv。', '',
      '只给本段需要的角色参考；合成多人图也要在Prompt中限定首次出现时间。D段六人局部参考不能让核心三人在前8秒抢先入画。素材数量超过面板上限时优先使用已检查的双人/三人/六人主图，不删角色、不上传未经核对的拼图。', '',
      '全能参考中的构图参考不等于已锁定首帧或尾帧。只有面板确实提供并启用相应模式才记录为锁定。E段高位全景是片段第4秒的目标，不可误放成12秒整段的尾帧、把揭示拖到最后；E不稳定时拆为E1/S11的4秒揭示与E2/S12的8秒群舞。', '',
      '## 生成顺序与降级', '',
      '先B段8秒 → 固定六人/Logo主图并验证E → 确定音乐节拍 → 补C、D和A → 合成终剪。每次查看实际积分报价，记录结果，不在某段失败时重跑全部内容。', '',
      'C可拆为4秒Feng、4秒Scott、4秒三人；D可拆为4秒双人、4秒Renwei、4秒六人；B可在完整遮挡处分成Jessica与Feng两个任务。逐镜Sxx提示词保留为拆段补救，不是12次任务的强制要求。', '',
      '若界面不支持目标时长，只选最近可用更长时长，并把多余时间写成保持末态，保存实际修改Prompt。不能直接把所有长源片拼满时间线。', '',
      '## 资产与空间', '',
      '图片按需用dream-painter / GPT Image 2多图编辑，沿用已认可角色，不批量重做多视图。现有HANDOFF三图用于B段；它们只证明局部构图可用，不证明和最终全景存在可连续升镜的三维关系。先固定高位STAGE_MASTER和GROUP_MASTER，再从同一母版派生群舞局部。', '',
      '若真实升镜造成Logo变形，可把D末镜和E起镜都改为同一高清全景母版的局部裁切，再在E前4秒二维拉远；记录二维方法，不能只换背景或把纯静帧冒充后8秒舞蹈。', '',
      '片头与片尾文字后期添加。48–52秒制作信息，52–60秒实际Prompt全文分页；暂停可读的交付解释仍需活动方认可。']
    (base/'05-GENERATION-PLAN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (base/'segments.json').write_text(json.dumps(SEGMENTS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write_asset_manifest(base, SEGMENTS)
    with (base/'generation-timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['segment','timeline_in','timeline_out','used_seconds','shots','prompt_file','selected_file'])
        for seg in SEGMENTS:
            w.writerow([seg['id'],seg['start'],seg['end'],seg['end']-seg['start'],';'.join(seg['shots']),seg['prompt_file'],f"selected/SEG-{seg['id']}.mp4"])
