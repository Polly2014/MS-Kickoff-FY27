"""Replace only creator typography; retain approved CG, A-E, timing and audio."""
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from assemble_f_group_photo_v04 import load_animation
from assemble_f_ending_v01 import FF, ROOT, run, smooth

FINAL = ROOT/'exports/FY27-CG-intro-A-F-55p43s-480P-v03-english-credits-music.mp4'
F1080 = ROOT/'videos/SEG-F-cameos-1080P-layout-v07-english-credits-silent.mp4'
F480 = ROOT/'videos/SEG-F-cameos-480P-v07-english-credits-silent.mp4'
PREVIEW = ROOT/'previews/SEG-E-F-8p50s-v07-english-credits-music.mp4'


def main():
    credits=json.loads((ROOT/'credits-info.json').read_text(encoding='utf-8'))
    layers,rois,source_fps,_=load_animation()
    source=Image.open(ROOT/'frames/F-E-tail-background-v01.png').convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).convert('RGBA')
    alpha=np.full((1080,1920),255,np.uint8)
    alpha[-100:,:]=np.linspace(255,0,100)[:,None].astype(np.uint8)
    source.putalpha(Image.fromarray(alpha))
    overlay=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(overlay)
    for text,y,fontname,size,color in [
        (credits['ending_idea_draft'],835,'seguisb.ttf',44,(232,245,255,255)),
        ('Created by Baoli Wang · Yun Gu',910,'segoeui.ttf',32,(225,233,245,255)),
        ('AI Models: '+credits['ending_models_display'],994,'segoeui.ttf',24,(185,202,223,255)),
        ('Tools: '+credits['ending_tools_display'],1031,'segoeui.ttf',24,(185,202,223,255))]:
        font=ImageFont.truetype(str(Path('C:/Windows/Fonts')/fontname),size)
        box=draw.textbbox((0,0),text,font=font)
        draw.text(((1920-box[2]+box[0])//2,y),text,font=font,fill=color)
    if not F1080.exists():
        proc=subprocess.Popen([FF,'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24',
            '-s','1920x1080','-r','30','-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','18',
            '-pix_fmt','yuv420p','-video_track_timescale','15360','-movflags','+faststart',str(F1080)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        for i in range(165):
            t=min(i,149)/30
            frame=Image.new('RGBA',(1920,1080),(4,12,29,255))
            frame.alpha_composite(source,(0,round(-90*smooth(t/.85))))
            txt=overlay.copy();visibility=smooth((t-.75)/.6)
            txt.putalpha(txt.getchannel('A').point(lambda a:round(a*visibility)));frame.alpha_composite(txt)
            for side in range(2):
                index=min(88 if side==0 else 92,round(t*source_fps))
                im=Image.fromarray(layers[side][index]).crop(rois[side]);scale=138/im.height
                im=im.resize((round(im.width*scale),138),Image.Resampling.LANCZOS)
                frame.alpha_composite(im,(42 if side==0 else 1920-42-im.width,1080-im.height+8))
            if i>=156:
                frame.alpha_composite(Image.new('RGBA',(1920,1080),(0,0,0,round(255*min(1,(i-156)/8)))))
            if i==120:frame.convert('RGB').save(ROOT/'previews/F-v07-english-credits-1080P-layout.jpg',quality=96)
            proc.stdin.write(frame.convert('RGB').tobytes())
        proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode()
    if not F480.exists():
        run(['-i',F1080,'-vf','scale=854:480:flags=lanczos','-an','-c:v','libx264','-crf',16,'-preset','slow','-pix_fmt','yuv420p','-video_track_timescale',15360,'-movflags','+faststart',F480])
    concat=ROOT/'exports/english-credits-v03-concat.txt'
    inputs=[ROOT/'videos/INTRO-B-CG-title-large-4s-480P-v02-silent.mp4',ROOT/'exports/FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-silent.mp4',F480]
    concat.write_text(''.join(f"file '{p.as_posix()}'\n" for p in inputs),encoding='utf-8')
    old=ROOT/'exports/FY27-CG-intro-A-F-55p43s-480P-v02-large-title-music.mp4'
    if not FINAL.exists():run(['-f','concat','-safe',0,'-i',concat,'-i',old,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',FINAL])
    if not PREVIEW.exists():run(['-i',FINAL,'-ss',1498/30-3,'-t',8.5,'-c:v','libx264','-crf',17,'-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',PREVIEW])
    cap=cv2.VideoCapture(str(FINAL));assert int(cap.get(7))==1663 and cap.get(5)==30;cap.release()
    def audio(path):return run(['-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-']).stdout
    assert audio(old)==audio(FINAL)
    run(['-xerror','-i',FINAL,'-f','null','-'])
    result={'output':str(FINAL),'preview':str(PREVIEW),'frames':1663,'fps':30,'duration_seconds':1663/30,
        'creator_line':'Created by Baoli Wang · Yun Gu','audio':'identical compressed packets to approved v02','credits_spent':0}
    (ROOT/'exports/english-credits-v03-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
