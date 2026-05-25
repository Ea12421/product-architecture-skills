# Arrow Routing

> **触发读取条件**：当前任务涉及画自动箭头 / 处理"添加连接"交互 / 处理"删除箭头"交互 → **写任何 SVG path 之前必读这份文件**。
>
> **前置依赖**：html-spec.md 中的 **三通道布局**（左侧 80px 层名列 + 60px 左通道 + 模块区 + 120px 右通道）是箭头能正确路由的前提，应先读 html-spec.md 再读本文件。
>
> ## ⚠️ 核心实施约束（v1.2.3 修订）
>
> 本文件 §2 包含一段 **MANDATORY CODE BLOCK**（必须原样复制的完整 JS 代码）。**这是过去 5 轮迭代失败的根因**——AI 看到伪代码后习惯"理解再重写"，重写时几何细节会按训练惯性偏离，导致跨层箭头不走侧边通道。
>
> **v1.2.2 关键变化**：**不是所有跨层箭头都走通道**——相邻层（跨 1 层）直接连，跨多层（跨 ≥2 层）才走可见的侧边通道。详见 §2.0 通道使用规则。
>
> **v1.2.3 新增**：
> - 外延流改用 `pathExternalBelow`（从源底边出，走层底下方水平带）—— 避免横线穿过中间模块
> - 加 `incomingUsage` 错位 —— 多条跨层箭头汇入同一目标时末段不重合
> - 加 "-1 级 DOM 前置核查" —— 防 left-channel / right-channel / arrows-svg 漏写导致静默失败
>
> **本次强约束**：
> - §2 MANDATORY CODE BLOCK 必须**逐字符复制**到 HTML 的 `<script>` 标签内
> - **不允许**重写、简化、合并、改函数名、改常量值、改 `layerSpan === 1` 的阈值判断
> - 你只负责在 `autoArrows` 数组里填业务数据（`from` / `to` / `label`），其余几何计算全部由 CODE BLOCK 处理
>
> ## 读完后自我确认（强制）
>
> 在写任何 SVG path 之前，逐条向自己确认：
>
> 1. "已阅读 arrow-routing.md，关键约束是：跨层走左/右通道、同层走 U 字、起终点段垂直、通道内多箭头错位、外延流必须有真实 badge DOM。"
> 2. "我将把 §2 MANDATORY CODE BLOCK **原样复制**到 HTML 内，不会重写 `pickChannel` / `pathDirect` / `pathThroughChannel` / `pathSameLayerU` / `pathExternalBelow` / `buildArrowPath` 这 6 个函数。"
> 3. "我只在 `autoArrows` 数组、`externalSystems` 数组、模块/层 DOM 结构里填业务内容。"
>
> 没做这 3 条自我确认 = 视为未读，必须重读。

---

## §1 自动数据流转箭头规格

**只画 3-5 条主流转箭头**，不细化到每个模块：

- 沉淀流：触达层 → 数据层（用户行为沉淀）— **必有**
- 回补流：数据层 → 上层（加工后回补）— **必有**
- 可选追加：外延流（连到层外部，如 CRM、第三方系统，**走右通道，目标 badge 必须真实渲染在右通道里**）

**箭头视觉规格**：

| 项 | 规格 |
|---|---|
| 形状 | SVG `<path>` cubic bezier 曲线。**绝对不要**直线、**绝对不要**直角拐弯 |
| 颜色 | 中性灰 `#94A3B8`（赛博风用 `#FF00FF`，其他风格按 visual-styles.md 强调色） |
| 粗细 | `stroke-width: 1.5px` |
| 箭头头部 | 用 SVG `<marker>` 定义三角形 |
| 标签 | 贴在曲线的水平段或纵向段中段，背景加半透明色块衬底防遮挡 |
| 标签字号 | 12px / font-weight 500 |

---

## §2 三通道路由（核心）⚠️

**核心思想**：所有箭头都走专属"通道"，不挤压模块空间，避免穿过模块卡片。三类通道：

### 2.0 通道使用规则 ⚠️ v1.2.2 关键变化

**不是所有跨层箭头都走通道**——这是过度工程。只有"跨度大、需要绕路解释"的箭头才走通道：

| 箭头类型 | 处理方式 |
|---|---|
| **跨 ≥2 层**（如触达→能力、触达→数据） | 走通道 A 或 B（按 midX 选边）—— 走可见通道 |
| **跨 1 层**（相邻层，如触达→场景） | **直连** `pathDirect()`：从源 cx 直接 bezier 到目标 cx，不走通道 |
| **同层** | 走通道 C U 字（在层底下方水平绕，保护中间模块） |
| **外延流**（连到 ERP/CRM 等右通道 badge） | 走通道 B + 真实 badge DOM（不论跨几层） |

**判断"跨几层"**：`Math.abs(fromLayerIdx - toLayerIdx)`，1 是相邻、≥2 是跨多层。

