"""Compare a beam-led hard cut with a brief light-only carryover onto existing B."""
import json
import subprocess
import tempfile
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
a=root/'videos'/'SEG-A-Wan3-480P-v07-adopted.mp4'
b=root/'videos'/'SEG-B-Wan3-480P-v08-adopted.mp4'
music=root/'music'/'MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
cut=298  # First Feng image in original A: all A footage from this frame onward is removed.

def get(path,index):
    c=cv2.VideoCapture(str(path));c.set(1,index);ok,f=c.read();c.release();assert ok,(path,index)
    return f

baseline=get(a,318).astype(np.float32)
clean_frames=[get(a,i) for i in range(cut-60,cut)]+[get(b,i) for i in range(60)]
light_frames=[f.copy() for f in clean_frames]
light_checks=[]
for i in range(8):
    donor=get(a,cut+i).astype(np.float32)
    # Vertical high-pass isolates the thin luminous line, excluding broad lighting patches.
    background=cv2.GaussianBlur(donor,(0,0),sigmaX=1,sigmaY=7)
    delta=np.maximum(donor-background,0)
    mask=np.zeros((480,854),np.float32)
    # The donor beam occupies the empty area left of Feng. Exclude all actors and floor.
    cyan=(donor[:,:,0]>donor[:,:,2]+25)&(donor[:,:,1]>donor[:,:,2]+20)
    energy=(delta[:,:,0]>5)&(delta[:,:,1]>5)
    mask[130:270,:330]=(cyan&energy)[130:270,:330]
    mask=cv2.GaussianBlur(mask,(0,0),0.65)
    weight=(1-i/8)
    glow=delta*mask[:,:,None]*weight
    target=clean_frames[60+i].astype(np.float32)
    composite=np.clip(target+glow,0,255).astype(np.uint8)
    light_frames[60+i]=composite
    light_checks.append(dict(b_frame=i,donor_a_frame=cut+i,affected_pixels=int(np.any(composite!=target.astype(np.uint8),axis=2).sum())))

def export(frames,path):
    if path.exists():
        raise FileExistsError(path)
    with tempfile.TemporaryDirectory(prefix='fy27-ab-beam-') as td:
        silent=Path(td)/'silent.mp4'
        cmd=[ffmpeg,'-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','bgr24',
             '-s','854x480','-r','30','-i','-','-an','-c:v','libx264','-crf','16',
             '-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        for frame in frames:proc.stdin.write(frame.tobytes())
        proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode()
        start=(cut-60)/30;end=start+4
        subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(silent),'-i',str(music),
            '-map','0:v:0','-map','1:a:0','-c:v','copy',
            '-af',f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,volume=-4dB',
            '-c:a','aac','-b:a','256k','-t','4','-movflags','+faststart',str(path)],check=True)
    c=cv2.VideoCapture(str(path));assert int(c.get(7))==120 and c.get(5)==30;c.release()

clean=root/'previews'/'SEG-AB-beam-relay-v01-clean-cut-music.mp4'
light=root/'previews'/'SEG-AB-beam-relay-v03-light-carry-music.mp4'
if not clean.exists():export(clean_frames,clean)
export(light_frames,light)
sheet=Image.new('RGB',(3*600,2*364),'#17191d');d=ImageDraw.Draw(sheet)
for j,(frame,label) in enumerate([(clean_frames[59],'A last beam-only frame 9.900s'),
                                (clean_frames[60],'B first frame | clean cut'),
                                (light_frames[60],'B first frame | light carry'),
                                (light_frames[62],'B 0.067s | light carry'),
                                (light_frames[65],'B 0.167s | fading'),
                                (light_frames[68],'B 0.267s | original image')]):
    im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));im.thumbnail((596,335))
    x=j%3*600;y=j//3*364;d.text((x+4,y+5),label,fill='white');sheet.paste(im,(x,y+25))
sheet.save(root/'previews'/'SEG-AB-beam-relay-comparison.jpg',quality=95)
manifest=dict(status='preview_only_pending_review',a_source='SEG-A-Wan3-480P-v07-adopted.mp4',
              proposed_a_frames=[0,cut],proposed_a_seconds=[0,cut/30],b_source=b.name,b_start_frame=0,
              previews=dict(clean=clean.name,light_carry=light.name,cut_seconds=2),
              light=dict(method='Vertical high-pass cyan-light extraction from original A, restricted to empty left-side ROI; added to first 8 B frames and faded',
                         donor_frames=[298,306],roi_xyxy=[0,130,330,270],checks=light_checks),
              credit_cost=0,note='Original media unchanged. No A footage showing Feng retained as a full frame. New rejected A08 is unused.')
(root/'SEG-AB-beam-relay-preview.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
