"""Rebuild the approved 1663-frame film from HuoShan enhancements."""
import json
import subprocess
import hashlib
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from assemble_f_ending_v01 import FF, ROOT, run, smooth
from assemble_f_group_photo_v04 import load_animation

FINAL=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-HuoShan-v01-music.mp4'
APPROVED=ROOT/'exports/FY27-CG-intro-A-F-55p43s-480P-v03-english-credits-music.mp4'
SPECS=[('INTRO','INTRO-CG-HuoShan-1080P30-HD-v01.mp4','INTRO-B-CG-ignite-4s-Wan3-480P-v01-source.mp4',120),
 ('A','SEG-A-v07-HuoShan-1080P30-HD-v01.mp4','SEG-A-Wan3-480P-v07-adopted.mp4',360),
 ('B','SEG-B-v08-HuoShan-1080P30-HD-v01.mp4','SEG-B-Wan3-480P-v08-adopted.mp4',360),
 ('C','SEG-C-v08-HuoShan-1080P30-HD-v01.mp4','SEG-C-Wan3-480P-v08-adopted.mp4',240),
 ('D08','SEG-D-v08-HuoShan-1080P30-HD-v01.mp4','SEG-D-Wan3-480P-v08-original.mp4',240),
 ('D13','SEG-D-v13-HuoShan-1080P30-HD-v01.mp4','SEG-D-Wan3-480P-v13-adopted.mp4',240),
 ('E','SEG-E-v08-HuoShan-1080P30-HD-v01.mp4','SEG-E-Wan3-480P-v08-adopted.mp4',240)]

def tiny_frames(path):
    cap=cv2.VideoCapture(str(path));fps=cap.get(5);meta={'file':str(path),'width':int(cap.get(3)),'height':int(cap.get(4)),'fps':fps,'frames':int(cap.get(7))};out=[]
    while True:
        ok,bgr=cap.read()
        if not ok:break
        out.append(cv2.resize(cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY),(320,180),interpolation=cv2.INTER_AREA))
    cap.release();assert len(out)==meta['frames'] and fps>0,path
    return out,meta

