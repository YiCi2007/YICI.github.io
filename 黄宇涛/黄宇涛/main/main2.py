import pygame, os, sys, random
from pygame.constants import SRCALPHA

pygame.init()
pygame.mixer.init()
# pygame.mixer.music.load("../music/背景音乐6.mp3")
按钮 = pygame.mixer.Sound("../defaultMusic/功能.mp3")
pygame.font.init()
font = pygame.font.SysFont("Kaiti", 30)
pygame.display.set_caption("黄宇涛生日快乐")
width, height = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("../img/icon.jpg")
screen_fill = pygame.transform.scale(icon, (width, height))
pygame.display.set_icon(icon)
FONT_COLOR = (255, 255, 255)
cursor_image = pygame.image.load("../img/光标.png").convert_alpha()
custom_cursor = pygame.cursors.Cursor((5, 5), cursor_image)
# 应用自定义光标
pygame.mouse.set_cursor(custom_cursor)
class 加载画面:
    def __init__(self):
        self.size = (width * 0.7, height*0.07)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(width/2, height*0.8))
        self.bg_color = (80, 255, 80)
        self.font = pygame.font.SysFont("Kaiti", 30, bold=False, italic=True)
        self.font_color = (255, 255, 255)
        self.texts = ["加载中", "加载中.", "加载中..", "加载中..."]
        self.text_end = "加载完成"
        self.text_目标 = self.texts[0]
        self.text = self.font.render(self.text_目标, True, self.font_color)
        self.speed = 1
        self.w = 0
        self.h = 0
        self.clock_进度条_1 = pygame.time.get_ticks()
        self.clock_加载中_1 = pygame.time.get_ticks()
    def update(self):
        self.image.fill((0, 0, 0, 0))
        self.加载进度条()
        self.加载中()
        screen.blit(self.image, self.rect)
    def 加载进度条(self):
        self.clock_进度条_2 = pygame.time.get_ticks()
        if self.clock_进度条_2 - self.clock_进度条_1 >= 500:
            self.clock_进度条_1 = pygame.time.get_ticks()
            self.speed = random.uniform(0.1, 4)
        self.w += self.speed
        self.w = max(0, min(self.w, self.rect.width))
        self.h += self.speed
        self.h = max(0, min(self.h, self.rect.height))
        pygame.draw.rect(self.image, self.bg_color, (0, (self.rect.height - self.h) / 2, self.w, self.h), 0,
                         border_radius=50)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.rect.width, self.rect.height), 7, border_radius=50)
    def 加载中(self):
        self.clock_加载中_2 = pygame.time.get_ticks()
        if self.clock_加载中_2 - self.clock_加载中_1 >= 300 and self.w < self.rect.width:
            self.clock_加载中_1 = pygame.time.get_ticks()
            if self.text_目标 == self.texts[-1]:
                self.text_目标 = self.texts[0]
            else:
                try:
                    self.text_目标 = self.texts[self.texts.index(self.text_目标) + 1]
                except:
                    pass
        elif self.w >= self.rect.width:
            self.text_目标 = self.text_end
            self.font_color = (255, 255, 80)
        self.text = self.font.render(self.text_目标, True, self.font_color)
        self.text_rect = self.text.get_rect(centery=self.rect.height/2)
        self.text_rect.x = self.rect.width*0.45
        self.image.blit(self.text, self.text_rect)
    def 重置(self):
        self.w = 0
        self.h = 0
        self.font_color = (255, 255, 255)
        self.clock_进度条_1 = pygame.time.get_ticks()
        self.clock_加载中_1 = pygame.time.get_ticks()
        self.text_目标 = self.texts[0]
        self.text = self.font.render(self.text_目标, True, self.font_color)
