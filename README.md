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

### 方法 C：claude.ai 网页（ZIP 上传）

claude.ai 不支持 git clone 也不支持 URL 安装，必须走 web UI：

1. 下载需要的 ZIP（在 GitHub 上点开文件，右上角 `Download raw file`）：
   - [`dist/product-architecture-build.zip`](./dist/product-architecture-build.zip)
   - [`dist/product-architecture-teardown.zip`](./dist/product-architecture-teardown.zip)
2. 打开 [claude.ai](https://claude.ai) → `Customize` → `Skills`
3. 点 `+ Create skill` → 上传 ZIP
4. 在 skill 列表里打开开关

> ⚠️ claude.ai 上使用 skills 需要先在 Settings 里开启 `Code execution and file creation`。详见 <https://support.claude.com/en/articles/12512180-use-skills-in-claude>

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
├── product-architecture-build/                      ← 第 1 个 plugin
│   ├── .claude-plugin/
│   │   └── plugin.json                              ← Plugin manifest
│   └── skills/
│       └── product-architecture-build/
│           └── SKILL.md                             ← 实际的 skill 内容（手动安装拷这个文件夹）
├── product-architecture-teardown/                   ← 第 2 个 plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── product-architecture-teardown/
│           └── SKILL.md
└── dist/
    ├── product-architecture-build.zip               ← 给 claude.ai 上传用（扁平结构）
    └── product-architecture-teardown.zip            ← 同上
```

**为什么是这种嵌套结构**：仓库同时支持四种安装方式，所以同一份 SKILL.md 需要在不同位置可被找到。

- **通用方法（手动 cp）**：拷 `product-architecture-<build|teardown>/skills/<同名子文件夹>/`
- **Claude Code marketplace**：识别仓库根的 `.claude-plugin/marketplace.json` 自动定位
- **claude.ai**：用 `dist/` 里的扁平 ZIP
- **Codex CLI**：用上面给的 GitHub URL

---

## 更新日志

- **v1.0.1** (2026-05-14) — README 修订：通用 git clone + cp 安装方式提升为推荐方法。明确 `/plugin` 命令的客户端限制。所有用户名占位符替换为实际值。
- **v1.0** (2026-05-14) — 初版发布。两个 skill：搭建 + 拆解。基于 4 层骨架方法论。同时作为 Claude Code Plugin Marketplace 分发。

---

## License

[MIT](./LICENSE)
