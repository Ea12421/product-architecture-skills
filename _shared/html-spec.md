# HTML Spec

> **触发读取条件**：用户在问题 4 选了 HTML 输出 → **已读 visual-styles.md** → 写任何 HTML/CSS 之前必读这份文件。
>
> 不涉及画箭头时不需要读 arrow-routing.md，但本文件里的"模块布局"和"工具栏"是箭头能正确路由的前提，所以总是先读这份再读 arrow-routing.md。
>
> **读完后自我确认**（强制）：在产出 HTML 前，用一句话向自己确认：
> "已阅读 html-spec.md，本次架构图布局是 [总体描述]，工具栏 60px 固定，左侧 80px 层名列，缩放用 zoom。**我已在 `<body>` 里规划了 `<div class="left-channel">`、`<div class="right-channel">`、`<svg class="arrows-svg">` 三个关键 DOM**——漏一个都会让 arrow-routing.md 的 MANDATORY CODE 静默失败。"
> 没做这句自我确认 = 视为未读，必须重读。

---

## §1 总体布局

产出一段完整的、独立可运行的 HTML 代码。结构：

```
┌────────────────────────────────────────────────────────────────────────┐
│ 顶部工具栏（60px 高，position:fixed）                                    │
│ [图标] 产品名  [+ 添加连接] [100%][75%][50%][Fit] [⬇ 下载修改后版本]      │
├────────────────────────────────────────────────────────────────────────┤
│ 主画布（无 hero、无大标题，直接进图）                                    │
│ ┌────┬────┬─────────────────────────────────────┬───────────────┐    │
│ │ 80 │ 60 │       主模块网格区（中间）            │  120px        │    │
│ │ px │ px │ ┌──┐┌──┐┌──┐┌──┐┌──┐               │  右侧通道     │    │
│ │ 层 │ 左 │ │触1││触2││触3││触4││触5│             │               │    │
│ │ 名 │ 通 │ └──┘└──┘└──┘└──┘└──┘               │  外延流目标   │    │
│ │ 列 │ 道 │ ┌──┐┌──┐┌──┐┌──┐┌──┐               │  badge 渲染   │    │
│ │    │    │ │场1││场2││场3││场4││场5│             │  在这里       │    │
│ │ 触 │    │ └──┘└──┘└──┘└──┘└──┘               │  （虚线边框） │    │
│ │ 达 │    │ ......                              │               │    │
│ │ 场 │    │                                     │  跨层箭头     │    │
│ │ 能 │    │                                     │  （偏右那部分）│    │
│ │ 数 │    │                                     │  也走这里     │    │
│ └────┴────┴─────────────────────────────────────┴───────────────┘    │
│                                                                        │
│  跨层箭头按 (from.cx+to.cx)/2 选左/右通道纵向走                          │
│  同层箭头走当前层下方 U 字（详见 arrow-routing.md §2）                   │
└────────────────────────────────────────────────────────────────────────┘
```

**关键约束**：
- **不要**任何 hero 区 / 大标题 / "PART 01" 分章 / 装饰性图形 / 产品介绍文字
- 打开页面**第一屏直接看到架构图**
- 4 层在 100% 缩放下尽量塞进一屏（塞不下则用 `Fit` 按钮自动缩放）
- 主画布**总宽度** = 80（层名）+ 60（左通道）+ 模块区 + 120（右通道）+ 左右各 20-32 边距

---

## §2 顶部工具栏（60px，固定不滚）

- `position: fixed; top: 0; left: 0; right: 0; height: 60px; z-index: 100;`
- 背景：`backdrop-filter: blur(20px)` + 当前风格背景色半透明（如风格 1 用 `rgba(15, 23, 42, 0.85)`），下方滚动时仍清晰
- **左侧**（约占 30% 宽）：产品图标 + 产品名（如"豆包产品架构"），字号 16-18px / font-weight 600，**可编辑**
- **中间**：`+ 添加连接` 按钮 + 缩放按钮组 `100%` `75%` `50%` `Fit`
- **右侧**：`⬇ 下载修改后版本` 按钮（用当前风格的主题色作为按钮背景，圆角按钮）

---

## §3 左侧 80px 层名列 + 60px 左通道

### 3.1 层名列（最左 80px）
- 紧贴主画布最左侧，宽度固定 80px
- 4 个层名纵向排列，每个层名对齐到对应层的中线
- 字号 18-22px，font-weight 700
- **不要旋转 90°**——用横向排版填满 80px 列宽，更易读
- 颜色：用所在层的主色（如触达层用 `#A78BFA`，参考 visual-styles.md 中选定风格的 4 层色）

