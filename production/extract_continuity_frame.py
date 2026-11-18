"""Extract the last included source frame of an actual selected clip. No generation."""
import argparse
import hashlib
import json
from pathlib import Path
import cv2
from PIL import Image

BASE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('segment',choices=['B','D','E1'])
    ap.add_argument('video',type=Path)
    ap.add_argument('--cut-out-frame',type=int,help='Exclusive source frame index of the actual chosen edit out point; default: end of selected clip')
    args=ap.parse_args()
    output=BASE/'frames'/f'SEG-{args.segment}-selected-last.png'
    if output.exists(): raise SystemExit('Refusing to overwrite: '+str(output))
    cap=cv2.VideoCapture(str(args.video))
    if not cap.isOpened(): raise SystemExit('Cannot open actual video: '+str(args.video))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS)
    out_frame=args.cut_out_frame if args.cut_out_frame is not None else count
    if not 0<out_frame<=count: raise SystemExit('Cut out frame must be in 1..'+str(count))
    cap.set(cv2.CAP_PROP_POS_FRAMES,out_frame-1);ok,frame=cap.read();cap.release()
    if not ok: raise SystemExit('Cannot decode selected out frame')
    Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).save(output)
    output.with_suffix('.json').write_text(json.dumps(dict(source=str(args.video.resolve()),
        source_sha256=hashlib.sha256(args.video.read_bytes()).hexdigest(),source_fps=fps,
        source_frame_count=count,exclusive_cut_out_frame=out_frame,extracted_frame=out_frame-1,
        note='Actual decoded source frame. No synthetic image used.'),indent=2)+'\n',encoding='utf-8')
    print(output)

if __name__=='__main__':main()
