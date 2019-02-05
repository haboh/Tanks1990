import pygame
import os

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


size = width, height = 960, 960
screen = pygame.display.set_mode(size)
BULLET_SPEED = 8
running = True
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_blocks = pygame.sprite.Group()
water_blocks = pygame.sprite.Group()
brick_blocks = pygame.sprite.Group()
metal_blocks = pygame.sprite.Group()
bush_blocks = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

block_size = 64

m = [
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 1, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
]


def gameover():
    exit(0)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(all_sprites, group, all_blocks)
        self.image = pygame.Surface((block_size, block_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * block_size
        self.rect.y = y * block_size


class Water(Block):
    water_image = load_image("water.png")

    def __init__(self, x, y):
        super().__init__(x, y, water_blocks)
        self.image = Water.water_image


class Brick(Block):
    brick_image = load_image("brick.png")

    def __init__(self, x, y):
        super().__init__(x, y, brick_blocks)
        self.image = Brick.brick_image


class Metal(Block):
    metal_image = load_image("metal.png")

    def __init__(self, x, y):
        super().__init__(x, y, metal_blocks)
        self.image = Metal.metal_image


class Bush(Block):
    bush_image = load_image("bush.png")

    def __init__(self, x, y):
        super().__init__(x, y, bush_blocks)
        self.image = Bush.bush_image


class Tank(Block):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.rotation = 0

    def rotate_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rotation = (self.rotation - 1) % 4

    def rotate_right(self):
        self.image = pygame.transform.rotate(self.image, -90)
        self.rotation = (self.rotation + 1) % 4

    def move_forward(self):
        x, y = self.rect.x, self.rect.y
        if self.rotation == 0:
            self.rect.y -= block_size
        if self.rotation == 1:
            self.rect.x += block_size
        if self.rotation == 2:
            self.rect.y += block_size
        if self.rotation == 3:
            self.rect.x -= block_size
        if pygame.sprite.spritecollideany(self, metal_blocks) or pygame.sprite.spritecollideany(self, brick_blocks) \
                or pygame.sprite.spritecollideany(self, water_blocks):
            self.rect.x = x
            self.rect.y = y

    def move_backward(self):
        x, y = self.rect.x, self.rect.y
        if self.rotation == 0:
            self.rect.y += block_size
        if self.rotation == 1:
            self.rect.x -= block_size
        if self.rotation == 2:
            self.rect.y -= block_size
        if self.rotation == 3:
            self.rect.x += block_size
        if pygame.sprite.spritecollideany(self, metal_blocks) or pygame.sprite.spritecollideany(self, brick_blocks) \
                or pygame.sprite.spritecollideany(self, water_blocks):
            self.rect.x = x
            self.rect.y = y

    def shoot(self):
        if self.rotation == 0:
            Bullet(self.rect.x + block_size // 2 - 4, self.rect.y - 9, 0, -BULLET_SPEED)
        if self.rotation == 2:
            Bullet(self.rect.x + block_size // 2 - 4, self.rect.y + block_size, 0, BULLET_SPEED)
        if self.rotation == 3:
            Bullet(self.rect.x - 8, self.rect.y + block_size // 2 - 4, -BULLET_SPEED, 0)
        if self.rotation == 1:
            Bullet(self.rect.x + block_size, self.rect.y + block_size // 2 - 4, BULLET_SPEED, 0)


class Player(Tank):
    player_image = load_image("player.png")

    def __init__(self, x, y):
        super().__init__(x, y, players)
        self.image = Player.player_image


class Enemy(Tank):
    enemy_image = load_image("enemy.png")

    def __init__(self, x, y):
        super().__init__(x, y, players)
        self.image = Enemy.enemy_image


class Bullet(Block):
    def __init__(self, x, y, dx, dy):
        super().__init__(x, y, bullets)
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx, self.dy = dx, dy

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if pygame.sprite.spritecollideany(self, all_blocks):
            if pygame.sprite.spritecollide(self, metal_blocks, False) or \
                    pygame.sprite.spritecollide(self, brick_blocks, True) or \
                    pygame.sprite.spritecollide(self, enemies, True):
                all_sprites.remove(self)
                bullets.remove(self)
            if pygame.sprite.spritecollideany(self, players):
                gameover()


class Throne(pygame.sprite.Sprite):
    pass


for i in range(width // block_size):
    for j in range(height // block_size):
        if m[i][j] == 1:
            Brick(j, i)
        if m[i][j] == 2:
            Bush(j, i)
        if m[i][j] == 3:
            Water(j, i)
        if m[i][j] == 4:
            Metal(j, i)
        if m[i][j] == 5:
            player = Player(j, i)
        if m[i][j] == 6:
            Enemy(j, i)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.move_backward()
            if event.key == pygame.K_UP:
                player.move_forward()
            if event.key == pygame.K_LEFT:
                player.rotate_left()
            if event.key == pygame.K_RIGHT:
                player.rotate_right()
            if event.key == pygame.K_SPACE:
                player.shoot()
    screen.fill((0, 0, 0))
    players.draw(screen)
    enemies.draw(screen)
    water_blocks.draw(screen)
    brick_blocks.draw(screen)
    metal_blocks.draw(screen)
    bullets.draw(screen)
    bush_blocks.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