### 3.2 左通道（紧跟层名右侧 60px）⚠️ v1.2.3 改为隐形 DOM
- **必须是实体 DOM 元素** `<div class="left-channel">`（作为坐标定位区，arrow-routing.md MANDATORY CODE 依赖它存在）
- 用途：跨**≥2 层**的箭头中"源和目标都偏左"那部分纵向通行
- 中心 x 坐标 = `80 + 30 = 110px`
- **CSS 默认完全透明**（v1.2.3）：
```css
.left-channel {
  position: absolute;
  left: 80px;
  width: 60px;
  top: 0;
  bottom: 0;
  border: none;
  background: transparent;
  pointer-events: none;  /* 不阻挡鼠标事件 */
}
```
- HTML 结构示例：
```html
<div class="left-channel"></div>
```
- **不加任何标签**——通道是"几何概念区"，对用户透明，只对 path 算法存在
- 如果整张图所有跨 ≥2 层的箭头都偏右，可以**不建立**左通道 DOM（详见 §3.5.3）

---

## §3.5 右侧 120px 通道（含外延流 badge）

### 3.5.1 通道本身 ⚠️ v1.2.3 改为隐形 DOM
- **必须是实体 DOM 元素** `<div class="right-channel">`（作为坐标定位区 + 外延 badge 容器）
- 画布最右侧，宽度 120px
- 中心 x 坐标 = `areaWidth - 60`
- 用途：
  - 跨 **≥2 层**的箭头中"源和目标都偏右"那部分纵向通行
  - **所有外延流的目标 badge** 渲染在内
- **CSS 默认完全透明**（v1.2.3）：
```css
.right-channel {
  position: absolute;
  right: 0;
  width: 120px;
  top: 0;
  bottom: 0;
  border: none;
  background: transparent;
}
.right-channel .external-badge {
  pointer-events: auto;  /* badge 自己要响应事件 */
}
```
- **不加通道标签**——通道对用户透明
- 即使没有跨多层箭头，**只要有外延流就必须建立**（外延流 badge 渲染在内）

### 3.5.2 外延 badge 渲染
- 每个外部系统（如 ERP / CRM）渲染成一个**虚线边框**的 badge 元素
- 跟所在层的 y 坐标对齐（layer-scene 的外延 badge 就跟场景层中线对齐）
- HTML 结构示例：
```html
<div class="right-channel">
  <div id="__external_erp__" class="external-badge" style="top: <layer-scene.offsetTop>px;">
    ERP / CRM
  </div>
</div>
```
- CSS：`.external-badge` 用 `border: 1px dashed <主色>;` + 比主模块**浅一档的背景**，跟主模块视觉区分
- 由 `renderExternalBadges()` 函数在页面加载时渲染，详见 `arrow-routing.md §6 陷阱 3`

### 3.5.3 通道何时存在
- **左通道**：当 `autoArrows + userArrows` 里存在**跨 ≥2 层且偏左**的箭头时建立
- **右通道**：当存在**跨 ≥2 层且偏右**的箭头 **或** 任何**外延流**时建立
- 如果整图箭头都是相邻层连接 + 没外延流：**两条通道都不建立**（避免空通道占空间）
- 通道存在与否在初始化时静态决定，**不动态切换**

---

## §4 模块视觉（药丸形顶部标签）

每个模块容器：
- 圆角按选定风格执行（参考 visual-styles.md：风格 1=8px / 风格 2=12px / 风格 3=4px / 风格 4=0px）
- 背景色比所在层略浅
- 模块名做成**药丸形（pill-shaped）标签悬浮在容器顶部边缘**：
  - `border-radius: 999px`
  - 背景用浅一点的纯色
  - padding `4px 12px`
  - 字号 14px / font-weight 600
- 模块内容用 bullet 列表，字号 12-13px，行距 1.6

---

## §5 架构图下方分析内容（**仅渲染规则**）

**HTML 必须包含完整的文字分析内容**，不能只是一张孤零零的架构图。结构：

```
┌─────────────────────────────────┐
│ 工具栏（60px 固定）              │
├─────────────────────────────────┤
│                                 │
│  4 层架构图（占第一屏，约 90vh）  │
│                                 │
├─────────────────────────────────┤
│                                 │  ← 用户向下滚动可见
│  文字分析内容（具体内容由主 SKILL.md │
│  工作流决定,本文件不重复）           │
│                                 │
└─────────────────────────────────┘
```

**渲染规则（不论分析内容是 PRD 要点还是 5 部分立项方案，下列规则都适用）**：

- 整体配色和上面的架构图风格保持一致（同一个 style preset，参考 visual-styles.md）
- 每个分析章节用 `<h2>` 标题（如"业务背景与需求"），下方为段落文字
- 章节之间留 **48-64px 间距**
- 段落文字字号 14-15px，行距 1.7
- **整段分析内容最宽 720px 居中**，不要顶满全宽（阅读体验差）
- 标题用所选风格的强调色
- 引用 / 关键数字用所选风格的强调色高亮
- 章节之间可以加一条细分隔线（颜色用主色 20% 透明度）

> ⚠️ **本文件不写"分析内容里要写什么"**。具体内容结构（路径 A 的 PRD 要点 / 路径 B 的 5 部分立项方案）由主 SKILL.md 工作流单一来源决定。本文件只负责"内容如何呈现在 HTML 里"。

---

## §6 缩放控制

工具栏中间的缩放按钮组：`100%` `75%` `50%` `Fit`，默认 100%（当前选中态高亮）。

