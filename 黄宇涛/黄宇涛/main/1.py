import pygame
import sys

# 初始化Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("平滑翻转动画")
clock = pygame.time.Clock()


# 加载/创建演示图像（你可以替换为自己的图片）
def create_demo_image(width, height):
    """创建带图案的演示图像"""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # 填充底色
    surf.fill((255, 200, 200))
    # 画一个圆和文字区分正反
    pygame.draw.circle(surf, (255, 0, 0), (width // 2, height // 2), 50)
    font = pygame.font.SysFont(None, 40)
    text = font.render("正面", True, (0, 0, 0))
    surf.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 80))
    return surf


# 图像参数
IMAGE_WIDTH, IMAGE_HEIGHT = 200, 300
original_image = create_demo_image(IMAGE_WIDTH, IMAGE_HEIGHT)
# 创建翻转后的图像（反面）
flipped_image = pygame.transform.flip(original_image, True, False)
flipped_image.fill((200, 255, 200), special_flags=pygame.BLEND_RGBA_MULT)
font = pygame.font.SysFont("华文琥珀", 40)
text = font.render("反面", True, (0, 0, 0))
flipped_image.blit(text, (IMAGE_WIDTH // 2 - text.get_width() // 2, IMAGE_HEIGHT // 2 - 80))

# 动画参数
flip_progress = 0.0  # 翻转进度 0.0~1.0
flip_speed = 0.02  # 每帧进度增量
is_flipping = False  # 是否正在翻转
flip_axis = "horizontal"  # 翻转轴：horizontal/vertical


def draw_flipping_animation(screen, original, flipped, x, y, progress, axis):
    """
    绘制平滑翻转动画
    :param screen: 显示表面
    :param original: 原始图像
    :param flipped: 翻转后的图像
    :param x/y: 图像位置
    :param progress: 翻转进度 0.0~1.0
    :param axis: 翻转轴 horizontal/vertical
    """
    if progress <= 0.0:
        # 未翻转，显示原图
        screen.blit(original, (x, y))
        return
    if progress >= 1.0:
        # 完全翻转，显示翻转后的图
        screen.blit(flipped, (x, y))
        return

    # 计算当前显示的图像和缩放比例
    current_scale = 1.0 - abs(progress - 0.5) * 2  # 0.5时缩放到0
    if axis == "horizontal":
        # 水平翻转：宽度缩放，高度不变
        scaled_width = int(original.get_width() * current_scale)
        scaled_height = original.get_height()
        # 计算居中偏移（避免缩放时图像偏移）
        offset_x = (original.get_width() - scaled_width) // 2
        offset_y = 0
    else:
        # 垂直翻转：高度缩放，宽度不变
        scaled_width = original.get_width()
        scaled_height = int(original.get_height() * current_scale)
        offset_x = 0
        offset_y = (original.get_height() - scaled_height) // 2

    # 选择当前显示的图像（0~0.5显示原图，0.5~1显示翻转后的图）
    if progress < 0.5:
        current_image = original
    else:
        current_image = flipped

    # 缩放图像（模拟翻转时的“变薄”效果）
    scaled_surf = pygame.transform.scale(current_image, (scaled_width, scaled_height))

    # 设置透明度（增强3D效果）
    alpha = int(255 * (1 - abs(progress - 0.5) * 2))
    scaled_surf.set_alpha(max(50, alpha))

    # 绘制到屏幕（居中显示）
    draw_x = x + offset_x
    draw_y = y + offset_y
    screen.blit(scaled_surf, (draw_x, draw_y))


# 图像初始位置
image_x = (WIDTH - IMAGE_WIDTH) // 2
image_y = (HEIGHT - IMAGE_HEIGHT) // 2

# 主循环
running = True
while running:
    screen.fill((30, 30, 30))  # 背景色

    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 鼠标点击触发翻转动画
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not is_flipping:
                is_flipping = True

    # 更新翻转进度
    if is_flipping:
        flip_progress += flip_speed
        # 进度超出范围时停止动画
        if flip_progress >= 1.0:
            flip_progress = 1.0
            is_flipping = False
        elif flip_progress <= 0.0:
            flip_progress = 0.0
            is_flipping = False

    # 绘制翻转动画
    draw_flipping_animation(
        screen, original_image, flipped_image,
        image_x, image_y, flip_progress, flip_axis
    )

    # 显示提示文字
    hint_font = pygame.font.SysFont(None, 30)
    hint_text = hint_font.render("点击屏幕触发水平翻转动画", True, (255, 255, 255))
    screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, 50))

    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()