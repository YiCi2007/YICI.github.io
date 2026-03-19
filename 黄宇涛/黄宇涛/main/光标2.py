import pygame
import sys

# 初始化pygame
pygame.init()

# 获取屏幕大小
w, h = pygame.display.Info().current_w, pygame.display.Info().current_h

# 创建窗口（使用NOFRAME标志去除窗口边框）
screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
pygame.display.set_caption("鼠标跟随")

# 加载并调整光标图片
cursor_path = "../存放素材/人物11.png"  # 替换为你的光标图片路径
try:
    cursor_surface = pygame.image.load(cursor_path).convert_alpha()
    # 调整光标大小为32x32
    cursor_surface = pygame.transform.scale(cursor_surface, (32, 32))
    # 设置热点位置（图片中心）
    hotspot = (16, 16)
    # 创建光标对象
    custom_cursor = pygame.cursors.Cursor(hotspot, cursor_surface)
    # 应用自定义光标
    pygame.mouse.set_cursor(custom_cursor)
except pygame.error as e:
    print(f"无法加载光标图片: {e}")

# 加载并调整子弹图片
image_path = "../存放素材/子弹.png"
try:
    image = pygame.image.load(image_path)
    # 调整图片大小
    image = pygame.transform.scale(image, (200, 300))
except pygame.error as e:
    print(f"无法加载图片: {e}")
    sys.exit()

# 主循环
clock = pygame.time.Clock()
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # 按ESC键退出 Pipeline
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # 清空屏幕
    screen.fill((0, 0, 0))

    # 获取鼠标位置
    x, y = pygame.mouse.get_pos()

    # 计算图片位置（鼠标位置偏移）
    image_x = x + 1
    image_y = y + 1

    # 绘制图片
    screen.blit(image, (image_x, image_y))

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)