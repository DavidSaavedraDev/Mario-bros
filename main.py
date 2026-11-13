import random
import sys

import pygame


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
TILE = 32
GROUND_Y = 544
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Bros. - Pixel Adventure")
clock = pygame.time.Clock()

SKY = (92, 148, 252)
INK = (35, 29, 48)
WHITE = (255, 255, 255)
RED = (214, 38, 42)
RED_DARK = (132, 25, 34)
SKIN = (255, 177, 115)
BLUE = (31, 83, 169)
BLUE_DARK = (19, 51, 112)
GOLD = (255, 205, 48)
GOLD_DARK = (196, 126, 26)
BRICK = (183, 75, 44)
BRICK_LIGHT = (224, 112, 62)
BRICK_DARK = (113, 48, 39)
PIPE = (27, 159, 73)
PIPE_LIGHT = (73, 210, 105)
PIPE_DARK = (14, 94, 48)


def pixel_rect(surface, color, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))


def make_player_frame(frame, jumping=False):
    image = pygame.Surface((48, 64), pygame.SRCALPHA)
    bob = 1 if frame == 1 and not jumping else 0
    # Sombra y pelo
    pixel_rect(image, INK, 10, 8 + bob, 29, 22)
    pixel_rect(image, RED_DARK, 8, 8 + bob, 30, 8)
    pixel_rect(image, RED, 12, 4 + bob, 29, 10)
    pixel_rect(image, RED, 8, 11 + bob, 18, 7)
    pixel_rect(image, SKIN, 16, 17 + bob, 23, 16)
    pixel_rect(image, INK, 33, 21 + bob, 4, 4)
    pixel_rect(image, SKIN, 12, 27 + bob, 9, 7)
    # Camisa, tirantes y overol
    pixel_rect(image, RED, 13, 33 + bob, 25, 12)
    pixel_rect(image, BLUE_DARK, 16, 34 + bob, 21, 21)
    pixel_rect(image, BLUE, 20, 38 + bob, 17, 15)
    pixel_rect(image, GOLD, 18, 36 + bob, 5, 5)
    pixel_rect(image, GOLD, 32, 36 + bob, 5, 5)
    pixel_rect(image, RED_DARK, 8, 43 + bob, 11, 8)
    pixel_rect(image, RED_DARK, 35, 43 + bob, 10, 8)
    if jumping:
        pixel_rect(image, RED_DARK, 7, 52, 14, 7)
        pixel_rect(image, RED_DARK, 34, 52, 14, 7)
    elif frame == 0:
        pixel_rect(image, RED_DARK, 10, 55, 13, 7)
        pixel_rect(image, RED_DARK, 34, 55, 13, 7)
    else:
        pixel_rect(image, RED_DARK, 6, 55, 15, 7)
        pixel_rect(image, RED_DARK, 36, 53, 12, 7)
    return image


def make_goomba_frame(frame):
    image = pygame.Surface((48, 40), pygame.SRCALPHA)
    pixel_rect(image, INK, 8, 13, 32, 20)
    pixel_rect(image, BRICK_DARK, 7, 13, 34, 16)
    pixel_rect(image, (145, 70, 38), 11, 6, 26, 22)
    pixel_rect(image, (177, 87, 42), 7, 13, 34, 14)
    pixel_rect(image, WHITE, 13, 14, 8, 9)
    pixel_rect(image, WHITE, 27, 14, 8, 9)
    pixel_rect(image, INK, 17, 17, 4, 5)
    pixel_rect(image, INK, 29, 17, 4, 5)
    pixel_rect(image, INK, 15, 28, 19, 4)
    if frame == 0:
        pixel_rect(image, INK, 5, 32, 16, 7)
        pixel_rect(image, INK, 29, 32, 16, 7)
    else:
        pixel_rect(image, INK, 9, 32, 13, 7)
        pixel_rect(image, INK, 27, 32, 13, 7)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [make_player_frame(0), make_player_frame(1)]
        self.jump_image = make_player_frame(0, True)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(120, GROUND_Y - 64))
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing = 1
        self.anim_timer = 0.0
        self.score = 0
        self.lives = 3
        self.invincible_until = 0

    def jump(self):
        if self.on_ground:
            self.velocity.y = -14
            self.on_ground = False

    def update_animation(self, dt):
        if not self.on_ground:
            self.image = self.jump_image
        elif abs(self.velocity.x) > 0.1:
            self.anim_timer += dt
            self.image = self.frames[int(self.anim_timer * 10) % 2]
        else:
            self.anim_timer = 0
            self.image = self.frames[0]
        old_bottom = self.rect.bottom
        self.rect.size = self.image.get_size()
        self.rect.bottom = old_bottom

    def hurt(self):
        now = pygame.time.get_ticks()
        if now < self.invincible_until:
            return False
        self.lives -= 1
        self.invincible_until = now + 1400
        self.rect.topleft = (120, GROUND_Y - self.rect.height)
        self.velocity.update(0, 0)
        return True


