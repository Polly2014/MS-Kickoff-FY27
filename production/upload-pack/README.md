# LibTV分段上传包

先核对当前模型的模式和报价。按每个文件夹内数字前缀上传；平台引用标签须通过页面控件插入。正式视频尚未生成，这些文件夹也尚未导入LibTV。

| 任务 | 图片数 | 尚缺 | 状态 |
| --- | --- | --- | --- |
| [A](A/README.md) | 2 | 无本地图像缺口 | 图像已准备，视频效果待试制 |
| [B](B/README.md) | 3 | 无本地图像缺口 | 图像已准备，视频效果待试制 |
| [C](C/README.md) | 5 | B_LAST | 待补素材：B_LAST；等待真实连续帧 |
| [D](D/README.md) | 8 | 无本地图像缺口 | 图像已准备，视频效果待试制 |
| [E](E/README.md) | 8 | D_LAST | 待补素材：D_LAST；等待真实连续帧 |
| [C-PREVIEW](C-PREVIEW/README.md) | 4 | 无本地图像缺口 | 预演：省略B真实出点帧，不保证与B连续 |
| [E-PREVIEW](E-PREVIEW/README.md) | 8 | 无本地图像缺口 | 预演：GROUP_LOCAL代替D真实出点帧，正式任务需换回D_LAST |
| [E1-PREVIEW-4s](E1-PREVIEW-4s/README.md) | 2 | 无本地图像缺口 | 四秒揭示预演；GROUP_LOCAL不是D实际末态，正式需替换首帧 |
| [E2-PREVIEW-8s](E2-PREVIEW-8s/README.md) | 7 | 无本地图像缺口 | 八秒群舞预演；正式需用E1真实出点帧衔接 |

C/E正式任务中的B_LAST/D_LAST必须从实际采用视频提取，不以设计图冒充。C-PREVIEW、E-PREVIEW及E1/E2-PREVIEW为可单独测试的图像参考版本。

二维揭示备用预演见`../previews/E1-reveal-2D-PREVIS-v01.mp4`，人物静止且有明确预演标识；不能冒充已生成的AI视频或真实三维升镜。