### 2.1 通道 A：左侧通道（60px 宽）

- **位置**：左侧 80px 层名列**右边**，宽 60px。中心 x ≈ `80 + 30 = 110px`
- **谁走这里**：跨层箭头，且**源和目标都偏左**——`(fromRect.cx + toRect.cx) / 2 < areaWidth / 2`
- **path 形状**：source 模块**底/顶边**出 → 反向水平到左通道 → 沿通道纵向 → 正向水平到 target **顶/底边**

### 2.2 通道 B：右侧通道（120px 宽，含外延 badge）

- **位置**：画布最右侧，宽 120px。中心 x ≈ `areaWidth - 60`
- **谁走这里**：
  - 跨层箭头，且源和目标都偏右：`(fromRect.cx + toRect.cx) / 2 ≥ areaWidth / 2`
  - **所有外延流**——目标 badge 直接渲染在右通道内
- **path 形状**：跟通道 A 镜像

### 2.3 通道 C：同层 U 字（当前层底部下方 20px）

- **位置**：源和目标所在层的**底边下方 20px** 处的水平带（在层内部，不超出当前层）
- **谁走这里**：同层连接（`fromLayer === toLayer`）
- **path 形状**：U 字——source **底边**出 → 向下 22px 起点段 → bezier 弯到下方水平带 → 水平横过去 → bezier 弯入 target → 向下 22px 终点段，回到 target **底边**

### 2.4 MANDATORY CODE BLOCK ⚠️（必须原样复制到 HTML）

**这是 v1.2.1 核心强约束（v1.2.2 扩展）**。下面这段 JS 代码必须**逐字符复制**到你产出的 HTML 的 `<script>` 标签内。

**不允许做的事**：
- ❌ 重写、简化、合并任何函数
- ❌ 改函数名（`pickChannel` / `pathDirect` / `pathThroughChannel` / `pathSameLayerU` / `pathExternalBelow` / `buildArrowPath` 必须保留 **6 个**）
- ❌ 改常量值（`LAYER_NAME_WIDTH` / `LEFT_CHANNEL_WIDTH` / `RIGHT_CHANNEL_WIDTH` / `SEG_LEN` / `U_DEPTH`）
- ❌ 改 bezier 控制点公式
- ❌ 把多个函数合并成一个"通用"path 函数
- ❌ 改 `pickChannel` 里 `layerSpan === 1` 的判断条件（这是"相邻层直连"的核心阈值，改了就回到 v1.2.0 的过度工程）
- ❌ 把外延流改回水平横线 path（v1.2.3 已确认横线在源远离 badge 时必穿模块——只能走 below）

**允许微调的事**：
- ✅ `getLayerIdx()` 里的层 id 数组可以按你实际的 DOM 层 id 改（如改成 `['touch', 'scene', 'capability', 'data']`）
- ✅ `getRect()` 内部如果你的 DOM 选择器不是 `.canvas-inner`，可以改选择器名——但**输入/返回值字段不能变**

