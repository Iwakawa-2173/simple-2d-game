import pygame
import sys

TILESIZE = 40
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

# Загрузка спрайтов
player_img = pygame.image.load("sophon.png").convert_alpha()
enemy_img = pygame.image.load("un.png").convert_alpha()
coin_img = pygame.image.load("computer.png").convert_alpha()

# Масштабирование под размер тайла
player_img = pygame.transform.scale(player_img, (TILESIZE, TILESIZE))
enemy_img = pygame.transform.scale(enemy_img, (TILESIZE, TILESIZE))
coin_img = pygame.transform.scale(coin_img, (TILESIZE, TILESIZE))

def loadlevel(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    levelmap = []
    i = 0
    while i < len(lines):
        levelmap.append(lines[i].strip())
        i += 1
    return levelmap

def drawlevel(screen, level):
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            if tile == '#':
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

def canmove(level, x, y):
    if y < 0 or y >= len(level) or x < 0 or x >= len(level[0]):
        return False
    return level[y][x] != '#'

def findpositions(level, char):
    positions = []
    for y, row in enumerate(level):
        for x, c in enumerate(row):
            if c == char:
                positions.append((x, y))
    return positions

def moveenemytowardsplayer(enemyx, enemyy, playerx, playery, level):
    dx = playerx - enemyx
    dy = playery - enemyy
    newx, newy = enemyx, enemyy
    if abs(dx) > abs(dy):
        stepx = 1 if dx > 0 else -1
        if canmove(level, enemyx + stepx, enemyy):
            newx = enemyx + stepx
        else:
            stepy = 1 if dy > 0 else -1
            if canmove(level, enemyx, enemyy + stepy):
                newy = enemyy + stepy
    else:
        stepy = 1 if dy > 0 else -1
        if canmove(level, enemyx, enemyy + stepy):
            newy = enemyy + stepy
        else:
            stepx = 1 if dx > 0 else -1
            if canmove(level, enemyx + stepx, enemyy):
                newx = enemyx + stepx
    return newx, newy

level = loadlevel("level.txt")
playerpos = findpositions(level, 'P')[0]
enemypos = findpositions(level, 'E')[0]
coins = findpositions(level, 'C')
collectedcoins = 0

movecounter = 0
movedelay = 10
enemymovecounter = 0
enemymovedelay = 30

game_won = False

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_won:
        keys = pygame.key.get_pressed()
        movecounter += 1
        if movecounter >= movedelay:
            newx, newy = playerpos
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                newx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                newx += 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                newy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                newy += 1
            if canmove(level, newx, newy):
                playerpos = (newx, newy)
                movecounter = 0

        enemymovecounter += 1
        if enemymovecounter >= enemymovedelay:
            enemypos = moveenemytowardsplayer(enemypos[0], enemypos[1], playerpos[0], playerpos[1], level)
            enemymovecounter = 0

        if playerpos in coins:
            coins.remove(playerpos)
            collectedcoins += 1
            if collectedcoins >= 2:
                game_won = True

        if playerpos == enemypos:
            lose_text = big_font.render("Поражение! ООН уничтожила софон!", True, RED)
            text_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(lose_text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

    screen.fill(BLACK)
    drawlevel(screen, level)

    for coinpos in coins:
        coinrect = pygame.Rect(coinpos[0] * TILESIZE, coinpos[1] * TILESIZE, TILESIZE, TILESIZE)
        screen.blit(coin_img, coinrect)

    playerrect = pygame.Rect(playerpos[0] * TILESIZE, playerpos[1] * TILESIZE, TILESIZE, TILESIZE)
    screen.blit(player_img, playerrect)

    enemyrect = pygame.Rect(enemypos[0] * TILESIZE, enemypos[1] * TILESIZE, TILESIZE, TILESIZE)
    screen.blit(enemy_img, enemyrect)

    text = font.render(f"Процессоров взломано: {collectedcoins}", True, YELLOW)
    screen.blit(text, (10, 10))

    if game_won:
        win_text = big_font.render("Победа! Вы уничтожили науку землян!", True, RED)
        text_rect = win_text.get_rect(center=(WIDTH // 2.1, HEIGHT // 2))
        screen.blit(win_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    else:
        pygame.display.flip()

pygame.quit()
sys.exit()

