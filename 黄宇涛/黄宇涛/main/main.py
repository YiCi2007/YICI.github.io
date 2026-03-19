import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口参数
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("黄宇涛生日快乐")

# 加载背景图片
try:
    icon = pygame.image.load("../img/icon.jpg")
    background = pygame.transform.scale(icon, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"无法加载图片: {e}")
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill((255, 20, 147))

# 初始化字体
pygame.font.init()
font_path = pygame.font.match_font('simhei') or pygame.font.match_font('kaiti') or pygame.font.get_default_font()


class Clock:
    def __init__(self, types, center_x):
        self.center_x = center_x
        self.image_width = 70
        self.image_height = 70
        self.item_height = 50

        # 创建显示表面和矩形
        self.image = pygame.Surface((self.image_width, self.image_height))
        self.rect = self.image.get_rect()

        # 生成数字列表
        self.numbers = []
        if types == "year":
            self.numbers = list(range(1999, 2050))
        elif types == "moon":
            self.numbers = list(range(1, 13))
        elif types == "day":
            self.numbers = list(range(1, 32))

        # 滑动相关属性
        self.inplace = 0
        self.place = 0
        self.last_inplace = 0  # 记录上一次滑动结束时的位置
        self.可滑动 = False

        # 字体参数
        self.min_font_size = 12
        self.max_font_size = 28

        # 创建内部图像（用于滚动）
        """self.inimage = pygame.Surface((self.image_width, self.item_height * len(self.numbers)))
        self.inrect = self.inimage.get_rect()"""
        #self.inrect.topleft = (0, self.inplace)

    def update(self):
        # 清空显示表面
        self.image.fill((200, 0, 200))
        # 更新滑动位置
        self.滑动()

        # 检查鼠标是否悬停
        self.is_mouse_over()

        # 设置组件位置
        self.rect.center = (self.center_x, HEIGHT / 2)

        # 动态渲染当前可见区域的数字
        self.render_visible_numbers()

        # 绘制到屏幕
        screen.blit(self.image, self.rect)

    def is_mouse_over(self):
        self.mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(self.mouse_pos)

    def 滑动(self):
        if self.可滑动:
            self.new_position = self.last_inplace + self.mouse_pos[1] - self.place
            max_scroll = -self.item_height * (len(self.numbers) - 1)
            self.inplace = max(max_scroll, min(self.new_position, 0))

    def 调准精度(self):
        self.inplace = round(self.inplace / self.item_height) * self.item_height

    def render_visible_numbers(self):
        # 计算当前可见区域的数字范围
        visible_start = abs(self.inplace) // self.item_height
        visible_end = visible_start + 3  # 显示中心位置前后几个数字
        visible_end = min(visible_end, len(self.numbers))
        # 计算每个可见数字的位置并渲染
        for i in range(max(0, visible_start - 1), visible_end):
            # 计算数字的中心位置（相对于显示窗口）
            number_center_y = (i * self.item_height) + self.inplace + self.item_height // 2
            # 计算数字到窗口中心的距离
            distance_to_center = abs(number_center_y - self.image_height // 2)
            # 根据距离计算字体大小（距离越近，字体越大）
            # 最大字体大小在中心位置，距离超过50像素时使用最小字体
            font_size = max(self.min_font_size, self.max_font_size - (distance_to_center // 2))
            # 创建字体对象
            font = pygame.font.Font(font_path, font_size)
            # 渲染数字
            number_text = str(self.numbers[i])
            text_surface = font.render(number_text, True, (255, 255, 255))
            # 计算文字位置（居中显示）
            text_rect = text_surface.get_rect(center=(self.image_width // 2, number_center_y))
            # 绘制数字
            self.image.blit(text_surface, text_rect)

# 创建日期选择器实例
year_selector = Clock("year", 300)
month_selector = Clock("moon", 400)
day_selector = Clock("day", 500)

# 创建帧率控制器
fps_clock = pygame.time.Clock()
FPS = 120
# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检查哪个选择器被点击
                if year_selector.is_mouse_over():
                    year_selector.place = year_selector.mouse_pos[1]
                    year_selector.可滑动 = True
                elif month_selector.is_mouse_over():
                    month_selector.place = month_selector.mouse_pos[1]
                    month_selector.可滑动 = True
                elif day_selector.is_mouse_over():
                    day_selector.place = day_selector.mouse_pos[1]
                    day_selector.可滑动 = True

        # 鼠标释放事件
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # 所有选择器停止滑动并调准精度
                for selector in [year_selector, month_selector, day_selector]:
                    if selector.可滑动:
                        selector.调准精度()
                        selector.可滑动 = False
                        selector.last_inplace = selector.inplace

    # 绘制背景
    screen.blit(background, (0, 0))

    # 更新和绘制所有选择器
    year_selector.update()
    month_selector.update()
    day_selector.update()

    # 刷新显示
    pygame.display.flip()

    # 控制帧率
    fps_clock.tick(FPS)

# 退出程序
pygame.quit()
sys.exit()