import pygame, os, sys, random

pygame.init()
pygame.font.init()
icon = pygame.image.load("../img/icon.jpg")
screen_fill = pygame.transform.scale(icon, (800, 600))
pygame.display.set_icon(icon)
pygame.display.set_caption("黄宇涛生日快乐")
weight, height = (800, 600)
screen = pygame.display.set_mode((weight, height))
color_alpha = 255


class Clock:
    def __init__(self, types, center_x):
        self.center_x = center_x
        self.image = pygame.Surface((100, 100), pygame.SRCALPHA)
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

        self.inplace = 0
        self.place = 0
        self.last_inplace = 0  # 记录上一次滑动结束时的位置
        self.可滑动 = False
        self.inimage = pygame.Surface((self.rect.height, self.rect.height * len(self.tuple)), pygame.SRCALPHA)
        self.inrect = self.inimage.get_rect()
        self.inrect.topleft = (0, self.inplace)

        self.font_max = 40
        self.font_min = 10
        self.font_color = (255, 128, 200)

    def update(self):
        self.滑动()
        self.is_mouse_over()
        self.rect.center = (self.center_x, height / 2)
        self.image.fill((0, 0, 0, 0))
        self.image.set_alpha(color_alpha)
        self.inimage.fill((0, 0, 0, 0))
        self.font_change()
        pygame.draw.rect(self.image, (100, 128, 200), (0, 0, 100, 100), border_radius=round(self.rect.height / 5))
        self.image.blit(self.inimage, self.inrect)
        screen.blit(self.image, self.rect)

    def font_change(self):
        if self.可滑动 or self.is_mouse_over():
            self.font_color = (255, 0, 0)
        else:
            self.font_color = (255, 128, 200)
        for i in range(len(self.tuple)):
            # 计算数字的中心位置（相对于显示窗口）
            self.number_center_y = (i * self.image.get_height()) + self.inplace + self.image.get_height() // 2
            # 计算数字到窗口中心的距离
            self.distance_to_center = abs(self.number_center_y - self.image.get_height() // 2)
            self.font_size = max(self.font_min,
                                 min(round(self.font_max - (self.distance_to_center // 2)), self.font_max))
            self.font = pygame.font.SysFont("kaiti", self.font_size, bold=True)
            self.inimage.blit(self.font.render(str(self.tuple[i]), True, (255, 128, 200)), (
            (self.rect.width - self.font.size(str(self.tuple[i]))[0]) / 2,
            self.rect.height * i + self.rect.height * 0.35))
            pygame.draw.rect(self.inimage, self.font_color, (
            (self.rect.height * 0.2, self.rect.height * i - self.rect.height * 0.05),
            (self.rect.height * 0.6, self.rect.height / 10)), 0, border_radius=round(self.rect.height / 10))
        pygame.draw.rect(self.inimage, self.font_color, (
        (self.rect.height * 0.2, self.inrect.height - self.rect.height * 0.05),
        (self.rect.height * 0.6, self.rect.height / 10)), 0, border_radius=round(self.rect.height / 10))

    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)

    def 滑动(self):
        if self.可滑动:
            self.new_position = self.last_inplace + self.mouse_pos[1] - self.place
            self.inplace = max(-self.rect.height * (len(self.tuple) - 1), min(self.new_position, 0))
            self.inrect.topleft = (0, self.inplace)

    def 调准精度(self):
        self.inplace = round(self.inplace / self.rect.height) * self.rect.height
        self.inrect.topleft = (0, self.inplace)

    def return_value(self):
        return self.tuple[abs(self.inplace) // self.rect.height]


class Unlock:
    def __init__(self):
        self.image = pygame.Surface((150, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(weight / 2, height / 1.3))
        self.font = pygame.font.SysFont("fangsong", 30, True)
        self.color = (255, 128, 200)
        pygame.draw.rect(self.image, self.color, (0, 0, 150, 80), border_radius=10)
        self.text = self.font.render("解锁", True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.rect.width / 2, self.rect.height / 2 * 1.2))
        self.unlock = False
        self.clock_image = "../img/clock.png"

    def update(self):
        if self.unlock:
            self.clock_image = "../img/unlock.png"
        if self.is_mouse_over():
            self.color = (255, 0, 0)
        else:
            self.color = (255, 128, 200)
        pygame.draw.rect(self.image, self.color, (0, 0, 150, 80), border_radius=10)
        self.image.blit(pygame.image.load(self.clock_image), ((self.rect.width - 65) / 2, 0))
        self.image.set_alpha(color_alpha)
        # self.image.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)

    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)


clock1 = Clock("year", 250)
clock2 = Clock("moon", 400)
clock3 = Clock("day", 550)
unlock1 = Unlock()
unlock2 = Unlock()


class Letter:
    def __init__(self, x, y):
        self.image = pygame.Surface((500, 550), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.letter_img = pygame.image.load("../img/bg.jpg")
        self.letter_img.set_alpha(255)
        # self.image.blit(self.letter_img, (0, 0))
        self.font = pygame.font.SysFont("华文行楷", 23)
        self.font_color = (0, 0, 0) # (80, 150, 220)
        # 读取文字
        with open("../Letter/letter.txt", "r", encoding="utf-8") as f:
            self.letters = f.read()
            self.letters = self.letters.replace(" ", "").replace("\n", "")
        # 初始化文字位置
        self.text_x = 10
        self.text_y = 25
        self.text_h = 35
        self.text_页边距 = 10
        self.char_data = []  # 存储(字符, x, y)元组

        for i in range(len(self.letters)):
            char = self.letters[i]
            char_width = self.font.size(char)[0]

            # 判断是否超过页边距
            if self.text_x > self.rect.width - self.text_页边距:
                self.text_x = self.text_页边距
                self.text_y += self.text_h

            # 存储字符位置
            self.char_data.append((char, self.text_x, self.text_y))

            # 设置下一个文字x的位置
            self.text_x += char_width

            # 段落换行
            if i > 0:
                if ((self.letters[i - 1] == "涛" and char == "：")
                        or (self.letters[i - 1] == "仗" and char == "。")):
                    self.text_x = self.font.size("一")[0] * 2 + self.text_页边距
                    self.text_y += self.text_h
                # 署名
                elif (self.letters[i - 1] == "吧") and (char == "！"):
                    self.text_x = self.rect.width * 0.55
                    self.text_y = self.rect.height * 0.85
                # 名字前空格
                elif (self.letters[i - 1] == "名") and (char == "："):
                    self.text_x += self.font.size("  ")[0]
                # 日期
                elif (self.letters[i - 1] == "佳") and (char == "成"):
                    self.text_x = self.rect.width * 0.55
                    self.text_y = self.rect.height * 0.9

        # 动画参数
        self.num_chars = len(self.char_data)
        self.char_alphas = [0] * self.num_chars  # 每个字符的透明度
        self.current_char_index = 0  # 当前正在显示的字符索引
        self.char_fade_speed = 10  # 每个字符的淡入速度
        self.is_completed = False  # 是否所有文字都已显示完成

        # 初始绘制（所有文字透明）
        self.draw_text()

    def update(self):
        screen.blit(self.image, self.rect)
        self.text_color_change()

    def draw_text(self):
        # 先清空文字区域（保留背景图）
        #self.image.blit(self.letter_img, (0, 0))
        for i in range(len(self.char_data)):
            char, x, y = self.char_data[i]
            text = self.font.render(char, True, self.font_color)
            text.set_alpha(self.char_alphas[i])
            text_rect = text.get_rect(left=x, top=y)
            self.image.blit(text, text_rect)

    def text_color_change(self):
        if self.is_completed:
            return

        # 当前字符淡入
        if self.current_char_index < self.num_chars:
            self.char_alphas[self.current_char_index] = min(
                255, self.char_alphas[self.current_char_index] + self.char_fade_speed
            )
            # 当当前字符完全显示，移到下一个
            if self.char_alphas[self.current_char_index] >= 255:
                self.current_char_index += 1
            # 重绘文字
            self.draw_text()
        else:
            self.is_completed = True


letter = Letter(weight / 2, height / 2)


def screen_1():
    screen.blit(screen_fill, (0, 0))
    screen_fill.set_alpha(color_alpha)
    clock1.update()
    clock2.update()
    clock3.update()
    unlock1.update()


def screen_2():
    unlock2.update()
    screen.blit(unlock2.image, unlock2.rect)
    letter.update()


a = False
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clock1.is_mouse_over():
                clock1.place = clock1.mouse_pos[1]
                clock1.可滑动 = True
            if clock2.is_mouse_over():
                clock2.place = clock2.mouse_pos[1]
                clock2.可滑动 = True
            if clock3.is_mouse_over():
                clock3.place = clock3.mouse_pos[1]
                clock3.可滑动 = True
        if event.type == pygame.MOUSEBUTTONUP:
            clock1.调准精度()
            clock1.可滑动 = False
            # 滑动结束时，更新last_inplace为当前位置
            clock1.last_inplace = clock1.inplace
            clock2.调准精度()
            clock2.可滑动 = False
            clock2.last_inplace = clock2.inplace
            clock3.调准精度()
            clock3.可滑动 = False
            clock3.last_inplace = clock3.inplace

            if clock1.return_value() == 2006 and clock2.return_value() == 6 and clock3.return_value() == 8 and unlock1.is_mouse_over():
                unlock1.unlock = True
    if color_alpha != 0 and a == True:
        screen_1()
    else:
        a = False
        color_alpha = 255
        screen_2()
    if unlock1.unlock:
        color_alpha = max(0, min(color_alpha - 3, 255))
    pygame.display.flip()
    pygame.time.Clock().tick(500)