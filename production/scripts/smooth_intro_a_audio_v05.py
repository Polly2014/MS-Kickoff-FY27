"""Carry a short diffuse tail from existing CG sound across the 4s picture cut."""
import json
import wave
import hashlib
import numpy as np
import cv2
from assemble_f_ending_v01 import ROOT, run
from polish_title_transition_sfx_v02 import decode_audio, save_wav, SR

BASE=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v04-scott-spin-sfx-music.mp4'
FINAL=ROOT/'exports/FY27-CG-intro-A-F-55p43s-1080P-v05-intro-a-audio-bridge-music.mp4'
PREVIEW=ROOT/'previews/INTRO-A-v05-audio-bridge-6s-review.mp4'
COMPARE=ROOT/'previews/INTRO-A-v04-v05-audio-bridge-before-after-6s.mp4'


def smooth_array(x):
    x=np.clip(x,0,1)
    return x*x*(3-2*x)


def bridge(total_samples):
    source=decode_audio(ROOT/'videos/INTRO-B-CG-ignite-4s-Wan3-480P-v01-source.mp4')
    # Unfaded CG source, never the body music or a fabricated new impact.
    begin=round(3.50*SR);cut=round(4*SR);dry=source[begin:cut].astype(np.float64)
    dry[-round(.004*SR):]*=np.linspace(1,0,round(.004*SR))[:,None]
    count=len(dry)+round(.28*SR);fft_n=1<<(count-1).bit_length()
    frequencies=np.fft.rfftfreq(fft_n,1/SR)
    color=(1-np.exp(-(frequencies/190)**4))*np.exp(-(frequencies/2800)**4)
    ir_n=round(.28*SR);t=np.arange(ir_n)/SR;rng=np.random.default_rng(20261120)
    wet=np.zeros((count,2))
    for channel in range(2):
        # Dense, decorrelated reflections with damped high end avoid distinct echoes.
        ir=rng.standard_normal(ir_n)*np.exp(-t/.060)
        ir[:round(.008*SR)]=0
        ir*=smooth_array((.28-t)/.035)
        ir/=np.sqrt(np.sum(ir*ir))
        for delay,gain in [(0.011,.32),(0.019,.25),(.031,.18),(.047,.12)]:
            ir[round((delay+channel*.0013)*SR)]+=gain
        mono=.86*dry[:,channel]+.14*dry[:,1-channel]
        wet[:,channel]=np.fft.irfft(np.fft.rfft(mono,fft_n)*np.fft.rfft(ir,fft_n)*color,fft_n)[:count]
    times=3.50+np.arange(count)/SR
    wet*=smooth_array((times-3.72)/.18)[:,None]
    wet*=smooth_array((4.28-times)/.06)[:,None]
    ref=wet[round(.48*SR):round(.55*SR)]
    gain=min(.040/max(float(np.sqrt(np.mean(ref*ref))),1e-12),.14/max(float(np.max(np.abs(wet))),1e-12))
    wet*=gain
    stem=np.zeros((total_samples,2),np.float32);stem[begin:begin+count]=wet
    return stem


def main():
    with wave.open(str(ROOT/'audio/MIX-HD-scott-spin-v04.wav'),'rb') as f:
        assert f.getframerate()==SR and f.getnchannels()==2
        original=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
    wet=bridge(len(original));mixed=original+wet
    a,b=round(3.72*SR),round(4.28*SR)
    assert not np.any(wet[:a]) and not np.any(wet[b:])
    assert np.array_equal(mixed[:a],original[:a]) and np.array_equal(mixed[b:],original[b:])
    assert np.max(np.abs(mixed))<.99
    stem=ROOT/'audio/SFX-INTRO-A-original-CG-reverb-tail-v05.wav';mix=ROOT/'audio/MIX-HD-intro-a-bridge-v05.wav'
    save_wav(stem,wet);save_wav(mix,mixed)
    if not FINAL.exists():
        run(['-i',BASE,'-i',mix,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',SR,'-t',1663/30,'-movflags','+faststart',FINAL])
    if not PREVIEW.exists():
        run(['-i',FINAL,'-ss',2,'-t',6,'-c:v','libx264','-preset','fast','-crf',18,'-c:a','aac','-b:a','256k','-movflags','+faststart',PREVIEW])
    if not COMPARE.exists():
        font="fontfile='C\\:/Windows/Fonts/segoeui.ttf'"
        filt=(f"[0:v]trim=start=2.5:duration=3,setpts=PTS-STARTPTS,scale=1280:720,drawtext={font}:text='Before':x=40:y=35:fontsize=32:fontcolor=white:box=1:boxcolor=black@0.45[v0];"
              '[0:a]atrim=start=2.5:duration=3,asetpts=PTS-STARTPTS[a0];'
              f"[1:v]trim=start=2.5:duration=3,setpts=PTS-STARTPTS,scale=1280:720,drawtext={font}:text='After':x=40:y=35:fontsize=32:fontcolor=white:box=1:boxcolor=black@0.45[v1];"
              '[1:a]atrim=start=2.5:duration=3,asetpts=PTS-STARTPTS[a1];'
              '[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]')
        run(['-i',BASE,'-i',FINAL,'-filter_complex',filt,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf',18,'-c:a','aac','-b:a','256k','-movflags','+faststart',COMPARE])
    def picture(path):return run(['-i',path,'-map','0:v:0','-c:v','copy','-f','h264','-']).stdout
    before,after=picture(BASE),picture(FINAL);assert before==after
    run(['-xerror','-i',FINAL,'-f','null','-'])
    cap=cv2.VideoCapture(str(FINAL));assert cap.get(7)==1663 and cap.get(5)==30 and cap.get(3)==1920 and cap.get(4)==1080;cap.release()
    output_audio=decode_audio(FINAL);old_audio=decode_audio(BASE);n=min(len(output_audio),len(old_audio))
    mask=np.ones(n,dtype=bool);mask[a-4096:b+4096]=False
    outside_rmse=float(np.sqrt(np.mean((output_audio[:n][mask]-old_audio[:n][mask])**2)));assert outside_rmse<.01
    result={'status':'pending_user_review','output':str(FINAL),'preview':str(PREVIEW),'comparison':str(COMPARE),'duration_seconds':1663/30,'frames':1663,'fps':30,'edit':{'picture_cut':4.0,'wet_interval':[3.72,4.28],'tail_into_A_seconds':.28,'source':'existing CG source final0.5s, damped diffuse stereo reflections','wet_peak':float(np.max(np.abs(wet))),'wet_rms_4_to_4p1':float(np.sqrt(np.mean(wet[4*SR:round(4.1*SR)]**2))),'music':'no offset, gain change, ducking or beat shift'},'mix_peak':float(np.max(np.abs(mixed))),'verification':{'video_stream':'byte-identical to v04','video_sha256':hashlib.sha256(after).hexdigest(),'full_decode':'passed','outside_edit_PCM':'unchanged before quantization and AAC encode','outside_edit_AAC_rmse':outside_rmse},'credits_spent':0}
    (ROOT/'exports/HD-intro-a-bridge-v05-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
