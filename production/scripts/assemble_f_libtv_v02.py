"""Key LibTV's actual two-person animation and composite the revised F credits."""
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from assemble_f_ending_v01 import FF, ROOT, run, smooth, video_frame

FPS, W, H = 30, 1920, 1080
AE_N, F_N = 1378, 182
SOURCE = ROOT/'videos/SEG-F-creators-peek-6s-Wan3-480P-v01-green.mp4'
F1080 = ROOT/'videos/SEG-F-LibTV-cameos-1080P-layout-v02-silent.mp4'
F480 = ROOT/'videos/SEG-F-LibTV-cameos-480P-v02-silent.mp4'
SILENT = ROOT/'exports/FY27-A-F-52s-480P-v02-silent.mp4'
FINAL = ROOT/'exports/FY27-A-F-52s-480P-v02-LibTV-cameos-music.mp4'
PREVIEW = ROOT/'previews/SEG-E-F-9p07s-LibTV-cameos-v02-music.mp4'


def key(rgb):
    signed=rgb.astype(np.float32)
    red, green, blue=signed[:,:,0],signed[:,:,1],signed[:,:,2]
    dominance=green-np.maximum(red,blue)
    candidate=((dominance>22)&(green>65)).astype(np.uint8)
    # Only key green connected to the outside, retaining enclosed logo colors.
    padded=np.pad(candidate,1,constant_values=1)
    cv2.floodFill(padded,None,(0,0),2)
    background=padded[1:-1,1:-1]==2
    alpha=(~background).astype(np.uint8)*255
    n, labels, stats, _ = cv2.connectedComponentsWithStats((alpha>0).astype(np.uint8),8)
    for label in range(1,n):
        if stats[label,cv2.CC_STAT_AREA]<25:
            alpha[labels==label]=0
    # Subpixel smoothing and conservative green-spill removal at the edge.
    alpha=cv2.GaussianBlur(alpha,(3,3),.45)
    edge=cv2.morphologyEx(alpha,cv2.MORPH_GRADIENT,np.ones((3,3),np.uint8))>0
    cleaned=rgb.copy()
    cleaned[:,:,1]=np.where(edge,np.minimum(green,np.maximum(red,blue)+8),green).astype(np.uint8)
    return np.dstack((cleaned,alpha))