```javascript
// ========== BEGIN MANDATORY CODE BLOCK: 必须原样复制 ==========

// --- 通道布局常量(与 html-spec.md §1 §3 §3.5 对齐) ---
const LAYER_NAME_WIDTH = 80;
const LEFT_CHANNEL_WIDTH = 60;
const RIGHT_CHANNEL_WIDTH = 120;
const SEG_LEN = 22;        // 起点/终点段垂直长度
const U_DEPTH = 20;        // 同层 U 字下沉深度(层底边下方)

// --- 多箭头错位计数器(renderArrows 开头必须 clear) ---
const channelUsage = new Map();   // key: 'A' | 'B'
const uUsage = new Map();         // key: layerId
const outgoingUsage = new Map();  // key: moduleId (用于 T+ label 横向错位)
const incomingUsage = new Map();  // key: moduleId (v1.2.3:跨层箭头汇入同目标时末段横向错位)
let _incomingTotals = new Map();  // 跨层 incoming 数量预统计,renderArrows 入口设置

function nextChannelOffset(channel) {
  const c = channelUsage.get(channel) || 0;
  channelUsage.set(channel, c + 1);
  return c * 10;
}

function nextUOffset(layerId) {
  const c = uUsage.get(layerId) || 0;
  uUsage.set(layerId, c + 1);
  return c * 10;
}

function nextOutgoingIdx(moduleId) {
  const c = outgoingUsage.get(moduleId) || 0;
  outgoingUsage.set(moduleId, c + 1);
  return c;
}

// v1.2.3:多条跨层箭头汇入同一目标时,末段 ex 横向错位避免重合
function nextIncomingOffset(moduleId) {
  const total = _incomingTotals.get(moduleId) || 0;
  if (total <= 1) return 0;
  const c = incomingUsage.get(moduleId) || 0;
  incomingUsage.set(moduleId, c + 1);
  return (c - (total - 1) / 2) * 14;  // 居中错位 14px/条
}

// v1.2.3:renderArrows 入口必须调一次,统计每个目标的跨层 incoming 数量
function getIncomingTotals(arrows) {
  const counts = new Map();
  arrows.forEach(a => {
    if (a.direction === 'external') return;  // 外延流走 below,不参与
    const fl = getLayerIdOfModule(a.from);
    const tl = getLayerIdOfModule(a.to);
    if (!fl || !tl || fl === tl) return;  // 同层走 U 字,不参与
    counts.set(a.to, (counts.get(a.to) || 0) + 1);
  });
  return counts;
}

// --- DOM 工具函数 ---
function getRect(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  const canvas = document.querySelector('.canvas-inner');
  const er = el.getBoundingClientRect();
  const cr = canvas.getBoundingClientRect();
  return {
    left:   er.left - cr.left,
    top:    er.top - cr.top,
    right:  er.right - cr.left,
    bottom: er.bottom - cr.top,
    cx: er.left - cr.left + er.width / 2,
    cy: er.top  - cr.top  + er.height / 2
  };
}

function getAreaWidth() {
  return document.querySelector('.canvas-inner').clientWidth;
}

function getLayerIdOfModule(moduleId) {
  const el = document.getElementById(moduleId);
  if (!el) return null;
  return el.closest('.layer')?.id || null;
}

function getLayerIdx(layerId) {
  // 改这里:把数组换成你实际的 4 层 DOM id (从触达层到数据层的顺序)
  const layers = ['layer-touch', 'layer-scene', 'layer-capability', 'layer-data'];
  return layers.indexOf(layerId);
}

// --- 通道选择 ---
function pickChannel(arrow, fromRect, toRect) {
  // 1. 外延流强制走右通道 B (无论跨几层)
  if (arrow.direction === 'external') return 'B';
  // 2. 同层走 U 字 (通道 C)
  const fromLayer = getLayerIdOfModule(arrow.from);
  const toLayer = getLayerIdOfModule(arrow.to);
  if (fromLayer && toLayer && fromLayer === toLayer) return 'C';
  // 3. 跨层:看跨度——相邻层直连,跨多层才走 A/B 通道
  const fromIdx = getLayerIdx(fromLayer);
  const toIdx   = getLayerIdx(toLayer);
  const layerSpan = Math.abs(fromIdx - toIdx);
  if (layerSpan === 1) return 'direct';   // ⚠️ v1.2.2:相邻层直连,不走可见通道
  // 跨 ≥2 层:看 midX 选 A 或 B
  const midX = (fromRect.cx + toRect.cx) / 2;
  return midX < getAreaWidth() / 2 ? 'A' : 'B';
}

// --- 跨层 path (通道 A 或 B) ---
function pathThroughChannel(arrow, fromRect, toRect, channel) {
  const areaWidth = getAreaWidth();
  const fromLayerIdx = getLayerIdx(getLayerIdOfModule(arrow.from));
  const toLayerIdx   = getLayerIdx(getLayerIdOfModule(arrow.to));
  const isDown = fromLayerIdx < toLayerIdx;

  const sx = fromRect.cx;
  const sy = isDown ? fromRect.bottom : fromRect.top;
  // v1.2.3:同目标多条跨层箭头,末段 ex 横向错位避免重合
  const ex = toRect.cx + nextIncomingOffset(arrow.to);
  const ey = isDown ? toRect.top : toRect.bottom;

  const sSegY = sy + (isDown ? SEG_LEN : -SEG_LEN);
  const eSegY = ey + (isDown ? -SEG_LEN : SEG_LEN);

  // 弯曲段长度封顶 50px,正反向都截断
  const span = eSegY - sSegY;
  const bendLen = Math.min(Math.abs(span) * 0.30, 50);
  const enterY = sSegY + bendLen * Math.sign(span);
  const exitY  = eSegY - bendLen * Math.sign(span);

  const channelCenterX = channel === 'A'
    ? LAYER_NAME_WIDTH + LEFT_CHANNEL_WIDTH / 2
    : areaWidth - RIGHT_CHANNEL_WIDTH / 2;
  const chX = channelCenterX + nextChannelOffset(channel);

  const path =
    `M ${sx} ${sy} L ${sx} ${sSegY} ` +
    `C ${sx} ${(sSegY+enterY)/2}, ${chX} ${(sSegY+enterY)/2}, ${chX} ${enterY} ` +
    `L ${chX} ${exitY} ` +
    `C ${chX} ${(exitY+eSegY)/2}, ${ex} ${(exitY+eSegY)/2}, ${ex} ${eSegY} ` +
    `L ${ex} ${ey}`;

  // T+ label: 紧贴源模块,同源多条 outgoing 沿 x 错开 64px
  const outIdx = nextOutgoingIdx(arrow.from);
  const labelX = fromRect.cx + outIdx * 64;
  const labelY = isDown ? fromRect.bottom + 14 : fromRect.top - 14;
  return { path, labelX, labelY, labelAnchor: 'middle' };
}

// --- 相邻层直连 (v1.2.2 新增,不走通道) ---
function pathDirect(arrow, fromRect, toRect) {
  const fromLayerIdx = getLayerIdx(getLayerIdOfModule(arrow.from));
  const toLayerIdx   = getLayerIdx(getLayerIdOfModule(arrow.to));
  const isDown = fromLayerIdx < toLayerIdx;

  const sx = fromRect.cx;
  const sy = isDown ? fromRect.bottom : fromRect.top;
  // v1.2.3:同目标多条跨层箭头,末段 ex 横向错位避免重合
  const ex = toRect.cx + nextIncomingOffset(arrow.to);
  const ey = isDown ? toRect.top : toRect.bottom;

  const sSegY = sy + (isDown ? SEG_LEN : -SEG_LEN);
  const eSegY = ey + (isDown ? -SEG_LEN : SEG_LEN);

  // 相邻层直连:bezier 控制点放在 sx/ex 各自的 y 中点
  const path =
    `M ${sx} ${sy} L ${sx} ${sSegY} ` +
    `C ${sx} ${(sSegY+eSegY)/2}, ${ex} ${(sSegY+eSegY)/2}, ${ex} ${eSegY} ` +
    `L ${ex} ${ey}`;

  // T+ label: 紧贴源,同源多条 outgoing 沿 x 错开 64px
  const outIdx = nextOutgoingIdx(arrow.from);
  const labelX = fromRect.cx + outIdx * 64;
  const labelY = isDown ? fromRect.bottom + 14 : fromRect.top - 14;
  return { path, labelX, labelY, labelAnchor: 'middle' };
}

// --- 同层 U 字 (通道 C) ---
function pathSameLayerU(arrow, fromRect, toRect) {
  const sx = fromRect.cx;
  const sy = fromRect.bottom;
  const ex = toRect.cx;
  const ey = toRect.bottom;

  const layerId = getLayerIdOfModule(arrow.from);
  const uOffset = nextUOffset(layerId);
  const layerBottom = Math.max(fromRect.bottom, toRect.bottom);
  const goY = layerBottom + U_DEPTH + uOffset;

  const sSegY = sy + SEG_LEN;
  const eSegY = ey + SEG_LEN;
  const sign = ex > sx ? 1 : -1;

  const path =
    `M ${sx} ${sy} L ${sx} ${sSegY} ` +
    `C ${sx} ${(sSegY+goY)/2}, ${sx} ${goY}, ${sx + sign*40} ${goY} ` +
    `L ${ex - sign*40} ${goY} ` +
    `C ${ex} ${goY}, ${ex} ${(eSegY+goY)/2}, ${ex} ${eSegY} ` +
    `L ${ex} ${ey}`;

  return { path, labelX: (sx+ex)/2, labelY: goY + 14, labelAnchor: 'middle' };
}

// --- 外延流 (v1.2.3:从源底边出,走源所在层底下方水平带,避免横穿模块) ---
function pathExternalBelow(arrow, fromRect, badgeRect) {
  const sx = fromRect.cx;
  const sy = fromRect.bottom;
  const ex = badgeRect.cx;
  const ey = badgeRect.bottom;  // 进入 badge 底边

  // 找源所在层的底边 + 14px,作为水平段 y
  const layerId = getLayerIdOfModule(arrow.from);
  const layer = document.getElementById(layerId);
  const layerBottom = layer ? layer.offsetTop + layer.clientHeight : fromRect.bottom + 30;
  const goY = layerBottom + 14;

  const sSegY = sy + SEG_LEN;
  const eSegY = ey + SEG_LEN;

  // 从源 cx 下行到 goY → 横走到 badge cx → 上行回 badge 底边
  const path =
    `M ${sx} ${sy} L ${sx} ${sSegY} ` +
    `C ${sx} ${(sSegY+goY)/2}, ${sx + 40} ${goY}, ${(sx+ex)/2} ${goY} ` +
    `C ${ex - 40} ${goY}, ${ex} ${(eSegY+goY)/2}, ${ex} ${eSegY} ` +
    `L ${ex} ${ey}`;

  return { path, labelX: (sx+ex)/2, labelY: goY - 8, labelAnchor: 'middle' };
}

// --- 路由分发 ---
function buildArrowPath(arrow) {
  const fromRect = getRect(arrow.from);
  if (!fromRect) return null;

  // 同层 U 字
  const fromLayer = getLayerIdOfModule(arrow.from);
  const toLayer = getLayerIdOfModule(arrow.to);
  if (fromLayer && toLayer && fromLayer === toLayer) {
    const toRect = getRect(arrow.to);
    if (!toRect) return null;
    return pathSameLayerU(arrow, fromRect, toRect);
  }

  // 外延流 (v1.2.3:走层底下方,不走水平横线)
  if (arrow.direction === 'external') {
    const badgeRect = getRect(arrow.to);  // arrow.to 必须是 externalSystems 里的真实 id
    if (!badgeRect) return null;
    return pathExternalBelow(arrow, fromRect, badgeRect);
  }

  // 跨层:看跨度选路由
  const toRect = getRect(arrow.to);
  if (!toRect) return null;
  const channel = pickChannel(arrow, fromRect, toRect);
  if (channel === 'direct') {
    // 相邻层直连
    return pathDirect(arrow, fromRect, toRect);
  }
  // 跨 ≥2 层走可见通道 A 或 B
  return pathThroughChannel(arrow, fromRect, toRect, channel);
}

// --- 右通道里渲染外延流 badge (必须在 renderArrows 前调一次) ---
function renderExternalBadges(externalSystems) {
  const rightChannel = document.querySelector('.right-channel');
  if (!rightChannel) return;
  externalSystems.forEach(sys => {
    if (document.getElementById(sys.id)) return;  // 已存在不重渲
    const layer = document.getElementById(sys.layerId);
    if (!layer) return;
    const badge = document.createElement('div');
    badge.id = sys.id;
    badge.className = 'external-badge';
    badge.textContent = sys.label;
    badge.style.top = (layer.offsetTop + layer.clientHeight / 2 - 18) + 'px';
    rightChannel.appendChild(badge);
  });
}

// --- 渲染入口:必须开头清零计数器 ---
function resetArrowCounters() {
  channelUsage.clear();
  uUsage.clear();
  outgoingUsage.clear();
  incomingUsage.clear();   // v1.2.3
}
// 你的 renderArrows() 必须以这两步开头:
//   resetArrowCounters();
//   _incomingTotals = getIncomingTotals(allArrows);  // ⚠️ v1.2.3:必须在循环 buildArrowPath 之前调
// 然后遍历箭头数组调 buildArrowPath()

// ========== END MANDATORY CODE BLOCK ==========
```

