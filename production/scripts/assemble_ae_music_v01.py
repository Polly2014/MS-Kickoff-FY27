"""Build the 48-second A-E review cut with the approved continuous soundtrack."""
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
videos = root / 'videos'
exports = root / 'exports'
exports.mkdir(exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
parts = [
    ('A', 'SEG-A-Wan3-480P-v07-adopted.mp4', 360),
    ('B', 'SEG-B-Wan3-480P-v08-adopted.mp4', 360),
    ('C', 'SEG-C-Wan3-480P-v08-adopted.mp4', 240),
    ('D', 'SEG-D-Wan3-480P-v14-edit-v08first4s-v13last4s.mp4', 240),
    ('E', 'SEG-E-Wan3-480P-v08-adopted.mp4', 240),
]
music = root / 'music' / 'MUSIC-FY27-street-dance-60s-ElevenMusicV3-v01.mp3'
silent = exports / 'FY27-A-E-48s-480P-roughcut-v01-silent.mp4'
output = exports / 'FY27-A-E-48s-480P-roughcut-v01-music.mp4'

def run(args):
    return subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-n', *args], check=True, capture_output=True)

def info(path):
    cap = cv2.VideoCapture(str(path))
    result = dict(file=path.name, frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                  fps=cap.get(cv2.CAP_PROP_FPS),
                  size=[int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))])
    cap.release()
    result['seconds'] = result['frames']/result['fps']
    return result

def frame(path, index):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, value = cap.read()
    cap.release()
    assert ok, (path, index)
    return value

timeline = []
cursor = 0
for label, filename, expected in parts:
    details = info(videos / filename)
    assert details['frames'] == expected and details['fps'] == 30 and details['size'] == [854, 480], details
    timeline.append(dict(segment=label, start=cursor/30, end=(cursor+expected)/30, source=details))
    cursor += expected

concat = exports / 'FY27-A-E-v01-concat.txt'
concat.write_text(''.join(f"file '../videos/{name}'\n" for _, name, _ in parts), encoding='utf-8')
if not silent.exists():
    run(['-f', 'concat', '-safe', '0', '-i', str(concat), '-map', '0:v:0', '-an',
         '-c:v', 'copy', '-movflags', '+faststart', str(silent)])
if not output.exists():
    run(['-i', str(silent), '-i', str(music), '-map', '0:v:0', '-map', '1:a:0',
         '-c:v', 'copy', '-af', 'atrim=start=0:end=48,asetpts=PTS-STARTPTS,volume=-4dB,afade=t=out:st=47.3:d=0.7',
         '-c:a', 'aac', '-b:a', '256k', '-ar', '44100', '-t', '48',
         '-movflags', '+faststart', str(output)])
details = info(output)
assert details['frames'] == 1440 and details['fps'] == 30 and details['seconds'] == 48
run(['-xerror', '-i', str(output), '-map', '0:v:0', '-f', 'null', '-'])

matches = []
offset = 0
for label, name, count in parts:
    for source_index in [0, count-1]:
        a = frame(output, offset+source_index)
        b = frame(videos/name, source_index)
        equal = bool(np.array_equal(a,b))
        assert equal, (label, source_index)
        matches.append(dict(segment=label, output_frame=offset+source_index, source_frame=source_index, exact_pixels=equal))
    offset += count

def pcm(path):
    raw = run(['-i', str(path), '-vn', '-t', '48', '-ac', '2', '-ar', '44100', '-f', 'f32le', '-']).stdout
    return np.frombuffer(raw, dtype='<f4').reshape(-1,2)

audio = pcm(output)
original = pcm(music)
n = min(len(audio), len(original), 48*44100)
expected = original[:n].copy() * 10**(-4/20)
times = np.arange(n)/44100
expected *= np.clip((48-times)/0.7,0,1)[:,None]
corr = float(np.corrcoef(audio[:n].ravel(),expected.ravel())[0,1])
peak = float(np.max(np.abs(audio)))
assert corr > .97 and peak < 1, (corr, peak)

sheet = Image.new('RGB',(5*427,2*270),'#17191d')
draw = ImageDraw.Draw(sheet)
for col, entry in enumerate(timeline):
    for row, local in enumerate([0, (entry['end']-entry['start'])-1]):
        t = entry['start']+local
        picture = Image.fromarray(cv2.cvtColor(frame(output,round(t*30)),cv2.COLOR_BGR2RGB))
        picture.thumbnail((423,238))
        x,y = col*427,row*270
        draw.text((x+5,y+5), f"{entry['segment']} | timeline {t:.2f}s", fill='white')
        sheet.paste(picture,(x,y+27))
sheet_path=root/'previews'/'FY27-A-E-roughcut-v01-overview.jpg'
sheet.save(sheet_path,quality=94)
manifest=dict(output=details,timeline=timeline,video='Stream copied; all segment durations preserved; hard cuts',
              audio=dict(source=music.name,sha256=hashlib.sha256(music.read_bytes()).hexdigest(),
                         source_range=[0,48],gain_db=-4,fade_out=[47.3,48],codec='AAC 256k stereo 44100Hz',
                         decoded_samples=len(audio),peak=peak,source_correlation=corr),
              verification=dict(full_video_decode='passed',source_boundary_matches=matches),
              scope='A-E only; 12-second F/outro not included; no generated sound effects',
              credit_cost=0)
(exports/'FY27-A-E-roughcut-v01-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