加载画面s = 加载画面()
class Clock:
    def __init__(self, types, center_x):
        self.center_x = center_x
        self.image = pygame.Surface((height//6, height//6))
        self.rect = self.image.get_rect()
        self.tuple = []
        if types == "year":
            for i in range(1999, 2050):
                self.tuple.append(i)
        elif types == "moon":
            for i in range(1, 13):
                self.tuple.append(i)
        elif types == "day":
            for i in range(1, 32):
                self.tuple.append(i)

        self.inplace = 0 # 当前窗口顶部的x坐标
        self.place = 0 # 鼠标坐标x
        self.last_inplace = 0  # 记录上一次窗口顶部的x坐标
        self.可滑动 = False

        self.font_path = pygame.font.match_font('simhei') or pygame.font.match_font(
            'kaiti') or pygame.font.get_default_font()

        self.font_max = 80
        self.font_min = 10
        self.item_height = self.rect.width #150
        self.font_color = (255, 128, 200)
        
        self.线条_w = self.item_height*0.6
        self.线条_h = self.item_height/10
    def update(self):
        self.滑动()
        self.is_mouse_over()
        self.rect.center = (self.center_x, height / 2)
        self.image.fill((100, 128, 200, 255))
        self.font_change()
        screen.blit(self.image, self.rect)
    def font_change(self):
        if self.可滑动 or self.is_mouse_over():
            self.font_color = (255, 0, 0)
        else:
            self.font_color = (255, 128, 200)
        # 计算当前可见区域的数字范围
        self.visible_start = abs(self.inplace) // self.item_height
        self.visible_end = self.visible_start + 3  # 显示中心位置前后几个数字
        self.visible_end = min(self.visible_end, len(self.tuple))
        # 计算每个可见数字的位置并渲染
        for i in range(self.visible_start, self.visible_end):
            # 计算数字的中心位置（相对于显示窗口）
            self.number_center_y = (i * self.item_height) + self.item_height // 2 + self.inplace
            # 计算数字到窗口中心的距离
            self.distance_to_center = abs(self.number_center_y - self.item_height // 2)

            self.font_size = max(self.font_min, min(self.font_max - (self.distance_to_center // 2), self.font_max))
            self.font = pygame.font.SysFont(self.font_path, self.font_size)
            # 渲染数字
            self.tuple_text = str(self.tuple[i])
            self.text_surface = self.font.render(self.tuple_text, True, (255, 128, 200))
            self.text_rect = self.text_surface.get_rect(center=(self.item_height // 2, self.number_center_y))

            self.image.blit(self.text_surface, self.text_rect)
            pygame.draw.rect(self.image, self.font_color, (((self.item_height - self.线条_w)//2, self.number_center_y-self.item_height//2-self.线条_h//2), (self.线条_w, self.线条_h)), 0, border_radius=round(self.线条_h))
        pygame.draw.rect(self.image, self.font_color, (((self.item_height - self.线条_w)//2, self.number_center_y+self.item_height//2-self.线条_h//2), (self.线条_w, self.线条_h)), 0, border_radius=round(self.线条_h))

    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)
    def 校准精度(self):
        if self.可滑动:
            self.inplace = round(self.inplace / self.item_height) * self.item_height
    def 滑动(self):
        if self.可滑动:
            self.new_position = self.last_inplace + self.mouse_pos[1] - self.place
            # 当前窗口顶部的x坐标
            self.inplace = max(-self.item_height * (len(self.tuple) - 1), min(self.new_position, 0))
    def return_value(self):
        return self.tuple[abs(self.inplace)//self.item_height]
    def 重置(self):
        self.inplace = 0
        self.last_inplace = 0  # 记录上一次滑动结束时的位置
        self.可滑动 = False
class Unlock:
    def __init__(self):
        self.size = (width*0.2, width*0.1)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(width / 2, height / 1.3))
        self.font = pygame.font.SysFont("Kaiti", 30, True)
        self.color = (255, 128, 200)
        pygame.draw.rect(self.image, self.color, (0, 0, self.size[0], self.size[1]), border_radius=10)
        self.text = self.font.render("解锁", True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.rect.width/2, self.rect.height/2*1.2))
        self.unlock = False
        self.clock_image = "../img/clock.png"
    def update(self):
        if self.unlock:
            self.clock_image = "../img/unlock.png"
        if self.is_mouse_over():
            self.color = (255, 0, 0)
        else:
            self.color = (255, 128, 200)
        pygame.draw.rect(self.image, self.color, ((0, 0), self.size), border_radius=10)
        self.image.blit(pygame.image.load(self.clock_image), ((self.rect.width-60)/2, 40))
        #self.image.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)
    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)
clock1 = Clock("year", width*0.3125)
clock2 = Clock("moon", width*0.5)
clock3 = Clock("day", width*0.6875)
unlock1 = Unlock()
unlock2 = Unlock()
class Letter:
    def __init__(self, x, y):
        self.width = width * 0.4
        self.height = 0
        self.height_max = height * 0.9
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.letter_img = pygame.image.load("../img/bg.jpg")
        self.letter_img.set_alpha(255)
        # self.image.blit(self.letter_img, (0, 0))
        self.font = pygame.font.SysFont("Kaiti", 20, False, False)
        self.font_color = (80, 100, 150)
        self.font_color_change_speed = 2
        self.font_srcalpha_change_speed = 10

        self.time_clock = True
        self.time_lock = pygame.time.get_ticks()
        # 读取文字
        """with open("../Letter/letter.txt", "r", encoding="utf-8") as f:
            self.letters = f.read()"""
        self.letters = "祝福语寿星黄宇涛：恭喜啊，虽然你又老了一岁，但在我心里，你永远是那个智商欠费、颜值来凑的家伙。希望你将来暴富（带我）、暴帅，苟富贵，勿相忘！同时也感谢你在我最低谷的时候拉我一把，在我得意的时候泼我冷水，这辈子有你这个兄弟，真的赚麻了。在将来咱一起努力发大财，去吃大餐，还要去东北打雪仗。好了，就先说这些，剩下的明年再说，这是我为你准备独一无二的礼物，希望你会喜欢（不喜欢给我受着），快去许愿吧！署名：  卢佳成日期：2026年6月8日"
        self.letters = self.letters.replace(" ", "").replace("\n", "")
        # 初始化文字位置
        self.text_页边距 = 30
        self.char = self.font.size(self.letters[0])[0]
        self.text_x = (self.width - self.char)/2 - self.char
        self.text_y = 40
        self.text_h = 45
        self.letter_rect_char = []
        for i in range(len(self.letters)):
            self.char = self.font.size(self.letters[i])[0]
            # 判断是否超过页边距
            if self.text_x > self.rect.width - self.text_页边距:
                self.text_x = self.text_页边距
                self.text_y += self.text_h

            # 存储文字位置
            self.letter_rect_char.append([self.letters[i], self.text_x, self.text_y, 0, [255, 255, 255]])
            # 设置下一个文字x的位置
            self.text_x += self.char

            # 段落换行
            if ((self.letters[i - 1] == "涛" and self.letters[i] == "：")
                    or (self.letters[i - 1] == "仗" and self.letters[i] == "。")):
                self.text_x = self.char * 2 + self.text_页边距
                self.text_y += self.text_h+10
            # 名字前空格
            elif (self.letters[i - 1] == "名") and (self.letters[i] == "："):
                self.none = "  "
                self.text_x += self.char
            # 祝福语空格
            elif (self.letters[i - 2] == "祝") and (self.letters[i - 1] == "福") and (self.letters[i] == "语"):
                self.text_x = self.text_页边距
                self.text_y += self.text_h*2
            # 署名
            elif (self.letters[i - 1] == "吧") and (self.letters[i] == "！"):
                self.text_x = self.width * 0.6
                self.text_y = self.height_max * 0.85
            # 日期
            elif (self.letters[i - 1] == "佳") and (self.letters[i] == "成"):
                self.text_x = self.width * 0.6
                self.text_y += self.text_h

        self.get_clock_yn = True
        self.get_clock_time = pygame.time.get_ticks()

        self.book_update_yn = False
        self.book_speed = -5
    def update(self):
        self.book_update()
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((240, 230, 100)) #(255, 225, 158)
        self.get_clock()
        screen.blit(self.image, self.rect)
    def book_update(self):
        self.height = max(0, min(self.height + self.book_speed, self.height_max))
    def get_clock(self):
        if self.get_clock_yn == True:
            self.get_clock_yn = False
            self.get_clock_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.get_clock_time > 1000:
            self.text_color_change()
    # 重置颜色透明度
    def reset_color_alpha(self):
        # self.get_clock_yn = True
        for i in range(len(self.letter_rect_char)):
            self.letter_rect_char[i][3] = 0
            self.letter_rect_char[i][4] = [255, 255, 255]
    def text_color_change(self):
        # 遍历每个字符
        for i in range(len(self.letter_rect_char)):
            # 单个文字加载
            self.text = self.font.render(self.letter_rect_char[i][0], True, self.letter_rect_char[i][4])

            # 文字透明度变化
            if i == 0:
                self.letter_rect_char[i][3] += self.font_srcalpha_change_speed
                self.letter_rect_char[i][3] = max(0, min(self.letter_rect_char[i][3], 255))
            elif self.letter_rect_char[i-1][3] > 30:
                self.letter_rect_char[i][3] += self.font_srcalpha_change_speed
                self.letter_rect_char[i][3] = max(0, min(self.letter_rect_char[i][3], 255))

            # 文字颜色变化
            if self.letter_rect_char[i][3] == 255:
                self.letter_rect_char[i][4][1] -= self.font_color_change_speed
                self.letter_rect_char[i][4][1] = max(self.font_color[1], min(self.letter_rect_char[i][4][1], 255))
                if self.letter_rect_char[i][4][1] == self.font_color[1]:
                    self.letter_rect_char[i][4][0] -= self.font_color_change_speed
                self.letter_rect_char[i][4][0] = max(self.font_color[0], min(self.letter_rect_char[i][4][0], 255))
                if self.letter_rect_char[i][4][0] == self.font_color[0]:
                    self.letter_rect_char[i][4][2] -= self.font_color_change_speed
                self.letter_rect_char[i][4][2] = max(self.font_color[2], min(self.letter_rect_char[i][4][2], 255))

            # 加载文字透明度
            self.text.set_alpha(self.letter_rect_char[i][3])

            # 定位文字位置
            self.text_rect = self.text.get_rect(left=self.letter_rect_char[i][1], top=self.letter_rect_char[i][2])
            # 将文字绘制到图片上
            self.image.blit(self.text, self.text_rect)
            # 文字颜色随鼠标位置变化， 并且文字透明度为255时才变化
            if self.is_mouse_over() and self.letter_rect_char[i][3] == 255:
                self.letter_rect_char[i][4][0] = 255
                self.letter_rect_char[i][4][1] = 255
                self.letter_rect_char[i][4][2] = 255
                # self.letter_rect_char[i][3] = 0
    # 判断鼠标位置是否在文字上
    def is_mouse_over(self):
        # 获取鼠标位置并改为列表形式，方便后续校准
        self.mouse_pos = list(pygame.mouse.get_pos())
        # 校准鼠标位置到文字矩形框内
        self.mouse_pos[0] -= self.rect.left
        self.mouse_pos[1] -= self.rect.top
        #返回鼠标位置是否在文字上的布尔值
        return self.text_rect.collidepoint(self.mouse_pos)
    def 重置(self):
        self.reset_color_alpha()
        self.height = 0
        self.book_speed = -5
        self.book_update_yn = False
class Underline:
    def __init__(self):
        self.line_width = 0
    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)
    def under_line(self):
        if self.is_mouse_over():
            self.line_width += 8
        else:
            self.line_width -= 5
        self.line_width = max(0, min(self.line_width, self.width))
class Button(Underline, pygame.sprite.Sprite):
    def __init__(self, icon, center_x, center_y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.icon = pygame.transform.scale(pygame.image.load(icon), (self.width, self.height))
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (center_x, center_y))

        self.yn_button = False

    def update(self):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.icon, (0, 0))
        self.under_line()
        pygame.draw.rect(self.image, (255, 0, 0), ((self.width-self.line_width)/2, self.height - 10, self.line_width, 10), border_radius=4)
        screen.blit(self.image, self.rect)

class Music_Panel:
    def __init__(self):
        self.image_panel = pygame.Surface((width*0.74, height-40), pygame.SRCALPHA)
        self.rect_panel = self.image_panel.get_rect()
        self.rect_panel.x, self.rect_panel.y = width*0.25, 20
        self.color_panel = (255, 255, 0, 0)
    def update(self):
        screen.blit(self.image_panel, self.rect_panel)
class Music_Area(Music_Panel):
    def __init__(self):
        super().__init__()
        self.image_area = pygame.Surface((width*0.74, height-200), pygame.SRCALPHA)
        self.rect_area = self.image_area.get_rect()
        self.rect_area.x, self.rect_area.y = 0, 0
        self.color_area = (255, 0, 0)

        self.滑动_area_speed = 0

    def update(self):
        pygame.draw.rect(music_area.image_area, (255, 255, 255),
                         (0, 0, music_area.rect_area.width, music_area.rect_area.height), border_radius=30)
        self.image_panel.blit(self.image_area, self.rect_area)
        if self.is_mouse_over():
            self.rect_area.x += 1
            # print(self.rect_area.x)
        super().update()
    def 上滑动(self):
        self.滑动_area_speed = 50
    def 下滑动(self):
        self.滑动_area_speed = -50
    def 不滑动(self):
        self.滑动_area_speed = 0
    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.relative_pos = (
            self.mouse_pos[0] - self.rect_panel.x,
            self.mouse_pos[1] - self.rect_panel.y
        )
        return self.rect_area.collidepoint(self.relative_pos)
music_area = Music_Area()
class Music_Button():
    def __init__(self, music_name, center_y, color):
        super().__init__()
        self.image_area = music_area
        self.rect_area = self.image_area.rect_area
        self.center_y = center_y
        self.image_item = pygame.Surface((width*0.7, 60))
        self.rect_item = self.image_item.get_rect(center = (self.rect_area.width/2, self.center_y))
        self.color_item = color
        self.new_color_item = color

        self.music_name = music_name

        self.font = pygame.font.SysFont("SimHei", 20)
        self.text = self.font.render(self.music_name.split(".")[0], True, (0, 0, 0))
        self.text_rect = self.text.get_rect(centery = 30)
        self.text_rect.x = 20

        self.image_播放 = pygame.transform.scale(pygame.image.load("../img/播放.png"), (30, 30))
        self.rect_播放 = self.image_播放.get_rect(center=(self.text_rect.width + 80, 30))

    def update(self):
        print(music_area.rect_area.x)
        self.image_item.fill(self.new_color_item)
        if self.image_area.is_mouse_over():
            self.rect_item.y += self.image_area.滑动_area_speed
        if self.is_mouse_over() and self.image_area.is_mouse_over():

            self.new_color_item = (220, 220, 220)
            self.image_item.blit(self.image_播放, self.rect_播放)
        else:
            self.new_color_item = self.color_item

        self.image_item.blit(self.text, self.text_rect)
        self.image_area.image_area.blit(self.image_item, self.rect_item)
    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.relative_pos = (
            self.mouse_pos[0] - self.image_area.rect_panel.x,
            self.mouse_pos[1] - self.image_area.rect_panel.y
        )
        return self.rect_item.collidepoint(self.relative_pos)

音乐总和_name = []
music_path = "../music/"
for path in os.listdir(music_path):
    音乐总和_name.append(path)
音乐按钮总和 = []
当前播放音乐 = None
当前播放音乐名称 = None
# 添加音乐按钮对象到音乐按钮总和列表中
for i in range(len(音乐总和_name)):
    if i % 2 == 0:
        color_music = (240, 240, 240)
    else:
        color_music = (255, 255, 255)
    音乐按钮总和.append(Music_Button(音乐总和_name[i], 65 * i + 35, color_music))

button_1 = Button("../img/zjl.png", width * 0.225, height * 0.75, width * 0.2, height//6)
button_2 = Button("../img/xy.png", width * 0.5, height * 0.65, width * 0.2, height//6)
button_3 = Button("../img/wyx.png", width * 0.775, height * 0.75, width * 0.2, height//6)
button_4 = Button("../img/letter.png", width*0.08, 400, 150, 100)

buttob_last = Button("../img/button_last.png", 80, 80, 100, 100)

letter = Letter(width/2, 25)
def 加载画面screen():
    screen.fill((128, 128, 128))
    加载画面s.update()
def 生日解锁screen():
    global screen_fill
    screen.blit(screen_fill, (0, 0))
    screen.fill((255, 255, 255))
    clock1.update()
    clock2.update()
    clock3.update()
    unlock1.update()
def 大厅选择screen():
    # screen.blit(screen_fill, (0, 0))
    # screen_fill.set_alpha(color_alpha)
    """unlock2.update()
    screen.blit(unlock2.image, unlock2.rect)"""
    screen.fill((255, 225, 158))
    button_1.update()
    button_2.update()
    button_3.update()
    button_4.update()
    if letter.book_update_yn == True or letter.book_speed != 0:
        letter.update()
def 听音乐screen():
    global 音乐按钮总和, 当前播放音乐名称, music_area
    screen.fill((230, 230, 230))
    music_area.update()
    for i in 音乐按钮总和:
        i.update()
    # 播放区
    pygame.draw.rect(screen, (255, 255, 255), (width*0.25, height - 150, width*0.74, 130), border_radius=30)
    if type(当前播放音乐名称) == str:
        music_name = font.render("正在播放："+当前播放音乐名称.split(".")[0], True, (0, 0, 0))
        screen.blit(music_name, (width*0.25 + 50, height - 100))
def 祝福语screen():
    screen.fill((255, 225, 0))
def 玩游戏screen():
    screen.fill((0, 225, 158))

def 播放音乐():
    global 当前播放音乐, 当前播放音乐名称
    for i in range(len(音乐按钮总和)):
        if 音乐按钮总和[i].is_mouse_over():
            if 当前播放音乐 != None:
                当前播放音乐.stop()
            当前播放音乐 = pygame.mixer.Sound("../music/" + 音乐按钮总和[i].music_name)
            当前播放音乐名称 = 音乐按钮总和[i].music_name
            当前播放音乐.play()

def 关卡1重置():
    加载画面s.重置()
def 关卡2重置():
    clock1.重置()
    clock2.重置()
    clock3.重置()
def 关卡3重置():
    letter.重置()
def 音乐暂停():
    global 当前播放音乐
    if 当前播放音乐 != None:
        当前播放音乐.stop()
    当前播放音乐 = None

def 当前关卡():
    global 当前关卡s
    if 当前关卡s[0] == True:
        return 1
    elif 当前关卡s[1] == True:
        return 2
    elif 当前关卡s[2] == True:
        return 3
    elif 当前关卡s[3] == True:
        return 4
    elif 当前关卡s[4] == True:
        return 5
    elif 当前关卡s[5] == True:
        return 6
    else:
        return 0
def 切换关卡(目标关卡):
    global 当前关卡s
    for i in range(0, len(当前关卡s)):# 0~5
        if i == 目标关卡-1:
            当前关卡s[i] = True
        else:
            当前关卡s[i] = False
def 返回关卡():
    a = 当前关卡()
    if a > 1:
        if a == 2:
            关卡1重置()
        if a == 3:
            关卡2重置()
        if a == 4 or a == 5 or a == 6:
            关卡3重置()
            当前关卡s[2] = True
            当前关卡s[3] = False
            当前关卡s[4] = False
            当前关卡s[5] = False
        else:
            当前关卡s[a-1] = False
            当前关卡s[a-2] = True
    else:
        pygame.quit()
        sys.exit()
当前关卡s = [False, False, False, True, False, True]
while True:
    #一开始默认不滑动
    music_area.不滑动()
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 当前关卡() == 2 and event.button == 1:
                if clock1.is_mouse_over():
                    clock1.place = clock1.mouse_pos[1]
                    clock1.可滑动 = True
                elif clock2.is_mouse_over():
                    clock2.place = clock2.mouse_pos[1]
                    clock2.可滑动 = True
                elif clock3.is_mouse_over():
                    clock3.place = clock3.mouse_pos[1]
                    clock3.可滑动 = True
            if 当前关卡() == 4:
                if event.button == 4:
                    music_area.上滑动()
                elif event.button == 5:
                    music_area.下滑动()
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttob_last.is_mouse_over():
                按钮.play()
                返回关卡()
            if 当前关卡() == 1:
                if not buttob_last.is_mouse_over() and 加载画面s.text_目标 == 加载画面s.text_end:

                    按钮.play()
                    关卡2重置()
                    切换关卡(2)

            elif 当前关卡() == 2:
                clock1.校准精度()
                clock1.可滑动 = False
                # 滑动结束时，更新last_inplace为当前位置
                clock1.last_inplace = clock1.inplace
                clock2.校准精度()
                clock2.可滑动 = False
                clock2.last_inplace = clock2.inplace
                clock3.校准精度()
                clock3.可滑动 = False
                clock3.last_inplace = clock3.inplace
                if  (clock1.return_value() == 2006 and clock2.return_value() == 6 and 
                        clock3.return_value() == 8 and unlock1.is_mouse_over()):
                    unlock1.unlock = True

                    按钮.play()
                    关卡3重置()
                    切换关卡(3)

            elif 当前关卡() == 3:
                if button_1.is_mouse_over():
                    button_1.yn_button = True

                    按钮.play()
                    音乐暂停()
                    切换关卡(4)

                elif button_2.is_mouse_over():
                    button_2.yn_button = True

                    按钮.play()
                    切换关卡(5)

                elif button_3.is_mouse_over():
                    button_3.yn_button = True

                    按钮.play()
                    切换关卡(6)

                elif button_4.is_mouse_over():

                    按钮.play()

                    letter.book_update_yn = not letter.book_update_yn
                    letter.book_speed *= -1
                    if letter.book_speed > 0:
                        letter.reset_color_alpha()
            elif 当前关卡() == 4:
                if event.button == 1:
                    播放音乐()

    if 当前关卡() == 1:
        加载画面screen()
    elif 当前关卡() == 2:
        生日解锁screen()
    elif 当前关卡() == 3:
        大厅选择screen()
    elif 当前关卡() == 4:
        听音乐screen()
    elif 当前关卡() == 5:
        祝福语screen()
    elif 当前关卡() == 6:
        玩游戏screen()
    buttob_last.update()
    pygame.display.flip()
    pygame.time.Clock().tick(120)