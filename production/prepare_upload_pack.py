"""Build local LibTV input folders. No network, generation or actual frame invention."""
from copy import deepcopy
from pathlib import Path
import csv
import hashlib
import json
import shutil
from prompt_review import render_segment_prompt

BASE = Path(__file__).resolve().parent
OUT = BASE/'upload-pack'

def build_job(name, seg, assets, status):
    dest = OUT/name
    dest.mkdir(parents=True,exist_ok=True)
    rows=[]
    for index,(alias,role) in enumerate(seg['refs'],1):
        spec=assets[alias]
        source=BASE/spec['path']
        filename=f'{index:02d}_{alias}.png'
        item=dict(order=index,alias=alias,upload_file=filename,source=spec['path'],role=role,exists=source.is_file())
        if source.is_file():
            target=dest/filename
            data=source.read_bytes()
            if target.exists() and target.read_bytes()!=data:
                raise SystemExit('Existing upload differs; use a new pack directory: '+str(target))
            if not target.exists(): shutil.copy2(source,target)
            item['sha256']=hashlib.sha256(data).hexdigest()
        rows.append(item)
    (dest/'mapping.json').write_text(json.dumps(dict(job=name,status=status,source_paths_relative_to='production/',images=rows),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (dest/'PROMPT-template.txt').write_text(render_segment_prompt(seg),encoding='utf-8')
    missing=[r['alias'] for r in rows if not r['exists']]
    if missing:
        status='待补素材：'+', '.join(missing)+'；'+status
    (dest/'README.md').write_text(
        f'# {name}\n\n状态：{status}\n\n'
        '按文件名前缀顺序上传。PROMPT-template.txt中的【别名】需通过LibTV页面素材引用控件逐一替换为真实标签；本文件夹没有伪造平台标签。\n\n'
        f'缺失项：{", ".join(missing) if missing else "无本地图像缺口；仍需核对模式、角色和报价"}。\n\n'
        '采用后保存真实展开的提示词、参数与结果。PREVIEW仅为技术预演，不是已经完成与前段衔接的正式任务。\n',encoding='utf-8')
    return dict(job=name,status=status,image_count=len(rows),missing=missing)

def main():
    manifest=json.loads((BASE/'asset-readiness.json').read_text(encoding='utf-8'))
    assets=manifest['assets']
    segments=json.loads((BASE/'segments.json').read_text(encoding='utf-8'))
    index=[]
    for seg in segments:
        index.append(build_job(seg['id'],seg,assets,'等待真实连续帧' if seg['id'] in 'CE' else '图像已准备，视频效果待试制'))
    c=deepcopy(segments[2]);c['refs']=[r for r in c['refs'] if r[0]!='B_LAST']
    c['beats'][0][1]=c['beats'][0][1].replace('承接B段结束姿态','Feng从自然站稳姿态开始')
    index.append(build_job('C-PREVIEW',c,assets,'预演：省略B真实出点帧，不保证与B连续'))
    e=deepcopy(segments[4]);e['refs']=[['GROUP_LOCAL' if a=='D_LAST' else a,
        '预演起始六人局部构图，不是D实际末态' if a=='D_LAST' else r] for a,r in e['refs']]
    e['beats'][0][1]=e['beats'][0][1].replace('承接D_LAST局部群像','从GROUP_LOCAL六人局部群像开始')
    index.append(build_job('E-PREVIEW',e,assets,'预演：GROUP_LOCAL代替D真实出点帧，正式任务需换回D_LAST'))
    e1=deepcopy(e);e1.update(start=0,end=4,title='四秒揭示技术预演')
    e1['refs']=[['GROUP_LOCAL','预演首帧的局部六人构图'],['GROUP_MASTER','四秒末尾到达的全景构图；严格首尾锁定须在面板实际启用']]
    e1['beats']=[['0–4秒','从GROUP_LOCAL六人局部开始，镜头一次连续升高后退，到达GROUP_MASTER完整全景；六人保持相对站位轻律动，已有折叠彩带、交叠与中心留白进入视野；以低亮环境光读出造型，边缘灯保持低亮，贯通点亮留到下一段。']]
    e1['end_state']='完整Logo与原六人稳定可见，舞台结构保持原样。'
    index.append(build_job('E1-PREVIEW-4s',e1,assets,'四秒揭示预演；GROUP_LOCAL不是D实际末态，正式需替换首帧'))
    e2=deepcopy(e);e2.update(start=0,end=8,title='八秒共同点亮与群舞技术预演')
    e2['refs']=[r for r in e2['refs'] if r[0]!='GROUP_LOCAL']
    e2['refs'][-1][1]='开头完整全景与站位参考；正式应使用E1实际采用的出点帧，而不是静态设计图'
    e2['beats']=[['0–2秒','从完整全景开始，镜头固定；六人同拍落脚，光沿已有Logo边缘贯通一次，接小幅左右踏步。'],
                 ['2–6秒','完整Logo持续可见，六人统一开手收回，再做一轮短手臂波浪，保持各自站位。'],
                 ['6–8秒','六人共同落脚开手，边缘光完成一次回环，最后短暂停格。']]
    index.append(build_job('E2-PREVIEW-8s',e2,assets,'八秒群舞预演；正式需用E1真实出点帧衔接'))
    (OUT/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# LibTV分段上传包','','先核对当前模型的模式和报价。按每个文件夹内数字前缀上传；平台引用标签须通过页面控件插入。正式视频尚未生成，这些文件夹也尚未导入LibTV。','',
           '| 任务 | 图片数 | 尚缺 | 状态 |','| --- | --- | --- | --- |']
    for row in index:
        lines.append(f"| [{row['job']}]({row['job']}/README.md) | {row['image_count']} | {', '.join(row['missing']) or '无本地图像缺口'} | {row['status']} |")
    lines += ['','C/E正式任务中的B_LAST/D_LAST必须从实际采用视频提取，不以设计图冒充。C-PREVIEW、E-PREVIEW及E1/E2-PREVIEW为可单独测试的图像参考版本。','',
              '二维揭示备用预演见`../previews/E1-reveal-2D-PREVIS-v01.mp4`，人物静止且有明确预演标识；不能冒充已生成的AI视频或真实三维升镜。']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(index,ensure_ascii=False))

if __name__=='__main__':
    main()
