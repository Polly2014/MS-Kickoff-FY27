"""2026-11-18 evidence-based prompt review. Pure local file generation."""
from pathlib import Path
import json

FRONT = 'assets/characters/production-pack/{0}/{0}-front-v01.png'
ASSETS = {
    **{name.upper(): dict(path='../'+FRONT.format(folder), kind='existing_character', note='单人正面身份与队服；白底不进入视频')
       for name, folder in [('Jessica','jessica'),('Feng','feng'),('Scott','scott'),('Song','song'),('Amy','amy'),('Renwei','wei')]},
    'STAGE_LOCAL': dict(path='frames/HANDOFF-stage-gpt-image-2-v01.png', kind='existing_trial', note='局部平缓带面，不能证明全景三维几何'),
    'JESSICA_FRAME': dict(path='frames/HANDOFF-jessica-gpt-image-2-v01.png', kind='existing_trial', note='Jessica身份、队服与局部构图'),
    'FENG_FRAME': dict(path='frames/HANDOFF-feng-gpt-image-2-v01.png', kind='existing_trial', note='Feng身份、队服与局部构图'),
    'STAGE_MASTER': dict(path='frames/STAGE_MASTER.png', kind='missing_image', note='待制作16:9全景，建议3840x2160；固定Logo拓扑、实面、主光'),
    'GROUP_MASTER': dict(path='frames/GROUP_MASTER.png', kind='missing_image', note='同一舞台六人全景，固定1+2+3，供E第4秒全貌目标'),
    'GROUP_LOCAL': dict(path='frames/GROUP_LOCAL.png', kind='missing_image', note='从同一空间设计派生低位六人局部，D末态/E预演起态'),
    'CORE3_MASTER': dict(path='frames/CORE3_MASTER.png', kind='missing_image', note='同一空间的Jessica/Feng/Scott三人局部，其余人不入画'),
    'DUO_MASTER': dict(path='frames/DUO_MASTER.png', kind='missing_image', note='同一空间的Song左/Amy右双人局部'),
    'B_LAST': dict(path='frames/SEG-B-selected-last.png', kind='future_extract', note='B采用源片的实际剪辑出点帧，不是原片最后一帧；尚待生成'),
    'D_LAST': dict(path='frames/SEG-D-selected-last.png', kind='future_extract', note='D采用源片的实际剪辑出点帧；尚待生成'),
}

IDENTITY = {
 'Jessica': 'Jessica的短齐发、眼镜、脸型与队服',
 'Feng': 'Feng的高额头、眼镜、脸型与队服',
 'Scott': 'Scott的浓密侧分短发与较低发际线、黑色矩形眼镜、较圆脸型和闭嘴微笑；与Feng是不同的人，保持单人定稿图身份',
 'Song': 'Song的短发、脸型与队服',
 'Amy': 'Amy的长发、脸型与队服',
 'Renwei': 'Renwei的不透明墨镜、短发、脸型与队服',
}

COMMON = ('电影级3D卡通，16:9横屏。参考图中的脸、头身比例和深蓝渐变饰边队服保持一致；'
          '柔和面部主光，克制青紫轮廓光；局部镜头采用贴近人物的低机位，以近处带缘、中景人物和远处高大折叠形成巨大空间的纵深。'
          '舞台结构固定，人物所在的既有带面宽阔平缓，双鞋有清楚接触阴影，舞步以小幅贴地踏步为主；'
          '全景参考约束造型、材质与站位，参考图的全亮状态不作为所有时段的照明。'
          '落脚触发细光沿已有带面传递，灯光变化只作用于带面与人物轮廓，面部入画时清楚、眼睛保持原样。'
          '只在指定切口换镜，每个人保留各自身份，交接靠剪切完成。'
          '不要字幕、对白、背景音乐或其他声音。')

