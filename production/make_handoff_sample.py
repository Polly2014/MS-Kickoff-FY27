"""Build the LibTV S03/S04 budget sample and contact sheets. No generation API."""
from pathlib import Path
import subprocess
import cv2
import imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PREVIEWS = ROOT / 'previews'
PREVIEWS.mkdir(exist_ok=True)

def contact(shot):
    cap = cv2.VideoCapture(str(ROOT / 'raw-video' / f'{shot}_v01.mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(shot, {'fps': fps, 'frames': cap.get(cv2.CAP_PROP_FRAME_COUNT),
                 'width': cap.get(3), 'height': cap.get(4)})
    board = Image.new('RGB', (960, 900))
    draw = ImageDraw.Draw(board)
    for i, t in enumerate([0, 1, 2, 3, 4, 4.8]):
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, frame = cap.read()
        if ok:
            xy = ((i % 2) * 480, (i // 2) * 300)
            board.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((480, 276)), xy)
            draw.text((xy[0] + 8, xy[1] + 280), f'{shot} {t}s', fill='white')
    cap.release()
    board.save(PREVIEWS / f'{shot}-contact.jpg')

if __name__ == '__main__':
    for shot in ['S03', 'S04']:
        if (ROOT / 'raw-video' / f'{shot}_v01.mp4').exists():
            contact(shot)
    if (ROOT / 'raw-video/S04_v01.mp4').exists():
        out = ROOT / 'exports/Jessica-to-Feng_4s_v01_480p.mp4'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y',
            '-i', str(ROOT / 'raw-video/S03_v01.mp4'),
            '-i', str(ROOT / 'raw-video/S04_v01.mp4'),
            '-filter_complex',
            '[0:v]trim=start=2:duration=2,setpts=PTS-STARTPTS,fps=30,scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2,setsar=1[a];'
            '[1:v]trim=start=0.5:duration=2,setpts=PTS-STARTPTS,fps=30,scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2,setsar=1[b];'
            '[a][b]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-an',
            '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', str(out)], check=True)
        print(out)
