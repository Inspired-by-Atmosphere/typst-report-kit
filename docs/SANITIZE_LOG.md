# Sanitize log

Source directory and provenance are recorded at the category level only; original
values are deliberately **not** recorded here (not even as hashes).

| 类别 | 条数 | 处理动作 |
|---|---|---|
| 内部项目名（文档标题 / 页脚运行文字） | 5 | 删除；页脚默认文字改为 `report()` 的 `doc-footer` 参数，默认 `none` |
| 组织名（院校 / 团队 / 竞赛名） | 6 | 替换为 `your-org` / `your-team` 占位 |
| 人物署名 | 2 | 替换为 `your-name` 占位 |
| 本机绝对路径（项目盘、用户目录、工具安装目录） | 9 | 删除；改为仓库内相对路径，或改为 `--flag` / `$ENV_VAR` 参数 |
| 内部文件用途字符串（scratch 目录名、内部库名） | 3 | 删除；相关脚本整体不收录（见下） |
| 内部文档正文（作册正文、笔记转换产物） | 4 | 不收录；示例改用占位文本 |
| 二进制产物（PDF / PNG / DOCX / 编译器 / 压缩包） | 7 | 不收录；README 只写官方安装指引 |
| 备份文件（`*.bak_*`） | 1 | 不收录；已写入 `.gitignore` |
| 中间产物与试验文件（wrapper / test / build 临时目录） | 10 | 不收录；相关规则写入 `.gitignore` |
| 第三方 clone 代码（外部作者的 Typst 库及主题文件） | 12 | 不收录（第三方版权，非自研）；依赖它的脚本一并排除 |
| 内部依赖引用（头部注释中指向内部示例文件名） | 2 | 改写为仓库内示例路径 |
| 注释内的用户会话措辞、日期与偏好记述 | 4 | 删除，改为中性技术说明 |
| 凭证 / 密钥 / 令牌 | 0 | 未发现 |
| 内网 IP / MAC / 主机名 | 0 | 未发现（README 中的回环代理地址为通用本地示例，非内网拓扑） |
| 真实邮箱 / QQ / 学号 | 0 | 未发现 |

## Excluded files and why

| 文件类别 | 排除理由 |
|---|---|
| 示例成品报告源文件及其 PDF | G3：含内部项目结论与真实业务内容 |
| 内部验证报告源文件及其 PDF | G3：竞赛/团队验证材料 |
| 书籍构建目录中的正文与渲染产物 | G3 + 大文件：真实内部正文、PDF、PNG、DOCX |
| 第三方 clone 的 Typst 库目录 | G1：非自研代码 |
| 官方编译器可执行文件与压缩包（约 74 MB） | 大文件；README 改为指向官方下载页 |
| 试验/中间文件（`wrapper*.typ`、`min_test*`、`test*`、`*_build/`） | 无价值中间产物 |
| `*.typ.bak_*` 备份 | 备份文件禁止提交 |

## License

MIT (default). No third-party source code is redistributed: `codly` and
`fletcher` are consumed as Typst universe **packages** (fetched by the Typst
package manager at build time, not vendored into this repository), so no third
party's source tree is copied here.