def refine_segments(segments):
    by_id = {s['id']: s for s in segments}
    by_id['A']['refs'] = [('JESSICA','仅参考Jessica白鞋、裤装和身体比例，本段只拍鞋和小腿'),
                          ('STAGE_LOCAL','局部地面材质与光线')]
    by_id['B']['refs'] = [('JESSICA_FRAME','图中唯一人物定义为Jessica，参考身份、队服、脚底位置和局部舞台'),
                          ('FENG_FRAME','图中唯一人物定义为Feng，参考身份、队服与遮挡后构图'),
                          ('STAGE_LOCAL','只参考空舞台材质与固定边缘，不增加人物')]
    by_id['B']['beats'] = [
        ('0–2秒','镜头一：只有Jessica，膝上中景，微笑抬眼；镜头短距离拉至全身。'),
        ('2–4秒','延续镜头一：Jessica面向镜头略偏右，一次短侧步并轻轻送手，落脚光纹先向右传出；全身阶段头鞋完整。'),
        ('4–6秒','镜头向右短横移，经过已经存在的固定近景带缘，由相机经过造成蓝紫前景遮满画面；第6秒在全遮挡处直接切镜。'),
        ('6–8秒','镜头二：遮挡退开后只有Feng，匹配上一镜的机位和人物大小；左侧光纹抵达鞋边，Feng轻踏接光，站稳微笑，结束时脸清楚。')]
    by_id['C']['refs'] = [(n.upper(), IDENTITY[n]) for n in ['Jessica','Feng','Scott']] + [
        ('CORE3_MASTER','只约束最后三人镜头的舞台、站位与构图：Feng前中央，Jessica左后，Scott右后'),
        ('B_LAST','只参考开头Feng的实际姿态、机位和脚边光；与FENG参考是同一人')]
    by_id['D']['refs'] = [(n.upper(), IDENTITY[n]) for n in ['Jessica','Feng','Scott','Song','Amy','Renwei']] + [
        ('DUO_MASTER','只用于0–4秒的Song左、Amy右双人构图'),
        ('GROUP_LOCAL','只用于8–12秒的六人构图；前中央Feng，第二排左Jessica右Scott，第三排从左到右Song/Amy/Renwei，各自身份以单人图为准')]
    by_id['E']['refs'] = [(n.upper(), IDENTITY[n]) for n in ['Jessica','Feng','Scott','Song','Amy','Renwei']] + [
        ('D_LAST','镜头起始姿态与局部构图；其中六人与六张单人图逐一对应，各一人'),
        ('GROUP_MASTER','同一六人与同一舞台的高位全景；第4秒到达的构图，随后保持此视角群舞')]
    by_id['C']['beats'] = [
        ('0–4秒','镜头一：只有Feng，承接B段结束姿态，轻压肩部并向右开手，光沿地面传出；机位稳定。'),
        ('4–8秒','镜头二：在向右流动的光上匹配切到Scott中景。Scott第三位首次露脸，轻踏接光，微笑，脸清楚；末尾向左开手。'),
        ('8–12秒','镜头三：切到核心三人中全景，Feng前中央，Jessica左后、Scott右后；同拍踏步后向中央开手，再把汇聚的光传向右侧，机位短暂停稳。画面严格三人，Logo全貌仍在画外。')]
    by_id['D']['beats'] = [
        ('0–4秒','镜头一：只有Song和Amy，Song左、Amy右，两人小幅左右踏步，手臂波浪从Song传到Amy；末尾Amy落脚，光向右传出。'),
        ('4–8秒','镜头二：在地面光点上匹配切到Renwei单人中景，墨镜保持不透明。Renwei轻踏接光，微笑开手，再向相邻站位短移一步。'),
        ('8–12秒','镜头三：切到六人局部群像，其余五人已经就位；保持GROUP_LOCAL的1＋2＋3队形，六人共同落脚后小幅踏步，脚下光汇聚蓄力。全Logo仍在画外。')]
    by_id['E']['beats'] = [
        ('0–4秒','承接D_LAST局部群像，镜头一次连续升高后退，到达GROUP_MASTER高位全景。六人在原位轻律动，已有折叠彩带、交叠与中心留白逐渐进入视野；环境微光足够辨认整体结构，边缘灯保持低亮，第4秒全貌稳定；全轮廓贯通点亮留到下一拍。'),
        ('4–6秒','保持高位全景，六人同拍落脚，光沿已有Logo边缘贯通一次，亮出完整轮廓；接小幅左右踏步。'),
        ('6–10秒','镜头稳定，完整Logo持续可见，六人统一开手收回，再做一轮短手臂波浪；各自保持原站位。'),
        ('10–12秒','六人共同落脚开手，边缘光完成一次回环；最后短暂停格，完整Logo与六人始终在画面内。')]
    # Keep one principal action per beat; precise musical alignment is an editing task.
    by_id['A']['end_state'] = '局部光向画面右侧流动，只有鞋与小腿，整体Logo仍在画外。'
    by_id['B']['end_state'] = '只有Feng在局部带面站稳，脸清楚，保留脚边微光；最后一个镜头至少持续2秒。'
    by_id['C']['end_state'] = '核心三人稳定同框，将光向右送出；完整Logo在画外。'
    by_id['D']['end_state'] = '六人按1＋2＋3在实面蓄力，完整Logo在画外，留稳定末态供下一段衔接。'
    by_id['E']['end_state'] = '完整Logo持续可见，六人开手落脚后短暂停格，边缘光完成一次回环。'
    for s in segments:
        s['prompt_revision'] = 'v05-reviewed-20261118'

