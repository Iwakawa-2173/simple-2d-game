import pygame
import sys

# Константы
TILE_SIZE = 40
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # цвет монетки
RED = (255, 0, 0)       # цвет врага

# Загрузка уровня из txt файла
def load_level(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    level_map = []
    i = 0
    while i < len(lines):
        level_map.append(lines[i].strip())
        i += 1
    return level_map

# Отрисовка уровня
def draw_level(screen, level):
    y = 0
    while y < len(level):
        row = level[y]
        x = 0
        while x < len(row):
            tile = row[x]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == '#':  # Стена
                pygame.draw.rect(screen, GRAY, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            x += 1
        y += 1

# Проверка, можно ли пройти на позицию
def can_move(level, x, y):
    if y < 0 or y >= len(level) or x < 0 or x >= len(level[0]):
        return False
    return level[y][x] != '#'

# Поиск монеток и персонажей в уровне, возвращает списки координат
def find_positions(level, char):
    positions = []
    y = 0
    while y < len(level):
        row = level[y]
        x = 0
        while x < len(row):
            if row[x] == char:
                positions.append((x, y))
            x += 1
        y += 1
    return positions

# Инициализация pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка уровня
level = load_level('level.txt')

# Стартовая позиция игрока (поиск символа 'P' в уровне)
player_pos = find_positions(level, 'P')[0]

# Стартовая позиция врага (поиск символа 'E' в уровне)
enemy_pos = find_positions(level, 'E')[0]

# Монетки — координаты в виде списка
coins = find_positions(level, 'C')

# Количество собранных монет
collected_coins = 0

# Переменные для замедления движения
move_counter = 0
move_delay = 10  # число кадров между перемещениями игрока

enemy_move_counter = 0
enemy_move_delay = 30  # враг двигается медленнее

font = pygame.font.SysFont(None, 36)

def move_enemy_towards_player(enemy_x, enemy_y, player_x, player_y, level):
    # Двигается по оси с наибольшей разницей, если возможно
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    
    new_x, new_y = enemy_x, enemy_y
    
    # Попытаемся сдвинуться по оси X
    if abs(dx) > abs(dy):
        step_x = 1 if dx > 0 else -1
        if can_move(level, enemy_x + step_x, enemy_y):
            new_x = enemy_x + step_x
        else:
            # если нельзя, пытаемся по Y
            step_y = 1 if dy > 0 else -1
            if can_move(level, enemy_x, enemy_y + step_y):
                new_y = enemy_y + step_y
    else:
        # Сдвигаемся по Y
        step_y = 1 if dy > 0 else -1
        if can_move(level, enemy_x, enemy_y + step_y):
            new_y = enemy_y + step_y
        else:
            # если нельзя, пытаемся по X
            step_x = 1 if dx > 0 else -1
            if can_move(level, enemy_x + step_x, enemy_y):
                new_x = enemy_x + step_x
                
    return new_x, new_y

# Игровой цикл
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()
    i = 0
    while i < len(events):
        event = events[i]
        if event.type == pygame.QUIT:
            running = False
        i += 1

    keys = pygame.key.get_pressed()
    move_counter += 1
    if move_counter >= move_delay:
        new_x, new_y = player_pos
        if keys[pygame.K_LEFT]:
            new_x -= 1
        if keys[pygame.K_RIGHT]:
            new_x += 1
        if keys[pygame.K_UP]:
            new_y -= 1
        if keys[pygame.K_DOWN]:
            new_y += 1
        if can_move(level, new_x, new_y):
            player_pos = (new_x, new_y)
        move_counter = 0

    # Враг двигается медленнее игрока
    enemy_move_counter += 1
    if enemy_move_counter >= enemy_move_delay:
        enemy_pos = move_enemy_towards_player(enemy_pos[0], enemy_pos[1], player_pos[0], player_pos[1], level)
        enemy_move_counter = 0

    # Проверяем, собрал ли игрок монетку
    if player_pos in coins:
        coins.remove(player_pos)
        collected_coins += 1

    # Проверяем столкновение с врагом — можно добавить обработку проигрыша здесь
    if player_pos == enemy_pos:
        # Здесь просто выйдем из игры, но можно сделать что-то другое
        print("Игрок пойман врагом! Игра окончена.")
        running = False

    # Отрисовка
    screen.fill(BLACK)
    draw_level(screen, level)

    # Отрисовка монеток
    for coin_pos in coins:
        coin_rect = pygame.Rect(coin_pos[0] * TILE_SIZE + TILE_SIZE//4, coin_pos[1] * TILE_SIZE + TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2)
        pygame.draw.ellipse(screen, YELLOW, coin_rect)

    # Отрисовка игрока
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Отрисовка врага
    enemy_rect = pygame.Rect(enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, RED, enemy_rect)

    # Отображение количества собранных монет
    text = font.render(f"Монеты: {collected_coins}", True, YELLOW)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
