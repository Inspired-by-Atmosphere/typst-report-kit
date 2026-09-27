# typst-report-kit

一套小巧、有主见的 **Typst 正式报告 / 书刊主题**——暖白纸底、墨色文字、一抹绿色强调色、细发丝边框、克制的编辑感排版。仓库包含可复用主题本体、五套候选配色对比样张，以及可直接照抄的示例（封面、卡片、结论条、徽章、清单、时间线、流程图）。

## 为什么做这个

中英混排的"好看的 PDF"管线，通常不是落到沉重的 HTML 转 PDF 工具链，就是落到一堆手工 Typst 文件里——抄来抄去，最后每个文件都不一样。本仓库把一个这样的文件抽成了：

- **一块设计令牌**——改十一个色值，整篇文档换肤；
- **一组参数化组件**——封面、提示卡片、结论条、状态徽章、复选框清单项、时间线、流程图；
- **一个 `report()` 模板**——A4 版心、封面页自动隐藏的页眉页脚、章节自动编号、统一样式的表格与代码块。

它有意不做成通用设计系统：只把一种风格做扎实。

## 目录结构

```
typst-report-kit/
├── theme.typ                  # 设计令牌 + 组件 + report() 模板
├── showcase.typ               # 五套候选配色，一套一页
├── examples/
│   ├── generic-report.typ     # 用到全部组件的通用示例（占位内容）
│   └── book/
│       ├── book.typ           # 书刊式外壳（不编号、书刊行距）
│       └── body.typ           # 占位正文
├── scripts/
│   ├── check_secrets.py       # 零依赖的泄漏扫描器
│   └── md_to_typst.py         # markdown -> pandoc -> typst -> PDF 管线
├── docs/SANITIZE_LOG.md
└── CHANGELOG.md
```

## 快速开始

1. **装 Typst ≥ 0.15**——到官方发布页下载对应平台的二进制文件（`https://github.com/typst/typst/releases`），或 `cargo install typst-cli`。不需要 npm，不需要 Node。
2. **编译示例**（首次编译会从 Typst universe 拉取 `codly` 与 `fletcher` 两个包，所以需要一次联网）：

   ```bash
   export HTTPS_PROXY=http://127.0.0.1:7897   # 只有在代理后面才需要
   typst compile --root . examples/generic-report.typ
   ```

3. **写自己的报告**——复制 `examples/generic-report.typ`，替换占位文字；想换强调色就改 `theme.typ` 顶部的令牌。

想看五套配色并排对比：

```bash
typst compile showcase.typ
```

## 配置项

没有配置文件，全部是具名参数。

| 位置 | 参数 | 默认值 | 含义 |
|---|---|---|---|
| `#report(...)` | `doc-title` | `none` | 页眉左侧运行标题，首页自动隐藏。 |
| | `doc-date` | `none` | 页眉右侧日期。 |
| | `doc-footer` | `none` | 页脚左侧文字，`none` 表示不显示。 |
| | `numbered` | `true` | 一级标题是否自动编号 `01`、`02`…… |
| | `leading` | `0.75em` | 行距（书刊用 `0.55em` 更合适）。 |
| | `quote-style` | `"amber"` | `"amber"` 奶油底琥珀左边条引用；`"green"` 浅绿卡片引用。 |
| `#cover(...)` | `kicker` / `title` / `sub` | `none` | 封面文字区。 |
| | `core-label` / `core` | `none` | 封面上白色"定位说明"卡片。 |
| | `meta` | `none` | 左下角补充信息行。 |
| | `decoration` | `"lines"` | `"lines"` 三条强调横线；`"disc"` 一个大浅色圆。 |
| `#card(...)` | `title` / `type` | `none` / `"gray"` | `type` 取 `gray`、`green`、`blue`、`cream`、`red`。 |
| `#badge(...)` | `level` | `"ok"` | `ok`、`warn`、`red`、`unk`，其它值渲染为蓝色信息徽章。 |
| `#check-item(...)` | `checked` | `false` | 勾选或未勾选的复选框清单项。 |
| `#timeline(...)` | — | — | 入参形如 `((日期, 名称), ...)`。 |

脚本用到的环境变量：

| 变量 | 使用者 | 含义 |
|---|---|---|
| `HTTPS_PROXY` / `HTTP_PROXY` | `typst` | 首次拉包用的代理。 |
| `TYPST_PATH` | `scripts/md_to_typst.py` | `typst` 可执行文件绝对路径。 |
| `PANDOC_PATH` | `scripts/md_to_typst.py` | `pandoc` 可执行文件绝对路径。 |

## Markdown 管线（可选）

`scripts/md_to_typst.py` 把一份 markdown 转成带主题的 PDF。它需要 `pandoc`（markdown → Typst）与 `typst`（Typst → PDF）；两个程序按 `--typst`/`--pandoc` → `$TYPST_PATH`/`$PANDOC_PATH` → `PATH` 的顺序查找。Python 3 标准库即可。

```bash
python scripts/md_to_typst.py notes.md notes.pdf \
  --title "文档标题" --date 2026-01-01 --footer "页脚运行文字" \
  --numbered
```

如果文件开头有 `---` 包裹的 frontmatter（`title:`、`created:`、`source:`），脚本会读取它，并在交给 pandoc 之前剥掉。脚本还会修掉几处 pandoc 数学转写器把符号粘连到相邻标识符的问题（见 `fix_body()`）。

## 已知局限

- **字体**：主题要求 `Microsoft YaHei`，回退 `Segoe UI`。在 Linux / macOS 上需要改那行 `set text(font: ...)`，可换成 `Noto Sans CJK SC` 或 `Source Han Sans`。
- **universe 包**（代码块用 `codly`，时间线与流程图用 `fletcher`）在首次编译时联网拉取。离线机器需要预先把它们放到本地 Typst 包目录下。
- **docx 是另一条路**。pandoc 的 Typst **读取器**解析不了 `@preview/...` 导入，所以从编译后的 `.typ` 转 docx 走不通。请保留 markdown 源作为 docx 源，把 Typst 只当作呈现目标。
- 配色是为低饱和、编辑感输出调的，不适合高对比 PPT 或按需印刷的色准要求。
- 验证环境：Typst **0.15.1**。

## 组件注意事项

- 表格：行要平铺写（每 `columns` 个单元格算一行）——Typst 0.15 不接受元组/数组当行。首列用 `1fr`，别用 `auto`；`auto` 首列会吞掉剩余宽度。
- `block` 用 `inset` 而不是 `padding`；`letter-spacing` 在 Typst 0.13 就被移除了。
- `include` **不**继承调用方作用域：被 include 的文件若要用组件，必须自己 `#import` 主题。pandoc 生成的正文不需要——它只用 Typst 内建函数。
- Typst 代码模式里嵌套的函数调用不加前置 `#`（即 `#grid(columns: ..., card(...))`）。
- 参数里含文字的场合优先传 `[...]` 内容而不是 `"..."` 字符串：字符串里的中文全角引号否则需要转义。

## 致谢

配色与组件思路参考 Notion 设计语言（暖白、低饱和、编辑感）。排版由 Typst 完成；代码高亮用 `codly`；图表用 `fletcher`（构建在 CeTZ 之上）。

## 许可证

MIT，见 `LICENSE`。作者署名：Inspired-by-Atmosphere。
