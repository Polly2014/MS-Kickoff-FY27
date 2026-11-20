"""Inspect regenerated A's final motion and create an untrimmed A08-to-B08 junction."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
a=root/'videos'/'SEG-A-Wan3-480P-v08-single-descent.mp4'
b=root/'videos'/'SEG-B-Wan3-480P-v08-adopted.mp4'
music=root/'music'/'MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
out=root/'previews'/'SEG-AB-A08-B08-direct-junction-music-v01.mp4'

def frame(path,index):
    c=cv2.VideoCapture(str(path));c.set(1,index);ok,f=c.read();c.release();assert ok,(path,index)
    return Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))

c=cv2.VideoCapture(str(a))
meta=dict(frames=int(c.get(7)),fps=c.get(5),width=int(c.get(3)),height=int(c.get(4)))
c.release();assert meta['frames']==360 and meta['fps']==30,meta
items=[('A08',a,i) for i in [285,294,300,306,312,318,324,330,336,342,348,354,359]]
items += [('B08',b,i) for i in [0,3,6,9,12,15,21,27,30]]
sheet=Image.new('RGB',(6*360,4*228),'#17191d');d=ImageDraw.Draw(sheet)
for j,(label,path,idx) in enumerate(items):
    im=frame(path,idx);im.thumbnail((356,200));x=j%6*360;y=j//6*228
    d.text((x+4,y+5),f'{label} {idx/30:.3f}s | f{idx}',fill='white');sheet.paste(im,(x,y+25))
sheet.save(root/'previews'/'SEG-A-v08-final-motion-review.jpg',quality=95)
detail=Image.new('RGB',(1708,510),'#17191d');d=ImageDraw.Draw(detail)
for j,(path,idx,label) in enumerate([(a,359,'A08 last frame 11.967s'),(b,0,'B08 first frame 0.000s')]):
    d.text((j*854+8,8),label,fill='white');detail.paste(frame(path,idx),(j*854,30))
detail.save(root/'previews'/'SEG-AB-A08-B08-boundary.jpg',quality=95)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
if not out.exists():
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(a),'-i',str(b),'-i',str(music),
        '-filter_complex',
        '[0:v]trim=start_frame=300:end_frame=360,setpts=N/(30*TB)[a];'
        '[1:v]trim=start_frame=0:end_frame=60,setpts=N/(30*TB)[b];'
        '[a][b]concat=n=2:v=1:a=0[v];'
        '[2:a]atrim=start=10:end=14,asetpts=PTS-STARTPTS,volume=-4dB[s]',
        '-map','[v]','-map','[s]','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',
        '-r','30','-fps_mode','cfr','-c:a','aac','-b:a','256k','-t','4','-movflags','+faststart',str(out)],check=True)
c=cv2.VideoCapture(str(out));assert int(c.get(7))==120 and c.get(5)==30;c.release()
print(json.dumps(dict(source=a.name,metadata=meta,preview=out.name,cut='A08 [10,12) + B08 [0,2); no trim adjustment'),indent=2))

# The regenerated A descends below B's starting pose. Match earlier in that single descent.
matched=root/'previews'/'SEG-AB-A08-B08-matched-junction-v02-music.mp4'
if not matched.exists():
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(a),'-i',str(b),'-i',str(music),
        '-filter_complex',
        '[0:v]trim=start_frame=280:end_frame=340,setpts=N/(30*TB)[a];'
        '[1:v]trim=start_frame=0:end_frame=60,setpts=N/(30*TB)[b];'
        '[a][b]concat=n=2:v=1:a=0[v];'
        '[2:a]atrim=start=9.3333333333:end=13.3333333333,asetpts=PTS-STARTPTS,volume=-4dB[s]',
        '-map','[v]','-map','[s]','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',
        '-r','30','-fps_mode','cfr','-c:a','aac','-b:a','256k','-t','4','-movflags','+faststart',str(matched)],check=True)
c=cv2.VideoCapture(str(matched));assert int(c.get(7))==120 and c.get(5)==30;c.release()
run_review=dict(source=a.name,metadata=meta,review_status='pending_user_review',
                observation='Only one final descent in sampled frames. New A ends lower than B starts; direct 12-second junction jumps upward.',
                recommended_edit=dict(a_source_frames=[0,340],a_source_end_seconds=340/30,b_source_start=0,
                                      preview=matched.name,preview_a_source_frames=[280,340],preview_b_source_frames=[0,60],preview_cut_seconds=2),
                raw_junction=out.name,credit_cost=48,remaining_credits=2491)
(root/'SEG-A-v08-result-review.json').write_text(json.dumps(run_review,indent=2),encoding='utf-8')
print(json.dumps(run_review,indent=2))
