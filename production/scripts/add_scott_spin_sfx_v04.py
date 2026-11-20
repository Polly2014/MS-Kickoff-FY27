"""One soft body-spin cue over the approved D solo; stream-copy approved picture."""
import json
import wave
import hashlib
import cv2
import numpy as np
from assemble_f_ending_v01 import ROOT, run
from polish_title_transition_sfx_v02 import decode_audio, save_wav, SR

BASE=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v03-title-relay-sfx-music.mp4'
FINAL=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v04-scott-spin-sfx-music.mp4'
PREVIEW=ROOT/'previews/Scott-spin-v04-sfx-5p5s-review.mp4'
START,END=34.30,37.12


def spin_sound():
    n=round((END-START)*SR);t=np.arange(n)/SR;u=np.arange(n)/n
    rng=np.random.default_rng(20271120);freq=np.fft.rfftfreq(n,1/SR)
    spectrum=np.fft.rfft(rng.standard_normal(n))
    def band(lo,hi):
        weight=(1-np.exp(-(freq/lo)**4))*np.exp(-(freq/hi)**4)
        noise=np.fft.irfft(spectrum*weight,n)
        return noise/(np.std(noise)+1e-12)
    warm,air=band(190,1050),band(480,2350)
    # One continuous rise and fall, with a quiet revolving texture, no hit/laser tone.
    envelope=np.sin(np.pi*u)**1.35
    texture=.87+.13*np.sin(2*np.pi*(1.15*t+.12*t*t))
    brightness=np.sin(np.pi*u)**.8
    mono=(.76*warm+.24*air*brightness)*envelope*texture
    mono/=np.max(np.abs(mono))
    pan=.30*np.sin(2*np.pi*(u-.18))
    stereo=np.stack([mono*np.cos((pan+1)*np.pi/4),mono*np.sin((pan+1)*np.pi/4)],axis=1)
    return stereo


def main():
    # Start from the original uncompressed v03 mix, avoiding cumulative AAC loss.
    mix_source=ROOT/'audio/MIX-HD-title-relay-sfx-v01.wav'
    with wave.open(str(mix_source),'rb') as f:
        assert f.getframerate()==SR and f.getnchannels()==2 and f.getsampwidth()==2
        original=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
    cue=spin_sound();a=round(START*SR);b=a+len(cue)
    music_rms=float(np.sqrt(np.mean(original[a:b]**2)));cue_rms=float(np.sqrt(np.mean(cue**2)))
    gain=min(.070,music_rms*.10/cue_rms);cue*=gain
    sfx=np.zeros_like(original);sfx[a:b]=cue;mixed=original+sfx
    assert np.max(np.abs(mixed))<.99
    assert np.array_equal(mixed[:a],original[:a]) and np.array_equal(mixed[b:],original[b:])
    stem=ROOT/'audio/SFX-Scott-single-spin-v01.wav';mix=ROOT/'audio/MIX-HD-scott-spin-v04.wav'
    save_wav(stem,sfx);save_wav(mix,mixed)
    if not FINAL.exists():
        run(['-i',BASE,'-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',SR,'-t',1663/30,'-movflags','+faststart',FINAL])
    if not PREVIEW.exists():
        run(['-i',FINAL,'-ss',33.5,'-t',5.5,'-c:v','libx264','-preset','fast','-crf',18,'-c:a','aac','-b:a','256k','-movflags','+faststart',PREVIEW])
    def picture(path):return run(['-i',path,'-map','0:v:0','-c:v','copy','-f','h264','-']).stdout
    before,after=picture(BASE),picture(FINAL);assert before==after
    run(['-xerror','-i',FINAL,'-f','null','-'])
    cap=cv2.VideoCapture(str(FINAL));assert cap.get(7)==1663 and cap.get(5)==30 and cap.get(3)==1920 and cap.get(4)==1080;cap.release()
    decoded=decode_audio(FINAL);old_decoded=decode_audio(BASE);n=min(len(decoded),len(old_decoded))
    outside=np.ones(n,dtype=bool);outside[max(0,a-4096):min(n,b+4096)]=False
    outside_rmse=float(np.sqrt(np.mean((decoded[:n][outside]-old_decoded[:n][outside])**2)))
    assert outside_rmse<.01,outside_rmse
    result={'status':'pending_user_review','output':str(FINAL),'preview':str(PREVIEW),'frames':1663,'fps':30,'duration_seconds':1663/30,'cue':{'segment':'D v08 solo, floor spin','start_seconds':START,'end_seconds':END,'sound':'one warm airflow swell, subtle rotating stereo texture, no impact','peak':float(np.max(np.abs(cue))),'relative_music_rms_db':float(20*np.log10(np.sqrt(np.mean(cue**2))/music_rms))},'sfx_stem':str(stem),'mix_source':str(mix_source),'mix_peak':float(np.max(np.abs(mixed))),'verification':{'video_stream':'byte-identical to approved v03','video_sha256':hashlib.sha256(after).hexdigest(),'full_decode':'passed','outside_cue_PCM':'unchanged before quantization and AAC encode','outside_cue_AAC_rmse':outside_rmse},'credits_spent':0}
    (ROOT/'exports/HD-scott-spin-v04-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