### 2.5 你需要填写的业务数据（这部分由你写）

只填这 3 处，**不要碰上面的 MANDATORY 函数**：

```javascript
// 1. autoArrows: 3-5 条主流转,只填业务字段
const autoArrows = [
  { from: 'm-touch-app', to: 'm-data-dialogs', label: '沉淀①: 对话记录' },
  { from: 'm-data-faq',  to: 'm-capability-rag', label: '回补①: 高频问题' },
  { from: 'm-scene-repair', to: '__external_erp__', label: '外延: 派单', direction: 'external' },
  // ... 同层连接的话不用写 direction,buildArrowPath 自动识别 fromLayer === toLayer
];

// 2. externalSystems: 外延流的目标 badge
const externalSystems = [
  { id: '__external_erp__', label: 'ERP / CRM', layerId: 'layer-scene' }
];

// 3. 调用顺序(在你的初始化代码里)
renderExternalBadges(externalSystems);

// 4. renderArrows 必须按这 3 步开头(v1.2.3 关键):
function renderArrows(autoArrows, userArrows = []) {
  const allArrows = [...autoArrows, ...userArrows];
  resetArrowCounters();
  _incomingTotals = getIncomingTotals(allArrows);  // ⚠️ 必须在循环之前
  // ... 然后遍历 allArrows 调 buildArrowPath() 渲染 SVG
  allArrows.forEach(arrow => {
    const result = buildArrowPath(arrow);
    if (!result) return;
    // 把 result.path / result.labelX / result.labelY / result.labelAnchor 渲染到 SVG
  });
}

renderArrows(autoArrows, userArrows);
```

