"""Adopt the approved beam carryover in the full A-E music review cut."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

root=Path(__file__).resolve().parents[1]
videos=root/'videos';exports=root/'exports';ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
a=videos/'SEG-A-Wan3-480P-v07-adopted.mp4'
b=videos/'SEG-B-Wan3-480P-v08-adopted.mp4'
ab=videos/'SEG-AB-v03-beam-relay-21p93s.mp4'
silent=exports/'FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-silent.mp4'
output=exports/'FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-music.mp4'
music=root/'music'/'MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
total_frames=1378;duration=total_frames/30

def run(args):
    return subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-n',*args],check=True,capture_output=True)

def frame(path,index):
    c=cv2.VideoCapture(str(path));c.set(1,index);ok,f=c.read();c.release();assert ok,(path,index)
    return f

glows=[]
for i in range(8):
    donor=frame(a,298+i).astype(np.float32)
    delta=np.maximum(donor-cv2.GaussianBlur(donor,(0,0),sigmaX=1,sigmaY=7),0)
    cyan=(donor[:,:,0]>donor[:,:,2]+25)&(donor[:,:,1]>donor[:,:,2]+20)
    energy=(delta[:,:,0]>5)&(delta[:,:,1]>5)
    mask=np.zeros((480,854),np.float32);mask[130:270,:330]=(cyan&energy)[130:270,:330]
    mask=cv2.GaussianBlur(mask,(0,0),0.65)
    glows.append(delta*mask[:,:,None]*(1-i/8))

if not ab.exists():
    proc=subprocess.Popen([ffmpeg,'-hide_banner','-loglevel','error','-n',
        '-f','rawvideo','-pix_fmt','bgr24','-s','854x480','-r','30','-i','-',
        '-an','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',
        '-video_track_timescale','15360','-movflags','+faststart',str(ab)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for path,count,apply_light in [(a,298,False),(b,360,True)]:
        cap=cv2.VideoCapture(str(path))
        for i in range(count):
            ok,f=cap.read();assert ok,(path,i)
            if apply_light and i<8:
                f=np.clip(f.astype(np.float32)+glows[i],0,255).astype(np.uint8)
            proc.stdin.write(f.tobytes())
        cap.release()
    proc.stdin.close();err=proc.stderr.read();assert proc.wait()==0,err.decode()

parts=[(ab,658),
       (videos/'SEG-C-Wan3-480P-v08-adopted.mp4',240),
       (videos/'SEG-D-Wan3-480P-v14-edit-v08first4s-v13last4s.mp4',240),
       (videos/'SEG-E-Wan3-480P-v08-adopted.mp4',240)]
concat=exports/'FY27-A-E-v03-beam-relay-concat.txt'
concat.write_text(''.join(f"file '../videos/{p.name}'\n" for p,_ in parts),encoding='utf-8')
if not silent.exists():
    run(['-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)])
if not output.exists():
    run(['-i',str(silent),'-i',str(music),'-map','0:v:0','-map','1:a:0','-c:v','copy',
         '-af',f'atrim=start=0:end={duration},asetpts=PTS-STARTPTS,volume=-4dB,afade=t=out:st={duration-.7}:d=0.7',
         '-c:a','aac','-b:a','256k','-ar','44100','-t',str(duration),'-movflags','+faststart',str(output)])
cap=cv2.VideoCapture(str(output));n=int(cap.get(7));fps=cap.get(5);cap.release()
assert n==total_frames and fps==30,(n,fps)
run(['-xerror','-i',str(output),'-f','null','-'])
checks=[]
approved=root/'previews'/'SEG-AB-beam-relay-v03-light-carry-music.mp4'
for out_idx,preview_idx in [(297,59),(298,60),(302,64),(306,68)]:
    value=float(cv2.PSNR(frame(output,out_idx),frame(approved,preview_idx)))
    assert value>35,(out_idx,value)
    checks.append(dict(output_frame=out_idx,approved_preview_frame=preview_idx,psnr=value))
offset=658
for path,count in parts[1:]:
    for idx in [0,count-1]:assert np.array_equal(frame(output,offset+idx),frame(path,idx)),(path,idx)
    offset+=count
raw=run(['-i',str(output),'-vn','-ac','2','-ar','44100','-f','f32le','-']).stdout
audio=np.frombuffer(raw,dtype='<f4');assert np.max(np.abs(audio))<1
assert abs(len(audio)/2/44100-duration)<.03
timeline=[];offset=0
for label,count in [('A',298),('B',360),('C',240),('D',240),('E',240)]:
    timeline.append(dict(segment=label,start=offset/30,end=(offset+count)/30));offset+=count
manifest=dict(status='approved_AB_transition_integrated',output=output.name,frames=n,fps=fps,duration=duration,
              timeline=timeline,a_source_frames=[0,298],b_source_frames=[0,360],light_b_frames=[0,8],
              video='AB encoded once at CRF16 with approved light carryover; CDE stream copied unchanged',
              audio=dict(source=music.name,range=[0,duration],continuous=True,gain_db=-4,fade_out=[duration-.7,duration],
                         decoded_peak=float(np.max(np.abs(audio)))),
              verification=dict(full_decode='passed',approved_preview_checks=checks,CDE_source_boundaries='exact pixels'),
              credit_cost=0)
(exports/'FY27-A-E-roughcut-v03-beam-relay-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
record=root/'SEG-AB-beam-relay-preview.json'
d=json.loads(record.read_text(encoding='utf-8'));d['status']='light_carry_approved_by_user';d['integrated_export']=output.name
record.write_text(json.dumps(d,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
