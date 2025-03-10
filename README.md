# Kivy Canvas2D API 实现
TODO: 
   ~~ 1. Y轴坐标翻转 ~~
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
- [x] measureText()  （不准确）

### 属性

- [x] lineWidth
- [x] font
- [x] textAlign
- [ ] textBaseline （有bug）
- [x] fillStyle
- [x] strokeStyle

### 路径操作
- [x] beginPath()
- [x] closePath()
- [x] moveTo()
- [x] lineTo()
- [x] rect()
- [ ] roundRect()
- [x] fill()
- [x] stroke()
- [ ] clip() ?

### 变换
- [x] rotate()
- [x] scale()
- [x] translate()
- [x] resetTransform() （待测试）

### 图像
- [x] drawImage()

### 状态管理
- [x] save()
- [x] restore()
- [x] reset()

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