**实现：用 CSS `zoom` 属性，不用 `transform: scale()`**

两个原因，按重要性排序：

1. **`contenteditable` 光标位置**：在 `transform: scale()` 缩放下，contenteditable 元素的光标位置会偏（浏览器已知 bug），用户编辑文字时点击位置和光标实际落点错位。`zoom` 不破坏 contenteditable。**这是必须选 zoom 的硬理由。**

2. **滚动条范围**：`transform: scale()` 不改变元素的盒模型占位，缩小后视觉内容在原占位的中心区域（默认 transform-origin 是 50% 50%），视觉之外是空的，滚动条范围不变。`zoom` 改变实际尺寸，滚动条自适应。

**实现**：
```javascript
// 100% / 75% / 50% 按钮
document.querySelector('.main-canvas').style.zoom = N;  // N = 1 / 0.75 / 0.5

// Fit 按钮：JS 计算适配视口的比例
const ratio = (window.innerHeight - 60) / canvas.scrollHeight;
document.querySelector('.main-canvas').style.zoom = ratio;
```

**缩放后不需要禁用 contenteditable**（zoom 不会破坏光标位置）。

---

## §7 可编辑要求

- 所有文字元素（层名、模块名、模块内容、箭头标签、产品名）加 `contenteditable="true"`
- 文字元素 hover 时给浅色背景提示用户可编辑（如 `:hover { background: rgba(255,255,255,0.05); }`）

---

## §8 下载功能

- 工具栏右侧的 `⬇ 下载修改后版本` 按钮
- 点击 → JavaScript 用 `document.documentElement.outerHTML` 拿当前完整 DOM → 用 Blob + URL.createObjectURL → 触发浏览器下载
- 文件名格式：`产品架构_[产品名]_[YYYYMMDD-HHmm].html`
- **关键**：序列化前要把用户的所有修改（编辑过的文字、加的箭头、加的标签）确认已经反映到 DOM 上

```javascript
function downloadHTML() {
  // 确保所有 contenteditable 修改已 commit 到 DOM
  document.activeElement && document.activeElement.blur();
  
  const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  
  const now = new Date();
  const stamp = now.toISOString().slice(0,16).replace(/[-:T]/g,'').slice(0,12);
  const productName = document.querySelector('.product-name').textContent;
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `产品架构_${productName}_${stamp}.html`;
  a.click();
  URL.revokeObjectURL(url);
}
```

---

## §9 与 web-design skill 协作（可选）

如果检测到项目里已存在 `DESIGN.md`（通常是 web-design skill 的产物），**优先读取**里面的色板 / 字体 / 密度 token 替换 visual-styles.md 中的视觉基线，让架构图视觉和项目其他页面统一。

DESIGN.md 不存在时按 visual-styles.md 中选定风格的基线产出。

---

## §10 适配两种环境

- **在 claude.ai 里**：作为 artifact 渲染，用户直接交互、点下载按钮
- **在 Claude Code / Codex 等环境里**：把完整 HTML 代码贴给用户，告诉用户"保存为 .html 文件后用浏览器打开即可"

两种环境下 HTML 代码完全相同，无需做环境检测。

---

## §11 HTML 专项自检（产出 HTML 前过一遍）

- [ ] 顶部 60px 工具栏 `position: fixed`，向下滚动时仍可见
- [ ] 打开页面**第一屏直接看到架构图**，无任何 hero / 大标题 / 装饰区挡路
- [ ] 4 层在 100% 缩放下尽量在一屏内可见
- [ ] 左侧 80px 层级标签清晰、字号大、横向不旋转
- [ ] 左侧 80px 层名列**右侧紧跟 60px 左通道**——**实体 DOM 但 CSS 默认透明**（v1.2.3：作为坐标定位区，对用户不可见），仅当存在跨 ≥2 层左偏箭头时建立
- [ ] 画布**最右侧有 120px 右通道**——**实体 DOM 但 CSS 默认透明**（同上），当存在跨多层右偏箭头 或 外延流时建立
- [ ] 如果有外延流：右通道里有真实 `.external-badge` DOM，**虚线边框**，跟所在层 y 对齐
- [ ] 模块名为药丸形（pill）顶部标签
- [ ] **架构图下方有完整的分析文字内容**（路径 A 的 PRD 要点 / 路径 B 的多部分立项方案）
- [ ] 分析内容最宽 720px 居中，不顶满全宽
- [ ] **缩放使用 CSS `zoom: N`，不用 `transform: scale()`**
- [ ] `+ 添加连接` 按钮有清晰的"开启 / 关闭"两态
- [ ] 所有文字元素加了 `contenteditable="true"`，hover 时有视觉提示
- [ ] 下载下来的 HTML 包含用户所有修改（开新窗口打开能看到加的箭头和编辑的文字）
- [ ] 没用 Tailwind 默认灰白卡片风格

> ⚠️ 涉及箭头的自检项（三通道选择、垂直进出、通道内错位、label 位置、外延 badge 实现）在 `arrow-routing.md` §8 自检节里，不在本文件重复。
