import pygame
import os
import random

pygame.init()

SOUNDSHOOT = pygame.mixer.Sound("data\\shoot.wav")
SOUNDDESTROY = pygame.mixer.Sound('data\\destroy.wav')
AMOUNT_OF_ENEMIES = 10
GAMEOVER = pygame.mixer.Sound('data\\gameover.wav')
pygame.mixer.music.set_volume(0.2)


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
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
bushes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
metal = pygame.sprite.Group()
players = pygame.sprite.Group()
thrones = pygame.sprite.Group()
waters = pygame.sprite.Group()
bullets = pygame.sprite.Group()
destructions = pygame.sprite.Group()

block_size = 32
n, m = width // block_size, height // block_size
THRONE_IS_ALIVE = True
types = {
    1: "brick.png",
    2: "bush.png",
    3: "metal.png",
    4: "enemy.png",
    5: "player.png",
    6: "player2.png",
    7: "eagle.png",
    8: "water.png",
}

groups = {
    1: bricks,
    2: bushes,
    3: metal,
    4: enemies,
    5: players,
    6: players,
    7: thrones,
    8: waters,
}


def start_page():
    pygame.mixer.music.load('data\\Start.mp3')
    running = True
    tanks1990 = load_image('start.png')
    pos = 0
    lines = ['1 Level',
             '2 Level',
             '3 Level',
             'About',
             'Quit']
    font = pygame.font.SysFont("verdana", 50)
    pointer = pygame.transform.rotate(load_image('player.png'), -90)
    pygame.mixer.music.play(loops=-1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pos = (pos - 1) % len(lines)
                if event.key == pygame.K_DOWN:
                    pos = (pos + 1) % len(lines)
                if event.key == pygame.K_SPACE:
                    process_position(lines[pos])
                    return
        screen.fill((0, 0, 0))
        screen.blit(pointer, (350, 465 + pos * 70))
        for i, line in enumerate(lines):
            string_rendered = font.render(line, 1, pygame.Color('gray'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x += 400
            intro_rect.y += 450 + i * 70
            screen.blit(string_rendered, intro_rect)
        screen.blit(tanks1990,
                    (width // 2 - tanks1990.get_rect()[2] // 2, height // 2 - tanks1990.get_rect()[3] // 2 - 150))
        pygame.display.flip()
        clock.tick(60)


def process_position(pos):
    global AMOUNT_OF_ENEMIES
    if pos == 'Quit':
        return
    if pos == '1 Level':
        AMOUNT_OF_ENEMIES = 5
        start_game_for_single_player()
    if pos == '2 Level':
        AMOUNT_OF_ENEMIES = 10
        start_game_for_single_player()
    if pos == '3 Level':
        AMOUNT_OF_ENEMIES = 20
        start_game_for_single_player()
    if pos == 'About':
        about()


def about():
    font = pygame.font.SysFont("verdana", 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    start_page()
        screen.fill((0, 0, 0))
        arrows = load_image('arrows.jpg')
        space = load_image('space.png')
        string_rendered = font.render('To move', 1, pygame.Color('gray'))
        screen.blit(string_rendered, (350, 60))
        screen.blit(arrows, (100, 20))
        string_rendered = font.render('To shoot', 1, pygame.Color('gray'))
        screen.blit(space, (100, 200))
        screen.blit(string_rendered, (550, 350))
        p = load_image('player.png')
        screen.blit(p, (150, 620))
        screen.blit(string_rendered, (200, 600))
        string_rendered = font.render('q - quit', 1, pygame.Color('gray'))
        screen.blit(string_rendered, (500, 600))
        pygame.display.flip()


def load_field():
    field = [[0] * n for _ in range(m)]
    for i in range(n):
        field[i][0] = field[i][m - 1] = 3
    for i in range(m):
        field[n - 1][i] = field[0][i] = 3
    field[n // 2][m - 2] = 7
    field[n // 2 - 1][m - 2] = field[n // 2 + 1][m - 2] = field[n // 2][m - 3] = field[n // 2 - 1][m - 3] = \
        field[n // 2 + 1][m - 3] = 1
    field[n // 2 - 2][m - 2] = 5
    lost = AMOUNT_OF_ENEMIES
    for j in range(m):
        for i in range(n):
            if field[i][j] == 0:
                field[i][j] = random.choice([0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 8])
            if field[i][j] == 0 and lost > 0:
                field[i][j] = 4
                lost -= 1
    return field


def start_game_for_single_player():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/fon.mp3')
    # pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    running = True
    field = load_field()
    player = None
    for i in range(n):
        for j in range(m):
            if field[i][j] != 0 and field[i][j] != 4 and field[i][j] != 5 and field[i][j] != 6:
                Block(field[i][j], groups[field[i][j]], i, j)
            if field[i][j] == 5:
                player = Tank(field[i][j], groups[field[i][j]], i, j)
            if field[i][j] == 4:
                Enemy(field[i][j], groups[field[i][j]], i, j)
    kup, kdown = 0, 0
    shoot = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    kdown = True
                if event.key == pygame.K_UP:
                    kup = True
                if event.key == pygame.K_LEFT:
                    player.turn_left()
                if event.key == pygame.K_RIGHT:
                    player.turn_right()
                if event.key == pygame.K_SPACE:
                    shoot = True
                    SOUNDSHOOT.play()
                    player.shoot()
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    kdown = False
                if event.key == pygame.K_UP:
                    kup = False
                if event.key == pygame.K_SPACE:
                    shoot = False

        screen.fill((0, 0, 0))
        # if shoot:
        #     player.shoot()
        if kup:
            player.move_forward()
        if kdown:
            player.move_back()
        if len(enemies.sprites()) == 0:
            win()
        # all_sprites.draw(screen)
        bricks.draw(screen)
        waters.draw(screen)
        bullets.draw(screen)
        bullets.update()
        metal.draw(screen)
        players.draw(screen)
        enemies.draw(screen)
        thrones.draw(screen)
        bushes.draw(screen)
        destructions.draw(screen)
        destructions.update()
        enemies.update()
        pygame.display.flip()
        clock.tick(60)


def win():
    image = load_image('youwin.png')
    GAMEOVER.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        screen.blit(image, (160, 160))
        pygame.display.flip()


DELTA = 2


def pause():
    font = pygame.font.SysFont("verdana", 50)
    line = 'PAUSE'
    string_rendered = font.render(line, 1, pygame.Color('gray'))
    string_rendered1 = font.render('QUIT - press q', 1, pygame.Color('gray'))
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
        screen.blit(string_rendered, (width // 2 - 2 * block_size, height // 2 - 2 * block_size))
        screen.blit(string_rendered1, (width // 2 - 4 * block_size, height // 2))
        pygame.display.flip()


class Block(pygame.sprite.Sprite):
    def __init__(self, type, group, x, y):
        super().__init__(group, all_sprites)
        self.image = load_image(types[type])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * block_size, y * block_size


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, type_of_bullet):
        super().__init__(bullets, all_sprites)
        self.type_of_bullet = type_of_bullet
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx, self.dy = dx, dy

    def update(self):
        global THRONE_IS_ALIVE
        self.rect.x += self.dx
        self.rect.y += self.dy
        if pygame.sprite.spritecollideany(self, players) and self.type_of_bullet:
            if THRONE_IS_ALIVE:
                respawn()
            else:
                game_over()
        if pygame.sprite.spritecollideany(self, enemies) and not self.type_of_bullet:
            enemy = pygame.sprite.spritecollide(self, enemies, False)[0]
            Destruction(enemy.rect.x, enemy.rect.y)
            enemies.remove(enemy)
            bullets.remove(self)

        if pygame.sprite.spritecollideany(self, metal):
            bullets.remove(self)

        if pygame.sprite.spritecollideany(self, bricks):
            brick = pygame.sprite.spritecollide(self, bricks, False)[0]
            bricks.remove(brick)
            bullets.remove(self)

        if pygame.sprite.spritecollideany(self, thrones):
            throne = pygame.sprite.spritecollide(self, thrones, False)[0]
            throne.image = load_image("flag.png")
            THRONE_IS_ALIVE = False


BULLET_SPEED = 8


def respawn():
    player = players.sprites()[0]
    player.rect.x, player.rect.y = block_size * (n // 2 - 2), block_size * (m - 2)


def game_over():
    image = load_image('gameover.png')
    GAMEOVER.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((0, 0, 0))
        screen.blit(image, (160, 160))
        pygame.display.flip()


class Tank(Block):
    def __init__(self, type, group, x, y):
        super().__init__(type, group, x, y)
        self.group = group
        self.direction = 0
        # self.image = pygame.transform.scale(self.image, (16, ))
        # self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = x * block_size, y * block_size

    def shoot(self):
        type_of_bullet = 0
        if self in enemies.sprites():
            type_of_bullet = 1
        if self.direction == 0:
            Bullet(self.rect.x + block_size // 2 - 1, self.rect.y - 2, 0, -BULLET_SPEED, type_of_bullet)
        if self.direction == 1:
            Bullet(self.rect.x - 2, self.rect.y + block_size // 2 - 1, -BULLET_SPEED, 0, type_of_bullet)
        if self.direction == 2:
            Bullet(self.rect.x + block_size // 2 - 1, self.rect.y + block_size + 1, 0, BULLET_SPEED, type_of_bullet)
        if self.direction == 3:
            Bullet(self.rect.x + block_size + 1, self.rect.y + block_size // 2 - 1, BULLET_SPEED, 0, type_of_bullet)

    def move_forward(self):
        x, y = self.rect.x, self.rect.y
        if self.direction == 0:
            self.rect.y -= DELTA
        if self.direction == 1:
            self.rect.x -= DELTA
        if self.direction == 2:
            self.rect.y += DELTA
        if self.direction == 3:
            self.rect.x += DELTA
        if pygame.sprite.spritecollideany(self, waters) or pygame.sprite.spritecollideany(self, bricks) \
                or pygame.sprite.spritecollideany(self, metal) or pygame.sprite.spritecollideany(
            self, thrones) or (
                self in enemies.sprites() and len(list(pygame.sprite.spritecollide(self, enemies, False))) > 1) \
                or (self in enemies.sprites() and pygame.sprite.spritecollideany(self, players)) or (
                self not in enemies.sprites() and pygame.sprite.spritecollideany(self, enemies)):
            self.rect.x, self.rect.y = x, y
            return False
        return True

    def move_back(self):
        x, y = self.rect.x, self.rect.y
        if self.direction == 0:
            self.rect.y += DELTA
        if self.direction == 1:
            self.rect.x += DELTA
        if self.direction == 2:
            self.rect.y -= DELTA
        if self.direction == 3:
            self.rect.x -= DELTA
        if pygame.sprite.spritecollideany(self, waters) or pygame.sprite.spritecollideany(self, bricks) \
                or pygame.sprite.spritecollideany(self, metal) or pygame.sprite.spritecollideany(
            self, thrones) or (
                self in enemies.sprites() and len(list(pygame.sprite.spritecollide(self, enemies, False))) > 1) \
                or (self in enemies.sprites() and pygame.sprite.spritecollideany(self, players)) or (
                self not in enemies.sprites() and pygame.sprite.spritecollideany(self, enemies)):
            self.rect.x, self.rect.y = x, y
            return False
        return True

    def turn_left(self):
        self.direction = (self.direction + 1) % 4
        self.image = pygame.transform.rotate(self.image, 90)

    def turn_right(self):
        self.direction = (self.direction - 1) % 4
        self.image = pygame.transform.rotate(self.image, -90)


class Enemy(Tank):
    def update(self):
        player = players.sprites()[0]
        if abs(player.rect.x - self.rect.x) < block_size // 2:
            if player.rect.y < self.rect.y and not random.randrange(10):
                if self.direction != 0:
                    self.turn_right()
                else:
                    self.shoot()
            else:
                if self.direction != 2:
                    self.turn_right()
                else:
                    self.shoot()
        if abs(player.rect.y - self.rect.y) < block_size // 2 and not random.randrange(10):
            if player.rect.x < self.rect.x:
                if self.direction != 1:
                    self.turn_left()
                else:
                    self.shoot()
            else:
                if self.direction != 3:
                    self.turn_left()
                else:
                    self.shoot()

        if self.move_forward():
            return
        if random.randrange(20) == 1:
            self.turn_left()
        if random.randrange(20) == 2:
            self.turn_right()
        if not random.randrange(5):
            self.shoot()


class Destruction(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, destructions)
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 255, 255), (1, 0, 1, 1))
        self.image.fill((255, 255, 255), (0, 1, 3, 1))
        self.image.fill((255, 255, 255), (1, 2, 1, 1))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.x, self.y = x, y
        self.delay = 0
        SOUNDDESTROY.play()

    def update(self):
        if not self.delay:
            self.image = pygame.transform.scale2x(self.image)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.x, self.y
            if self.rect[2] > 32:
                destructions.remove(self)
        self.delay = (self.delay + 1) % 4


start_page()

pygame.quit()
