"""Cut A on Feng's first dip, then join B-E with continuous approved music."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
videos, exports = root/'videos', root/'exports'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
original_a = videos/'SEG-A-Wan3-480P-v07-adopted.mp4'
trimmed_a = videos/'SEG-A-Wan3-480P-v02-edit-first-dip-10p5s.mp4'
silent = exports/'FY27-A-E-46p5s-480P-roughcut-v02-silent.mp4'
output = exports/'FY27-A-E-46p5s-480P-roughcut-v02-music.mp4'
preview = root/'previews'/'SEG-AB-v02-first-dip-junction-music.mp4'
music = root/'music'/'MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
parts = [
    ('A', trimmed_a, 315),
    ('B', videos/'SEG-B-Wan3-480P-v08-adopted.mp4', 360),
    ('C', videos/'SEG-C-Wan3-480P-v08-adopted.mp4', 240),
    ('D', videos/'SEG-D-Wan3-480P-v14-edit-v08first4s-v13last4s.mp4', 240),
    ('E', videos/'SEG-E-Wan3-480P-v08-adopted.mp4', 240),
]

def run(args):
    return subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-n',*args],check=True,capture_output=True)

def frame(path,index):
    c=cv2.VideoCapture(str(path)); c.set(cv2.CAP_PROP_POS_FRAMES,index)
    ok,f=c.read(); c.release(); assert ok,(path,index)
    return f

def info(path):
    c=cv2.VideoCapture(str(path))
    result=dict(file=path.name,frames=int(c.get(cv2.CAP_PROP_FRAME_COUNT)),fps=c.get(cv2.CAP_PROP_FPS),
                size=[int(c.get(cv2.CAP_PROP_FRAME_WIDTH)),int(c.get(cv2.CAP_PROP_FRAME_HEIGHT))])
    c.release();result['seconds']=result['frames']/result['fps']
    return result

if not trimmed_a.exists():
    run(['-i',str(original_a),'-vf','trim=start_frame=0:end_frame=315,setpts=N/(30*TB)',
         '-an','-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',
         '-r','30','-fps_mode','cfr','-video_track_timescale','15360','-movflags','+faststart',str(trimmed_a)])
timeline=[];offset=0
for label,path,count in parts:
    meta=info(path)
    assert meta['frames']==count and meta['fps']==30 and meta['size']==[854,480],meta
    timeline.append(dict(segment=label,start=offset/30,end=(offset+count)/30,file=path.name))
    offset+=count
concat=exports/'FY27-A-E-v02-concat.txt'
concat.write_text(''.join(f"file '../videos/{path.name}'\n" for _,path,_ in parts),encoding='utf-8')
if not silent.exists():
    run(['-f','concat','-safe','0','-i',str(concat),'-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(silent)])
if not output.exists():
    run(['-i',str(silent),'-i',str(music),'-map','0:v:0','-map','1:a:0','-c:v','copy',
         '-af','atrim=start=0:end=46.5,asetpts=PTS-STARTPTS,volume=-4dB,afade=t=out:st=45.8:d=0.7',
         '-c:a','aac','-b:a','256k','-ar','44100','-t','46.5','-movflags','+faststart',str(output)])
if not preview.exists():
    run(['-i',str(output),'-vf','trim=start_frame=255:end_frame=375,setpts=N/(30*TB)',
         '-af','atrim=start=8.5:end=12.5,asetpts=PTS-STARTPTS',
         '-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',
         '-r','30','-fps_mode','cfr','-c:a','aac','-b:a','256k','-t','4','-movflags','+faststart',str(preview)])
meta=info(output)
assert meta['frames']==1395 and meta['fps']==30 and meta['seconds']==46.5,meta
assert info(preview)['frames']==120 and info(preview)['seconds']==4
run(['-xerror','-i',str(output),'-f','null','-'])
checks=[];offset=0
for label,path,count in parts:
    for idx in [0,count-1]:
        assert np.array_equal(frame(output,offset+idx),frame(path,idx)),(label,idx)
        checks.append(dict(segment=label,output_frame=offset+idx,source_frame=idx,exact_pixels=True))
    offset+=count
psnr=[float(cv2.PSNR(frame(trimmed_a,i),frame(original_a,i))) for i in [0,300,314]]
assert min(psnr)>35,psnr
raw=run(['-i',str(output),'-vn','-ac','2','-ar','44100','-f','f32le','-']).stdout
audio=np.frombuffer(raw,dtype='<f4').reshape(-1,2)
assert abs(len(audio)/44100-46.5)<.03 and np.max(np.abs(audio))<1

sheet=Image.new('RGB',(4*427,270),'#17191d');draw=ImageDraw.Draw(sheet)
for col,(idx,label) in enumerate([(309,'A 10.300s'),(314,'A 10.467s | last'),(315,'B 0.000s | first'),(324,'B 0.300s')]):
    im=Image.fromarray(cv2.cvtColor(frame(output,idx),cv2.COLOR_BGR2RGB));im.thumbnail((423,238))
    draw.text((col*427+4,5),label,fill='white');sheet.paste(im,(col*427,27))
sheet.save(root/'previews'/'SEG-AB-v02-first-dip-result.jpg',quality=95)
manifest=dict(output=meta,timeline=timeline,edit=dict(a_source_frames=[0,315],a_source_seconds=[0,10.5],
              removed_a_seconds=[10.5,12],b_source_start=0,reason='Cut during the first descent before A rebounds and dips again'),
              video='Only A trim re-encoded at CRF16; B-E stream copied; no speed changes or dissolves',
              audio=dict(source=music.name,range=[0,46.5],continuous=True,gain_db=-4,fade_out=[45.8,46.5],
                         decoded_seconds=len(audio)/44100,peak=float(np.max(np.abs(audio)))),
              preview=preview.name,verification=dict(full_decode='passed',frame_matches=checks,a_encode_psnr=psnr),
              credit_cost=0)
(exports/'FY27-A-E-roughcut-v02-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
