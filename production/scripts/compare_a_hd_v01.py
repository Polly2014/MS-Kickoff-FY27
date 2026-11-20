"""Align downloaded enhancement outputs and produce equal-scale comparison media."""
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from assemble_f_ending_v01 import ROOT,run

PATHS=[ROOT/'videos/SEG-A-Wan3-480P-v07-adopted.mp4',ROOT/'videos/SEG-A-v07-HuoShan-1080P30-HD-v01.mp4',ROOT/'videos/SEG-A-v07-Topazlabs-1080P30-HD-v01.mp4']
LABELS=['Original 480P (Lanczos to 1080)','HuoShan 1080P | 4 credits','Topazlabs 1080P | 48 credits']
POINTS=[9,39,120,222,279,330]

def main():
    samples=[];small=[];meta=[]
    for path in PATHS:
        cap=cv2.VideoCapture(str(path));m={'path':str(path),'width':int(cap.get(3)),'height':int(cap.get(4)),'fps':cap.get(5),'frames':int(cap.get(7))}
        frames={};tiny=[];i=0
        while True:
            ok,bgr=cap.read()
            if not ok:break
            if i in POINTS:
                frames[i]=Image.fromarray(cv2.cvtColor(cv2.resize(bgr,(1920,1080),interpolation=cv2.INTER_LANCZOS4),cv2.COLOR_BGR2RGB))
            tiny.append(cv2.resize(cv2.cvtColor(bgr,cv2.COLOR_BGR2GRAY),(320,180),interpolation=cv2.INTER_AREA))
            i+=1
        cap.release();assert i==360 and m['fps']==30
        samples.append(frames);small.append(tiny);meta.append(m)
    # Check nearest temporal matches rather than assuming enhancement preserves frame order.
    matches={}
    for model in (1,2):
        result=[]
        for i in POINTS:
            distances={j:float(np.mean(np.abs(small[0][i].astype(np.float32)-small[model][j].astype(np.float32)))) for j in range(max(0,i-3),min(360,i+4))}
            result.append({'source_frame':i,'best_output_frame':min(distances,key=distances.get),'mae_by_frame':distances})
        matches[LABELS[model]]=result
        assert all(r['source_frame']==r['best_output_frame'] for r in result),result
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
    sheet=Image.new('RGB',(1920,400*len(POINTS)),(5,11,22));d=ImageDraw.Draw(sheet)
    for row,i in enumerate(POINTS):
        for col in range(3):
            sheet.paste(samples[col][i].resize((640,360),Image.Resampling.LANCZOS),(col*640,row*400+40))
            d.text((col*640+12,row*400+5),f'{LABELS[col]}  t={i/30:.2f}s',font=font,fill='white')
    sheet.save(ROOT/'previews/HD-A-three-way-contact-v01.jpg',quality=96)
    for i in (39,222,330):
        # Same central crop at native output scale; do not sharpen any panel locally.
        boxes={39:(640,180,1280,820),222:(590,280,1230,920),330:(670,200,1310,840)}
        crop=Image.new('RGB',(1920,690),(5,11,22));dc=ImageDraw.Draw(crop)
        for col in range(3):
            crop.paste(samples[col][i].crop(boxes[i]),(col*640,50))
            dc.text((col*640+10,9),LABELS[col],font=font,fill='white')
        crop.save(ROOT/f'previews/HD-A-detail-frame-{i:03}-v01.jpg',quality=98)
    out=ROOT/'previews/HD-A-HuoShan-vs-Topaz-12s-side-by-side-v01.mp4'
    if not out.exists():
        run(['-i',PATHS[1],'-i',PATHS[2],'-filter_complex',
            "[0:v]scale=960:540:flags=lanczos,pad=960:580:0:40:color=0x050b16,drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':text='HuoShan 1080P - 4 credits':x=20:y=8:fontsize=24:fontcolor=white[l];"
            "[1:v]scale=960:540:flags=lanczos,pad=960:580:0:40:color=0x050b16,drawtext=fontfile='C\\:/Windows/Fonts/segoeui.ttf':text='Topazlabs 1080P - 48 credits':x=20:y=8:fontsize=24:fontcolor=white[r];[l][r]hstack=inputs=2[v]",
            '-map','[v]','-an','-frames:v',360,'-r',30,'-c:v','libx264','-preset','fast','-crf',17,'-pix_fmt','yuv420p','-movflags','+faststart',out])
    run(['-xerror','-i',out,'-f','null','-'])
    manifest={'sources':meta,'temporal_alignment':matches,'comparison':str(out),'contact_sheet':'previews/HD-A-three-way-contact-v01.jpg','normalization':'all full images resized to 1920x1080 with Lanczos; HuoShan width 1922 normalized to1920','credits_spent':52,'balance_before':2451,'balance_after':2399}
    (ROOT/'exports/HD-A-comparison-v01.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
