"""Build shot prompts, editable manifests and a schematic storyboard. No AI/API calls."""
from pathlib import Path
import csv
import json
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent
FONT = Path('C:/Windows/Fonts/msyh.ttc')

CAST = {
    'Jessica': 'assets/characters/production-pack/jessica/jessica-front-v01.png',
    'Feng': 'assets/characters/production-pack/feng/feng-front-v01.png',
    'Scott': 'assets/characters/production-pack/scott/scott-front-v01.png',
    'Song': 'assets/characters/production-pack/song/song-front-v01.png',
    'Amy': 'assets/characters/production-pack/amy/amy-front-v01.png',
    'Renwei': 'assets/characters/production-pack/wei/wei-front-v01.png',
}
FORMATION = ('相对主镜头采用1＋2＋3浅箭头队形：Feng在最靠镜头的前排中央；'
             'Jessica在第二排画面左侧、Scott在第二排右侧；Song、Amy、Renwei从画面左到右在第三排错位展开。'
             '前排指靠近镜头，不指画面上方；六人脸不互相遮挡。所有站位必须落在既有Logo的可见实面，'
             '避开中心留白与陡坡；在实面范围内调整间距，不为队形新增平台或改变Logo轮廓。')
STAGE = 'assets/stage/copilot-logo-stage-overview-v01.png'
SHOTS = [
    dict(id='S01', start=0, end=4, gen=5, source_in=0.5, cast=['Jessica'], title='白鞋第一拍',
         zone='蓝青色平缓带面，只有局部地面', camera='低位脚部特写；机位朝彩带右侧，完整 Logo 不入画',
         frame='只出现 Jessica 的双脚与少量小腿，白鞋完整，双脚站在蓝青色平缓带面上，脚边短光纹，画面上部留出片头字空间；不要在图中生成文字。',
         motion='0–1秒双脚站稳；1–3秒左右轻点两次，随落脚出现两圈短光纹；3–5秒彩光沿地面向画面右侧流动，镜头微微抬升但不露出整个舞台。',
         cut='直接切到同色地面的 Jessica 全身，光的方向一致。', qc='白鞋款式不变，脚不多、不陷地；不能露出完整 Logo。'),
    dict(id='S02', start=4, end=8, gen=5, source_in=0.5, cast=['Jessica'], title='Jessica 领舞',
         zone='同一蓝青色平缓带面', camera='眼平略低的单人全身，人物约占画面高度70%，脸清楚，头鞋不裁切',
         frame='Jessica 一人面向镜头站稳，双脚自然分开，双手放松，保持定稿发型、红色矩形眼镜与亲切笑容；身后只有彩带局部。',
         motion='0–1秒轻压肩部；1–3秒左右踏步，重心自然；3–4秒将右手舒展地向画面右侧打开；4–5秒准备侧移但不离开镜头。镜头轻微向右横移。',
         cut='在向右开手动作上切到 S03，Jessica 仍是同一个人。', qc='整段脸与眼镜稳定；至少2秒清楚认脸，肢体不遮脸。'),
    dict(id='S03', start=8, end=10, gen=5, source_in=1.5, cast=['Jessica'], title='Jessica 滑出',
         zone='蓝青带面通向蓝紫弯道', camera='全身侧向跟拍，始终向画面右侧运动',
         frame='Jessica 位于画面左三分之一，脚已站稳，身子微向右侧移，前方蓝青彩带向右弯曲；画面右侧有可掠过镜头的近景彩带边缘。',
         motion='0–1.5秒 Jessica 轻压重心准备；1.5–3.5秒向画面右侧舒展侧滑，白鞋贴地短滑，彩光跟随脚下；3.5–5秒她滑出右边缘，镜头追随光进入彩带弯道，近景彩带边缘掠过镜头。不要变脸、不要出现第二人。',
         cut='取1.5–3.5秒作初始建议；实际切点选滑出或彩带掠镜的强拍，S04延续向右。', qc='短滑不是跑步、飞行或跌落；人物没有变成 Feng。'),
    dict(id='S04', start=10, end=12, gen=5, source_in=0.5, cast=['Feng'], title='Feng 滑入',
         zone='相邻蓝紫平缓带面，与 S03 弯道保持材质和方向', camera='单人全身中景，向右轻跟拍后停稳',
         frame='Feng 一人位于画面左侧，双脚已在彩带上，身体朝右准备短滑；前方是宽阔平缓的蓝紫区域。与 S03 同向、相近机位高度。',
         motion='0–0.5秒 Feng 在左侧准备；0.5–1.5秒顺势向画面右侧短滑至中间；1.5–2.5秒踩拍站稳，抬头微笑；2.5–5秒接轻微肩部律动，保持脸清楚。',
         cut='接 S03 的运动方向；落脚强拍进入 S05。短甩镜遮接缝最多数帧，不用长叠化把脸融在一起。', qc='Feng 的高额头与眼镜等定稿特征保持；滑入后确实站稳。'),
    dict(id='S05', start=12, end=16, gen=5, source_in=0.5, cast=['Feng'], title='Feng 回应',
         zone='同一蓝紫平缓区域', camera='单人全身，低幅横移，不绕到背后',
         frame='Feng 面向镜头，双脚站稳，手臂放松，姿态和 S04 落脚后衔接，保持全部定稿特征。',
         motion='0–1秒轻压肩部；1–3秒左右踏步并做一小段手臂波浪；3–4秒向画面右侧开手，将彩光交给 Scott 所在方向；4–5秒收手并保持律动。',
         cut='沿向右的开手与彩光切到 Scott 独立亮相。', qc='不得与 Scott 混脸；完整正面展示，脸不被手臂挡住。'),
    dict(id='S06', start=16, end=20, gen=5, source_in=0.5, cast=['Scott'], title='Scott 第三位亮相',
         zone='与蓝紫带面相邻的金橙平缓区', camera='单人全身中景，微向右横移后稳定，脸清楚',
         frame='画面只有 Scott，面向镜头站稳，保持定稿头发、矩形眼镜与队服；脚下彩光由左进入，背景只有局部彩带。Jessica 与 Feng 均不入画。',
         motion='0–1秒 Scott 轻踏一步接住彩光；1–3秒左右踏步并做短手臂波浪；3–4秒向画面左侧开手回应已经出场的两位；4–5秒收手继续律动。至少2秒清楚认脸，不安排长滑行。',
         cut='沿回应手势切核心三人同框；Scott 此前不得作为背景角色提前露脸。', qc='恰好一人；Scott 是第三位首次露脸者，不与 Feng 混脸。'),
    dict(id='S07', start=20, end=24, gen=5, source_in=0.5, cast=['Jessica','Feng','Scott'], title='核心三人同框',
         zone='同一Logo的邻近宽缓实面，隐藏整体轮廓', camera='三人中全景，Feng居中靠前，Jessica左后、Scott右后，三张脸清楚',
         frame='画面只有 Jessica、Feng、Scott。Feng 在前排中央；Jessica 在第二排画面左侧，Scott 在第二排右侧。三人脚踩既有彩带实面、彼此不遮脸，后方不出现其他角色，不露完整Logo。',
         motion='0–1秒三人轻踏同一拍；1–2秒 Jessica 与 Scott 向中央开手呼应；2–3秒 Feng 接住动作并向两侧舒展开手；3–4秒三人一起踏步，彩光向画面右侧传出；4–5秒保持队形继续律动。',
         cut='先立住三人阵容，再沿彩光切 Song 与 Amy；Feng 保持视觉中心。', qc='严格三人，Feng前排中央；Jessica和Scott左右不交换；其他成员尚未露脸。'),
    dict(id='S08', start=24, end=28, gen=5, source_in=0.5, cast=['Song','Amy'], title='Song 与 Amy 接力',
         zone='彩带左前方绿黄平缓舞蹈区', camera='双人中全景，Song 左、Amy 右，略错位但不遮脸',
         frame='画面只有 Song 与 Amy，Song 在左、Amy 在右；两人面向镜头，双脚站稳，保持各自定稿发型与脸型。绿黄彩带局部从左通向右。',
         motion='0–1秒两人站稳接节奏；1–3秒左右踏步，手臂波浪从左传到右；3–4秒右侧 Amy 轻踏一步，彩光沿带面向右流出；4–5秒回正。',
         cut='在右侧踏步与光纹上接 S09，不必每次滑行。', qc='Song 短发与 Amy 长发不混淆；两张脸和两双鞋均可见。'),
    dict(id='S09', start=28, end=32, gen=5, source_in=0.5, cast=['Renwei'], title='Renwei 接上最后一棒',
         zone='右侧紫红平缓彩带，紧邻第三排右侧站位', camera='单人全身中景，保持深色墨镜与脸型清楚',
         frame='只有 Renwei，使用已确认对应的 Wei 素材，保持定稿深色墨镜、发型与队服；面向镜头站稳，背景只见局部紫红彩带。',
         motion='0–1秒轻踏接拍；1–3秒肩部轻摆并开手；3–4秒向画面右侧短距离侧移一步，准备进入紧邻的第三排右侧位置；4–5秒稳住重心，墨镜保持不透明。',
         cut='沿短侧移动作接 S10，其他五人已在汇合位置；正式显示名使用 Renwei。', qc='恰好一位 Renwei；不凭空露眼、不新增道具、不长距离奔跑。'),
    dict(id='S10', start=32, end=36, gen=5, source_in=0.5, cast=list(CAST), title='六人同一拍',
         zone='固定 Logo 表面的六个平缓实面站位，中心留白无人', camera='低位斜向六人群像，1＋2＋3层次清楚，隐藏完整舞台外轮廓',
         frame='严格六位角色，按上传的六人站位主图保持空间关系。'+FORMATION+'Renwei 位于第三排右侧，已在站立实面，其余五人已就位。',
         motion='0–1秒 Renwei 在第三排右侧紧邻位置小幅侧移站稳，其余五人轻律动；1–2秒六人共同踏稳；2–4秒一起左右踏步并开手；4–5秒继续同一节奏。每人只一具身体，1＋2＋3站位不交换。',
         cut='共同落拍后保持站位，接 S11 升镜。', qc='全程恰好六人；Feng前排中央，Jessica左中排、Scott右中排，后三人不遮脸；后两镜站位一致。'),
    dict(id='S11', start=36, end=40, gen=5, source_in=0.5, cast=list(CAST), title='升镜揭示 Logo',
         zone='与 S10 完全相同的舞台和六人站位', camera='由低位斜向平稳升高后退，到与定稿全景相符的高位斜俯视',
         frame='以 S10 实际选用末帧为首帧，不另造一座舞台；六人姿态和空间关系不改变。另备同一布局的高位全景作为尾帧参考。',
         motion='0–0.5秒保持低位；0.5–4.5秒镜头连续平稳升高并后退，六人只做轻微原地踏步，舞台不变形，逐渐揭示完整 Copilot Logo；4.5–5秒完整轮廓保持稳定。中心留白、折叠交叠和人物相对站位不变。',
         cut='末尾全貌构图接 S12 的完整 Logo；没有新增或瞬间变形的舞台。', qc='主反转必须靠运镜出现；Logo不变成∞、螺旋或新图标；六人身份与数量不变。'),
    dict(id='S12', start=40, end=48, gen=10, source_in=1, cast=list(CAST), title='全员高潮与定格',
         zone='固定完整 Logo，高位视角', camera='与 S11 末帧一致的高位斜俯视；完整 Logo 始终在画面内，不再明显拉远',
         frame='以 S11 实际末帧或同一六人全景主图为首帧，完整 Logo 占画面宽度约75%，留出边缘，六人站位保持一致，中心留白和关键轮廓无遮挡。',
         motion='0–1秒保持节奏；1–3秒六人左右踏步并轻压肩部；3–5秒一同开手并收回；5–7秒简短手臂波浪；7–8秒小幅侧移回正；8–9秒共同踏步开手定格；9–10秒保持姿势，边缘灯完成一次回环。完整 Logo 全程可辨认，镜头稳定，严格六人。',
         cut='用8秒核心舞段；接48秒片尾卡，音乐继续。', qc='整段完整轮廓稳定；全员有舞蹈动作，不能用纯定帧冒充；不多出人体或失去角色。'),
]

