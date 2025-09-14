import pygame
import sys

TILE_SIZE = 40
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Здесь загрузка уровня из txt файла
def load_level(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    level_map = []
    i = 0 # Синтаксис python ужасен
    while i < len(lines):
        level_map.append(lines[i].strip())
        i += 1 # Синтаксис python ужасен
    return level_map

# Здесь отрисовка уровня
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
            x += 1 # Синтаксис python ужасен
        y += 1 # Синтаксис python ужасен

# Функция проверки, можно ли пройти на позицию
def can_move(level, x, y):
    if y < 0 or y >= len(level) or x < 0 or x >= len(level[0]):
        return False
    return level[y][x] != '#'

# Здесь функция, осуществляющая поиск монеток и персонажей в уровне, возвращает списки координат
def find_positions(level, char):
    positions = []
    y = 0
    while y < len(level):
        row = level[y]
        x = 0
        while x < len(row):
            if row[x] == char:
                positions.append((x, y))
            x += 1 # Синтаксис python ужасен
        y += 1 # Синтаксис python ужасен
    return positions


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


level = load_level('level.txt')

# Определяется начальная позиция игрока (поиск символа 'P' в уровне)
player_pos = find_positions(level, 'P')[0]

# Определяется начальная позиция врага (поиск символа 'E' в уровне)
enemy_pos = find_positions(level, 'E')[0]

# Координаты монеток списком
coins = find_positions(level, 'C')

collected_coins = 0

# Переменные для замедления движения
move_counter = 0
move_delay = 10  # число кадров между перемещениями игрока

enemy_move_counter = 0
enemy_move_delay = 30  # враг двигается медленнее в три раза

font = pygame.font.SysFont(None, 36)

def move_enemy_towards_player(enemy_x, enemy_y, player_x, player_y, level):
    # Расстояние по обеим осям двумерного пространства
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    
    new_x, new_y = enemy_x, enemy_y
    # Враг двигается по оси с наибольшей разницей, если возможно
    # Враг пытается сдвинуться по оси X
    if abs(dx) > abs(dy):
        step_x = 1 if dx > 0 else -1
        if can_move(level, enemy_x + step_x, enemy_y):
            new_x = enemy_x + step_x
        else:
            # Если нельзя, попытка по Y
            step_y = 1 if dy > 0 else -1
            if can_move(level, enemy_x, enemy_y + step_y):
                new_y = enemy_y + step_y
    else:
        # Враг пытается сдвигаться по Y
        step_y = 1 if dy > 0 else -1
        if can_move(level, enemy_x, enemy_y + step_y):
            new_y = enemy_y + step_y
        else:
            # Ксли нельзя, пытается по X
            step_x = 1 if dx > 0 else -1
            if can_move(level, enemy_x + step_x, enemy_y):
                new_x = enemy_x + step_x
                
    return new_x, new_y

# Основной цикл игры
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()
    i = 0
    while i < len(events):
        # Среди всех событий, произошедших в игре событие конца осуществляет прерывание цикла
        event = events[i]
        if event.type == pygame.QUIT:
            running = False
        i += 1 # Синтаксис python ужасен
    
    keys = pygame.key.get_pressed()
    move_counter += 1 # Синтаксис python ужасен
    if move_counter >= move_delay:
        new_x, new_y = player_pos
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_y += 1
        if can_move(level, new_x, new_y):
            player_pos = (new_x, new_y)
        move_counter = 0

    enemy_move_counter += 1 # Синтаксис python ужасен
    if enemy_move_counter >= enemy_move_delay:
        enemy_pos = move_enemy_towards_player(enemy_pos[0], enemy_pos[1], player_pos[0], player_pos[1], level)
        enemy_move_counter = 0

    # Проверка, собрал ли игрок монетку
    if player_pos in coins:
        coins.remove(player_pos)
        collected_coins += 1 # Синтаксис python ужасен

    # Если игрок и враг оказались в одном месте, игра заканчивается
    if player_pos == enemy_pos:
        print("Игрок пойман врагом! Игра окончена.")
        running = False

    # Здесь отрисовка происходящего хтонического кошмара
    screen.fill(BLACK)
    draw_level(screen, level)

    # Здесь отрисовка монеток
    
    i = 0
    while i < len(coins):
        coin_pos = coins[i]
        coin_rect = pygame.Rect(coin_pos[0] * TILE_SIZE + TILE_SIZE // 4, coin_pos[1] * TILE_SIZE + TILE_SIZE // 4, TILE_SIZE // 2, TILE_SIZE // 2)

        pygame.draw.ellipse(screen, YELLOW, coin_rect)
        i += 1 # Синтаксис python ужасен


    # Здесь отрисовка игрока
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

    # здесь отрисовка врага
    enemy_rect = pygame.Rect(enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, RED, enemy_rect)

    # Здесь отображение количества собранных монет
    text = font.render(f"Монеты: {collected_coins}", True, YELLOW)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
