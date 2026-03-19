import pygame
import random

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 创建精灵类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()  # 删除子弹

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 15)
        self.rect = self.image.get_rect(center=(random.randint(0, screen_width), 0))
        self.speed = random.randint(1, 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.kill()  # 删除敌人

# 创建精灵组
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(event.pos[0], screen_height - 10)
            bullets.add(bullet)

    # 更新精灵组
    bullets.update()
    enemies.update()

    # 创建敌人精灵
    if len(enemies) < 5:
        enemy = Enemy()
        enemies.add(enemy)

    # 检测碰撞并删除子弹和敌人
    pygame.sprite.groupcollide(enemies, bullets, True, True, collided = pygame.sprite.collide_mask)

    # 绘制精灵
    screen.fill((0, 0, 0))
    bullets.draw(screen)
    enemies.draw(screen)

    # 更新屏幕
    pygame.display.flip()
    pygame.time.Clock().tick(200)

# 退出游戏
pygame.quit()