import tkinter as tk
from tkinter import messagebox
import random
import os
from datetime import datetime
import math

# ==================== 配置参数 ====================
MAX_WINDOWS = 60           # 减少窗口数，确保渐变流畅
CARD_W, CARD_H = 320, 130
FONT = ('微软雅黑', 20, 'bold')
POP_INTERVAL = 250       # 放慢弹出速度，增强观赏体验
COLOR_CHANGE_SPEED = 80    # 色彩变化间隔（值越大越舒缓）
COLOR_TRANSITION_MODES = [  # 色彩过渡模式
    "linear",    # 线性渐变
    "radial",    # 径向渐变
    "hue_shift", # 色相偏移
    "random_wave"# 随机波动
]

# 私人个性化配置
PERSONAL_NAME = "余心留白"
SPECIAL_DATES = {
    (12, 25): "圣诞快乐呀～",
    (1, 1): "新年新气象！",
    (2, 14): "今天的专属甜蜜～",
    (5, 20): "520快乐，我的宝～"
}
ICON_PATH = "emoji_icon.ico"

# 优化的基础色彩库（更和谐的色调组合）
BASE_COLORS = [
    ("#ff6b6b", "#ff8e8e"), ("#ffd166", "#f9c74f"),  # 暖色系
    ("#06d6a0", "#90e0ef"), ("#118ab2", "#0077b6"),  # 冷色系
    ("#9b5de5", "#f15bb5"), ("#fee440", "#00f5d4"),  # 亮色系
    ("#5e60ce", "#73d2de"), ("#f8b195", "#f67280")   # 过渡色系
]

# 个性化祝福语
WORDS = [
    f"{PERSONAL_NAME}，今天的阳光和你一样温暖～",
    f"突然想起上次和{PERSONAL_NAME}一起喝的奶茶，甜度刚好",
    "路过街角的花店，看到你喜欢的那束花又开了",
    f"{PERSONAL_NAME}皱眉的时候，睫毛会轻轻垂下来，像小扇子一样",
    "刚才的歌单里，偷偷藏了好多想和你一起听的歌",
    "今天的备忘录里，记着你说过的每句可爱的话",
    f"今天穿了件和{PERSONAL_NAME}同款色系的衣服，莫名开心",
    "看到一只像你家猫咪（或狗狗）的小家伙，差点想抱回家",
    f"{PERSONAL_NAME}笑起来的时候，眼角的小细纹都在发光呢",
    "刚才抬头看云，发现一朵像你画的小兔子的形状",
    "买咖啡时，下意识点了和你一样的口味",
    f"突然想知道{PERSONAL_NAME}现在在做什么，是不是也在发呆呀",
    "整理相册时，翻到上次和你合照，嘴角忍不住上扬了",
    "今天的风很舒服，适合和你一起慢慢散步",
    f"{PERSONAL_NAME}认真做事的时候，侧脸轮廓真好看",
    "听到一句很美的诗，第一个想分享给你",
    "冰箱里还剩你上次带来的饼干，舍不得吃完",
    f"如果{PERSONAL_NAME}现在在身边，好想轻轻捏一下你的脸颊",
    "今天学到一个冷知识，等见面时讲给你听",
    "看到小朋友手里的气球，想起你说小时候最怕气球爆炸",
    f"{PERSONAL_NAME}的声音，比雨天的白噪音还好听",
    "路过我们上次一起躲雨的屋檐，雨又下起来了",
    "今天的月亮好圆，像你送我的那个小镜子",
    f"突然发现，和{PERSONAL_NAME}有关的小事都记得好清楚",
    "吃到一家超好吃的店，已经记在小本本上，等你回来一起去",
    "今天也有努力生活，因为想快点跟上你的脚步呀",
    f"{PERSONAL_NAME}偶尔犯迷糊的样子，其实超可爱的",
    "看到一句情话：'你走的每一步，都在我心上'，觉得很适合我们",
    "天气转晴了，适合晒被子，也适合想你",
    f"和{PERSONAL_NAME}在一起的时间，连空气都是甜的",
    "今天穿了新鞋子，走了很多路，想走到你身边去",
    "听到你喜欢的歌手发了新歌，第一时间分享给你啦",
    f"{PERSONAL_NAME}的名字，在我心里念了一遍又一遍",
    "买了本想和你一起看的书，已经标好了想和你讨论的段落",
    "今天的晚霞是粉色的，像你上次涂的口红颜色",
    f"就算不说什么，只要{PERSONAL_NAME}在身边，就很安心",
    "看到一对老夫妻牵手散步，突然想到我们老了会不会也这样",
    "今天喝了太多水，因为你说多喝水对身体好",
    f"{PERSONAL_NAME}的小缺点，在我眼里都变成了小可爱",
    "攒了好多有趣的日常，等见面时一股脑讲给你听",
    "今天也有好好吃饭，因为记得你说过要照顾好自己"
]
# =============================================