class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [make_goomba_frame(0), make_goomba_frame(1)]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.direction = -1
        self.speed = 1.15
        self.anim_timer = random.random()

    def update(self, dt):
        self.rect.x += round(self.direction * self.speed)
        self.anim_timer += dt
        self.image = self.frames[int(self.anim_timer * 5) % 2]


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center = (x, y)
        self.phase = random.random() * 6
        self.image = pygame.Surface((32, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.center)

    def update(self, dt):
        self.phase += dt * 7
        width = max(4, int(abs(pygame.math.Vector2(1, 0).rotate(self.phase).x) * 20))
        self.image.fill((0, 0, 0, 0))
        pixel_rect(self.image, GOLD_DARK, 16 - width // 2, 4, width, 32)
        pixel_rect(self.image, GOLD, 17 - width // 2, 5, max(2, width - 3), 29)
        pixel_rect(self.image, WHITE, 15, 8, 3, 8)
        self.rect = self.image.get_rect(center=self.center)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, kind="brick"):
        super().__init__()
        self.kind = kind
        self.image = pygame.Surface((TILE, TILE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.draw()

    def draw(self):
        self.image.fill(BRICK if self.kind == "brick" else GOLD_DARK)
        if self.kind == "brick":
            pygame.draw.rect(self.image, BRICK_LIGHT, (1, 1, 30, 3))
            pygame.draw.rect(self.image, BRICK_DARK, (0, 15, 32, 3))
            pygame.draw.rect(self.image, BRICK_DARK, (15, 0, 3, 15))
            pygame.draw.rect(self.image, BRICK_DARK, (7, 17, 3, 15))
            pygame.draw.rect(self.image, BRICK_DARK, (24, 17, 3, 15))
        else:
            self.image.fill(GOLD)
            pygame.draw.rect(self.image, GOLD_DARK, (1, 1, 30, 30), 3)
            font = pygame.font.Font(None, 30)
            mark = font.render("?", True, WHITE)
            self.image.blit(mark, mark.get_rect(center=(16, 16)))


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        super().__init__()
        self.image = pygame.Surface((80, height), pygame.SRCALPHA)
        pixel_rect(self.image, PIPE_DARK, 10, 0, 60, height)
        pixel_rect(self.image, PIPE, 16, 0, 48, height)
        pixel_rect(self.image, PIPE_LIGHT, 20, 0, 12, height)
        pixel_rect(self.image, PIPE_DARK, 0, 0, 80, 16)
        pixel_rect(self.image, PIPE, 4, 3, 72, 12)
        pixel_rect(self.image, PIPE_LIGHT, 10, 4, 18, 5)
        self.rect = self.image.get_rect(bottomleft=(x, GROUND_Y))


def draw_cloud(surface, x, y):
    color = WHITE
    for rectangle in ((x, y + 12, 74, 20), (x + 14, y, 34, 32),
                      (x + 42, y + 7, 43, 25)):
        pygame.draw.rect(surface, color, rectangle)
    pixel_rect(surface, INK, x + 20, y + 18, 5, 5)
    pixel_rect(surface, INK, x + 55, y + 18, 5, 5)


def draw_hill(surface, x, y, width, height, camera):
    points = [(x - camera, GROUND_Y), (x + width // 2 - camera, y),
              (x + width - camera, GROUND_Y)]
    pygame.draw.polygon(surface, (54, 177, 75), points)
    pygame.draw.polygon(surface, (25, 116, 62),
                        [(x + width // 2 - camera, y), (x + width - camera, GROUND_Y),
                         (x + width // 2 + 18 - camera, GROUND_Y)])
    for row in range(3):
        for column in range(4):
            px = x + width // 2 - 50 + column * 24 + row * 9 - camera
            py = y + 50 + row * 28
            if px > -20 and px < SCREEN_WIDTH:
                pixel_rect(surface, (36, 137, 65), px, py, 7, 7)


def draw_background(surface, camera):
    surface.fill(SKY)
    for x, y in ((70, 70), (430, 125), (790, 58), (1250, 92), (1700, 58)):
        draw_cloud(surface, x - camera // 3, y)
    draw_hill(surface, 80, 360, 300, 184, camera // 2)
    draw_hill(surface, 520, 405, 390, 139, camera // 2)
    draw_hill(surface, 1080, 350, 350, 194, camera // 2)
    # Suelo de ladrillos clásico
    pixel_rect(surface, BRICK_DARK, 0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y)
    for y in range(GROUND_Y, SCREEN_HEIGHT, TILE):
        for x in range(-TILE, SCREEN_WIDTH + TILE, TILE):
            px = x - (camera % TILE)
            pygame.draw.rect(surface, BRICK, (px + 1, y + 1, TILE - 2, TILE - 2))
            pygame.draw.line(surface, BRICK_LIGHT, (px + 2, y + 2), (px + TILE - 3, y + 2), 2)
        pygame.draw.line(surface, BRICK_DARK, (0, y), (SCREEN_WIDTH, y), 3)


def build_level():
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    scenery = pygame.sprite.Group()
    # Suelo invisible para colisionar; el arte se dibuja en el fondo.
    for x in range(-200, 3200, TILE):
        platforms.add(pygame.sprite.Sprite())
        platforms.sprites()[-1].rect = pygame.Rect(x, GROUND_Y, TILE, SCREEN_HEIGHT - GROUND_Y)
    for x, y in ((360, 400), (520, 320), (720, 400), (930, 290),
                 (1160, 380), (1400, 320), (1660, 400), (1940, 350), (2250, 400)):
        block = Block(x, y, "brick")
        blocks.add(block)
        platforms.add(block)
    for x, y in ((430, 400), (462, 400), (752, 400), (1010, 290),
                 (1192, 380), (1432, 320), (1700, 400), (1980, 350)):
        coin = Coin(x, y - 38)
        coins.add(coin)
    for x, y in ((330, 2), (820, 2), (1320, 1), (1850, 2), (2460, 1)):
        pipe = Pipe(x, 96 if y == 2 else 64)
        scenery.add(pipe)
        platforms.add(pipe)
    for x in (610, 1080, 1510, 1800, 2160, 2600):
        enemy = Goomba(x, GROUND_Y)
        enemies.add(enemy)
    return platforms, enemies, coins, blocks, scenery


def reset_game():
    player = Player()
    platforms, enemies, coins, blocks, scenery = build_level()
    return player, platforms, enemies, coins, blocks, scenery


def move_player(player, platforms, dt):
    player.velocity.x = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity.x = -4
        player.facing = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity.x = 4
        player.facing = 1
    player.velocity.y = min(player.velocity.y + 0.62, 15)
    player.rect.x += round(player.velocity.x)
    for platform in pygame.sprite.spritecollide(player, platforms, False):
        if player.velocity.x > 0:
            player.rect.right = platform.rect.left
        elif player.velocity.x < 0:
            player.rect.left = platform.rect.right
    old_bottom = player.rect.bottom
    player.rect.y += round(player.velocity.y)
    player.on_ground = False
    for platform in pygame.sprite.spritecollide(player, platforms, False):
        if player.velocity.y > 0 and old_bottom <= platform.rect.top + 6:
            player.rect.bottom = platform.rect.top
            player.velocity.y = 0
            player.on_ground = True
        elif player.velocity.y < 0 and player.rect.top < platform.rect.bottom:
            player.rect.top = platform.rect.bottom
            player.velocity.y = 0
    if player.rect.top > SCREEN_HEIGHT + 80:
        player.lives = 0
    player.update_animation(dt)


def draw_text(surface, text, position, size=24, color=WHITE):
    font = pygame.font.Font(None, size)
    shadow = font.render(text, True, INK)
    surface.blit(shadow, (position[0] + 2, position[1] + 2))
    surface.blit(font.render(text, True, color), position)


def main():
    player, platforms, enemies, coins, blocks, scenery = reset_game()
    camera = 0
    game_over = False
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w) and not game_over:
                    player.jump()
                elif event.key == pygame.K_r and game_over:
                    player, platforms, enemies, coins, blocks, scenery = reset_game()
                    camera = 0
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            move_player(player, platforms, dt)
            enemies.update(dt)
            coins.update(dt)
            for enemy in enemies:
                if enemy.rect.left < 0 or enemy.rect.right > 3000:
                    enemy.direction *= -1
            for enemy in pygame.sprite.spritecollide(player, enemies, False):
                if player.velocity.y > 1 and player.rect.bottom - enemy.rect.top < 18:
                    enemy.kill()
                    player.velocity.y = -8
                    player.score += 100
                elif player.hurt() and player.lives <= 0:
                    game_over = True
            for coin in pygame.sprite.spritecollide(player, coins, True):
                player.score += 50
            if player.rect.right > camera + SCREEN_WIDTH * 0.45:
                camera = min(player.rect.right - SCREEN_WIDTH * 0.45, 2200)
            if player.lives <= 0:
                game_over = True

        draw_background(screen, int(camera))
        for sprite in scenery:
            screen.blit(sprite.image, (sprite.rect.x - camera, sprite.rect.y))
        for sprite in blocks:
            screen.blit(sprite.image, (sprite.rect.x - camera, sprite.rect.y))
        for sprite in coins:
            screen.blit(sprite.image, (sprite.rect.x - camera, sprite.rect.y))
        for sprite in enemies:
            screen.blit(sprite.image, (sprite.rect.x - camera, sprite.rect.y))
        if not (pygame.time.get_ticks() < player.invincible_until and
                (pygame.time.get_ticks() // 90) % 2):
            screen.blit(player.image, (player.rect.x - camera, player.rect.y))
        draw_text(screen, f"MARIO  {player.score:06d}", (22, 18), 25)
        draw_text(screen, f"VIDAS x {player.lives}", (22, 47), 22, GOLD)
        draw_text(screen, "Flechas/A-D: mover   ESPACIO: saltar", (SCREEN_WIDTH - 330, 20), 18)
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((16, 18, 42, 170))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "GAME OVER", (SCREEN_WIDTH // 2 - 105, 235), 52, RED)
            draw_text(screen, "Pulsa R para reiniciar", (SCREEN_WIDTH // 2 - 104, 305), 25)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
