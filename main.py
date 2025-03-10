from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel, LabelBase
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics.stencil_instructions import StencilPush, StencilPop, StencilUse
from kivy.graphics import (
    RoundedRectangle, Color, Rectangle, Line,
    Mesh, PushMatrix, PopMatrix,
    Rotate, Scale, Translate,
)

import re
import math
import copy
import numpy as np
from threading import Thread
from functools import wraps

class CSSColorParser:
    COLORS = {
        'aliceblue': (240, 248, 255),
        'antiquewhite': (250, 235, 215),
        'aqua': (0, 255, 255),
        'aquamarine': (127, 255, 212),
        'azure': (240, 255, 255),
        'beige': (245, 245, 220),
        'bisque': (255, 228, 196),
        'black': (0, 0, 0),
        'blanchedalmond': (255, 235, 205),
        'blue': (0, 0, 255),
        'blueviolet': (138, 43, 226),
        'brown': (165, 42, 42),
        'burlywood': (222, 184, 135),
        'cadetblue': (95, 158, 160),
        'chartreuse': (127, 255, 0),
        'chocolate': (210, 105, 30),
        'coral': (255, 127, 80),
        'cornflowerblue': (100, 149, 237),
        'cornsilk': (255, 248, 220),
        'crimson': (220, 20, 60),
        'cyan': (0, 255, 255),
        'darkblue': (0, 0, 139),
        'darkcyan': (0, 139, 139),
        'darkgoldenrod': (184, 134, 11),
        'darkgray': (169, 169, 169),
        'darkgrey': (169, 169, 169),
        'darkgreen': (0, 100, 0),
        'darkkhaki': (189, 183, 107),
        'darkmagenta': (139, 0, 139),
        'darkolivegreen': (85, 107, 47),
        'darkorange': (255, 140, 0),
        'darkorchid': (153, 50, 204),
        'darkred': (139, 0, 0),
        'darksalmon': (233, 150, 122),
        'darkseagreen': (143, 188, 143),
        'darkslateblue': (72, 61, 139),
        'darkslategray': (47, 79, 79),
        'darkslategrey': (47, 79, 79),
        'darkturquoise': (0, 206, 209),
        'darkviolet': (148, 0, 211),
        'deeppink': (255, 20, 147),
        'deepskyblue': (0, 191, 255),
        'dimgray': (105, 105, 105),
        'dimgrey': (105, 105, 105),
        'dodgerblue': (30, 144, 255),
        'firebrick': (178, 34, 34),
        'floralwhite': (255, 250, 240),
        'forestgreen': (34, 139, 34),
        'fuchsia': (255, 0, 255),
        'gainsboro': (220, 220, 220),
        'ghostwhite': (248, 248, 255),
        'gold': (255, 215, 0),
        'goldenrod': (218, 165, 32),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        'green': (0, 128, 0),
        'greenyellow': (173, 255, 47),
        'honeydew': (240, 255, 240),
        'hotpink': (255, 105, 180),
        'indianred': (205, 92, 92),
        'indigo': (75, 0, 130),
        'ivory': (255, 255, 240),
        'khaki': (240, 230, 140),
        'lavender': (230, 230, 250),
        'lavenderblush': (255, 240, 245),
        'lawngreen': (124, 252, 0),
        'lemonchiffon': (255, 250, 205),
        'lightblue': (173, 216, 230),
        'lightcoral': (240, 128, 128),
        'lightcyan': (224, 255, 255),
        'lightgoldenrodyellow': (250, 250, 210),
        'lightgray': (211, 211, 211),
        'lightgrey': (211, 211, 211),
        'lightgreen': (144, 238, 144),
        'lightpink': (255, 182, 193),
        'lightsalmon': (255, 160, 122),
        'lightseagreen': (32, 178, 170),
        'lightskyblue': (135, 206, 250),
        'lightslategray': (119, 136, 153),
        'lightslategrey': (119, 136, 153),
        'lightsteelblue': (176, 196, 222),
        'lightyellow': (255, 255, 224),
        'lime': (0, 255, 0),
        'limegreen': (50, 205, 50),
        'linen': (250, 240, 230),
        'magenta': (255, 0, 255),
        'maroon': (128, 0, 0),
        'mediumaquamarine': (102, 205, 170),
        'mediumblue': (0, 0, 205),
        'mediumorchid': (186, 85, 211),
        'mediumpurple': (147, 112, 219),
        'mediumseagreen': (60, 179, 113),
        'mediumslateblue': (123, 104, 238),
        'mediumspringgreen': (0, 250, 154),
        'mediumturquoise': (72, 209, 204),
        'mediumvioletred': (199, 21, 133),
        'midnightblue': (25, 25, 112),
        'mintcream': (245, 255, 250),
        'mistyrose': (255, 228, 225),
        'moccasin': (255, 228, 181),
        'navajowhite': (255, 222, 173),
        'navy': (0, 0, 128),
        'oldlace': (253, 245, 230),
        'olive': (128, 128, 0),
        'olivedrab': (107, 142, 35),
        'orange': (255, 165, 0),
        'orangered': (255, 69, 0),
        'orchid': (218, 112, 214),
        'palegoldenrod': (238, 232, 170),
        'palegreen': (152, 251, 152),
        'paleturquoise': (175, 238, 238),
        'palevioletred': (219, 112, 147),
        'papayawhip': (255, 239, 213),
        'peachpuff': (255, 218, 185),
        'peru': (205, 133, 63),
        'pink': (255, 192, 203),
        'plum': (221, 160, 221),
        'powderblue': (176, 224, 230),
        'purple': (128, 0, 128),
        'rebeccapurple': (102, 51, 153),
        'red': (255, 0, 0),
        'rosybrown': (188, 143, 143),
        'royalblue': (65, 105, 225),
        'saddlebrown': (139, 69, 19),
        'salmon': (250, 128, 114),
        'sandybrown': (244, 164, 96),
        'seagreen': (46, 139, 87),
        'seashell': (255, 245, 238),
        'sienna': (160, 82, 45),
        'silver': (192, 192, 192),
        'skyblue': (135, 206, 235),
        'slateblue': (106, 90, 205),
        'slategray': (112, 128, 144),
        'slategrey': (112, 128, 144),
        'snow': (255, 250, 250),
        'springgreen': (0, 255, 127),
        'steelblue': (70, 130, 180),
        'tan': (210, 180, 140),
        'teal': (0, 128, 128),
        'thistle': (216, 191, 216),
        'tomato': (255, 99, 71),
        'turquoise': (64, 224, 208),
        'violet': (238, 130, 238),
        'wheat': (245, 222, 179),
        'white': (255, 255, 255),
        'whitesmoke': (245, 245, 245),
        'yellow': (255, 255, 0),
        'yellowgreen': (154, 205, 50)
    }

    @classmethod
    def parse_color(cls, color_str):
        color_str = color_str.strip().lower()
        if not color_str:
            raise ValueError("Empty color string")

        # 颜色名称解析
        if color_str in cls.COLORS:
            r, g, b = cls.COLORS[color_str]
            return (r/255.0, g/255.0, b/255.0, 1.0)

        # 十六进制解析
        if color_str.startswith('#'):
            return cls._parse_hex(color_str)

        # RGB/RGBA解析
        if color_str.startswith(('rgb', 'rgba')):
            return cls._parse_rgb(color_str)

        raise ValueError(f"Unrecognized color format: {color_str}")

    @classmethod
    def _parse_hex(cls, color_str):
        hex_str = color_str.lstrip('#')
        length = len(hex_str)

        if length not in (3, 4, 6, 8):
            raise ValueError(f"Invalid hex color: {color_str}")

        # 扩展短格式
        if length in (3, 4):
            hex_str = ''.join([c*2 for c in hex_str])
            length = len(hex_str)

        try:
            # 解析颜色分量
            components = [int(hex_str[i:i+2], 16) for i in range(0, length, 2)]
            r = components[0] / 255.0
            g = components[1] / 255.0
            b = components[2] / 255.0
            a = components[3]/255.0 if length ==8 else 1.0
        except ValueError:
            raise ValueError(f"Invalid hex color: {color_str}")

        return (r, g, b, a)

    @classmethod
    def _parse_rgb(cls, color_str):
        # 提取参数部分
        match = re.match(r'^rgba?\((.*)\)$', color_str, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid RGB format: {color_str}")

        components = []
        for part in re.split(r'[,\s/]+', match.group(1)):
            part = part.strip()
            if part:
                components.append(part)

        if len(components) not in (3, 4):
            raise ValueError(f"Invalid RGB components: {color_str}")

        # 解析颜色分量
        r = cls._parse_component(components[0], max_val=255)
        g = cls._parse_component(components[1], max_val=255)
        b = cls._parse_component(components[2], max_val=255)
        a = cls._parse_component(components[3], max_val=1.0) if len(components)>3 else 1.0

        return (r, g, b, a)

    @classmethod
    def _parse_component(cls, component, max_val):
        component = component.strip().lower()
        if component.endswith('%'):
            value = float(component[:-1]) * max_val / 100.0
        else:
            value = float(component)
        
        # 标准化数值范围
        normalized = value / (255.0 if max_val ==255 else 1.0)
        return max(0.0, min(1.0, normalized))

class CSSFont:
    def __init__(self, font_str):
        self.font_str = font_str
        self._parse_font_str(font_str)
    
    def _parse_font_str(self, font_str):
        """解析CSS font字符串的正则表达式增强版"""
        pattern = re.compile(r"""
            ^  # 开头
            (?:  # 可选的 font-style（如 italic）
                (?:italic|oblique|normal)(?:\s+(?:italic|oblique|normal))*\s+
            )?
            (?:  # 可选的 font-variant（如 small-caps）
                (?:small-caps|normal)(?:\s+(?:small-caps|normal))*\s+
            )?
            (?:  # 可选的 font-weight（如 bold）
                (?:bold|lighter|bolder|\d{3}|normal)(?:\s+(?:bold|lighter|bolder|\d{3}|normal))*\s+
            )?
            (\d+\.?\d*)  # 必要的字号值（如 20）
            (px|pt|em|mm)?  # 可选的单位
            (?:  # 可选的行高（以 / 分隔）
                \s*/\s*
                (\d+\.?\d*)  # 行高值
                (px|pt|em|mm)?  # 行高单位
                \s*
            )?
            (?:  # 可选的第二个行高（通常不需要，但保留原逻辑）
                \s*/\s*
                (\d+\.?\d*)  # 第二个行高值
                (px|pt|em|mm)?  # 第二个行高单位
                \s*
            )?
            \s+  # 必须有空格分隔字体族
            (  # 字体族部分
                (?:'[^']*'|"[^"]*"|\w+(?:\s+\w+)*)  # 支持带引号或无引号的多单词字体名
                (?:  # 允许逗号分隔的多个字体族
                    \s*,\s*
                    (?:'[^']*'|"[^"]*"|\w+(?:\s+\w+)*)  
                )*
            )
            $  # 结尾
        """, re.VERBOSE | re.IGNORECASE)

        match = pattern.match(font_str.strip())
        if not match:
            raise ValueError(f"Invalid font format: {font_str}")

        # 提取解析结果
        self.font_style = match.group(1) or 'normal'  # 若存在font-style组则需调整
        self.font_variant = match.group(2) or 'normal'
        self.font_weight = match.group(3) or 'normal'
        self._parse_size(match)      # 处理字号和单位
        self._parse_font_family(match.group(7))  # 字体族改为group(7)

    def _parse_size(self, match):
        """解析字号和单位转换"""
        # 基础字号（第一个尺寸值）
        size_val = float(match.group(1))  # 修正为 group(1)
        size_unit = match.group(2) or 'px'  # 修正为 group(2)
        self.font_size = self._convert_unit(size_val, size_unit)

        # 行高（第二个尺寸值）
        if match.group(3):  # 行高值的分组索引调整为 group(3)
            line_height_val = float(match.group(3))
            line_height_unit = match.group(4) or 'px'  # 行高单位为 group(4)
            self.line_height = self._convert_unit(line_height_val, line_height_unit)
        else:
            self.line_height = None

    def _convert_unit(self, value, unit):
        """单位转换到像素（简化版）"""
        conversions = {
            'px': lambda x: x,
            'pt': lambda x: x * 1.3333,  # 1pt ≈ 1.3333px
            'em': lambda x: x * 16,       # 假设基础字号16px
            'mm': lambda x: x * 3.7795    # 1mm ≈ 3.7795px
        }
        return conversions[unit.lower()](value) if unit in conversions else value

    def _parse_font_family(self, family_str):
        """处理字体族解析"""
        families = []
        current = []
        in_quote = False
        quote_char = None
        
        for c in family_str.strip():
            if c in ('"', "'"):
                if not in_quote:
                    in_quote = True
                    quote_char = c
                elif c == quote_char:
                    in_quote = False
                    quote_char = None
                continue
            
            if not in_quote and c == ',':
                if current:
                    families.append(''.join(current).strip())
                    current = []
                continue
                
            current.append(c)
        
        if current:
            families.append(''.join(current).strip())
        
        self.font_family = families

    def apply_to_text(self, text_widget):
        """应用属性到TextInput控件"""
        if self.font_size:
            text_widget.font_size = self.font_size
        if self.font_family:
            text_widget.font_name = self._get_kivy_font_name()
        self._apply_font_style(text_widget)
        self._apply_font_weight(text_widget)

    def _get_kivy_font_name(self):
        """转换字体族为Kivy兼容格式"""
        kivy_fonts = []
        for font in self.font_family:
            # 移除引号并处理空格
            font = font.strip('\'"')  # 去除可能存在的引号
            kivy_fonts.append(font)
        return ','.join(kivy_fonts)

    def _apply_font_style(self, widget):
        """应用斜体样式"""
        if 'italic' in self.font_style.lower() or 'oblique' in self.font_style.lower():
            widget.font_style = 'italic'

    def _apply_font_weight(self, widget):
        weight_map = {'bold': '700', 'normal': '400', 'lighter': '300', 'bolder': '700'}
        weight = self.font_weight.lower()
        weight = weight_map.get(weight, weight)
        if weight.isdigit() and int(weight) >= 600:
            widget.bold = True

class TextMetrics:
    def __init__(self, label, context):
        self._label = label
        self._ctx = context  # Canvas2DContext实例
        self._texture = label.texture if label else None

    @property
    def width(self) -> float:
        """实际文本宽度（像素）"""
        return self._texture.width if self._texture else 0

    @property
    def actualBoundingBoxLeft(self) -> float:
        """基于对齐点的左侧溢出距离"""
        align = self._ctx.textAlign
        base_x = self._get_alignment_base_x()
        return abs(base_x - 0)  # 实际渲染的左侧坐标

    @property
    def actualBoundingBoxRight(self) -> float:
        """基于对齐点的右侧溢出距离"""
        align = self._ctx.textAlign
        base_x = self._get_alignment_base_x()
        return abs(self.width - base_x)

    @property
    def actualBoundingBoxAscent(self) -> float:
        """实际内容上沿高度"""
        return self._ctx.font_size * 0.8  # 估算为字号的80%

    @property
    def actualBoundingBoxDescent(self) -> float:
        """实际内容下沿高度"""
        return self._ctx.font_size * 0.2  # 估算为字号的20%

    @property
    def fontBoundingBoxAscent(self) -> float:
        """字体理论上沿高度"""
        return self._ctx.font_size  # 保守估算为全字号

    @property
    def fontBoundingBoxDescent(self) -> float:
        """字体理论下沿高度"""
        return self._ctx.font_size * 0.25  # 典型西文字体比例

    @property
    def emHeightAscent(self) -> float:
        """EM方块上沿（通常等于字号）"""
        return self._ctx.font_size

    @property
    def emHeightDescent(self) -> float:
        """EM方块下沿（通常为0）"""
        return 0  # 根据CSS规范EM框定义

    @property
    def hangingBaseline(self) -> float:
        """悬挂基线偏移量"""
        return self._ctx.font_size * 0.8  # 近似印度语基线

    @property
    def alphabeticBaseline(self) -> float:
        """字母基线偏移量"""
        return 0  # 基准线对齐点

    @property
    def ideographicBaseline(self) -> float:
        """表意文字基线偏移量"""
        return -self._ctx.font_size * 0.1  # 近似中文基线位置

    def _get_alignment_base_x(self):
        """获取当前对齐方式下的基准X坐标"""
        if self._ctx.textAlign == 'left':
            return 0
        elif self._ctx.textAlign == 'center':
            return self.width / 2
        elif self._ctx.textAlign == 'right':
            return self.width
        return 0

class Canvas2DContext(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._textureFlipList = []

        self._lock = False

        self._lastFuncResult = None

        self._methodsPatchList = [
            'fillText', 'strokeText', 'measureText',
            'clearRect', 'fillRect', 'strokeRect',
            'beginPath', 'closePath', 'moveTo', 'lineTo',
            'rect', 'roundRect', 'fill', 'stroke',
            'clip', 'rotate', 'scale', 'translate',
            'setTransform', 'resetTransform', 'loadTexture',
            'drawImage', 'save', 'restore', 'reset'
        ]

        self._propertiesPatchList = [
            'fillStyle',
            'strokeStyle',
            'lineWidth', 
            'font', 
            'textAlign', 
            'textBaseline',
            'filter',
            'enableGlFlip'
        ]

        self._origMethodsList = {}
        self._warppedMethodsList = {}
        self._origPropertiesList = {}
        self._wrappedPropertiesList = {}

        self.reset()

        self.bind(pos=self._update_rect, size=self._update_rect)

        self.size = Window.size

        self._patchAll()

    def __enter__(self):
        self.beginDraw()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.endDraw()
    
    def _update_rect(self, *args):
        self.___rect.pos = self.pos
        self.___rect.size = self.size
        self._applyMatrix()
        self.canvas.ask_update()
    
    #---------- 样式属性 ----------
    
    @property
    def lineWidth(self) -> float:
        return self._line_width

    @lineWidth.setter
    def lineWidth(self, value: float) -> None:
        self._line_width = value

    @property
    def textAlign(self) -> str:
        return self._text_align

    @textAlign.setter
    def textAlign(self, value: str) -> None:
        self._text_align = value

    @property
    def textBaseline(self) -> str:
        return self._text_baseline

    @textBaseline.setter
    def textBaseline(self, value: str) -> None:
        self._text_baseline = value

    @property
    def font(self):
        return self._font
    
    @font.setter
    def font(self, value):
        self._font = value
        css_font = CSSFont(value)
        self.font_size = css_font.font_size
        self.font_name = css_font._get_kivy_font_name()

    @property
    def fillStyle(self):
        return self._fill_style
    
    @fillStyle.setter
    def fillStyle(self, color_str):
        #设置填充颜色 支持CSS颜色格式
        self._fill_style = CSSColorParser.parse_color(color_str)

    @property
    def strokeStyle(self):
        return self._stroke_style
    
    @strokeStyle.setter
    def strokeStyle(self, color_str):
        #设置描边颜色 支持CSS颜色格式
        self._stroke_style = CSSColorParser.parse_color(color_str)

    @property
    def filter(self) -> str:
        """暂时不实现"""
        return self._filter

    @filter.setter
    def filter(self, value: str) -> None:
        self._filter = value
    
    @property
    def enableGlFlip(self) -> str:
        # 是否使用GPU加速翻转纹理
        return self._enableGlFlip

    @enableGlFlip.setter
    def enableGlFlip(self, value: bool) -> None:
        self._enableGlFlip = value

    #以下为内部方法

    def _draw_shape(self, fill=False):
        """绘制预定义形状"""
        if self._current_shape:
            shape_type, params = self._current_shape
            if shape_type == 'rect':
                x, y, w, h = params
                return Rectangle(pos=(x, y), size=(w, h))
            elif shape_type == 'round_rect':
                x, y, w, h, r = params
                return RoundedRectangle(pos=(x, y), size=(w, h), radius=[r])
        return None

    def _patchAll(self):
        for method in self._methodsPatchList:
            self._wrap_method(method)

        for prop in self._propertiesPatchList:
            self._wrap_property_setter(prop)

    def _restoreAll(self):
        for method in self._methodsPatchList:
            self._restore_method(method)

        for prop in self._propertiesPatchList:
            self._restore_property_setter(prop)

    def _wrap_method(self, method_name):
        if method_name not in self._origMethodsList or method_name not in self._warppedMethodsList:
            self._origMethodsList[method_name] = getattr(self, method_name)
            self._warppedMethodsList[method_name] = self._create_scheduled_method(self._origMethodsList[method_name])
        setattr(self, method_name, self._warppedMethodsList[method_name])

    def _restore_method(self, method_name):
        setattr(self, method_name, self._origMethodsList[method_name])

    def _create_scheduled_method(self, original_func):
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            self._drawInsts.append(
                (original_func, (args, kwargs))
            )
            if original_func.__name__ in [
                'measureText', 'loadTexture'
            ]:
                self.endDraw()
                self.beginDraw()
                
                result = self._lastFuncResult
                self._lastFuncResult = None
                return result
        return wrapper
    
    def _wrap_property_setter(self, prop_name):
        prop = getattr(type(self), prop_name)
        if isinstance(prop, property) and prop.fset:
            if prop_name not in self._origPropertiesList or prop_name not in self._wrappedPropertiesList:
                self._origPropertiesList[prop_name] = prop.fset
                self._wrappedPropertiesList[prop_name] = self._create_scheduled_method(self._origPropertiesList[prop_name])
            new_prop = property(
                fget=prop.fget,
                fset=self._wrappedPropertiesList[prop_name],
                fdel=prop.fdel,
                doc=prop.__doc__
            )
            setattr(type(self), prop_name, new_prop)

    def _restore_property_setter(self, prop_name):
        prop = getattr(type(self), prop_name)
        if isinstance(prop, property) and prop.fset:
            new_prop = property(
                fget=prop.fget,
                fset=self._origPropertiesList[prop_name],
                fdel=prop.fdel,
                doc=prop.__doc__
            )
            setattr(type(self), prop_name, new_prop)
    
    def _apply_clip(self):
        """应用保存的裁剪路径到画布"""
        if not self.clip_path:
            return

        # 使用 Stencil 指令定义裁剪区域
        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            StencilPush()

            # 填充裁剪路径到 Stencil
            Color(1, 1, 1, 1)
            for subpath in self.clip_path:
                if len(subpath) >= 3:
                    vertices = []
                    for point in subpath:
                        vertices.extend((point[0], point[1], 0, 0))  # x, y, u, v
                    Mesh(
                        vertices=vertices,
                        indices=list(range(len(subpath))),
                        mode='triangle_fan'
                    )
            
            StencilUse()
            StencilPop()
            PopMatrix()
    
    def _rotatectx(self):
        Rotate(angle=self._rotation, origin=self.center)

    def _scalectx(self):
        Scale(x=self._scale_x, y=self._scale_y)

    def _translatectx(self):
        Translate(x=self._translate_x, y=self._translate_y)

    def _applyMatrix(self):
        Translate(0, Window.height)
        self._rotatectx()
        self._scalectx()
        self._translatectx()

    def _exce_draw(self, *args, **kwargs):
        self._restoreAll()
        for inst in self._drawInsts:
            mtd, args = inst
            self._lastFuncResult = mtd(*args[0], **args[1])
        self._patchAll()
        self._lock = False

    def _flip(self, texture: Texture):
        if self._enableGlFlip:
            texture.flip_vertical()
            self._textureFlipList.append(texture.id)
            return texture
        pixels = np.frombuffer(texture.pixels, dtype=np.uint8)
        pixels = pixels.reshape((texture.height, texture.width, 4))
        flipped_pixels = pixels.tobytes()
        texture = Texture.create(size=texture.size, colorfmt='rgba')
        texture.blit_buffer(flipped_pixels, colorfmt='rgba')
        self._textureFlipList.append(texture.id)
        return texture

    #以下为暴露的方法

    def beginDraw(self):
        while self._lock: pass
        self._drawInsts = []

    def endDraw(self):
        self._lock = True
        Clock.schedule_once(self._exce_draw, 0)

    def reset(self):
        self._rotation = 0
        self._scale_x = 1
        self._scale_y = 1
        self._translate_x = 0
        self._translate_y = 0
        self._fill_style = (0, 0, 0, 1)
        self._stroke_style = (0, 0, 0, 1)
        self._line_width = 1.0
        self.font_size = 14
        self.font_name = 'Arial'
        self._text_align = 'left'
        self._text_baseline = 'alphabetic'
        self._font = '10px sans-serif'
        self.current_path = []
        self.clip_path = None
        self._state_stack = []
        self._filter = None
        self._enableGlFlip = True
        
        self.canvas.clear()

        with self.canvas:
            Color(1, 1, 1, 1)
            self.___rect = Rectangle(pos=self.pos, size=self.size) # 白色背景
    
    #---------- 基础绘图 API ----------
    def clearRect(self, x, y, width, height):
        """清除指定矩形区域的像素 模拟clearRect"""
        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(1, 1, 1, 1)
            Rectangle(pos=(x, -y), size=(width, -height))
            PopMatrix()

    def fillRect(self, x, y, width, height):
        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(*self.fillStyle)
            Rectangle(pos=(x, -y), size=(width, -height))
            PopMatrix()

    def strokeRect(self, x, y, width, height):
        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(*self.strokeStyle)
            Line(width=self.lineWidth, rectangle=(x, -y, width, -height), close=True)
            PopMatrix()

    #---------- 文本 API ----------
    def fillText(self, text: str, x: float, y: float, max_width: float = None) -> None:
        y = -y
        label = CoreLabel(text=text, font_size=self.font_size, font_name=self.font_name.split(',')[0], valign='top')
        label.refresh()

        texture = self._flip(label.texture)

        text_width, text_height = texture.width, texture.height
        scale_factor = min(max_width / text_width, 1) if max_width else 1.0

        ascent = self.font_size * 0.8
        descent = self.font_size * 0.2
        total_height = ascent + descent

        match self.textBaseline:
            case 'top':
                y_adjust = 0
            case 'middle':
                y_adjust = -total_height / 2
            case 'bottom':
                y_adjust = -total_height
            case _:
                y_adjust = -ascent

        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(*self.fillStyle)
            Rectangle(
                pos=(x, y + y_adjust),
                size=(text_width * scale_factor, -text_height * scale_factor),
                texture=texture
            )
            PopMatrix()


    def strokeText(self, text: str, x: float, y: float, max_width: float = None) -> None:
        """实现描边文本功能"""
        y = -y
        # 创建核心标签对象
        label = CoreLabel(
            text=text,
            font_size=self.font_size,
            font_name=self.font_name.split(',')[0],  # 取第一个可用字体
            valign='top'
        )
        label.refresh()
        
        if not label.texture:
            return

        # 获取文本尺寸和纹理
        texture = label.texture
        text_width = texture.width
        text_height = texture.height

        # 处理最大宽度限制
        scale_factor = 1.0
        if max_width and text_width > max_width:
            scale_factor = max_width / text_width
            text_width = max_width
            text_height *= scale_factor

        # 计算水平位置
        if self.textAlign == 'center':
            x -= text_width * scale_factor / 2
        elif self.textAlign == 'right':
            x -= text_width * scale_factor

        # 计算垂直位置（基于估算的字体度量）
        ascent = self.font_size * 0.8  # 假设ascender占80%
        descent = self.font_size * 0.2  # 假设descender占20%
        total_height = ascent + descent

        match self.textBaseline:
            case 'top':
                y_adjust = 0
            case 'middle':
                y_adjust = -total_height / 2
            case 'bottom':
                y_adjust = -total_height
            case 'alphabetic':
                y_adjust = -ascent
            case _:
                y_adjust = -ascent

        # 应用坐标调整
        pos = (x, y + y_adjust)
        size = (text_width * scale_factor, text_height * scale_factor)

        # 生成描边偏移量（圆形分布）
        radius = int(self.lineWidth)
        offsets = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if dx*dx + dy*dy <= radius*radius:
                    offsets.append((dx, dy))

        # 绘制描边（多偏移量绘制）
        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(*self.strokeStyle)
            for dx, dy in offsets:
                # 应用缩放因子到偏移量
                scaled_dx = dx * scale_factor
                scaled_dy = dy * scale_factor
                Rectangle(
                    pos=(pos[0] + scaled_dx, pos[1] + scaled_dy),
                    size=size,
                    texture=texture
                )
            PopMatrix()

    def measureText(self, text: str) -> dict:
        """完整字体度量实现"""
        label = CoreLabel(
            text=text,
            font_size=self.font_size,
            font_name=self.font_name.split(',')[0],
            valign='top'
        )
        label.refresh()
        return TextMetrics(label, self)

    #---------- 路径 API ----------
    def beginPath(self) -> None:
        """开始新路径"""
        self.current_path = []
        self._current_shape = None

    def closePath(self) -> None:
        """闭合路径"""
        if self.current_path and self.current_path[-1]:  # 检查是否存在子路径及点
            current_subpath = self.current_path[-1]
            if len(current_subpath) >= 1:  # 确保有起点
                # 将首点添加到末尾闭合路径
                current_subpath.append(current_subpath[0])

    def moveTo(self, x: float, y: float) -> None:
        self.current_path.append([(x, -y)])  # 新子路径以当前点开始

    def lineTo(self, x, y):
        """添加直线路径"""
        if not self.current_path:
            self.moveTo(x, y)  # 无子路径时自动创建
        else:
            self.current_path[-1].append((x, -y))

    def rect(self, x, y, w, h):
        """添加矩形路径"""
        self._current_shape = ('rect', (x, y, w, h))
        self.current_path.append([
            (x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)
        ])

    def roundRect(self, x, y, w, h, r):
        """添加圆角矩形路径"""
        self._current_shape = ('round_rect', (x, y, w, h, r))

    def fill(self, fill_rule: str = None) -> None:
        """填充所有子路径"""
        with self.canvas:
            PushMatrix()       # 开启变换上下文
            self._applyMatrix()  # 应用坐标系转换
            self._apply_clip()
            Color(*self.fillStyle)
            for subpath in self.current_path:
                if len(subpath) >= 3:
                    vertices = []
                    for point in subpath:
                        x, y = point
                        vertices.extend([x, y, 0, 0])  # 正确构建顶点数据
                    Mesh(
                        vertices=vertices,
                        indices=list(range(len(subpath))),
                        mode='triangle_fan'
                    )
            PopMatrix()

    def stroke(self) -> None:
        with self.canvas:
            PushMatrix()       # 开启变换上下文
            self._applyMatrix()  # 应用坐标系转换
            self._apply_clip()
            Color(*self.strokeStyle)
            for subpath in self.current_path:
                if len(subpath) >= 2:
                    points = []
                    for point in subpath:
                        points.extend(point)  # 直接展开坐标
                    Line(points=points, width=self.lineWidth)
            PopMatrix()

    def clip(self, fill_rule: str = None) -> None:
        """裁剪路径，保存当前路径为裁剪区域"""
        if self.current_path:
            self.clip_path = [subpath.copy() for subpath in self.current_path]
        else:
            self.clip_path = None

    #---------- 变换 API ----------
    def rotate(self, angle):
        """旋转操作"""
        self._rotation += angle

    def scale(self, sx, sy):
        """缩放操作"""
        self._scale_x *= sx
        self._scale_y *= sy

    def translate(self, tx, ty):
        """平移操作"""
        self._translate_x += tx
        self._translate_y += ty

    def setTransform(self, a, b, c, d, tx, ty):
        """设置变换属性"""
        # 计算缩放
        self._scale_x = math.sqrt(a * a + b * b)
        self._scale_y = math.sqrt(c * c + d * d)

        # 计算旋转角度
        self._rotation = math.degrees(math.atan2(b, a))

        # 平移
        self._translate_x = tx
        self._translate_y = ty

    def resetTransform(self):
        """重置变换操作"""
        self._rotation = 0
        self._scale_x = 1
        self._scale_y = 1
        self._translate_x = 0
        self._translate_y = 0

    @property
    def globalAlpha(self) -> float:
        """全局透明度"""
        return 1.0

    @globalAlpha.setter
    def globalAlpha(self, value: float) -> None:
        pass

    #---------- 图像 API ----------
    def loadTexture(self, image):
        #加载不同格式的图像源为纹理
        if isinstance(image, str):
            texture = CoreImage(image).texture
            texture = self._flip(texture)
            return texture
        if isinstance(image, Texture):
            if not image.id in self._textureFlipList:
                image = self._flip(image)
            return image
        if hasattr(image, "texture"):
            if not image.texture.id in self._textureFlipList:
                return self._flip(image.texture)
            return image.texture
        raise TypeError("Unsupported image type")
    
    def drawImage(self, image, *args):
        """
        支持三种重载形式：
        1. drawImage(image, dx, dy)
        2. drawImage(image, dx, dy, dWidth, dHeight)
        3. drawImage(image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
        """

        match len(args):
            case 2:
                dx, dy = args
                source_rect = None
                dw, dh = None, None
            case 4:
                dx, dy, dw, dh = args
                source_rect = None
            case 8:
                sx, sy, sw, sh, dx, dy, dw, dh = args
                source_rect = (sx, sy, sw, sh)
            case _:
                raise ValueError("Invalid arguments. Expected 2, 4 or 8 parameters")
        
        texture = self.loadTexture(image)
        
        if source_rect:
            sx, sy, sw, sh = source_rect
            # 转换坐标系（浏览器左上角原点到Kivy左下角原点）
            sy_adj = texture.height - (sy + sh)
            source_region = texture.get_region(sx, sy_adj, sw, sh)
        else:
            sw, sh = texture.width, texture.height
            source_region = texture
            if len(args) == 2:  # 使用原始尺寸
                dw, dh = sw, sh

        with self.canvas:
            PushMatrix()
            self._applyMatrix()
            Color(1, 1, 1, 1)
            Rectangle(
                texture=source_region,
                pos=(dx, -dy),
                size=(dw, -dh) if dh else (sw, -sh)
            )
            PopMatrix()

    def save(self) -> None:
        state = {
            'fill_style': self._fill_style,
            'stroke_style': self._stroke_style,
            'line_width': self._line_width,
            'font': self._font,
            'text_align': self._text_align,
            'text_baseline': self._text_baseline,
            'clip_path': copy.deepcopy(self.clip_path),
            'scale_x': self._scale_x,
            'scale_y': self._scale_y,
            'rotation': self._rotation,
            'translate_x': self._translate_x,
            'translate_y': self._translate_y,
            'current_path': copy.deepcopy(self.current_path),
            'filter': self._filter,
            'global_alpha': self.globalAlpha,
            'enableGlFlip': self._enableGlFlip
        }
        self._state_stack.append(state)

    def restore(self) -> None:
        state = self._state_stack.pop()
        self._fill_style = state['fill_style']
        self._stroke_style = state['stroke_style']
        self._line_width = state['line_width']
        self.font = state['font']
        self._text_align = state['text_align']
        self._text_baseline = state['text_baseline']
        self.clip_path = state['clip_path']
        self._scale_x = state['scale_x']
        self._scale_y = state['scale_y']
        self._rotation = state['rotation']
        self._translate_x = state['translate_x']
        self._translate_y = state['translate_y']
        self.current_path = copy.deepcopy(state['current_path'])
        self._filter = state['filter']
        self.globalAlpha = state['global_alpha']
        self._enableGlFlip = state['enableGlFlip']

    def regFont(self, name: str, path: str) -> None:
        #注册字体
        LabelBase.register(
            name=name,
            fn_regular=path
        )

if __name__ == '__main__':
    ctx = Canvas2DContext()
    class ctxApp(App):
        def build(self, **kwargs): return ctx

    app = ctxApp()
    
    def draw():
        import time
        with ctx:
            #ico = ctx.loadTexture('icon.ico')
            ctx.regFont('Phigros', 'font.ttf')
        while True:
            with ctx:
                ctx.reset()

                ctx.beginPath()
                ctx.strokeStyle = 'blue'
                ctx.moveTo(20, 20)
                ctx.lineTo(200, 20)
                ctx.stroke()

                ctx.beginPath()
                ctx.strokeStyle = 'red'
                ctx.moveTo(20, 20)
                ctx.lineTo(120, 120)
            time.sleep(1 / 60)

    Thread(target = draw, daemon = True).start()
    app.run()