def encoder(path):
    return subprocess.Popen([FF,'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-video_track_timescale','15360','-movflags','+faststart',str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)

def finish(p):
    p.stdin.close();err=p.stderr.read();assert p.wait()==0,err.decode()

def title_layer():
    overlay=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(overlay)
    for text,y,size in [('STCA M365 Copilot',361,91),('Foundation & Platform Team',485,66)]:
        font=ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',size);box=draw.textbbox((0,0),text,font=font)
        draw.text(((1920-(box[2]-box[0]))//2,y),text,font=font,fill=(237,251,255,255),stroke_width=1,stroke_fill=(3,14,30,200))
    glow=Image.new('RGBA',overlay.size,(45,200,255,0));glow.putalpha(overlay.getchannel('A').filter(ImageFilter.GaussianBlur(10)).point(lambda a:round(a*.45)));glow.alpha_composite(overlay)
    return glow

def beam_layers():
    cap=cv2.VideoCapture(str(ROOT/'videos/SEG-A-Wan3-480P-v07-adopted.mp4'));out=[];i=0
    while i<306:
        ok,donor=cap.read();assert ok
        if i>=298:
            donor=donor.astype(np.float32);delta=np.maximum(donor-cv2.GaussianBlur(donor,(0,0),sigmaX=1,sigmaY=7),0)
            cyan=(donor[:,:,0]>donor[:,:,2]+25)&(donor[:,:,1]>donor[:,:,2]+20);energy=(delta[:,:,0]>5)&(delta[:,:,1]>5)
            mask=np.zeros((480,854),np.float32);mask[130:270,:330]=(cyan&energy)[130:270,:330];mask=cv2.GaussianBlur(mask,(0,0),.65)
            glow=delta*mask[:,:,None]*(1-(i-298)/8)
            out.append(cv2.resize(glow,(1920,1080),interpolation=cv2.INTER_LANCZOS4))
        i+=1
    cap.release();return out

def main():
    metadata=[]
    for label,hd,original,count in SPECS:
        output,m=tiny_frames(ROOT/'videos'/hd);source,sm=tiny_frames(ROOT/'videos'/original)
        assert m['frames']==count and m['fps']==30 and m['height']==1080,m
        matches=[]
        for i in [9,count//4,count//2,3*count//4,count-10]:
            oi=min(len(source)-1,round(i/30*sm['fps']))
            distances={j:float(np.mean(np.abs(source[oi].astype(np.float32)-output[j].astype(np.float32)))) for j in range(max(0,i-3),min(count,i+4))}
            best=min(distances,key=distances.get);matches.append({'frame':i,'best_output_frame':best,'mae':distances[best]})
            assert best==i,(label,matches)
        m['alignment']=matches;metadata.append(m);print('Aligned',label,flush=True)
    beams=beam_layers();title=title_layer();parts=[];tail=None
    for label,hd,_,count in SPECS:
        part=ROOT/f'videos/HD-edit-{label}-1080P30-v01-silent.mp4';parts.append(part)
        start,end=(0,298) if label=='A' else ((0,120) if label=='D08' else ((120,240) if label=='D13' else (0,count)))
        cap=cv2.VideoCapture(str(ROOT/'videos'/hd));p=None if part.exists() else encoder(part)
        for i in range(count):
            ok,bgr=cap.read();assert ok,(label,i)
            if not start<=i<end:continue
            bgr=cv2.resize(bgr,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
            if label=='B' and i<8:bgr=np.clip(bgr.astype(np.float32)+beams[i],0,255).astype(np.uint8)
            frame=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)).convert('RGBA')
            if label=='INTRO':
                t=i/30;v=smooth((t-.65)/.3)*(1-smooth((t-3.1)/.3));txt=title.copy();txt.putalpha(txt.getchannel('A').point(lambda a:round(a*v)));frame.alpha_composite(txt)
            if label=='E' and i==239:tail=frame.copy();tail.convert('RGB').save(ROOT/'frames/F-E-tail-HuoShan-1080P-v01.png')
            if p:p.stdin.write(frame.convert('RGB').tobytes())
        cap.release()
        if p:finish(p)
        print('Rendered',label,flush=True)
    fpart=ROOT/'videos/HD-edit-F-1080P30-v01-silent.mp4';parts.append(fpart)
    if not fpart.exists():
        credits=json.loads((ROOT/'credits-info.json').read_text(encoding='utf-8'));layers,rois,source_fps,_=load_animation()
        alpha=np.full((1080,1920),255,np.uint8);alpha[-100:,:]=np.linspace(255,0,100)[:,None].astype(np.uint8);tail.putalpha(Image.fromarray(alpha))
        overlay=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(overlay)
        for text,y,fontname,size,color in [(credits['ending_idea_draft'],835,'seguisb.ttf',44,(232,245,255,255)),('Created by Baoli Wang · Yun Gu',910,'segoeui.ttf',32,(225,233,245,255)),('AI Models: '+credits['ending_models_display'],994,'segoeui.ttf',24,(185,202,223,255)),('Tools: '+credits['ending_tools_display'],1031,'segoeui.ttf',24,(185,202,223,255))]:
            font=ImageFont.truetype(str(Path('C:/Windows/Fonts')/fontname),size);box=draw.textbbox((0,0),text,font=font);draw.text(((1920-box[2]+box[0])//2,y),text,font=font,fill=color)
        p=encoder(fpart)
        for i in range(165):
            t=min(i,149)/30;frame=Image.new('RGBA',(1920,1080),(4,12,29,255));frame.alpha_composite(tail,(0,round(-90*smooth(t/.85))))
            txt=overlay.copy();visibility=smooth((t-.75)/.6);txt.putalpha(txt.getchannel('A').point(lambda a:round(a*visibility)));frame.alpha_composite(txt)
            for side in range(2):
                index=min(88 if side==0 else 92,round(t*source_fps));im=Image.fromarray(layers[side][index]).crop(rois[side]);scale=138/im.height;im=im.resize((round(im.width*scale),138),Image.Resampling.LANCZOS);frame.alpha_composite(im,(42 if side==0 else 1920-42-im.width,1080-im.height+8))
            if i>=156:frame.alpha_composite(Image.new('RGBA',(1920,1080),(0,0,0,round(255*min(1,(i-156)/8)))))
            if i==120:frame.convert('RGB').save(ROOT/'previews/F-HD-english-credits-v01.jpg',quality=96)
            p.stdin.write(frame.convert('RGB').tobytes())
        finish(p)
    concat=ROOT/'exports/HD-full-v01-concat.txt';concat.write_text(''.join(f"file '{p.as_posix()}'\n" for p in parts),encoding='utf-8')
    if not FINAL.exists():run(['-f','concat','-safe',0,'-i',concat,'-i',APPROVED,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',FINAL])
    cap=cv2.VideoCapture(str(FINAL));assert int(cap.get(7))==1663 and cap.get(5)==30 and cap.get(3)==1920 and cap.get(4)==1080
    indices=[60,119,120,416,417,418,425,777,778,1017,1018,1137,1138,1257,1258,1497,1498,1530,1618,1654,1662];images=[];i=0
    while True:
        ok,bgr=cap.read()
        if not ok:break
        if i in indices:images.append((i,Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB))))
        if i==1662:assert bgr.max()==0
        i+=1
    cap.release();assert i==1663
    sheet=Image.new('RGB',(1920,310*((len(images)+2)//3)),(5,11,22));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
    for j,(i,im) in enumerate(images):
        x=j%3*640;y=j//3*310;sheet.paste(im.resize((512,288),Image.Resampling.LANCZOS),(x,y+22));d.text((x+4,y),f'Frame {i} | {i/30:.3f}s',font=font,fill='white')
    sheet.save(ROOT/'previews/HD-full-boundaries-v01.jpg',quality=95)
    def audio(path):return run(['-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-']).stdout
    audio_data=audio(FINAL);assert audio_data==audio(APPROVED)
    run(['-xerror','-i',FINAL,'-f','null','-'])
    result={'status':'pending_user_review','output':str(FINAL),'frames':1663,'fps':30,'width':1920,'height':1080,'duration_seconds':1663/30,'inputs':metadata,'credits_spent_this_batch':18,'balance_before':2399,'balance_after':2381,'enhancement':'HuoShan 1080P30, normalized 1922 to 1920 wide','audio':'identical compressed audio packets to approved 480P v03','audio_sha256':hashlib.sha256(audio_data).hexdigest(),'verification':{'full_decode':'passed','sampled_temporal_alignment':'all exact frame indices','last_frame':'black','timeline':'120+298+360+240+120+120+240+165=1663'},'F':'HD E tail, existing tiny 480P avatar animation; typography rerendered at1080','AB':'approved 480P glow isolated then resized, first8 B frames'}
    (ROOT/'exports/HD-full-v01-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
