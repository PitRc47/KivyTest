# Kivy Canvas2D API 实现

## 已实现的功能

### 基础绘图
- **`clearRect()`** → `clear_rect` 方法实现
- **`fillRect()`** → `fill_rect` 方法实现
- **`strokeRect()`** → `stroke_rect` 方法实现
- **`fillText()`** → `fill_text` 方法实现
- **`strokeText()`** → `stroke_text` 方法实现
- **`measureText()`** → `measure_text` 返回 `TextMetrics` 对象（包含 `width`、`actualBoundingBox*` 等属性）

### 属性
- **`lineWidth`** → 通过 `line_width` 属性控制
- **`font`** → 支持 CSS 样式解析（`CSSFont` 类）
- **`textAlign`** → 通过 `text_align` 属性控制
- **`textBaseline`** → 通过 `text_baseline` 属性控制
- **`fillStyle`** → 支持 CSS 颜色解析（`CSSColorParser`）
- **`strokeStyle`** → 支持 CSS 颜色解析

### 路径操作
- **`beginPath()`** → `begin_path` 方法
- **`closePath()`** → `close_path` 方法
- **`moveTo()`** → `move_to` 方法
- **`lineTo()`** → `line_to` 方法
- **`rect()`** → `rect` 方法
- **`roundRect()`** → `round_rect` 方法（圆角矩形路径）
- **`fill()`** → 填充路径
- **`stroke()`** → 描边路径
- **`clip()`** → 路径裁剪

### 变换
- **`rotate()`** → 旋转变换
- **`scale()`** → 缩放变换
- **`translate()`** → 平移变换
- **`resetTransform()`** → 重置变换矩阵

### 图像
- **`drawImage()`** → 支持多种参数的 `draw_image` 方法

### 状态管理
- **`save()`** → 保存当前状态
- **`restore()`** → 恢复之前状态
- **`reset()`** → 重置所有属性

---

## 未实现或部分实现的功能

### 待实现
1. **渐变/阴影**
   - **`createLinearGradient()`** → 未实现
   - **`shadowBlur`** → 未实现
   - **`shadowColor`** → 未实现

2. **像素操作**
   - **`getImageData()`** → 未实现
   - **`imageSmoothingEnabled`** → 未实现

3. **画布属性**
   - **`canvas`** → 当前实现中未直接暴露画布对象

4. **透明度**
   - **`globalAlpha`** → 属性存在但未实际生效（setter 为空）

5. **滤镜**
   - **`filter`** → 属性存在但未实现具体功能（setter 为空）

---

## 其他说明
- **文本描边优化**：`stroke_text` 使用多偏移量模拟描边效果
- **字体度量**：`TextMetrics` 类实现 `actualBoundingBox` 等 CSS 度量属性
- **兼容性**：支持 `Kivy` 的 `CoreLabel` 和 `Texture` 系统