def render_segment_prompt(seg):
    refs = '\n'.join(f'【{alias}】：{role}。' for alias, role in seg['refs'])
    beats = '\n'.join(f'[{time}] {action}' for time, action in seg['beats'])
    mapping = '同一人物在单人图、构图图和连续帧里仍是同一个人；构图图中的人物不增加人数。'
    visibility = ('本段只见带面局部，完整Logo始终在画外；人物脸部清楚，远处结构沉在暗部，只有脚边与接力路径逐步亮起。'
                  if seg['id'] != 'E' else
                  '全貌通过镜头位移显现，舞台结构始终固定；揭示阶段以低亮环境光读出造型，共同落脚后才贯通点亮完整边缘。')
    return (f"素材对应：\n{refs}\n{mapping}\n"
            f"生成{seg['end']-seg['start']}秒视频，{seg['title']}。以下均为本段局部时间。\n"
            f"{COMMON}{visibility}\n镜头顺序与动作：\n{beats}\n结束状态：{seg['end_state']}\n")

def write_asset_manifest(base, segments):
    import hashlib
    from PIL import Image
    assets = {alias: {**spec, 'exists': (base/spec['path']).is_file()} for alias, spec in ASSETS.items()}
    selections = base/'preparation-manifest.json'
    if selections.exists():
        for alias, selected in json.loads(selections.read_text(encoding='utf-8')).get('assets', {}).items():
            if alias in assets:
                assets[alias].update(path=selected['path'], kind='prepared_reference',
                                     note=selected['review'], selection_status=selected['status'],
                                     exists=(base/selected['path']).is_file())
    for spec in assets.values():
        if spec['exists']:
            path = base/spec['path']
            with Image.open(path) as im:
                spec['size'] = list(im.size)
            spec['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    jobs = []
    for seg in segments:
        aliases = [a for a, _ in seg['refs']]
        jobs.append(dict(segment=seg['id'], image_count=len(aliases), aliases=aliases,
                         missing=[a for a in aliases if not assets[a]['exists']],
                         reference_files_present=all(assets[a]['exists'] for a in aliases)))
    (base/'asset-readiness.json').write_text(json.dumps(dict(
        audited='2026-11-18', note='Existence is not creative approval or proof of 3D continuity. preparation-manifest.json records selected image references. B_LAST/D_LAST require actual selected videos.',
        assets=assets, jobs=jobs), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
