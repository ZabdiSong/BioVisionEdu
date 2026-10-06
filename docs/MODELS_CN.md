# Blender 模型说明

本次用 Blender 4.2 创建四个可编辑原生文件，重新打开验证网格存在，并导出 GLB。没有制作新动画，也没有以改后缀的方式伪造 Blender 文件。

| 模型 | Blender 文件 | 网页/通用 3D 文件 |
| --- | --- | --- |
| 线粒体 | `assets/models/mitochondrion.blend` | `mitochondrion.glb` |
| 叶绿体 | `assets/models/chloroplast.blend` | `chloroplast.glb` |
| 呼吸电子传递链 | `assets/models/respiratory-etc.blend` | `respiratory-etc.glb` |
| 类囊体光反应 | `assets/models/light-reactions.blend` | `light-reactions.glb` |

## 教学含义

- 线粒体：双层膜、基质、嵴和 ATP 合酶，展示膜面积和区室关系。
- 叶绿体：包膜、基质、基粒与基质片层，区分类囊体膜和基质。
- 呼吸 ETC：复合体 I–IV、Q、细胞色素 c、氧受体与 ATP 合酶；复合体 II 不泵质子。高质子侧为膜间隙，ATP 合酶头部朝向基质。
- 光反应：PSII、PQ、b6f、质体蓝素、PSI、FNR 与 ATP 合酶；高质子侧为类囊体腔，NADPH/ATP 形成侧为基质。

颜色与形状是用于教学的简化。文件不是原子结构、真实蛋白质折叠或按比例重建；电子路线是静态示意，不是分子轨迹模拟。

## 编辑和重建

直接在 Blender 中打开 `.blend`，结构对象带有 `part_id` 和说明属性，可以改材质和形状。原始生成配方为 `tools/build_models.py`：

```sh
blender --background --python tools/build_models.py
```

运行会重新生成四个模型并覆盖当前输出。先复制你手工编辑的版本，再运行配方。网页不直接读取 `.blend`；它使用同目录 `model-data.js` 中的几何数据，因此修改模型后也要同步网页导出。配方同时输出 `.blend`、`.glb`、`model-data.js` 和 `model-manifest.json`。

## 网页操作

拖动旋转、滚轮缩放；键盘方向键旋转，`+` / `-` 缩放。点击结构按钮或可选内部网格显示说明。透明外膜/剖切帮助看内部；隔离选中部分用于单独查看结构。Gallery 的模型按钮可以打开较大窗口。