def load_animation():
    cap=cv2.VideoCapture(str(SOURCE));fps=cap.get(5);frames=[]
    while True:
        ok,bgr=cap.read()
        if not ok:break
        frames.append(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB))
    cap.release();assert frames and fps>0
    height,width=frames[0].shape[:2]
    layers=[[],[]];rois=[]
    for side in range(2):
        alpha_union=np.zeros((height,width//2),np.uint8)
        for rgb in frames:
            half=rgb[:,side*(width//2):(side+1)*(width//2)]
            rgba=key(half);layers[side].append(rgba)
            alpha_union=np.maximum(alpha_union,rgba[:,:,3])
        ys,xs=np.where(alpha_union>100)
        assert len(xs)>0
        # A fixed spatial crop preserves the model's real peek-up trajectory.
        rois.append((max(0,int(xs.min())-4),max(0,int(ys.min())-4),
                     min(width//2,int(xs.max())+5),height))
    return layers,rois,fps,len(frames)


def main():
    layers,rois,source_fps,source_n=load_animation()
    credits=json.loads((ROOT/'credits-info.json').read_text(encoding='utf-8'))
    source=Image.open(ROOT/'frames/F-E-tail-background-v01.png').convert('RGB')
    source=source.resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
    alpha=np.full((H,W),255,np.uint8)
    alpha[-100:,:]=np.linspace(255,0,100)[:,None].astype(np.uint8)
    source.putalpha(Image.fromarray(alpha))
    overlay=Image.new('RGBA',(W,H));draw=ImageDraw.Draw(overlay)
    fonts=Path('C:/Windows/Fonts')
    for text,y,fontname,size,color in [
        (credits['ending_idea_draft'],835,'seguisb.ttf',44,(232,245,255,255)),
        ('创作团队  Baoli Wang · Yun Gu',910,'msyh.ttc',32,(225,233,245,255)),
        ('AI Models: '+credits['ending_models_display'],994,'segoeui.ttf',24,(185,202,223,255)),
        ('Tools: '+credits['ending_tools_display'],1031,'segoeui.ttf',24,(185,202,223,255))]:
        font=ImageFont.truetype(str(fonts/fontname),size)
        box=draw.textbbox((0,0),text,font=font);assert box[2]-box[0]<1660
        draw.text(((W-box[2]+box[0])//2,y),text,font=font,fill=color)
    if not F1080.exists():
        proc=subprocess.Popen([FF,'-hide_banner','-loglevel','error','-n',
            '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
            '-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
            '-video_track_timescale','15360','-movflags','+faststart',str(F1080)],
            stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        for i in range(F_N):
            t=i/FPS
            frame=Image.new('RGBA',(W,H),(4,12,29,255))
            frame.alpha_composite(source,(0,round(-90*smooth(t/.85))))
            text=overlay.copy();visibility=smooth((t-.75)/.6)
            text.putalpha(text.getchannel('A').point(lambda a:round(a*visibility)))
            frame.alpha_composite(text)
            index=min(source_n-1,round(t*source_fps))
            for side in range(2):
                im=Image.fromarray(layers[side][index]).crop(rois[side])
                scale=138/im.height
                im=im.resize((round(im.width*scale),138),Image.Resampling.LANCZOS)
                x=42 if side==0 else W-42-im.width
                frame.alpha_composite(im,(x,H-im.height+8))
            fade=smooth((t-5.7)/(.3667))
            if fade:frame.alpha_composite(Image.new('RGBA',(W,H),(0,0,0,round(255*fade))))
            if i in (0,30,60,90,120,150,175):
                frame.convert('RGB').save(ROOT/f'previews/F-LibTV-v02-frame-{i:03}.jpg',quality=95)
            proc.stdin.write(frame.convert('RGB').tobytes())
        proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode(errors='replace')
    if not F480.exists():
        run(['-i',F1080,'-vf','scale=854:480:flags=lanczos','-an','-c:v','libx264',
             '-crf','16','-preset','slow','-pix_fmt','yuv420p','-video_track_timescale','15360',
             '-movflags','+faststart',F480])
    ae=ROOT/'exports/FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-silent.mp4'
    concat=ROOT/'exports/FY27-A-F-v02-concat.txt'
    concat.write_text(f"file '{ae.as_posix()}'\nfile '{F480.as_posix()}'\n",encoding='utf-8')
    if not SILENT.exists():
        run(['-f','concat','-safe','0','-i',concat,'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',SILENT])
    # Reuse the already assembled ending music; no additional music generation.
    old=ROOT/'exports/FY27-A-F-52s-480P-v01-music.mp4'
    if not FINAL.exists():
        run(['-i',SILENT,'-i',old,'-map','0:v:0','-map','1:a:0','-c','copy','-t','52','-movflags','+faststart',FINAL])
    if not PREVIEW.exists():
        run(['-i',FINAL,'-ss',AE_N/FPS-3,'-t',3+F_N/FPS,'-c:v','libx264','-crf','17',
             '-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',PREVIEW])
    cap=cv2.VideoCapture(str(FINAL));n=int(cap.get(7));fps=cap.get(5);cap.release()
    assert n==AE_N+F_N and fps==FPS
    for index in (0,297,298,657,897,1137,1377):
        assert np.array_equal(video_frame(ae,index),video_frame(FINAL,index))
    run(['-xerror','-i',FINAL,'-f','null','-'])
    manifest={'status':'pending_user_review','output':str(FINAL),'frames':n,'fps':fps,'duration':n/fps,
        'f_start':AE_N/FPS,'libtv_source':str(SOURCE),'source_fps':source_fps,'source_frames':source_n,
        'fixed_key_rois':rois,'cameo_max_visible_height_1080p':130,'credits_spent':24,
        'stage':'E tail, full-width upward reframe, no shrinking','text':'local overlay, exact current credits',
        'verification':{'full_decode':'passed','sampled_AE_frames':'exact pixels','audio':'stream copied from prior 52s mix'}}
    (ROOT/'exports/FY27-A-F-52s-v02-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
