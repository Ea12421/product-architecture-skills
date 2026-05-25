# Product Architecture Skills

一套用于 AI 产品架构搭建与逆向拆解的 Agent Skills。基于 4 层骨架（数据 / 能力 / 场景 / 触达）+ 数据流转方法论。

兼容所有支持 Agent Skills 开放标准的客户端：Claude Code（CLI 和 IDE 扩展）、claude.ai、Cursor、Codex CLI、Gemini CLI、GitHub Copilot 等。

## 包含的 Skills

| Skill | 中文名 | 用途 |
|-------|--------|------|
| product-architecture-build | 产品架构搭建 | 从 0 搭建 AI 产品的架构图或完整立项方案 |
| product-architecture-teardown | 产品架构拆解 | 逆向拆解已有 AI 产品的架构（六步法） |

两个 skill 互相独立，可单独安装。

---

## 安装方法

### 🌟 通用方法（推荐，所有客户端都能用）

不依赖任何特殊命令、不需要权限授权、不依赖 marketplace 机制，只是把 SKILL.md 所在的文件夹拷到你 AI 客户端的 skills 目录里。

```bash
# 1. 克隆仓库
git clone https://github.com/Ea12421/product-architecture-skills.git
cd product-architecture-skills

# 2. 拷到 AI 客户端的 skills 目录
#    Claude Code（CLI 或 IDE 扩展通用）：
cp -r product-architecture-build/skills/product-architecture-build ~/.claude/skills/
cp -r product-architecture-teardown/skills/product-architecture-teardown ~/.claude/skills/

# 3. 重启 AI 客户端
```

⚠️ **v1.1 起 skill 内部新增 `references/` 子目录**，上面的 `cp -r` 会自动把整个 skill 文件夹（包含 references/）拷过去，无需额外操作。

**不同客户端的 skills 目录路径**：

