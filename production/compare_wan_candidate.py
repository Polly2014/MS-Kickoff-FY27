"""Preserve a downloaded candidate and make deterministic review artifacts."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'raw-video/SEG-B_v01.mp4'
NEW = ROOT / 'raw-video/SEG-B_WAN30_480P_v01.mp4'
EXPECTED = 'dff801324b2420f86c31b6d099c61e3756f3cafd4129f72f093f0bb20b7ccc2c'
assert hashlib.sha256(OLD.read_bytes()).hexdigest() == EXPECTED
if not NEW.exists():
    shutil.copyfile(sys.argv[1], NEW)
else:
    raise FileExistsError(NEW)

cap = cv2.VideoCapture(str(NEW))
meta = {'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'bytes': NEW.stat().st_size,
        'sha256': hashlib.sha256(NEW.read_bytes()).hexdigest()}
meta['duration'] = meta['frames'] / meta['fps']
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
sheet = Image.new('RGB', (1280, 4 * 204), '#14141c')
draw = ImageDraw.Draw(sheet)
for i in range(16):
    t = i * .5
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, frame = cap.read()
    if not ok:
        continue
    tile = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((320, 180))
    x, y = (i % 4) * 320, (i // 4) * 204
    sheet.paste(tile, (x, y + 24))
    draw.text((x + 5, y), f'{t:.1f}s', font=font, fill='white')
cap.release()
sheet.save(ROOT / 'previews/SEG-B-WAN30-480P-v01-contact.jpg', quality=94)
header = Image.new('RGB', (1280, 42), '#101018')
draw = ImageDraw.Draw(header)
draw.text((15, 8), 'Seedance 2.5 / 1080P / 880 credits', font=font, fill='white')
draw.text((655, 8), 'Wan 3.0 / 480P / 32 credits', font=font, fill='white')
header_path = ROOT / 'previews/SEG-B-comparison-header.png'
header.save(header_path)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
probe = subprocess.run([ffmpeg, '-hide_banner', '-i', str(NEW)], capture_output=True, text=True)
meta['ffmpeg_inspection'] = probe.stderr
meta['has_audio'] = 'Audio:' in probe.stderr
preview = ROOT / 'exports/SEG-B_WAN30_480P_v01_review.mp4'
subprocess.run([ffmpeg, '-n', '-i', str(NEW), '-t', '8', '-an', '-vf', 'fps=30',
                '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                str(preview)], check=True, capture_output=True)
comparison = ROOT / 'exports/SEG-B_SD25-vs-WAN30_comparison.mp4'
filters = ('[0:v]trim=duration=8,setpts=PTS-STARTPTS,scale=640:360,fps=30,setsar=1[a];'
           '[1:v]trim=duration=8,setpts=PTS-STARTPTS,scale=640:360,fps=30,setsar=1[b];'
           '[a][b]hstack=inputs=2[v];[2:v]fps=30,setsar=1[h];[h][v]vstack=inputs=2[out]')
subprocess.run([ffmpeg, '-n', '-i', str(OLD), '-i', str(NEW), '-loop', '1', '-i', str(header_path),
                '-filter_complex', filters, '-map', '[out]', '-t', '8', '-an',
                '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                str(comparison)], check=True, capture_output=True)
manifest_path = ROOT / 'SEG-B-WAN30-480P-v01-generation.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.update(status='completed; awaiting user comparison review', actual_media=meta,
                review_export=str(preview.relative_to(ROOT)), comparison_export=str(comparison.relative_to(ROOT)),
                original_seedance_sha256_verified=EXPECTED)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
assert hashlib.sha256(OLD.read_bytes()).hexdigest() == EXPECTED
print(json.dumps(meta, ensure_ascii=False, indent=2))