### 2.6 反例：这些重写都不允许 ❌

**反例 1**：「我看懂了，直接 source→target」
```javascript
// ❌ 这种"简化"是过去 5 轮迭代失败的根因
function buildArrowPath(arrow) {
  const fromRect = getRect(arrow.from);
  const toRect = getRect(arrow.to);
  return { path: `M ${fromRect.cx} ${fromRect.bottom} L ${toRect.cx} ${toRect.top}` };
}
```
后果：跨层箭头不经过 x=110 或 areaWidth-60 通道，path 中段直接穿过中间层模块。

**反例 2**：「合并 pathThroughChannel 和 pathSameLayerU」
```javascript
// ❌ 不允许
function buildPath(arrow) {
  if (sameLayer) { /* U 字逻辑 */ } else { /* 通道逻辑 */ }
  // 写着写着就漏分支或参数串味
}
```
后果：分支条件容易写错，几何参数互相污染。

**反例 3**：「我用 D3 / 用现成的连线库代替这些 path 函数」
```javascript
// ❌ 不允许
import { linkVertical } from 'd3-shape';
const path = linkVertical()({ source: [sx, sy], target: [ex, ey] });
```
后果：现成库不知道"侧边通道"概念，画出来的还是 source-to-target 弯线。

**反例 4**：「把 chX 改成 sx 和 ex 的平均值，让 path 更短」
```javascript
// ❌ 不允许
const chX = (sx + ex) / 2;  // 完全违反"侧边通道"设计
```
后果：path 中段在 source-target 中点，根本不在通道里。