| 客户端 | 路径 |
|--------|------|
| Claude Code（CLI 或 IDE 扩展） | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills-cursor/` |
| Codex CLI | `~/.codex/skills/` |
| 其他 | 查阅各自客户端文档 |

只要把上面 `cp` 命令的目标路径换成对应客户端的目录即可。

---

### 方法 B：Claude Code CLI 一键 marketplace 安装

> ⚠️ **此方法仅适用于 Claude Code 终端 CLI**。VSCode/Cursor 扩展、claude.ai 网页等图形客户端**不支持** `/plugin` 命令，请用上面的"通用方法"。

在 Claude Code CLI 会话里跑：

```
/plugin marketplace add Ea12421/product-architecture-skills
/plugin install product-architecture-build@product-architecture-skills
/plugin install product-architecture-teardown@product-architecture-skills
```

两个 skill 可单独装，只装一个跳过对应那行即可。

---

### 方法 C：claude.ai 网页（.skill 上传）

claude.ai 不支持 git clone 也不支持 URL 安装，必须走 web UI：

1. 下载需要的 `.skill` 文件（在 GitHub 上点开文件，右上角 `Download raw file`）：
   - [`dist/product-architecture-build.skill`](./dist/product-architecture-build.skill)
   - [`dist/product-architecture-teardown.skill`](./dist/product-architecture-teardown.skill)
2. 打开 [claude.ai](https://claude.ai) → `Customize` → `Skills`
3. 点 `+ Create skill` → 上传 `.skill` 文件
4. 在 skill 列表里打开开关

> ⚠️ claude.ai 上使用 skills 需要先在 Settings 里开启 `Code execution and file creation`。详见 <https://support.claude.com/en/articles/12512180-use-skills-in-claude>
>
> ℹ️ `.skill` 是 Anthropic 官方推荐的 skill 打包格式，本质是 ZIP。v1.0 时使用 `.zip` 扩展名，v1.1 起改用官方 `.skill` 格式（用 Anthropic 官方 `package_skill.py` 打包生成）。

---

### 方法 D：Codex CLI

```
$skill-installer install https://github.com/Ea12421/product-architecture-skills/tree/main/product-architecture-build/skills/product-architecture-build
$skill-installer install https://github.com/Ea12421/product-architecture-skills/tree/main/product-architecture-teardown/skills/product-architecture-teardown
```

重启 Codex 后生效。

---

## product-architecture-build（产品架构搭建）

### 它能做什么

帮你从 0 到 1 搭建 AI 产品的整体架构。覆盖三种场景（中大型公司 / 小公司创业 / 个人项目），两种路径（仅架构图 / 完整 5 部分立项方案），三种产出形态（文字 / Mermaid / HTML 可视化）。

### 什么时候用

- 想搭建/设计一个 AI 产品的架构
- 想画 4 层架构图（数据/能力/场景/触达）
- 想撰写 AI 产品的立项方案/项目方案
- 想从 0 到 1 把一个产品的整体结构想清楚

### 什么时候不用

- UI/UX 设计、页面交互（属于信息架构）
- 单纯写 PRD（你没明确要求架构图或立项方案）
- 技术栈选型、代码实现细节（属于技术架构）
- 早期需求探索 / 功能 brainstorm（产品还没想清楚）
- 单个功能模块的设计（产品架构是全局视角）
- 想分析/拆解已有产品（用 teardown skill）

### 触发示例

- "帮我搭建一个面向制造业的 AI 售后客服的产品架构"
- "我要给老板写一份 AI 客服项目的完整立项方案"
- "画一个 AI 法律助手的 4 层架构图"
- "我想做一个个人用的读书笔记 AI 工具，给自己出份方案算笔账"

### 产出形态

- 文字结构化说明
- Mermaid 架构图代码
- HTML 可视化（**文字可编辑** + 带「下载修改后版本」按钮）

---

## product-architecture-teardown（产品架构拆解）

### 它能做什么

帮你逆向拆解已有 AI 产品的整体架构。通过六步反向追问法（体验 → 穷举 → 归类 → 反推能力 → 反推数据 → 画图），把任意产品装进 4 层骨架。两种深度（快速概览 / 完整六步法）、两种目的（深度研究学习 / 找竞品机会）。

### 什么时候用

- 想拆解/逆向/分析某个 AI 产品的架构
- 想看懂一个产品由哪些业务模块组成
- 想找参考产品的薄弱环节作为竞品切入点
- 想用六步法或 4 层骨架做产品复盘

### 什么时候不用

- 单纯的功能对比、feature 清单对比
- UI/UX 评测、界面体验评价
- 技术栈分析、技术实现猜测
- 商业模式 / 盈利模式分析
- 用户画像 / 市场调研
- 产品发展史 / 版本迭代分析
- 想搭建自己的新产品（用 build skill）

### 触发示例

- "拆解一下豆包的产品架构"
- "用六步法分析 Mem.ai 的架构"
- "帮我找一下 Notion AI 的薄弱模块作为差异化切入点"
- "快速看一下 ChatGPT 的 4 层骨架"

### 产出形态

- 文字结构化说明（Claude 推测部分自动标 `[推测]`）
- Mermaid 架构图代码
- HTML 可视化（**文字可编辑** + 推测内容虚线框标注 + 带「下载修改后版本」按钮）

---

## 文件结构

```
product-architecture-skills/                         ← 仓库根（也是 marketplace 根）
├── .claude-plugin/
│   └── marketplace.json                             ← Claude Code marketplace 索引
├── README.md
├── LICENSE
├── _shared/                                         ← v1.1 新增：共享 references 单一来源
│   ├── visual-styles.md                             ←   4 风格色板 + 通用视觉原则
│   ├── html-spec.md                                 ←   HTML 静态产出规范
│   └── arrow-routing.md                             ←   箭头路由 + 添加/删除交互
├── scripts/                                         ← v1.1 新增：工具脚本
│   ├── sync_references.py                           ←   把 _shared/ 同步到两个 skill 的 references/
│   ├── validate_and_sync.py                         ←   sync + 校验的 wrapper
│   ├── quick_validate.py                            ←   Anthropic 官方校验器（复制进 repo）
│   └── package_skill.py                             ←   Anthropic 官方打包工具（复制进 repo）
├── .pre-commit-config.yaml                          ← v1.1 新增：pre-commit hook 配置
├── product-architecture-build/                      ← 第 1 个 plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── product-architecture-build/
│           ├── SKILL.md                             ← 主 skill 文件（薄）
│           └── references/                          ← v1.1 新增：从 _shared/ sync 而来
│               ├── visual-styles.md
│               ├── html-spec.md
│               └── arrow-routing.md
├── product-architecture-teardown/                   ← 第 2 个 plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── product-architecture-teardown/
│           ├── SKILL.md
│           └── references/
│               ├── visual-styles.md                 ←   sync 自 _shared/
│               ├── html-spec.md                     ←   sync 自 _shared/
│               ├── arrow-routing.md                 ←   sync 自 _shared/
│               └── speculation-markers.md           ←   teardown 专属，不 sync
└── dist/
    ├── product-architecture-build.skill             ← 给 claude.ai 上传用（v1.1 从 .zip 改为 .skill）
    └── product-architecture-teardown.skill          ← 同上
