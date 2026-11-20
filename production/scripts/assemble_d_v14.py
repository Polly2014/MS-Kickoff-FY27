"""Build D v14 from v08 frames 0:120 and v13 frames 120:240."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
videos = root / 'videos'
out = videos / 'SEG-D-Wan3-480P-v14-edit-v08first4s-v13last4s.mp4'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
parts = [
    ('SEG-D-Wan3-480P-v08-original.mp4', 0, 120, 'SEG-D-v14-part1-v08-0-4s.mp4'),
    ('SEG-D-Wan3-480P-v13-adopted.mp4', 120, 240, 'SEG-D-v14-part2-v13-4-8s.mp4'),
]

def run(args):
    subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)

for source, start, end, target in parts:
    if (videos / target).exists():
        raise FileExistsError(target)
    run(['-i', str(videos / source), '-vf',
         f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS',
         '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
         '-pix_fmt', 'yuv420p', '-r', '30', '-video_track_timescale', '15360',
         '-movflags', '+faststart', str(videos / target)])

if out.exists():
    raise FileExistsError(out)
concat = videos / 'SEG-D-v14-concat.txt'
concat.write_text(''.join(f"file '{p[3]}'\n" for p in parts), encoding='utf-8')
run(['-f', 'concat', '-safe', '0', '-i', str(concat), '-c', 'copy',
     '-movflags', '+faststart', str(out)])

def frame(path, index):
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ok, value = cap.read()
    cap.release()
    assert ok, (path, index)
    return value

checks = []
for path, expected in [(videos / p[3], 120) for p in parts] + [(out, 240)]:
    cap = cv2.VideoCapture(str(path))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]
    cap.release()
    assert count == expected and fps == 30 and size == [854, 480], (path, count, fps, size)
    checks.append(dict(file=path.name, frames=count, fps=fps, size=size, seconds=count/fps))

matches = []
for output_index, source, source_index in [
    (0, parts[0][0], 0), (119, parts[0][0], 119),
    (120, parts[1][0], 120), (239, parts[1][0], 239),
]:
    psnr = cv2.PSNR(frame(out, output_index), frame(videos/source, source_index))
    assert psnr > 32, (output_index, psnr)
    matches.append(dict(output_frame=output_index, source=source, source_frame=source_index, psnr=psnr))

sheet = Image.new('RGB', (1100, 680), '#15171b')
draw = ImageDraw.Draw(sheet)
for n, (index, label) in enumerate([(0, 'v08 opening | output 0.00s'),
                                   (119, 'v08 last frame | output 3.97s'),
                                   (120, 'v13 first frame | output 4.00s'),
                                   (239, 'v13 ending | output 7.97s')]):
    x, y = (n % 2)*550+10, (n//2)*340+10
    draw.text((x, y), label, fill='white')
    picture = Image.fromarray(cv2.cvtColor(frame(out, index), cv2.COLOR_BGR2RGB))
    picture.thumbnail((530, 298))
    sheet.paste(picture, (x, y+25))
preview = root/'previews'/'SEG-D-v14-edit-review.jpg'
sheet.save(preview, quality=93)
manifest = dict(output=out.name, edit='Hard cut at 4.000s; v08 [0,4) + v13 [4,8); silent',
                checks=checks, source_match_checks=matches)
(videos/'SEG-D-v14-edit-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
print(preview)