**反例 5（v1.2.2 新增）**：「相邻层也走通道」
```javascript
// ❌ 这是 v1.2.0 / v1.2.1 的过度工程,v1.2.2 已修正
function pickChannel(arrow, fromRect, toRect) {
  // 所有跨层都走 A/B...
  const midX = (fromRect.cx + toRect.cx) / 2;
  return midX < getAreaWidth() / 2 ? 'A' : 'B';
}
```
后果：相邻层（如触达→场景）箭头被强行绕到 x=110，**短距离反复弯曲，视觉混乱**，通道也失去"为什么绕"的解释力。**v1.2.2 正确做法：跨度 = 1 时返回 `'direct'`，由 `pathDirect()` 处理。**

✅ **正确做法**：把上面 MANDATORY CODE BLOCK 整段复制粘贴到 HTML `<script>` 标签内。复制后做一次自检：
- 函数名 `pickChannel` / `pathDirect` / `pathThroughChannel` / `pathSameLayerU` / `pathExternalBelow` / `buildArrowPath` **6 个**是否在你 HTML 里都能搜到？
- bezier 控制点公式 `${chX} ${(sSegY+enterY)/2}` 是否原样保留？
- `pickChannel` 里 `if (layerSpan === 1) return 'direct';` 这一行是否保留？
- 是否在 renderArrows 开头调了 `resetArrowCounters()`？

---





## §3 起点段 / 终点段必须垂直于模块边 ⚠️

**问题来源**：箭头三角形（marker）的朝向由 SVG path 末段的切线方向决定。如果末段是斜的曲线，marker 会跟着斜，像从侧面斜着插进模块的钉子。

**强制规则**：所有箭头的**起点段和终点段**必须是**纯直线段**（不是曲线），方向必须**垂直于源/目标模块的边**：

- 进 / 出**顶边或底边**（跨层 + 同层 U 字）：直线方向**纯垂直**（同 x 坐标），至少 22px
- 进 / 出**左边或右边**（外延流到右通道 badge）：直线方向**纯水平**（同 y 坐标），至少 22px

---

## §4 通道内多箭头错位（概念说明）

> 代码实现已在 §2.4 MANDATORY CODE BLOCK 里。本节只解释**为什么**要这么做，方便人审 + 后续维护理解。

### 通道 A / B（纵向通道）：水平错位 10px
通道宽 60-120px，多条箭头如果都在中心线纵向走会重叠。`nextChannelOffset()` 给每条沿 x 错开 10px。

### 通道 C（同层 U 字）：纵向错位 10px
同层多条 U 字水平段都在层底下方，错位 y 避免重叠。

### 同目标 incoming：末段横向错位 14px ⚠️ v1.2.3 新增
多条跨层箭头汇入同一目标模块（如 5 个触达 → 对话库）时，所有箭头的末段 `ex` 默认都是 `toRect.cx`，必然重合。`nextIncomingOffset()` 给每条沿 x 居中错开 14px——前提是 `renderArrows` 入口必须先调 `_incomingTotals = getIncomingTotals(allArrows)` 统计总数。

### 重置（关键）⚠️
渲染入口必须开头调 `resetArrowCounters()`——清零 `channelUsage` / `uUsage` / `outgoingUsage` / `incomingUsage` 四个 Map。**不清零 = hover / resize / 添加箭头时每次累计错位，箭头越漂越远**。这是 §2.4 MANDATORY CODE 里 `resetArrowCounters()` 函数的强制约束。

---

## §5 手动添加连接（画线模式）

工具栏 `+ 添加连接` 按钮，点击进入"画线模式"。

### 画线流程

1. **进入画线模式**：按钮变 `✕ 取消`，颜色高亮
2. **激活模块**：hover 边框高亮、光标变 `crosshair`
3. **点击第一个模块（源）**：边框变实色，浮"源"标签
4. **移动鼠标**：实时绘制**虚线预览**
5. **点击第二个模块（目标）**：
   - 用 §2 通道选择规则**自动决定路由**（A / B / C）
   - 用 §4 错位算法决定通道内位置
   - 视觉**完全等同**于自动箭头
   - path 中段弹文字输入框
6. **用户输入标签**：回车确认 / Esc 取消
7. **自动退出画线模式**

### 视觉一致性强约束

用户加的箭头**和自动箭头看不出区别**——同样走 §2 三通道、同样遵守 §3 §4 规则。

区分只在 DOM 内部：自动 `class="auto-arrow"`，手动 `class="user-arrow"`（用于"恢复自动箭头"）。

---

