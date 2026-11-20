"""Local F credits preview; preserve approved A-E video by stream copying."""
from pathlib import Path
import json
import math
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H = 30, 1920, 1080
AE_FRAMES, TOTAL_FRAMES = 1378, 1560
F_FRAMES = TOTAL_FRAMES - AE_FRAMES
DURATION = TOTAL_FRAMES / FPS
OUT = ROOT / 'exports'
FRAMES = ROOT / 'frames' / 'creators'
F1080 = ROOT / 'videos/SEG-F-local-credits-1080P-layout-v01-silent.mp4'
F480 = ROOT / 'videos/SEG-F-local-credits-480P-v01-silent.mp4'
SILENT = OUT / 'FY27-A-F-52s-480P-v01-silent.mp4'
FINAL = OUT / 'FY27-A-F-52s-480P-v01-music.mp4'
PREVIEW = ROOT / 'previews/SEG-E-F-9p07s-credits-v01-music.mp4'


def run(args):
    result = subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-n', *map(str, args)],
                            capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return result


def smooth(x):
    x = max(0., min(1., x))
    return x * x * (3 - 2 * x)


def centered(layer, text, y, font, fill):
    d = ImageDraw.Draw(layer)
    box = d.textbbox((0, 0), text, font=font)
    x = (W - (box[2] - box[0])) // 2
    d.text((x, y), text, font=font, fill=fill,
           stroke_width=1, stroke_fill=(5, 12, 27, 170))


def video_frame(path, number):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, number)
    ok, frame = cap.read()
    cap.release()
    assert ok, (path, number)
    return frame


