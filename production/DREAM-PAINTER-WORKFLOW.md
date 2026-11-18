# 图像本地调用，视频 LibTV：交接段试制

2026-11-18追加：五种空间参考已完成，当前六人全景与局部均选v03，Scott第二排右侧已修正。查看[准备包](07-PREPARATION-READY.md)与[实际输入、Prompt及检查记录](preparation-manifest.json)。下文保留最初HANDOFF三图的实测过程。

2026-11-18。本轮图片通过仓库 dream-painter 调用 Azure `gpt-image-2` 部署；不使用 LibTV 图片积分。API 费用独立于 LibTV，未取得账单前不估算实际花费。

## 已适配

- `run_dream_asset.py` 可重复传入 `--reference`，位置参数参考图为 Image 1，其后按参数顺序排列。
- 用 `--deployment gpt-image-2` 对单次调用显式指定部署；没有修改共享 `config.env`，其旧默认仍是 `gpt-image-1.5`。
- 编辑请求传入全部图片、quality、size、PNG 输出选项；失败直接报错，不降级到无图文生图，也不换模型。
- 输出保留服务实际返回的原始尺寸，不再强制缩到1536像素。此次目标为2048×1152。
- 原人物定稿、旧 LibTV 素材保留；新图使用独立版本文件名。接口成功代表指定部署可调用，不等于已经验收身份和几何。

## 素材顺序

1. `HANDOFF-stage-gpt-image-2-v01.png`：从旧舞台概念派生局部平缓空舞台，不提前展示完整 Logo。
2. `HANDOFF-jessica-gpt-image-2-v01.png`：Image 1＝新空舞台，Image 2＝Jessica 单人正面图。
3. `HANDOFF-feng-gpt-image-2-v01.png`：Image 1＝同一空舞台，Image 2＝Feng 单人正面图，Image 3＝新 Jessica 首帧（仅约束构图、脚底位置、人物大小，不继承身份）。

提示词全文在 `actual-prompts/HANDOFF-*-gpt-image-2-v01.txt`；每图有同名 `.log`，输出尺寸需从图片实际读取。所有图暂为视频试制参考，不自动升级为已认可定稿。

## 本轮观察

空舞台与 Jessica 已成功返回2048×1152 PNG。空舞台有平缓蓝青地面、远处紫色弯带和右侧近景边缘，未显示完整 Logo。Jessica 保留了短发、眼镜、队服和白鞋，背景布局接近空舞台；并非像素级固定。她没有完全遵循最初要求的48%画面高度，而是约78%，准备侧步的屈膝姿态也不明显。Feng 的实际提示词因此改为匹配此图约12%头顶、90%鞋底的近全身构图，避免两人镜头大小不一致。最终能否保持舞步仍需 LibTV 视频测试。

Feng 亦已成功返回2048×1152 PNG；三张均为实际 API 输出。目视检查显示两位角色全身完整、头顶与脚底高度接近、背景彩带轮廓和机位接近，Feng 的角色特征未被 Jessica 的构图参考替换。两人都较偏正面静态站姿，舞步准备姿态尚不明显；接下来的动作与转场仍需视频验证。`previews/HANDOFF-gpt-image-2-v01.jpg` 为三图预览；`HANDOFF-gpt-image-2-manifest.json` 记录参考顺序、提示词路径、实际尺寸与输出SHA-256，`run-log.csv` 已追加三条试制记录。未继续消耗 LibTV 积分。

## 复现示例

在项目根目录运行 PowerShell：

```powershell
$env:PYTHONIOENCODING='utf-8'
python run_dream_asset.py production/frames/HANDOFF-stage-gpt-image-2-v01.png production/actual-prompts/HANDOFF-jessica-gpt-image-2-v01.txt production/frames/HANDOFF-jessica-gpt-image-2-v02.png --reference assets/characters/production-pack/jessica/jessica-front-v01.png --deployment gpt-image-2 --size 2048x1152 --quality high
```

示例会收费生成一个新 v02。脚本拒绝覆盖已有图片。若当前输出名的图片未生成但已有失败日志，再试时也应换版本号保留失败记录。

## 下一步视频

当前按[v05五段计划](05-GENERATION-PLAN.md)与[操作指南](03-LIBTV-GUIDE-v05.md)执行：先验证B段8秒，以落脚传光、短侧步和遮挡交接；随后验证六人舞台与E段揭示。现有三张图保留为参考，不代表新版动作、完整Logo几何或长段连续性已验证。会员已由用户确认开通；实际模型选项、时长与报价以生成时页面为准。

图片检查后上传 LibTV，使用页面插入的 `@` 素材标签，明确角色身份参考、空舞台参考和构图参考各自用途。先测试一段8秒的 Jessica → Feng 接力；人物交替通过遮挡切换，禁止人物变形互换。按当前账户的模型、权限和实际报价决定是否启动。此图像试制流程不自动购买会员或启动视频生成。
