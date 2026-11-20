"""Local optional polish: larger first title, one glyph sweep, three quiet relay cues."""
import json
import wave
import hashlib
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from assemble_f_ending_v01 import ROOT, run, smooth
from assemble_full_hd_v01 import encoder, finish

BASE=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-HuoShan-v01-music.mp4'
TITLE_ONLY=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v02-title-polish-music.mp4'
FINAL=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v03-title-relay-sfx-music.mp4'
INTRO=ROOT/'videos/HD-edit-INTRO-1080P30-v02-title-polish-silent.mp4'
SR=44100
# Times follow the visible beam, not a blanket effect on every edit.
CUES=[{'name':'AB','start':13.22,'duration':.88,'pan':[-.65,.50],'seed':27},
      {'name':'BC','start':25.39,'duration':.83,'pan':[.50,-.45],'seed':28},
      {'name':'CD','start':33.22,'duration':.62,'pan':[.40,-.35],'seed':29}]


def typography():
    text=Image.new('RGBA',(1920,1080));draw=ImageDraw.Draw(text)
    for label,y,size in [('STCA M365 Copilot',361,100),('Foundation & Platform Team',485,66)]:
        font=ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',size)
        box=draw.textbbox((0,0),label,font=font);assert box[2]-box[0]<1700
        draw.text(((1920-(box[2]-box[0]))//2,y),label,font=font,fill=(237,251,255,255),stroke_width=1,stroke_fill=(3,14,30,200))
    glow=Image.new('RGBA',text.size,(45,200,255,0))
    glow.putalpha(text.getchannel('A').filter(ImageFilter.GaussianBlur(10)).point(lambda a:round(a*.45)))
    glow.alpha_composite(text)
    # Crop the effect to glyphs: one moving cyan highlight, no line across the scene.
    return glow,np.asarray(text.getchannel('A'),dtype=np.float32)


def render_intro():
    if INTRO.exists():return
    title,alpha=typography();xx=np.arange(1920,dtype=np.float32)[None,:]
    cap=cv2.VideoCapture(str(ROOT/'videos/INTRO-CG-HuoShan-1080P30-HD-v01.mp4'));p=encoder(INTRO)
    for i in range(120):
        ok,bgr=cap.read();assert ok
        frame=Image.fromarray(cv2.cvtColor(cv2.resize(bgr,(1920,1080),interpolation=cv2.INTER_LANCZOS4),cv2.COLOR_BGR2RGB)).convert('RGBA')
        t=i/30;visibility=smooth((t-.65)/.3)*(1-smooth((t-3.1)/.3))
        overlay=title.copy();overlay.putalpha(overlay.getchannel('A').point(lambda a:round(a*visibility)));frame.alpha_composite(overlay)
        if .97<=t<=1.62:
            u=(t-.97)/.65;center=350+1220*u
            intensity=np.exp(-.5*((xx-center)/95)**2)*np.sin(np.pi*u)*.48*visibility
            sweep=Image.new('RGBA',(1920,1080),(135,239,255,0))
            sweep.putalpha(Image.fromarray(np.uint8(np.clip(alpha*intensity,0,255))))
            soft=Image.new('RGBA',frame.size,(40,200,255,0));soft.putalpha(sweep.getchannel('A').filter(ImageFilter.GaussianBlur(5)));frame.alpha_composite(soft);frame.alpha_composite(sweep)
        if i in (30,39,48,60):frame.convert('RGB').save(ROOT/f'previews/INTRO-polish-v02-frame-{i:03}.jpg',quality=96)
        p.stdin.write(frame.convert('RGB').tobytes())
    cap.release();finish(p)


def decode_audio(path):
    return np.frombuffer(run(['-i',path,'-vn','-ar',SR,'-ac',2,'-f','f32le','-']).stdout,dtype='<f4').reshape(-1,2).copy()


def whoosh(cue):
    n=round(SR*cue['duration']);t=np.arange(n)/SR;u=t/cue['duration'];rng=np.random.default_rng(cue['seed'])
    noise=rng.standard_normal(n)
    freq=np.fft.rfftfreq(n,1/SR);spectrum=np.fft.rfft(noise)
    def band(lo,hi):
        filt=(1-np.exp(-(freq/lo)**4))*np.exp(-(freq/hi)**4)
        a=np.fft.irfft(spectrum*filt,n);return a/(np.std(a)+1e-10)
    low,high=band(350,1600),band(1100,5200)
    # Smooth airflow rises and falls; tiny warm pulse anchors the passing light.
    envelope=np.sin(np.pi*u)**1.7
    noise=(low*(1-u)+high*u)*envelope
    pulse_start=cue['duration']*.48;pt=np.maximum(t-pulse_start,0)
    pulse=np.sin(2*np.pi*(710*pt-180*pt**2))*np.exp(-pt/0.055)*(t>=pulse_start)
    mono=.90*noise+.15*pulse
    mono/=max(np.max(np.abs(mono)),1e-9)
    pan=cue['pan'][0]+(cue['pan'][1]-cue['pan'][0])*smooth_array(u)
    return np.stack([mono*np.cos((pan+1)*np.pi/4),mono*np.sin((pan+1)*np.pi/4)],axis=1)


def smooth_array(x):return x*x*(3-2*x)


def save_wav(path,audio):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(np.int16(np.clip(audio,-1,1)*32767).tobytes())


def main():
    render_intro()
    parts=[INTRO]+[ROOT/f'videos/HD-edit-{s}-1080P30-v01-silent.mp4' for s in ['A','B','C','D08','D13','E','F']]
    concat=ROOT/'exports/HD-title-polish-v02-concat.txt';concat.write_text(''.join(f"file '{p.as_posix()}'\n" for p in parts),encoding='utf-8')
    if not TITLE_ONLY.exists():run(['-f','concat','-safe',0,'-i',concat,'-i',BASE,'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',TITLE_ONLY])
    original=decode_audio(BASE);sfx=np.zeros_like(original);levels=[]
    for cue in CUES:
        effect=whoosh(cue);start=round(cue['start']*SR);end=start+len(effect)
        local_rms=float(np.sqrt(np.mean(original[start:end]**2)))
        effect_rms=float(np.sqrt(np.mean(effect**2)))
        gain=min(.065,local_rms*.30/max(effect_rms,1e-9))
        effect*=gain;sfx[start:end]+=effect
        levels.append(dict(cue,peak=float(np.max(np.abs(effect))),relative_rms_db=float(20*np.log10(np.sqrt(np.mean(effect**2))/local_rms))))
    mixed=original+sfx
    assert np.max(np.abs(mixed))<.99,'Do not change music globally to accommodate SFX'
    assert np.array_equal(mixed[:4*SR],original[:4*SR])
    assert not np.any(sfx[:13*SR]) and not np.any(sfx[34*SR:])
    stem=ROOT/'audio/SFX-three-relays-local-v01.wav';mix=ROOT/'audio/MIX-HD-title-relay-sfx-v01.wav'
    save_wav(stem,sfx);save_wav(mix,mixed)
    if not FINAL.exists():run(['-i',TITLE_ONLY,'-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',SR,'-t',1663/30,'-movflags','+faststart',FINAL])
    # Intro-only and three-cut preview, preserving HD frame boundaries.
    preview=ROOT/'previews/INTRO-polish-v02-first9s-music.mp4'
    if not preview.exists():run(['-i',FINAL,'-t',9,'-c','copy','-movflags','+faststart',preview])
    relay=ROOT/'previews/HD-three-relays-v03-sfx-review.mp4'
    if not relay.exists():
        filt=';'.join(f'[0:v]trim=start={t}:duration=2,setpts=PTS-STARTPTS[v{i}];[0:a]atrim=start={t}:duration=2,asetpts=PTS-STARTPTS[a{i}]' for i,t in enumerate([12.7,24.8,32.7]))
        filt+=';[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]'
        run(['-i',FINAL,'-filter_complex',filt,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf',18,'-c:a','aac','-b:a','256k','-movflags','+faststart',relay])
    run(['-xerror','-i',FINAL,'-f','null','-'])
    def stream(path,kind,fmt):return run(['-i',path,'-map',kind,'-c','copy','-f',fmt,'-']).stdout
    assert stream(TITLE_ONLY,'0:a:0','adts')==stream(BASE,'0:a:0','adts')
    assert stream(TITLE_ONLY,'0:v:0','h264')==stream(FINAL,'0:v:0','h264')
    a=cv2.VideoCapture(str(BASE));b=cv2.VideoCapture(str(FINAL));assert b.get(7)==1663 and b.get(5)==30 and b.get(3)==1920 and b.get(4)==1080
    for i in range(1663):
        oka,fa=a.read();okb,fb=b.read();assert oka and okb
        if i>=120:assert np.array_equal(fa,fb),i
    a.release();b.release()
    decoded=decode_audio(FINAL);n=min(len(original),len(decoded));intro_error=float(np.sqrt(np.mean((decoded[:4*SR]-original[:4*SR])**2)))
    assert intro_error<.01,intro_error
    result={'status':'pending_user_review','output':str(FINAL),'title_only_original_audio':str(TITLE_ONLY),'intro_preview':str(preview),'sfx_preview':str(relay),'frames':1663,'fps':30,'duration_seconds':1663/30,'title_sizes':[100,66],'previous_title_sizes':[91,66],'title_effect':'one cyan glyph-limited sweep .97-1.62s, no added intro audio','cues':levels,'sfx_stem':str(stem),'mix_peak':float(np.max(np.abs(mixed))),'intro_reencode_rmse':intro_error,'verification':{'full_decode':'passed','body_frames_after_intro':'all1543frames pixel identical to approvedHD','title_only_audio':'identical compressed packets to approvedHD','intro_sound':'original PCM unchanged before AAC encode, no added cue before13.22s','ending_sound':'no added cue after33.84s, original music tail and fade retained'},'credits_spent':0}
    (ROOT/'exports/HD-polish-v03-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