## §6 6 个易错陷阱（已在 §2.4 MANDATORY CODE 中内化）⚠️

下面 6 个陷阱是过去多轮迭代里 AI 最容易写错的。**只要你按 §2.4 原样复制 MANDATORY CODE BLOCK 且按 §2.5 正确调用 `_incomingTotals = getIncomingTotals(allArrows)`，下面陷阱都自动避开**。本节只列概念性警告，方便你 review 自己的产出有没有"自作主张改回去"。

### 陷阱 1：同层连接 fallback 到 'down'
**症状**：同层模块之间的箭头穿过中间模块，或绕怪路。  
**根因**：direction 算法漏了"`fromLayer === toLayer` → same-layer"分支，回退到 'down'。  
**MANDATORY CODE 怎么避免**：`buildArrowPath()` 第一段就是检测 `fromLayer === toLayer` → 调 `pathSameLayerU()`，**没有 down/up fallback 路径**。

### 陷阱 2：跨层箭头自己另算"间隙列"
**症状**：跨层箭头不走 x=110 / areaWidth-60 通道，而是在源/目标之间画弯线。  
**根因**：v1.1 旧设计是"算 gapColRatio"，AI 训练习惯也是"source-to-target"——不强约束就回到这种。  
**MANDATORY CODE 怎么避免**：`pathThroughChannel()` 里 `channelCenterX = 'A' ? 110 : areaWidth-60`——这是**硬编码常量**，不能根据箭头属性变。

### 陷阱 3：外延流目标用占位字符串
**症状**：箭头指向"空气"——画到画布右边缘，但右边没东西。  
**根因**：autoArrows 写成 `{ to: 'external', ... }`，AI 没渲染真实 badge DOM。  
**MANDATORY CODE 怎么避免**：
- `renderExternalBadges()` 必须先调一次（创建 badge DOM）
- `autoArrows` 里 `to` 必须是 `externalSystems[].id`（如 `'__external_erp__'`）
- `pathExternalBelow()` 用 `getRect(arrow.to)` 拿 badge 坐标——如果 badge 没创建会返回 null，path 不会渲染

### 陷阱 4：水平方向的 label 压在 bullet 上 / 通道 label 压模块
**症状**：label 落在模块卡片中央，挡住业务文字。  
**根因**：label 用 path 中段 y，但模块中线 y 也在 path 中段附近，必然冲突。  
**MANDATORY CODE 怎么避免**：T+ label——label 紧贴源模块（`fromRect.bottom + 14` 或 `fromRect.top - 14`），用 `labelAnchor: 'middle'` 居中对齐 source.cx。

### 陷阱 5：通道 DOM 漏写 → 静默失败 ⚠️ v1.2.3 新增
**症状**：产出的 HTML 看起来"几乎对的"，但外延流箭头不见了 / 跨多层箭头不走通道。  
**根因**：CSS 里定义了 `.left-channel` `.right-channel`，但 `<body>` 里**没真正实例化** `<div class="left-channel">` `<div class="right-channel">` 这两个 DOM。  
**为什么静默**：
- `renderExternalBadges()` 里 `if (!rightChannel) return;` 静默退出，**外延 badge 根本不被创建**
- 然后 `pathExternalBelow` 调 `getRect(arrow.to)` 返回 null → 外延流箭头静默消失
- AI 自检看代码逻辑没问题，**不打开浏览器目视检查就发现不了**

**MANDATORY CODE 怎么避免**：不能从代码层避免，必须在自检阶段做 **§8 第 -1 级 DOM 前置核查**——搜 HTML 字符串确认 `class="left-channel"` / `class="right-channel"` / `<svg class="arrows-svg">` 三个 DOM 都存在。

### 陷阱 6：多条跨层箭头汇入同目标末段重合 ⚠️ v1.2.3 新增
**症状**：5 个触达模块都连到对话库，目标模块顶部入口 5 条线挤在一起，视觉上是"一坨"。  
**根因**：`pathThroughChannel` / `pathDirect` 的 `ex` 默认都是 `toRect.cx`，几何上必然重合。  
**MANDATORY CODE 怎么避免**：
- `getIncomingTotals()` + `nextIncomingOffset()` 让每条沿 x 居中错开 14px
- **但必须在 renderArrows 入口调** `_incomingTotals = getIncomingTotals(allArrows)`——这一步漏掉，错位机制就不生效

---

## §7 删除箭头

- 点击任何箭头（自动 / 手动均可删）→ 标签旁浮 `×` 按钮
- × 直径 18-20px，红色背景 `#EF4444`，白色 ×
- hover × 时整条箭头变红
- 点击 × 即删除
- **自动箭头被删后**：工具栏出现 `↩ 恢复自动箭头` 链接 → 点击复原

---

## §8 箭头自检（产出含箭头的 HTML 前过一遍）

