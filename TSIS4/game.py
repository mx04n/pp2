import pygame
import random
from config import COLS, ROWS, GRID, W, H
 
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 200, 0)
RED     = (200, 0, 0)
DARK_RED= (120, 0, 0)
YELLOW  = (240, 200, 0)
BLUE    = (50, 100, 220)
ORANGE  = (255, 140, 0)
PURPLE  = (160, 32, 240)
GRAY    = (80, 80, 80)
DGRAY   = (40, 40, 40)
 
FOOD_WEIGHTS = [(1, 10), (2, 5), (5, 2)]  # (points, weight)
FOOD_LIFETIME = 5000  # ms
 
 
class Food:
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        self.born = pygame.time.get_ticks()
 
    def expired(self):
        return pygame.time.get_ticks() - self.born > FOOD_LIFETIME
 
    def draw(self, surface):
        x, y = self.pos
        color = (200, 60, 60) if self.value == 1 else (240, 180, 0) if self.value == 2 else (0, 200, 200)
        pygame.draw.rect(surface, color, (x*GRID+2, y*GRID+82, GRID-4, GRID-4), border_radius=4)
 
 
class PoisonFood:
    def __init__(self, pos):
        self.pos = pos
        self.born = pygame.time.get_ticks()
 
    def expired(self):
        return pygame.time.get_ticks() - self.born > FOOD_LIFETIME
 
    def draw(self, surface):
        x, y = self.pos
        pygame.draw.rect(surface, DARK_RED, (x*GRID+2, y*GRID+82, GRID-4, GRID-4), border_radius=4)
        pygame.draw.rect(surface, (80,0,0), (x*GRID+2, y*GRID+82, GRID-4, GRID-4), 2, border_radius=4)
 
 
