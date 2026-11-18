"""Deterministic 2D reveal PREVIS from one master. No video/image model calls."""
from pathlib import Path
import json
import subprocess
import hashlib
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

BASE=Path(__file__).resolve().parent

def main():
    data=json.loads((BASE/'preparation-manifest.json').read_text(encoding='utf-8'))
    source=BASE/data['assets']['GROUP_MASTER']['path']
    im=Image.open(source).convert('RGB')
    if im.size!=(3840,2160):raise SystemExit('Recheck crop coordinates for a different master resolution')
    rect=(1550,850,3470,1930)
    crop=BASE/'frames/GROUP_LOCAL-exact-crop-v01.png'
    if not crop.exists():im.crop(rect).save(crop)
    out=BASE/'previews/E1-reveal-2D-PREVIS-v01.mp4'
    if out.exists():raise SystemExit('Refusing to overwrite preview: '+str(out))
    command=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-n',
        '-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-',
        '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',30)
    for i in range(120):
        u=i/119;s=u*u*(3-2*u)
        x=1550*(1-s);y=850*(1-s);w=1920+1920*s;h=1080+1080*s
        frame=im.crop((round(x),round(y),round(x+w),round(y+h))).resize((1920,1080),Image.Resampling.LANCZOS)
        d=ImageDraw.Draw(frame);d.rectangle((20,18,800,72),fill='#081426')
        d.text((34,25),'二维拉远预演 · 静态人物 · 非最终视频',font=font,fill='white')
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait()!=0:raise SystemExit('ffmpeg failed')
    (BASE/'previews/reveal-2D-derivation.json').write_text(json.dumps(dict(
        source=str(source.relative_to(BASE)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        exact_crop=str(crop.relative_to(BASE)),crop_xyxy=rect,source_size=list(im.size),
        preview=str(out.relative_to(BASE)),preview_size=[1920,1080],fps=30,frames=120,
        note='Same pixels, smooth 2D crop pullout. Static people; not AI video, not a 3D camera move, not final.'),indent=2)+'\n',encoding='utf-8')
    print(out)

if __name__=='__main__':main()