### -1. DOM 前置核查 ⚠️ v1.2.3 最先做（这一级不过，后面全白做）
- [ ] HTML 里能搜到 `class="left-channel"` 字符串（若存在跨 ≥2 层箭头）
- [ ] HTML 里能搜到 `class="right-channel"` 字符串（若存在外延流或跨多层右偏箭头）
- [ ] HTML 里有 `<svg class="arrows-svg">` 且包含 `<marker id="arrowhead">` 定义
- [ ] **三个 DOM 漏一个，arrow-routing.md MANDATORY CODE 会静默失败**（外延 badge 不创建 / 箭头消失）

### 0. MANDATORY CODE 原样复制核查 ⚠️ 第二最重要
- [ ] 我的 HTML `<script>` 里能搜到 `pickChannel`、`pathDirect`、`pathThroughChannel`、`pathSameLayerU`、`pathExternalBelow`、`buildArrowPath` **6 个函数名**
- [ ] `pickChannel` 里有 `if (layerSpan === 1) return 'direct';` 这一行（v1.2.2 核心规则）
- [ ] `pathThroughChannel` 里 `channelCenterX` 用的是 `LAYER_NAME_WIDTH + LEFT_CHANNEL_WIDTH / 2` 或 `areaWidth - RIGHT_CHANNEL_WIDTH / 2`（不是其他公式）
- [ ] `pathThroughChannel` 里的 bezier 控制点表达式包含 `${chX}`（不是 `${sx}` 或 `${ex}` 的平均值）
- [ ] `bendLen = Math.min(Math.abs(span) * 0.30, 50)`（不是 `span * 0.30`，**正负都截断**）
- [ ] `pathThroughChannel` 和 `pathDirect` 里 `ex = toRect.cx + nextIncomingOffset(arrow.to)`（v1.2.3 同目标错位）
- [ ] `buildArrowPath` 里有 `if (channel === 'direct') return pathDirect(...)` 分支
- [ ] `buildArrowPath` 里外延流分支调的是 `pathExternalBelow`（v1.2.3 改名，不是 pathExternalRight）
- [ ] `renderArrows()` 开头调了 `resetArrowCounters()` **且** `_incomingTotals = getIncomingTotals(allArrows)`
- [ ] `externalSystems` 数组定义了，`renderExternalBadges()` 在 `renderArrows()` 前调用过一次

### 1. 视觉效果（打开浏览器目视检查，不是看代码）
- [ ] **相邻层箭头直连**——从源底部 bezier 直接到目标顶部，不绕到 x=110 / areaWidth-60
- [ ] **跨 ≥2 层箭头走侧边路径**——有清晰的纵向段在 x=110 或 x=areaWidth-60（通道本身隐形不可见，但 path 形态能看出绕侧）
- [ ] **没有任何箭头切穿任何模块卡片**——尤其外延流不再水平横穿中间模块（v1.2.3 用 pathExternalBelow 走层底下方）
- [ ] **多条跨层箭头汇入同目标时末段不重合**——5 个触达→对话库这种 case，目标顶部入口能看到 5 个不同的点（v1.2.3 incomingUsage 错位）
- [ ] 没有 label 压在任何模块卡片上
- [ ] 起点段和终点段是**纯直线，垂直于模块边**

### 2. 通道选择与建立
- [ ] 通道 DOM `<div class="left-channel">` `<div class="right-channel">` **存在但 CSS 透明**（v1.2.3：作为坐标定位区，不可见）
- [ ] 同层连接走通道 C U 字（在层底下方水平带）
- [ ] 跨层 → 看 layerSpan：=1 走 `pathDirect`，≥2 看 midX 选 A 或 B
- [ ] 外延流走 `pathExternalBelow`（从源底→层底水平带→badge 底进入），不再用水平横线

### 3. Label
- [ ] 所有 label 用 `labelAnchor: 'middle'`（T+ 方案，紧贴源模块）
- [ ] 沉淀流（向下）label 在 `fromRect.bottom + 14`；回补流（向上）label 在 `fromRect.top - 14`
- [ ] 同源多条 outgoing label 沿 x 错开 64px（`nextOutgoingIdx` 起作用）

### 4. 多箭头错位
- [ ] 通道 A / B 同侧多条水平错位 10px（`channelUsage` 计数生效）
- [ ] 通道 C 同层多条 U 字纵向错位 10px（`uUsage` 计数生效）
- [ ] 同目标多条 incoming 末段错位 14px（`incomingUsage` 计数生效，v1.2.3）
- [ ] 重新 hover / resize 时箭头位置稳定（说明 `resetArrowCounters()` 生效）

### 5. 交互
- [ ] 点击箭头出现 × 按钮，hover × 时整箭头变红
- [ ] 删除自动箭头后工具栏出现 `↩ 恢复自动箭头`
- [ ] 用户手动添加的箭头视觉等同于自动箭头（同样走 MANDATORY CODE 的 buildArrowPath）

