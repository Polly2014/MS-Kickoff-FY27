"""Encode a small compatible 720P copy of the approved final without changing timing."""
import json
import hashlib
import cv2
from assemble_f_ending_v01 import ROOT, run

SOURCE=ROOT/'exports/FY27-Kickoff-FINAL-1080P.mp4'
OUTPUT=ROOT/'exports/FY27-Kickoff-WeChat-720P.mp4'


def main():
    if not OUTPUT.exists():
        log=ROOT/'exports/WeChat-720P-encode-v01'
        video=['-i',SOURCE,'-map','0:v:0','-vf','scale=1280:720:flags=lanczos','-r',30,'-c:v','libx264','-preset','slow','-b:v','1200k','-maxrate','1800k','-bufsize','3600k','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-passlogfile',log]
        run([*video,'-pass',1,'-an','-f','null','NUL'])
        run([*video,'-pass',2,'-map','0:a:0','-c:a','aac','-b:a','96k','-ar',44100,'-ac',2,'-movflags','+faststart',OUTPUT])
    cap=cv2.VideoCapture(str(OUTPUT));assert cap.get(3)==1280 and cap.get(4)==720 and cap.get(5)==30 and cap.get(7)==1663;cap.release()
    run(['-xerror','-i',OUTPUT,'-f','null','-'])
    assert OUTPUT.stat().st_size<10_000_000
    result={'status':'ready','source':SOURCE.name,'file':OUTPUT.name,'width':1280,'height':720,'fps':30,'frames':1663,'duration_seconds':1663/30,'video':'H.264 High Level3.1 / yuv420p / two-pass1200k','audio':'AAC stereo96k /44100Hz','faststart':True,'bytes':OUTPUT.stat().st_size,'source_bytes':SOURCE.stat().st_size,'reduction_percent':round((1-OUTPUT.stat().st_size/SOURCE.stat().st_size)*100,1),'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),'verification':'frame count, dimensions and full decode passed','note':'sharing copy; official delivery remains the approved1080P file','credits_spent':0}
    (ROOT/'exports/FY27-Kickoff-WeChat-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
