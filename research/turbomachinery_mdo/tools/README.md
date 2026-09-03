# 数据 provenance 工具（不做科学推断）

这里的工具仅服务于 `REENTRY_REQUIREMENTS.md` 所要求的**版本化数据 manifest**。它们不是模型训练、CFD、优化或论文实验代码。

## `build_data_manifest.py`

对一个已经以合法方式取得的本地目录，生成稳定排序的 JSON provenance manifest：

- 相对文件路径、字节数和流式 SHA-256；
- `.mat` 文件的字节级容器识别（可能的 HDF5/v7.3 或 Level-5 header）；
- 若执行环境已**显式记录地**安装 SciPy 或 h5py，则尽力列出变量名/shape/dtype；解析失败会写入 JSON；
- `.npz` 文件的文件级 provenance。

它**不会**从文件名、变量名或数组维度推断：样本数、训练/测试 split、物理单位、`Temperature` 的金属/流体语义、孔身份、共享 case ID 或 GE-E3/Pak-B 的耦合关系。这些必须由数据卡、schema 和人工核验另行确认。

### 用法

```bash
python research/turbomachinery_mdo/tools/build_data_manifest.py \
  --root /path/to/legal/local/GE-E3 \
  --dataset-label GE-E3 \
  --output research/turbomachinery_mdo/manifests/ge-e3-provenance.json
```

若只希望扫描 MAT 文件，可追加 `--suffix .mat`；注意命令行的默认值已经包含 `.mat` 和 `.npz`，重复追加时会保留两者。输出路径可在数据目录之外。**不要**把受许可限制、体积巨大的 MAT 文件或未经允许的内容复制进本仓库。

### 本地测试

测试只创建临时的伪 header/字节文件；它不下载、不读取也不代表 GE-E3 或 Pak-B 数据：

```bash
python -m unittest discover \
  -s research/turbomachinery_mdo/tools/tests \
  -p 'test_*.py' -v
```

截至 2026-09-01，本工作区没有成功取得任何实际 GE-E3/Pak-B MAT binary，因此尚未针对真实数据运行该工具，也不存在任何已生成的数据 manifest。