```

**为什么是这种嵌套结构**：仓库同时支持四种安装方式，所以同一份 SKILL.md 需要在不同位置可被找到。

- **通用方法（手动 cp）**：拷 `product-architecture-<build|teardown>/skills/<同名子文件夹>/`（含 references/）
- **Claude Code marketplace**：识别仓库根的 `.claude-plugin/marketplace.json` 自动定位
- **claude.ai**：用 `dist/` 里的扁平 `.skill` 文件
- **Codex CLI**：用上面给的 GitHub URL

---

## 维护者指南（v1.1 新增）

> 如果你只是想**使用**这两个 skill，到上面"安装方法"为止就够了。本节只对**想修改这两个 skill 内容**的人有用。

### 单一来源原则

v1.1 起，两个 skill 的 `references/` 子目录里 3 份共享 reference（`visual-styles.md` / `html-spec.md` / `arrow-routing.md`）**不要直接编辑**——它们顶部都有 `<!-- AUTO-GENERATED from _shared/. Do not edit here. -->` 注释。

**所有修改都改 `_shared/<对应文件>`，然后跑 sync 脚本同步到两个 skill。**

teardown 专属的 `speculation-markers.md` 不由 sync 管理，直接在它原位置编辑即可。

### Prerequisites（运行 scripts/ 下任何工具前）

- **Python 3.7+**
- **PyYAML**（`quick_validate.py` 依赖）：`pip3 install pyyaml`
- **pre-commit**（可选，启用 hook 才需要）：`pip3 install pre-commit`

### 常用命令

所有命令都**必须从仓库根目录（这个 README 所在目录）跑**，因为脚本用 `python3 -m scripts.xxx` 的模块语法（必须能找到 `scripts` 包）。

```bash
# 1. 改了 _shared/ 之后，把改动同步到两个 skill 的 references/
python3 scripts/sync_references.py

# 2. 校验单个 skill 是否符合 Anthropic Skills 规范（先 sync，再校验）
python3 -m scripts.validate_and_sync product-architecture-build/skills/product-architecture-build
python3 -m scripts.validate_and_sync product-architecture-teardown/skills/product-architecture-teardown

# 3. 打包成 .skill 文件供 claude.ai 上传
python3 -m scripts.package_skill product-architecture-build/skills/product-architecture-build dist/
python3 -m scripts.package_skill product-architecture-teardown/skills/product-architecture-teardown dist/
```

⚠️ **注意 `-m` 语法**：必须用 `python3 -m scripts.package_skill ...`，**不能**用 `python3 scripts/package_skill.py ...`，否则会报 `ModuleNotFoundError: No module named 'scripts'`（因为 `package_skill.py` 内部有 `from scripts.quick_validate import validate_skill`，需要 Python 把 `scripts/` 识别为包）。

### pre-commit hook（可选，自动跑 sync）

装上后，每次 `git commit` 会自动跑 `sync_references.py`。**双保险**：即使忘了手动 sync，commit 前也会同步。

```bash
# 一次性安装
pip3 install pre-commit
pre-commit install

# 验证
git commit --allow-empty -m "test"   # 应该看到 sync 自动跑
```

如果 pre-commit 装失败，本仓库主流程不受影响——`validate_and_sync.py` 在每次校验前都会先 sync，是 95% 覆盖的安全网。

### 改一份共享 reference 的完整流程

```
1. 改 _shared/visual-styles.md（或其他共享文件）
2. python3 scripts/sync_references.py           # 同步到两个 references/
3. python3 -m scripts.validate_and_sync \
      product-architecture-build/skills/product-architecture-build
4. python3 -m scripts.validate_and_sync \
      product-architecture-teardown/skills/product-architecture-teardown
5. python3 -m scripts.package_skill \
      product-architecture-build/skills/product-architecture-build dist/
6. python3 -m scripts.package_skill \
      product-architecture-teardown/skills/product-architecture-teardown dist/
7. git add -A && git commit -m "..."             # pre-commit hook 再次跑 sync 兜底
8. git push
```

---

## 更新日志

- **v1.1** (2026-05-15) — references 架构重构：把 monolithic SKILL.md 拆成"主文件 + references"结构，引入 `_shared/` 单一来源 + sync 脚本 + 双保险 (`validate_and_sync` + pre-commit hook)。dist/ 文件扩展名从 `.zip` 改为 `.skill`（Anthropic 官方推荐格式）。顺手修复 v4 bug：开场 5 问统一（v4 标题写 4 问/正文 5 问的矛盾）、`transform: scale` 错误描述（实际原因是 contenteditable 光标偏移 + 滚动条范围）。维护性提升（改色板只动一处），HTML 输出场景 token 加载 +7%（接受，换可维护性）。
- **v1.0.1** (2026-05-14) — README 修订：通用 git clone + cp 安装方式提升为推荐方法。明确 `/plugin` 命令的客户端限制。所有用户名占位符替换为实际值。
- **v1.0** (2026-05-14) — 初版发布。两个 skill：搭建 + 拆解。基于 4 层骨架方法论。同时作为 Claude Code Plugin Marketplace 分发。

---

## License

[MIT](./LICENSE)