class Powerup:
    TYPES = {
        "speed":  (ORANGE, "SPD"),
        "slow":   (BLUE,   "SLW"),
        "shield": (PURPLE, "SHD"),
    }
 
    def __init__(self, pos, kind):
        self.pos = pos
        self.kind = kind
        self.color, self.label = self.TYPES[kind]
        self.born = pygame.time.get_ticks()
 
    def expired(self):
        return pygame.time.get_ticks() - self.born > 8000
 
    def draw(self, surface, font):
        x, y = self.pos
        pygame.draw.rect(surface, self.color, (x*GRID+1, y*GRID+81, GRID-2, GRID-2), border_radius=5)
        t = font.render(self.label[0], True, WHITE)
        surface.blit(t, (x*GRID + (GRID - t.get_width())//2, y*GRID + 81 + (GRID - t.get_height())//2))
 
 
class Game:
    def __init__(self, settings, personal_best=0):
        self.settings  = settings
        self.snake     = [(COLS//2, ROWS//2)]
        self.direction = (1, 0)
        self.next_dir  = (1, 0)
        self.score     = 0
        self.level     = 1
        self.foods_eaten = 0
        self.personal_best = personal_best
        self.alive     = True
        self.obstacles = set()
        self.foods     = []
        self.poison    = None
        self.powerup   = None
        self.active_pu = None
        self.pu_end    = 0
        self.shield    = False
        self.base_speed = 8
        self.font_small = pygame.font.SysFont("Arial", 13)
        self._spawn_food()
 
    def _free_cells(self):
        taken = set(self.snake) | self.obstacles
        if self.poison: taken.add(self.poison.pos)
        if self.powerup: taken.add(self.powerup.pos)
        for f in self.foods: taken.add(f.pos)
        return [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in taken]
 
    def _spawn_food(self):
        free = self._free_cells()
        if not free:
            return
        pos = random.choice(free)
        weights = [w for _, w in FOOD_WEIGHTS]
        value = random.choices([v for v, _ in FOOD_WEIGHTS], weights=weights)[0]
        self.foods.append(Food(pos, value))
 
        # maybe spawn poison (30% chance)
        free2 = self._free_cells()
        if free2 and random.random() < 0.3:
            self.poison = PoisonFood(random.choice(free2))
 
    def _spawn_powerup(self):
        if self.powerup:
            return
        free = self._free_cells()
        if free:
            kind = random.choice(["speed", "slow", "shield"])
            self.powerup = Powerup(random.choice(free), kind)
 
    def _place_obstacles(self):
        self.obstacles = set()
        head = self.snake[0]
        count = 3 + self.level * 2
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if abs(x - head[0]) > 3 or abs(y - head[1]) > 3]
        for pos in random.sample(free, min(count, len(free))):
            self.obstacles.add(pos)
 
    def handle_key(self, key):
        dirs = {
            pygame.K_UP:    (0, -1), pygame.K_DOWN:  (0, 1),
            pygame.K_LEFT:  (-1, 0), pygame.K_RIGHT: (1, 0),
        }
        if key in dirs:
            nd = dirs[key]
            if (nd[0] != -self.direction[0]) or (nd[1] != -self.direction[1]):
                self.next_dir = nd
 
    def get_speed(self):
        speed = self.base_speed + (self.level - 1) * 2
        now = pygame.time.get_ticks()
        if self.active_pu == "speed" and now < self.pu_end:
            speed += 5
        if self.active_pu == "slow" and now < self.pu_end:
            speed = max(3, speed - 4)
        return speed
 
    def update(self):
        if not self.alive:
            return
 
        now = pygame.time.get_ticks()
 
        # expire active powerup
        if self.active_pu and now > self.pu_end:
            self.active_pu = None
            self.shield = False
 
        # expire food/poison/powerup on field
        self.foods = [f for f in self.foods if not f.expired()]
        if self.poison and self.poison.expired():
            self.poison = None
        if self.powerup and self.powerup.expired():
            self.powerup = None
 
        # spawn food if none
        if not self.foods:
            self._spawn_food()
 
        # maybe spawn powerup every ~10s
        if random.randint(0, 300) == 0:
            self._spawn_powerup()
 
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]
 
        # wall collision
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
            if self.shield:
                self.shield = False
                self.active_pu = None
                nx = max(0, min(COLS-1, nx))
                ny = max(0, min(ROWS-1, ny))
            else:
                self.alive = False
                return
 
        # obstacle collision
        if (nx, ny) in self.obstacles:
            if self.shield:
                self.shield = False
                self.active_pu = None
            else:
                self.alive = False
                return
 
        # self collision
        if (nx, ny) in self.snake[1:]:
            if self.shield:
                self.shield = False
                self.active_pu = None
            else:
                self.alive = False
                return
 
        self.snake.insert(0, (nx, ny))
        grew = False
 
        # eat food
        for f in self.foods[:]:
            if (nx, ny) == f.pos:
                self.score += f.value
                self.foods_eaten += 1
                self.foods.remove(f)
                grew = True
                self._spawn_food()
                if self.foods_eaten % 5 == 0:
                    self.level += 1
                    if self.level >= 3:
                        self._place_obstacles()
                break
 
        # eat poison
        if self.poison and (nx, ny) == self.poison.pos:
            self.poison = None
            self.snake = self.snake[:-min(2, len(self.snake)-1)]
            if len(self.snake) <= 1:
                self.alive = False
                return
            grew = True  # already trimmed
 
        # eat powerup
        if self.powerup and (nx, ny) == self.powerup.pos:
            kind = self.powerup.kind
            self.powerup = None
            self.active_pu = kind
            if kind in ("speed", "slow"):
                self.pu_end = now + 5000
            elif kind == "shield":
                self.shield = True
                self.pu_end = now + 99999
 
        if not grew:
            self.snake.pop()
 
    def draw(self, surface):
        surface.fill(DGRAY)
 
        # HUD
        pygame.draw.rect(surface, (20, 20, 20), (0, 0, W, 80))
        font = pygame.font.SysFont("Arial", 16)
        surface.blit(font.render(f"Score: {self.score}", True, WHITE), (10, 8))
        surface.blit(font.render(f"Level: {self.level}", True, WHITE), (10, 30))
        surface.blit(font.render(f"Best:  {self.personal_best}", True, YELLOW), (10, 52))
 
        if self.active_pu:
            now = pygame.time.get_ticks()
            left = max(0, (self.pu_end - now) // 1000)
            colors = {"speed": ORANGE, "slow": BLUE, "shield": PURPLE}
            label = f"{self.active_pu.upper()}" + (f" {left}s" if left < 9999 else "")
            surface.blit(font.render(label, True, colors.get(self.active_pu, WHITE)), (W-150, 30))
 
        # grid overlay
        if self.settings.get("grid", True):
            for x in range(COLS):
                pygame.draw.line(surface, (50,50,50), (x*GRID, 80), (x*GRID, H))
            for y in range(ROWS):
                pygame.draw.line(surface, (50,50,50), (0, y*GRID+80), (W, y*GRID+80))
 
        # obstacles
        for ox, oy in self.obstacles:
            pygame.draw.rect(surface, GRAY, (ox*GRID, oy*GRID+80, GRID, GRID))
            pygame.draw.rect(surface, (60,60,60), (ox*GRID, oy*GRID+80, GRID, GRID), 1)
 
        # food / poison / powerup
        for f in self.foods: f.draw(surface)
        if self.poison: self.poison.draw(surface)
        if self.powerup: self.powerup.draw(surface, self.font_small)
 
        # snake
        snake_color = tuple(self.settings.get("snake_color", [0, 200, 0]))
        for i, (sx, sy) in enumerate(self.snake):
            col = snake_color if i > 0 else WHITE
            pygame.draw.rect(surface, col, (sx*GRID+1, sy*GRID+81, GRID-2, GRID-2), border_radius=3)
 