def main():
    tail = video_frame(ROOT/'videos/SEG-E-Wan3-480P-v08-adopted.mp4', 239)
    bg = Image.fromarray(cv2.cvtColor(tail, cv2.COLOR_BGR2RGB)).resize((W, H), Image.Resampling.LANCZOS)
    backdrop = bg.filter(ImageFilter.GaussianBlur(65)).convert('RGBA')
    backdrop.alpha_composite(Image.new('RGBA', (W, H), (3, 10, 25, 155)))
    # Feather the shrinking image into the dark blue stage surround.
    yy, xx = np.mgrid[:H, :W]
    edge = np.minimum.reduce([xx / 75., (W-1-xx) / 75., yy / 75., (H-1-yy) / 75.])
    feather = np.clip(edge, 0, 1)
    font_dir = Path('C:/Windows/Fonts')
    names_font = ImageFont.truetype(str(font_dir/'msyhbd.ttc'), 41)
    idea_font = ImageFont.truetype(str(font_dir/'segoeui.ttf'), 29)
    small_font = ImageFont.truetype(str(font_dir/'segoeui.ttf'), 24)
    credits = Image.new('RGBA', (W, H))
    centered(credits, '创作团队  Baoli Wang · Yun Gu', 817, names_font, (247,250,255,255))
    centered(credits, 'Passing the spark, bringing Copilot to life together.', 885,
             idea_font, (195,224,242,255))
    d = ImageDraw.Draw(credits)
    d.line((840, 787, 1080, 787), fill=(92,210,239,165), width=2)
    d.text((90, 986), 'AI Models: Wan 3.0 · GPT Image 2 · Lib Image 2.5 Pro · ElevenMusic V3',
           font=small_font, fill=(187,201,222,255))
    d.text((90, 1024), 'Tools: Codex · LibTV · dream-painter · Python / FFmpeg',
           font=small_font, fill=(187,201,222,255))
    avatars = []
    for name in ('Baoli-Wang', 'Yun-Gu'):
        im = Image.open(FRAMES/f'F-cameo-{name}-v02-transparent.png').convert('RGBA')
        # A tiny choke removes white matte fringes before shrinking.
        im.putalpha(im.getchannel('A').filter(ImageFilter.MinFilter(3)))
        im.thumbnail((64, 60), Image.Resampling.LANCZOS)
        avatars.append(im)

    if not F1080.exists():
        process = subprocess.Popen([FF, '-hide_banner', '-loglevel', 'error', '-n',
            '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
            '-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
            '-video_track_timescale','15360','-movflags','+faststart',str(F1080)],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        for i in range(F_FRAMES):
            t = i / FPS
            progress = smooth(t / 1.65)
            scale = 1 - .16 * progress - .007 * min(t / 6, 1)
            stage = bg.convert('RGBA')
            stage.putalpha(Image.fromarray((255 * ((1-progress)+progress*feather)).astype(np.uint8)))
            stage = stage.resize((round(W*scale),round(H*scale)), Image.Resampling.LANCZOS)
            frame = backdrop.copy()
            frame.alpha_composite(stage, ((W-stage.width)//2, round((H-stage.height)/2-72*progress)))
            # A soft bottom shade makes text legible without covering the Logo.
            shade = np.zeros((H,W,4),dtype=np.uint8)
            shade[:,:,:3] = (3,9,23)
            shade[:,:,3] = (np.clip((yy-705)/260,0,1)*145*progress).astype(np.uint8)
            frame.alpha_composite(Image.fromarray(shade))
            text = credits.copy()
            text.putalpha(text.getchannel('A').point(lambda a: round(a*smooth((t-.65)/.75))))
            frame.alpha_composite(text)
            for j, avatar in enumerate(avatars):
                entry = smooth((t-(1.15+.45*j))/.65)
                leave = smooth((t-5.15-.12*j)/.55)
                visible = entry*(1-leave)
                nod = math.sin(max(0,min(1,(t-(3.0+.2*j))/.8))*math.pi)
                angle = (-1 if j else 1)*(5*math.sin(t*2+j)*visible + 7*nod)
                im = avatar.rotate(angle, Image.Resampling.BICUBIC, expand=True)
                x = (1766 if j==0 else 1830) - (im.width-avatar.width)//2
                y = round(H+7-visible*61+3*nod)
                frame.alpha_composite(im,(x,y))
            fade = smooth((t-5.5)/(.5667))
            if fade:
                frame.alpha_composite(Image.new('RGBA',(W,H),(0,0,0,round(255*fade))))
            if i in (0,45,105,155):
                frame.convert('RGB').save(ROOT/f'previews/F-credits-v01-frame-{i:03}.jpg',quality=95)
            process.stdin.write(frame.convert('RGB').tobytes())
        process.stdin.close()
        error=process.stderr.read(); assert process.wait()==0,error.decode(errors='replace')
    if not F480.exists():
        run(['-i',F1080,'-vf','scale=854:480:flags=lanczos','-an','-c:v','libx264',
             '-crf','16','-preset','slow','-pix_fmt','yuv420p','-video_track_timescale','15360',
             '-movflags','+faststart',F480])
    concat = OUT/'FY27-A-F-v01-concat.txt'
    ae = OUT/'FY27-A-E-45p93s-480P-roughcut-v03-beam-relay-silent.mp4'
    concat.write_text(f"file '{ae.as_posix()}'\nfile '{F480.as_posix()}'\n",encoding='utf-8')
    if not SILENT.exists():
        run(['-f','concat','-safe','0','-i',concat,'-map','0:v:0','-an','-c:v','copy',
             '-movflags','+faststart',SILENT])
    music = ROOT/'music/MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
    # Preserve A-E audio timing; skip one eight-second phrase within F and
    # use the source's natural closing fade rather than fading mid-phrase.
    music_length=60.08163265306123
    audio_filter = (f'[1:a]asplit=2[head][tail];'
        f'[head]atrim=0:48.15,asetpts=PTS-STARTPTS[h];'
        f'[tail]atrim=start={music_length-4}:end={music_length},asetpts=PTS-STARTPTS[t];'
        '[h][t]acrossfade=d=0.15:c1=tri:c2=tri,volume=-4dB[a]')
    if not FINAL.exists():
        run(['-i',SILENT,'-i',music,'-filter_complex',audio_filter,'-map','0:v:0',
             '-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','44100',
             '-t',DURATION,'-movflags','+faststart',FINAL])
    if not PREVIEW.exists():
        run(['-i',FINAL,'-ss',AE_FRAMES/FPS-3,'-t',3+F_FRAMES/FPS,
             '-c:v','libx264','-crf','17','-preset','fast','-c:a','aac','-b:a','192k',
             '-movflags','+faststart',PREVIEW])
    cap=cv2.VideoCapture(str(FINAL)); count=int(cap.get(7)); rate=cap.get(5);cap.release()
    assert count==TOTAL_FRAMES and rate==FPS,(count,rate)
    for n in (0,297,298,657,897,1137,1377):
        assert np.array_equal(video_frame(ae,n),video_frame(FINAL,n)), n
    run(['-xerror','-i',FINAL,'-f','null','-'])
    raw=run(['-i',FINAL,'-vn','-ar','44100','-ac','2','-f','f32le','-']).stdout
    sound=np.frombuffer(raw,dtype='<f4');peak=float(np.max(np.abs(sound)))
    assert peak<1,peak
    assert abs(len(sound)/2/44100-DURATION)<.04
    manifest={'status':'local_preview_pending_user_review','output':str(FINAL),
        'frames':count,'fps':rate,'duration':DURATION,'f_start':AE_FRAMES/FPS,
        'f_frames':F_FRAMES,'f_duration':F_FRAMES/FPS,
        'background':'E last frame, locally scaled and softly darkened; no new model animation',
        'cameos':'approved v02 static transparent PNGs; local translation and rotation; visible height about 5%',
        'credits':'locally rendered at 1920x1080 then scaled to review size; stage remains 480P source',
        'audio':{'source':str(music),'head':[0,48.15],'tail':[music_length-4,music_length],
                 'crossfade_seconds':.15,'gain_db':-4,'decoded_peak':peak},
        'verification':{'full_decode':'passed','sampled_AE_frames':'exact decoded pixels','audio_duration':'passed'},
        'libtv_credit_cost':0}
    (OUT/'FY27-A-F-52s-v01-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    main()
