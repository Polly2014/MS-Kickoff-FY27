# 生成前准备包 · v05

最新制作进度：B段首版已在LibTV生成并下载，880积分，待用户看样；见[B段实际结果与检查](SEG-B-v01-REVIEW.md)。下文“本轮未启动视频”等边界保留为准备阶段历史，当前以此条实际记录为准。

舞台执行方向已确认：保留Logo造型，局部以低机位和前景表现巨大尺度，人物站在平缓实面并有清楚接触阴影；36–40秒低亮读形，40秒共同落脚才全亮。全亮参考图不约束前段曝光，单首帧模式按需补暗光首帧。详见[空间与灯光执行说明](STAGE-SPATIAL-REFERENCE.md)。

2026-11-18：五种空间参考图已补齐并完成目视检查；人物原始定稿未改。前两版六人全景含Scott身份错误，已弃用，当前全景选择v03。所有图片均为制作参考，尚非用户确认的最终美术或已生成的视频。

[准备素材总览](previews/preparation-assets-v05.jpg) · [逐段上传文件夹](upload-pack/README.md) · [实际输入/Prompt/哈希与检查记录](preparation-manifest.json)

| 素材 | 实际文件 | 尺寸 |
| --- | --- | --- |
| 01 空舞台全景 | [STAGE_MASTER](frames/STAGE_MASTER-gpt-image-2-v02.png) | 3840×2160 |
| 02 六人全景 · Scott已修正 | [GROUP_MASTER](frames/GROUP_MASTER-gpt-image-2-v03.png) | 3840×2160 |
| 03 六人局部 | [GROUP_LOCAL](frames/GROUP_LOCAL-gpt-image-2-v03.png) | 2048×1152 |
| 04 Jessica / Feng / Scott | [CORE3_MASTER](frames/CORE3_MASTER-gpt-image-2-v02.png) | 2048×1152 |
| 05 Song / Amy | [DUO_MASTER](frames/DUO_MASTER-gpt-image-2-v01.png) | 2048×1152 |

## 已准备

- A/B/D的本地图像参考可直接开始技术试制；C/E正式包只缺B_LAST/D_LAST实际剪辑出点帧。另有C-PREVIEW、E-PREVIEW、E1四秒与E2八秒技术预演包，可先验证高风险环节。
- 每个上传包包含按顺序编号的图片、素材映射JSON、Prompt模板与说明。按缩略图通过LibTV页面控件插入真实@引用，未伪造平台标签；这些文件尚未导入LibTV。
- Scott第二排右侧：浓密侧分头发、低发际线、黑色矩形眼镜、圆脸和闭嘴微笑；Feng前中央：高额头、较细眼镜、椭圆脸和自己的笑容。全景、局部与三人图分别检查，避免重复角色。
- [二维拉远预演](previews/E1-reveal-2D-PREVIS-v01.mp4)：同一母版原像素局部裁切到全景，1920×1080、4秒、30fps/120帧；人物静止，有明确预演标识。具体方法见[空间连续性说明](STAGE-SPATIAL-REFERENCE.md)，不冒充真实三维升镜或群舞。
- [临时120BPM节拍器](audio/TEMP-click-120BPM-60s.wav)：60秒试剪网格，不是最终AI音乐；正式原创音乐Prompt已备。
- [实际末态提取工具](extract_continuity_frame.py)支持B、D、E1，按实际选段出点解码原视频帧，拒绝覆盖，不生成假末帧。

## 下一步制作

1. LibTV先测B段8秒：使用upload-pack/B，核对实际Seedance 2.5多参考模式、时长、分辨率、数量、音频与报价，再启动一版。
2. 同时优先验证E1四秒揭示与E2八秒群舞；真实升镜不稳时采用已准备的二维空间路线，并把D末镜与E首镜统一到同一母版。
3. 锁定正式原创音乐，测实际BPM后补齐其余段落并精剪；视频仍全部使用LibTV模型。
4. 保存B/D/E1的实际采用源片及剪辑出点，提取真实连续帧后再更新正式上传包。

```powershell
python -X utf8 production/extract_continuity_frame.py B production/selected/SEG-B.mp4
python -X utf8 production/extract_continuity_frame.py D production/selected/SEG-D.mp4
# 如果输入的是未裁切源片，额外指定 --cut-out-frame N（实际出点，不包含第N帧）
python -X utf8 production/build_pack.py
python -X utf8 production/prepare_upload_pack.py
```

## 实际记录与边界

本轮通过dream-painter显式调用Azure gpt-image-2，完成8张API输出，选用5张空间参考；其余3张为弃用/中间候选。首次控制台编码错误发生在API调用前；另有一次上传连接超时和一次429限流，均保留失败记录并换版本重试。API账单未查询，超时请求不据此断言未计费。原始人物与既有试片均保留。
图片API费用独立于LibTV，本轮未启动LibTV收费视频任务。当前空间参考仍不等于经过标定的三维模型；音乐成品、真实@绑定、平台报价、动态身份一致性及真实Logo升镜均留待实际制作核对。
