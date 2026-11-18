"""Render pause-readable verbatim actual prompt cards from a production log.

Run normally only after filling run-log.csv and credits-info.json.
--preview renders clearly marked planned text separately; no claim of actual use.
"""
import argparse
import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
FONT = 'C:/Windows/Fonts/msyh.ttc'
W,H = 1920,1080
M = 96
LINE = 36
TOP = 164
BOTTOM = 966


def font(size):
    return ImageFont.truetype(FONT,size)


def wrap(text, draw, body):
    """Keep every character; wrap without clipping. Original text kept separately."""
    lines=[]
    for raw in text.split('\n'):
        if not raw:
            lines.append('')
            continue
        current=''
        for ch in raw:
            if draw.textlength(current+ch,font=body)>W-2*M:
                lines.append(current)
                current=ch
            else:
                current+=ch
        lines.append(current)
    return lines


def render(preview=False):
    info=json.loads((BASE/'credits-info.json').read_text(encoding='utf-8'))
    if not preview:
        missing=[k for k,v in info.items() if not str(v).strip() or 'PENDING' in str(v) or '[' in str(v)]
        if missing:
            raise SystemExit('Fill actual credits-info.json fields first: '+', '.join(missing))
    entries=[]
    if preview:
        for path in sorted((BASE/'prompts').glob('*.txt')):
            # S11 image prompt explains extracting an actual frame, not image generation.
            if path.name=='S11-image.txt':
                continue
            entries.append((path.stem,'计划文本，尚未生成',path,path.read_text(encoding='utf-8')))
        for path in sorted((BASE.parent/'prompts').glob('*.txt')):
            entries.append(('既有来源/'+path.stem,'既有生成记录；以实际采用记录为准',path,path.read_text(encoding='utf-8')))
    else:
        rows=list(csv.DictReader((BASE/'run-log.csv').open(encoding='utf-8-sig',newline='')))
        for row in rows:
            if row.get('used_in_final','').strip().lower() not in {'yes','true','1','y'}:
                continue
            asset=row.get('asset_id','').strip()
            model=row.get('model','').strip()
            prompt_name=row.get('actual_prompt_file','').strip()
            output_name=row.get('output_file','').strip()
            if not all([asset,model,prompt_name,output_name]) or 'PENDING' in model:
                raise SystemExit(f'Incomplete actual log row: {asset!r}')
            path=(BASE/prompt_name).resolve()
            output=(BASE/output_name).resolve()
            if not path.is_file() or not output.is_file():
                raise SystemExit(f'Missing actual prompt or used output for {asset}: {path}, {output}')
            entries.append((asset,model,path,path.read_text(encoding='utf-8-sig')))
        if not entries:
            raise SystemExit('No actually used prompts logged. Fill run-log.csv or use --preview.')
    out=BASE/('credits-preview' if preview else 'credits')
    cards=out/'cards';cards.mkdir(parents=True,exist_ok=True)
    body=font(26);title=font(34);small=font(22)
    scratch=ImageDraw.Draw(Image.new('RGB',(W,H)))
    capacity=(BOTTOM-TOP)//LINE
    pages=[];archive=[];seen=set()
    for asset,model,path,text in entries:
        # Preserve every used asset attribution, deduplicate identical prompt body only.
        archive.append(f'ASSET: {asset}\nMODEL: {model}\nSOURCE: {path.relative_to(BASE) if path.is_relative_to(BASE) else path}\n\n{text}\n\n'+('='*72)+'\n')
        if text in seen:
            continue
        seen.add(text)
        wrapped=wrap(text,scratch,body)
        for j in range(0,len(wrapped),capacity):
            pages.append((asset,model,wrapped[j:j+capacity]))
    if len(pages)>80:
        raise SystemExit(f'{len(pages)} pages need more than 8 seconds at minimum 3 frames/page. Revise delivery plan.')
    total=len(pages)
    if not total:
        raise SystemExit('No prompt text.')
    for i,(asset,model,lines) in enumerate(pages,1):
        im=Image.new('RGB',(W,H),'#081426');d=ImageDraw.Draw(im)
        label='计划稿 · 非实际使用记录' if preview else '完整原始 Prompt · 可暂停 / 逐帧阅读'
        d.text((M,42),label,font=title,fill='#90d9ff')
        header=f'{i:02d}/{total:02d}  {asset}  |  {model}'
        # Metadata wraps independently; body remains at fixed safe TOP.
        hlines=wrap(header,d,small)
        if len(hlines)>2:
            raise SystemExit('Prompt metadata too long; shorten asset/model labels.')
        for n,line in enumerate(hlines):d.text((M,94+n*27),line,font=small,fill='#bdd0e8')
        for n,line in enumerate(lines):d.text((M,TOP+n*LINE),line,font=body,fill='#f0f3f8')
        d.text((M,1010),'完整文本另附；本页为暂停阅读，不代表正常速度可读完。',font=small,fill='#a8bad2')
        im.save(cards/f'prompt-{i:03d}.png')
    (out/('PLANNED-PROMPTS.txt' if preview else 'ACTUAL-PROMPTS.txt')).write_text('\n'.join(archive),encoding='utf-8')
    im=Image.new('RGB',(W,H),'#081426');d=ImageDraw.Draw(im)
    titletext=info['title']+(' · 制作信息计划稿' if preview else '')
    d.text((M,90),titletext,font=font(48),fill='white')
    contents=[info['team']+' · FY27 Kickoff',f"导演：{info['director']}  主创：{info['creators']}",
              '图像：'+info['image_tools'],'视频：'+info['video_tools'],'音乐：'+info['music_tools'],
              '剪辑：'+info['editing_tools'],'创意思路：'+info['idea']]
    y=205
    for text in contents:
        lines=wrap(text,d,font(34))
        for line in lines:
            if y>940:raise SystemExit('Credits info too long for one readable card; shorten tool labels.')
            d.text((M,y),line,font=font(34),fill='#e7eef8');y+=61
    im.save(cards/'credits-info.png')
    q,r=divmod(240,total)
    with (out/'card-timeline.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['file','start_frame_30fps','duration_frames','start_seconds','end_seconds'])
        w.writerow(['cards/credits-info.png',1440,120,48,52])
        pos=1560
        for i in range(total):
            dur=q+(1 if i<r else 0)
            w.writerow([f'cards/prompt-{i+1:03d}.png',pos,dur,f'{pos/30:.6f}',f'{(pos+dur)/30:.6f}'])
            pos+=dur
        assert pos==1800
    (out/'README.txt').write_text(
        f"{'PREVIEW ONLY; not actual production.' if preview else 'Actual prompts from selected logged outputs.'}\n"
        f'{total} prompt cards over 240 frames (8 seconds), 30fps. Pause/frame-step to read.\n'
        'Use card-timeline.csv, not default still-image durations. Reruns may leave older images; import ONLY listed files.\n',encoding='utf-8')
    print(f'{out}: {total} pause-readable prompt cards; information 48–52s; prompts 52–60s.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true')
    render(p.parse_args().preview)