windows = []  # 存储所有卡片窗口的列表

def get_special_greeting():
    """获取特殊日期的专属祝福"""
    today = datetime.now()
    month_day = (today.month, today.day)
    return SPECIAL_DATES.get(month_day, None)

def hex_to_rgb(hex_color):
    """将十六进制颜色转换为RGB值"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """将RGB值转换为十六进制颜色"""
    return '#%02x%02x%02x' % rgb

def blend_colors(color1, color2, ratio):
    """混合两种颜色，优化了色彩过渡算法"""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    
    # 使用平方缓和曲线使过渡更自然（先慢后快再慢）
    eased_ratio = 0.5 - 0.5 * math.cos(ratio * math.pi)
    
    r = int(r1 * (1 - eased_ratio) + r2 * eased_ratio)
    g = int(g1 * (1 - eased_ratio) + g2 * eased_ratio)
    b = int(b1 * (1 - eased_ratio) + b2 * eased_ratio)
    
    return rgb_to_hex((r, g, b))

def hsv_to_rgb(h, s, v):
    """HSV色彩空间转RGB（用于色相偏移效果）"""
    if s == 0:
        return (v, v, v)
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    i = i % 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    return (v, p, q)

def rgb_to_hsv(r, g, b):
    """RGB转HSV色彩空间"""
    r, g, b = r/255.0, g/255.0, b/255.0
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    h, s, v = max_val, max_val, max_val
    
    d = max_val - min_val
    s = 0 if max_val == 0 else d / max_val
    
    if max_val == min_val:
        h = 0
    else:
        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    return (h, s, v)

def draw_linear_gradient(canvas, w, h, color1, color2, angle=0):
    """绘制线性渐变（支持角度调整）"""
    canvas.delete("all")
    angle_rad = math.radians(angle)
    
    for y in range(h):
        for x in range(w):
            # 计算当前点在渐变方向上的比例
            pos = x * math.cos(angle_rad) + y * math.sin(angle_rad)
            max_pos = w * math.cos(angle_rad) + h * math.sin(angle_rad)
            ratio = max(0, min(1, pos / max_pos))
            color = blend_colors(color1, color2, ratio)
            canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline="")

def draw_radial_gradient(canvas, w, h, color1, color2):
    """绘制径向渐变（从中心向外扩散）"""
    canvas.delete("all")
    center_x, center_y = w/2, h/2
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(h):
        for x in range(w):
            # 计算到中心的距离比例
            dist = math.sqrt((x - center_x)** 2 + (y - center_y)**2)
            ratio = min(1, dist / max_dist)
            color = blend_colors(color1, color2, ratio)
            canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline="")

def draw_hue_shift(canvas, w, h, base_hue, phase):
    """色相偏移渐变（同一亮度不同色相）"""
    canvas.delete("all")
    for y in range(h):
        for x in range(w):
            # 计算色相偏移值
            hue = (base_hue + (x/w + y/h + phase) % 1) % 1
            r, g, b = hsv_to_rgb(hue, 0.7, 0.9)
            color = rgb_to_hex((int(r*255), int(g*255), int(b*255)))
            canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline="")

def draw_random_wave(canvas, w, h, color1, color2, phase):
    """随机波浪渐变（模拟流体效果）"""
    canvas.delete("all")
    for y in range(h):
        # 生成波浪基线
        wave = math.sin(y/h * 4 + phase) * 0.2 + 0.5
        for x in range(w):
            # 叠加随机波动
            noise = math.sin(x/w * 8 + phase*0.7) * 0.1
            ratio = wave + noise
            ratio = max(0, min(1, ratio))
            color = blend_colors(color1, color2, ratio)
            canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline="")

def update_colors(card_win, canvas, mode, color_data, phase):
    """更新卡片颜色（根据不同模式）"""
    if card_win not in windows:
        return
    
    new_phase = (phase + 0.02) % (2 * math.pi)  # 相位缓慢变化
    
    # 根据不同模式绘制渐变
    if mode == "linear":
        color1, color2, angle = color_data
        draw_linear_gradient(canvas, CARD_W-4, CARD_H-4, color1, color2, angle + phase*10)
        base_color = blend_colors(color1, color2, 0.5)
        
    elif mode == "radial":
        color1, color2 = color_data
        draw_radial_gradient(canvas, CARD_W-4, CARD_H-4, color1, color2)
        base_color = color1
        
    elif mode == "hue_shift":
        base_hue = color_data
        draw_hue_shift(canvas, CARD_W-4, CARD_H-4, base_hue, phase)
        r, g, b = hsv_to_rgb((base_hue + phase/5) % 1, 0.7, 0.9)
        base_color = rgb_to_hex((int(r*255), int(g*255), int(b*255)))
        
    elif mode == "random_wave":
        color1, color2 = color_data
        draw_random_wave(canvas, CARD_W-4, CARD_H-4, color1, color2, phase)
        base_color = blend_colors(color1, color2, 0.5)
    
    # 计算文字颜色（确保可读性）
    r, g, b = hex_to_rgb(base_color)
    brightness = (r * 299 + g * 587 + b * 114) // 1000
    text_color = "#ffffff" if brightness < 160 else "#333333"
    canvas.itemconfig("text", fill=text_color)
    
    # 继续更新
    card_win.after(COLOR_CHANGE_SPEED, update_colors, card_win, canvas, mode, color_data, new_phase)

def create_card():
    """创建带高级色彩过渡的祝福卡片"""
    global windows
    
    if len(windows) >= MAX_WINDOWS:
        old_win = windows.pop(0)
        old_win.destroy()

    # 选择祝福文字
    special_greet = get_special_greeting()
    text = special_greet if special_greet else random.choice(WORDS)
    
    # 随机选择过渡模式
    mode = random.choice(COLOR_TRANSITION_MODES)
    
    # 根据模式准备颜色数据
    if mode == "linear":
        color_pair = random.choice(BASE_COLORS)
        color_data = (*color_pair, random.randint(0, 180))  # 颜色1, 颜色2, 角度
    elif mode == "radial":
        color_data = random.choice(BASE_COLORS)  # 颜色1, 颜色2
    elif mode == "hue_shift":
        color_data = random.random()  # 基础色相
    elif mode == "random_wave":
        color_data = random.choice(BASE_COLORS)  # 颜色1, 颜色2

    # 创建窗口
    card_win = tk.Toplevel()
    card_win.title(f"给{PERSONAL_NAME}的小惊喜")
    
    # 设置图标
    if os.path.exists(ICON_PATH):
        try:
            card_win.iconbitmap(ICON_PATH)
        except:
            pass
    
    card_win.configure(bg="#f0f0f0")
    card_win.geometry(f"{CARD_W}x{CARD_H}")
    card_win.attributes("-topmost", False)

    # 创建画布
    canvas = tk.Canvas(
        card_win,
        width=CARD_W-4,
        height=CARD_H-4,
        highlightthickness=0
    )
    canvas.place(x=2, y=2)

    # 添加文字
    canvas.create_text(
        (CARD_W-4)//2, (CARD_H-4)//2,
        text=text,
        font=FONT,
        width=CARD_W-60,
        tags="text"
    )

    # 随机位置
    screen_width = card_win.winfo_screenwidth()
    screen_height = card_win.winfo_screenheight()
    x_pos = random.randint(0, max(0, screen_width - CARD_W - 20))
    y_pos = random.randint(0, max(0, screen_height - CARD_H - 60))
    card_win.geometry(f"+{x_pos}+{y_pos}")

    # 启动色彩更新
    update_colors(card_win, canvas, mode, color_data, 0)

    # 拖动功能
    def start_drag(event):
        card_win._drag_x = event.x
        card_win._drag_y = event.y

    def on_drag(event):
        new_x = card_win.winfo_x() + (event.x - card_win._drag_x)
        new_y = card_win.winfo_y() + (event.y - card_win._drag_y)
        card_win.geometry(f"+{new_x}+{new_y}")

    canvas.bind("<Button-1>", start_drag)
    canvas.bind("<B1-Motion>", on_drag)

    # 双击关闭
    def close_on_double_click(event):
        if card_win in windows:
            windows.remove(card_win)
        card_win.destroy()
    canvas.bind("<Double-1>", close_on_double_click)

    windows.append(card_win)

def show_help():
    """显示帮助信息"""
    messagebox.showinfo(
        "使用说明",
        f"这是给{PERSONAL_NAME}的专属渐变祝福卡片～\n"
        "• 双击卡片可以关闭它\n"
        "• 拖动卡片可以改变位置\n"
        "• 卡片有多种色彩流动效果哦\n"
        "• 特殊日期会有专属祝福"
    )

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_help()

    def pop_cards():
        create_card()
        root.after(POP_INTERVAL, pop_cards)

    root.after(1000, pop_cards)
    root.mainloop()
