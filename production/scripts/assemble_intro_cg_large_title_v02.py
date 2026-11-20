"""Enlarge the approved two-line team typography to LibTV's CG background and prepend it to v06."""
import json
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from assemble_f_ending_v01 import FF, ROOT, run, smooth

RAW = ROOT/'videos/INTRO-B-CG-ignite-4s-Wan3-480P-v01-source.mp4'
BASE = ROOT/'exports/FY27-A-F-51p43s-480P-v06-group-photo-avfade03-music.mp4'
INTRO = ROOT/'videos/INTRO-B-CG-title-large-4s-480P-v02-silent.mp4'
FINAL = ROOT/'exports/FY27-CG-intro-A-F-55p43s-480P-v02-large-title-music.mp4'
PREVIEW = ROOT/'previews/INTRO-B-CG-to-Jessica-first9s-v02-large-title-music.mp4'
TITLE = ['STCA M365 Copilot','Foundation & Platform Team']


def main():
    overlay = Image.new('RGBA',(1920,1080))
    draw = ImageDraw.Draw(overlay)
    for text,y,size in [(TITLE[0],361,91),(TITLE[1],485,66)]:
        font = ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',size)
        box = draw.textbbox((0,0),text,font=font)
        draw.text(((1920-(box[2]-box[0]))//2,y),text,font=font,
                  fill=(237,251,255,255),stroke_width=1,stroke_fill=(3,14,30,200))
    glow = Image.new('RGBA',overlay.size,(45,200,255,0))
    glow.putalpha(overlay.getchannel('A').filter(ImageFilter.GaussianBlur(10)).point(lambda a:round(a*.45)))
    glow.alpha_composite(overlay)
    overlay=glow.resize((854,480),Image.Resampling.LANCZOS)
    cap=cv2.VideoCapture(str(RAW));source_fps=cap.get(5);source_n=int(cap.get(7));cap.release()
    assert source_n>0 and abs(source_n/source_fps-4)<.1
    if not INTRO.exists():
        cap=cv2.VideoCapture(str(RAW))
        proc=subprocess.Popen([FF,'-hide_banner','-loglevel','error','-n','-f','rawvideo',
            '-pix_fmt','rgb24','-s','854x480','-r','30','-i','-','-an','-c:v','libx264',
            '-preset','fast','-crf','16','-pix_fmt','yuv420p','-video_track_timescale','15360',
            '-movflags','+faststart',str(INTRO)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        # Convert the generator's frame rate to the film's 30fps without changing its duration.
        frames=[]
        while True:
            ok,bgr=cap.read()
            if not ok:break
            frames.append(bgr)
        cap.release()
        for i in range(120):
            t=i/30;bgr=frames[min(len(frames)-1,round(t*source_fps))]
            frame=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)).resize((854,480),Image.Resampling.LANCZOS).convert('RGBA')
            visibility=smooth((t-.65)/.3)*(1-smooth((t-3.1)/.3))
            if visibility:
                text=overlay.copy();text.putalpha(text.getchannel('A').point(lambda a:round(a*visibility)))
                frame.alpha_composite(text)
            if i in (0,20,30,60,90,105,119):
                frame.convert('RGB').save(ROOT/f'previews/INTRO-B-CG-title-large-v02-frame-{i:03}.jpg',quality=95)
            proc.stdin.write(frame.convert('RGB').tobytes())
        proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode()
    concat=ROOT/'exports/INTRO-B-CG-prepend-concat-v02-large-title.txt'
    concat.write_text(f"file '{INTRO.as_posix()}'\nfile '{BASE.as_posix()}'\n",encoding='utf-8')
    # Keep the generated effect dynamics; lower only if its peak would be excessive.
    sound=np.frombuffer(run(['-i',RAW,'-vn','-ar',48000,'-ac',2,'-f','f32le','-']).stdout,dtype='<f4')
    assert len(sound)>0,'Generated video has no decodable audio'
    peak=float(np.max(np.abs(sound)));gain=min(1.,.85/max(peak,1e-8))
    approved_audio=ROOT/'exports/FY27-CG-intro-A-F-55p43s-480P-v01-music.mp4'
    if not FINAL.exists():
        run(['-f','concat','-safe',0,'-i',concat,'-i',approved_audio,
             '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',FINAL])
    def audio(path):
        return run(['-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-']).stdout
    assert audio(approved_audio)==audio(FINAL)
    if not PREVIEW.exists():
        run(['-i',FINAL,'-t',9,'-c:v','libx264','-preset','fast','-crf',17,
             '-c:a','aac','-b:a',192000,'-movflags','+faststart',PREVIEW])
    cap=cv2.VideoCapture(str(FINAL));assert cap.get(7)==1663 and cap.get(5)==30;cap.release()
    original=cv2.VideoCapture(str(BASE));revised=cv2.VideoCapture(str(FINAL))
    for i in range(120):assert revised.read()[0]
    for i in range(1543):
        ok,a=original.read();ok2,b=revised.read();assert ok and ok2
        if i in (0,297,298,657,897,1137,1377,1542):assert np.array_equal(a,b),i
    original.release();revised.release()
    run(['-xerror','-i',FINAL,'-f','null','-'])
    manifest={'status':'pending_user_review','output':str(FINAL),'preview':str(PREVIEW),
        'frames':1663,'fps':30,'duration_seconds':1663/30,'intro_seconds':4,
        'source':str(RAW),'source_fps':source_fps,'title_lines':TITLE,
        'title_sizes_1080p':[91,66],'previous_title_sizes':[76,57],
        'title_scale':[91/76,66/57],'title_visible_interval':[.65,3.4],'credits_spent':0,'generated_audio_peak':peak,'intro_gain':gain,
        'audio':'generated CG sound effects followed by original v06 music, body timing shifted exactly 4s',
        'verification':{'AEF_sampled_frames':'exact pixels, sequential decode','full_decode':'passed','audio_packets':'identical to approved v01'},
        'limitations':'generation prompt compliance and perceived sound quality require user review'}
    (ROOT/'exports/INTRO-B-CG-assembled-v02-large-title-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