IMAGE_COMMON = ('用途：本片视频首帧，不是拼贴分镜。生成一张16:9横屏、至少1920×1080的统一3D卡通电影画面。'
 '只参考所上传人物图中的人物身份、头身比例和队服，不继承其白底；舞台图只约束材质、配色和几何。'
 '保持已定稿的脸、发型、眼镜；深蓝短夹克、白色圆领衫、双袖口和腰边窄渐变饰边、纯深蓝裤、白鞋。'
 '深蓝演播空间、柔和面部主光、克制的青紫轮廓光，地面为巨大Copilot折叠彩带的一部分。'
 '脚与带面真实接触，跳舞区平缓。无文字、水印、额外人物或道具，不改变Logo整体拓扑，不让人站在中心留白。')
VIDEO_COMMON = ('以上传的单张首帧为起始画面，保持人物身份、脸型、发型、眼镜、头身比例、服装、舞台材质和光线一致。'
 '统一3D卡通电影质感，轻快自信的原创电子Funk舞蹈气质。单镜头，不自动切镜；不说话、不唱歌，不在视频内生成字幕。'
 '人物不变脸、不互换、不复制，肢体数量正常，鞋贴地，不穿透。此镜的音乐后期统一铺设，不依赖模型自带配乐。')


def build():
    (BASE/'prompts').mkdir(exist_ok=True)
    for sub in ['frames','raw-video','selected','audio','exports','actual-prompts']:
        (BASE/sub).mkdir(exist_ok=True)
    for s in SHOTS:
        names='、'.join(s['cast'])
        refs='；'.join(f'{n}＝人物参考图{idx+1}' for idx,n in enumerate(s['cast']))
        s['first_frame_prompt']=IMAGE_COMMON+'\n素材对应：'+refs+'。\n景别与机位：'+s['camera']+'。\n区域：'+s['zone']+'。\n画面：'+s['frame']
        s['video_prompt']=VIDEO_COMMON+f"\n此镜人物：{names}，共{len(s['cast'])}位。\n镜头：{s['camera']}。\n本次源片段{s['gen']}秒，动作："+s['motion']
        if s['id']=='S11':
            s['first_frame_prompt']='此镜不重新生成首帧。使用 S10 选用片段的实际末帧；另制作同一舞台、同一六人站位的高位全景尾帧。'+s['first_frame_prompt']
        for kind,key in [('image','first_frame_prompt'),('video','video_prompt')]:
            (BASE/'prompts'/f"{s['id']}-{kind}.txt").write_text(s[key]+'\n',encoding='utf-8')
    (BASE/'shots.json').write_text(json.dumps(SHOTS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (BASE/'edit-timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
        fields=['shot','timeline_in','timeline_out','used_seconds','planned_source_seconds','suggested_source_in','suggested_source_out','speed','transition','file']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for s in SHOTS:
            used=s['end']-s['start']
            w.writerow(dict(shot=s['id'],timeline_in=s['start'],timeline_out=s['end'],used_seconds=used,planned_source_seconds=s['gen'],suggested_source_in=s['source_in'],suggested_source_out=s['source_in']+used,speed=1,transition='hard cut; choose exact beat manually',file=f"selected/{s['id']}.mp4"))
        w.writerow(dict(shot='CREDITS',timeline_in=48,timeline_out=52,used_seconds=4,file='credits-info.png'))
        w.writerow(dict(shot='PROMPTS',timeline_in=52,timeline_out=60,used_seconds=8,file='actual prompt cards; see credits tool'))
    log=BASE/'run-log.csv'
    if not log.exists():
        with log.open('w',encoding='utf-8-sig',newline='') as f:
            csv.writer(f).writerow(['asset_id','used_in_final','model','mode','resolution','duration_seconds','inputs','actual_prompt_file','output_file','credits_spoken_name','notes'])
    lines=['# 逐镜分镜 · 执行版','', '六人名单、前三位出场顺序Jessica→Feng→Scott、1＋2＋3队形已确认；具体动作与其余三人分镜为制作建议。12镜合计48秒，片尾12秒，总长60秒。所有源片先生成较长，再选取表中需要的长度。', '',
           '[构图示意总览](storyboard-contact-sheet.png)只表示人物数量、运动方向和机位，不是正式首帧，不能上传它代替人物资产。', '',
           '## 固定资产与站位', '',
           '单人图均为现有生成素材，使用前对照已认可的六人总览检查脸和队服；三视图只在侧背面需要时补充。用户已于2026-11-18确认Wei＝Renwei；显示名使用Renwei，源素材文件名保留Wei。', '',
           '| 人物 | 相对项目根目录的参考文件 | 状态 |','| --- | --- | --- |']
    for n,p in CAST.items():
        lines.append(f"| {n} | {('`'+p+'`') if p else '待补照片、制成并确认统一卡通角色后存入 `assets/characters/production-pack/'+n.lower()+'/'+n.lower()+'-front-v01.png`'} | {'缺素材，不用随机脸补位' if not p else ('已确认Wei＝Renwei，核对定稿后使用' if n=='Renwei' else '已有，核对定稿后使用')} |")
    lines += ['', '群舞采用相对主镜头的1＋2＋3浅箭头队形：Feng在最靠镜头的前排中央；Jessica在第二排画面左侧，Scott在第二排右侧；Song、Amy、Renwei从画面左到右在第三排错位展开。所有人必须站在既有Logo的可见实面，避开中心留白与陡坡；在实面范围内调整间距，不为队形新增平台或改变外轮廓。六人全景确认后才能从它衍生S10较低机位；S07先展示同一布局中的核心三人，后排三人尚不入画。', '',
              '## 逐镜镜头卡', '']
    for s in SHOTS:
        lines += [f"### {s['id']}｜{s['start']:02d}–{s['end']:02d}秒｜{s['title']}", '',
                  f"- **成片／源素材**：{s['end']-s['start']}秒／计划生成{s['gen']}秒。建议先取源片{s['source_in']}–{s['source_in']+s['end']-s['start']}秒；实际按脸、动作和落拍微调起点，保持成片时长。", 
                  f"- **人物**：{'、'.join(s['cast'])}。**区域**：{s['zone']}。", f"- **机位**：{s['camera']}。",f"- **首帧**：{s['frame']}",
                  f"- **动作（源片局部时间）**：{s['motion']}",f"- **转场**：{s['cut']}",f"- **验收**：{s['qc']}",
                  f"- **复制用文本**：[首帧提示词](prompts/{s['id']}-image.txt)／[视频提示词](prompts/{s['id']}-video.txt)。正式视频节点使用已选首帧 `frames/{s['id']}.png`，不要把构图示意当参考。", '']
    lines += ['## 镜头接力的连续性核对','',
              'S02→S03 的 Jessica 服装、舞台颜色和运动方向一致；S03→S04 始终向画面右侧，利用弯道遮挡或强拍硬切；S04→S05 的 Feng 落脚姿势衔接；S05→S06 沿彩光引出第三位Scott；S06→S07回应核心三人，S07→S09用开手、光纹和同一乐句递进；S10→S12 用同一布局和实际末帧继续，不生成三座不同舞台。', '',
              'S03／S04 可各生成5秒后各取2秒，组合成4秒交接小样；这4秒已经包含在8–12秒时间线，不额外增加成片长度。', '',
              '## 片尾镜头','', '48–52秒为实际制作信息卡；52–60秒为全部实际原始Prompt的分页卡，按页数均分8秒，支持逐帧暂停阅读。详情见操作指南。']
    (BASE/'02-STORYBOARD.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    draw_board()
    print('Built 12 shot cards, 24 prompt files, timeline, manifest and schematic board.')


def draw_board():
    font=lambda n:ImageFont.truetype(str(FONT),n)
    W,H=1800,1680
    im=Image.new('RGB',(W,H),'#091326');d=ImageDraw.Draw(im)
    d.text((34,20),'FOCUS KICKOFF · 12 镜构图示意',font=font(32),fill='white')
    d.text((34,65),'非生成首帧｜圆点表示人物｜箭头表示运动或光的接力｜00:48 后进入片尾',font=font(22),fill='#b4c6df')
    colors=['#48c4dc','#42abc9','#469ac8','#587bc9','#6868d0','#7272d1','#8bbd69','#db9c66','#b56ecd','#727cb7','#7179ad','#7179ad']
    for i,s in enumerate(SHOTS):
        x=24+(i%3)*592;y=112+(i//3)*385
        d.rounded_rectangle((x,y,x+570,y+365),radius=15,fill='#14233c',outline='#34465f',width=2)
        d.text((x+15,y+12),f"{s['id']}  {s['start']:02d}–{s['end']:02d}s  {s['title']}",font=font(23),fill='white')
        # Curving ribbon is only a local schematic, never a purported logo reconstruction.
        d.line([(x+20,y+225),(x+130,y+190),(x+310,y+235),(x+540,y+185)],fill=colors[i],width=62)
        names=s['cast']
        if i==0:
            for dx in (250,300):d.rounded_rectangle((x+dx,y+150,x+dx+35,y+220),radius=8,fill='white')
        else:
            for j,n in enumerate(names):
                if len(names)<=2:cx=x+210+j*160;cy=y+170
                else:
                    positions={'Feng':(285,210),'Jessica':(180,150),'Scott':(390,150),'Song':(100,90),'Amy':(285,90),'Renwei':(470,90)}
                    dx,dy=positions[n];cx=x+dx;cy=y+dy
                d.ellipse((cx-14,cy-42,cx+14,cy-14),fill='#f1d7bc')
                d.line((cx,cy-12,cx,cy+22),fill='#e8f0ff',width=13)
                d.line((cx-16,cy+39,cx,cy+19,cx+16,cy+39),fill='#e8f0ff',width=6)
                label=n
                d.text((cx-47,cy+42),label,font=font(14),fill='#f4f4f4')
        d.line((x+50,y+290,x+510,y+290),fill='#7ee1ff',width=3)
        d.polygon([(x+510,y+290),(x+497,y+282),(x+497,y+298)],fill='#7ee1ff')
        caption='升高后退，揭示整体' if s['id']=='S11' else ('保持全貌，16拍群舞' if s['id']=='S12' else '运动 / 节奏向右传递')
        d.text((x+20,y+315),caption,font=font(19),fill='#b4c6df')
    im.save(BASE/'storyboard-contact-sheet.png')


if __name__=='__main__':
    build()
