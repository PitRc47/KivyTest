# Kivy Canvas2D API 实现
TODO: 
   1. Y轴坐标翻转
   2. 渐变/阴影
   3. 画布属性
   4. 透明度
   5. 滤镜

### 基础绘图
- [x] clearRect() 
- [x] fillRect() 
- [x] strokeRect() 
- [x] fillText() 
- [x] strokeText()
- [x] measureText()  （未测试，可能不准确）

### 属性

- [x] lineWidth
- [ ] font （差模拟API）
- [ ] textAlign
- [ ] textBaseline
- [x] fillStyle → 支持 CSS 颜色解析（CSSColorParser）
- [x] strokeStyle → 支持 CSS 颜色解析

### 路径操作
- [x] beginPath()
- [x] closePath() （待测试）
- [x] moveTo() （待测试）
- [x] lineTo() （待测试）
- [x] rect()
- [x] roundRect()
- [x] fill()
- [x] stroke()
- [x] clip() （待测试）

### 变换
- [x] rotate()
- [x] scale()
- [x] translate()
- [x] resetTransform() （待测试）

### 图像
- [x] drawImage() （待整理）

### 状态管理
- [x] save() （待测试）
- [x] restore() （待测试）
- [x] reset() （待测试）

未实现
---

1. 渐变/阴影
   - createLinearGradient()
   - shadowBlur
   - shadowColor

2. 像素操作
   - getImageData()
   - imageSmoothingEnabled

3. 画布属性
   - canvas

4. 透明度
   - globalAlpha

5. 滤镜
   - filter

---