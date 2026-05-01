import pygame
import random
import time
 
W, H = 480, 640
ROAD_LEFT  = 80
ROAD_RIGHT = 400
LANE_W = (ROAD_RIGHT - ROAD_LEFT) // 3
LANES = [ROAD_LEFT + LANE_W * i + LANE_W // 2 for i in range(3)]
 
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (100, 100, 100)
YELLOW = (240, 200, 0)
RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
 
CAR_COLORS = {"red": RED, "blue": BLUE, "green": GREEN}
 
DIFF = {
    "easy":   {"speed": 4, "spawn_rate": 90},
    "normal": {"speed": 6, "spawn_rate": 60},
    "hard":   {"speed": 9, "spawn_rate": 35},
}
 
 
class Player:
    def __init__(self, color):
        self.lane = 1
        self.x = LANES[self.lane]
        self.y = H - 120
        self.w = 40
        self.h = 70
        self.color = CAR_COLORS.get(color, RED)
        self.shield = False
        self.nitro = False
        self.nitro_end = 0
        self.shield_used = False
 
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)
 
    def draw(self, screen):
        col = self.color
        pygame.draw.rect(screen, col, self.rect(), border_radius=6)
        pygame.draw.rect(screen, WHITE, self.rect(), 2, border_radius=6)
        if self.shield:
            pygame.draw.rect(screen, BLUE, self.rect().inflate(10, 10), 3, border_radius=8)
        if self.nitro:
            pygame.draw.rect(screen, ORANGE, self.rect().inflate(6, 6), 2, border_radius=7)
 
    def move(self, direction):
        self.lane = max(0, min(2, self.lane + direction))
        self.x = LANES[self.lane]
 
    def update(self):
        if self.nitro and time.time() > self.nitro_end:
            self.nitro = False
 
 
class Enemy:
    def __init__(self, speed):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -40
        self.w = 40
        self.h = 70
        self.speed = speed
        self.color = (random.randint(80, 200), random.randint(80, 200), random.randint(80, 200))
 
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)
 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=6)
        pygame.draw.rect(screen, WHITE, self.rect(), 2, border_radius=6)
 
    def update(self, speed_mult):
        self.y += self.speed * speed_mult
 
 
class Obstacle:
    TYPES = {
        "oil":     (GRAY,   "OIL",  "slow"),
        "barrier": (ORANGE, "|||",  "stop"),
        "pit":     (BLACK,  "PIT",  "stop"),
    }
 
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -30
        self.w = 50
        self.h = 30
        self.kind = random.choice(list(self.TYPES.keys()))
        self.color, self.label, self.effect = self.TYPES[self.kind]
 
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)
 
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=4)
        txt = font.render(self.label, True, WHITE)
        screen.blit(txt, (self.x - txt.get_width() // 2, self.y - txt.get_height() // 2))
 
    def update(self, speed):
        self.y += speed
 
 
class Powerup:
    TYPES = {
        "nitro":  (ORANGE, "N"),
        "shield": (BLUE,   "S"),
        "repair": (GREEN,  "R"),
    }
 
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -25
        self.w = 35
        self.h = 35
        self.kind = random.choice(list(self.TYPES.keys()))
        self.color, self.label = self.TYPES[self.kind]
        self.spawn_time = time.time()
 
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)
 
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect(), border_radius=18)
        pygame.draw.rect(screen, WHITE, self.rect(), 2, border_radius=18)
        txt = font.render(self.label, True, WHITE)
        screen.blit(txt, (self.x - txt.get_width() // 2, self.y - txt.get_height() // 2))
 
    def update(self, speed):
        self.y += speed
 
    def expired(self):
        return time.time() - self.spawn_time > 6
 
 
class Coin:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.x = LANES[self.lane]
        self.y = -20
        self.r = 12
        self.value = random.choice([1, 1, 1, 2, 5])
 
    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)
 
    def draw(self, screen, font):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.r)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.r, 2)
        txt = font.render(str(self.value), True, BLACK)
        screen.blit(txt, (self.x - txt.get_width() // 2, self.y - txt.get_height() // 2))
 
    def update(self, speed):
        self.y += speed
 
 
class Game:
    def __init__(self, settings):
        self.settings = settings
        self.player = Player(settings["car_color"])
        diff = DIFF[settings["difficulty"]]
        self.base_speed = diff["speed"]
        self.spawn_rate = diff["spawn_rate"]
        self.speed_mult = 1.0
        self.enemies   = []
        self.obstacles = []
        self.powerups  = []
        self.coins     = []
        self.score     = 0
        self.distance  = 0
        self.coin_count = 0
        self.frame     = 0
        self.road_y    = 0
        self.alive     = True
        self.crashed   = 0  # crash count
        self.active_powerup = None
        self.powerup_label  = ""
        self.powerup_end    = 0
        self.font_small = pygame.font.SysFont("Arial", 14)
 
    def spawn_safe(self, lane):
        if lane == self.player.lane and abs(self.player.y - H) < 150:
            return False
        return True
 
    def update(self):
        if not self.alive:
            return
 
        self.frame += 1
        self.distance += 1
        self.speed_mult = 1.0 + self.distance / 3000
        speed = self.base_speed * self.speed_mult
        if self.player.nitro:
            speed *= 1.6
 
        # road scroll
        self.road_y = (self.road_y + speed) % 80
 
        # spawn enemies
        if self.frame % max(20, int(self.spawn_rate / self.speed_mult)) == 0:
            lane = random.randint(0, 2)
            if self.spawn_safe(lane):
                self.enemies.append(Enemy(self.base_speed))
 
        # spawn obstacles
        if self.frame % max(40, int(120 / self.speed_mult)) == 0:
            lane = random.randint(0, 2)
            if self.spawn_safe(lane):
                self.obstacles.append(Obstacle())
 
        # spawn powerups
        if self.frame % 180 == 0:
            self.powerups.append(Powerup())
 
        # spawn coins
        if self.frame % 30 == 0:
            self.coins.append(Coin())
 
        # update all
        for e in self.enemies:   e.update(self.speed_mult)
        for o in self.obstacles: o.update(speed)
        for p in self.powerups:  p.update(speed)
        for c in self.coins:     c.update(speed)
 
        # remove off-screen
        self.enemies   = [e for e in self.enemies   if e.y < H + 60]
        self.obstacles = [o for o in self.obstacles if o.y < H + 40]
        self.powerups  = [p for p in self.powerups  if p.y < H + 40 and not p.expired()]
        self.coins     = [c for c in self.coins     if c.y < H + 30]
 
        # powerup timer
        if self.active_powerup and time.time() > self.powerup_end:
            self.active_powerup = None
            self.player.nitro = False
 
        self.player.update()
        self._check_collisions()
 
        self.score = self.coin_count * 10 + self.distance // 10
 
    def _check_collisions(self):
        pr = self.player.rect()
 
        # enemies
        for e in self.enemies:
            if pr.colliderect(e.rect()):
                if self.player.shield:
                    self.player.shield = False
                    self.active_powerup = None
                    self.enemies.remove(e)
                else:
                    self.alive = False
                return
 
        # obstacles
        for o in self.obstacles:
            if pr.colliderect(o.rect()):
                if self.player.shield:
                    self.player.shield = False
                    self.active_powerup = None
                    self.obstacles.remove(o)
                elif o.effect == "slow":
                    self.speed_mult = max(0.5, self.speed_mult - 0.3)
                    self.obstacles.remove(o)
                else:
                    self.alive = False
                return
 
        # powerups
        for p in self.powerups[:]:
            if pr.colliderect(p.rect()):
                self._apply_powerup(p.kind)
                self.powerups.remove(p)
 
        # coins
        for c in self.coins[:]:
            if pr.colliderect(c.rect()):
                self.coin_count += c.value
                self.coins.remove(c)
 
    def _apply_powerup(self, kind):
        self.active_powerup = kind
        self.player.shield = False
        self.player.nitro  = False
        if kind == "nitro":
            self.player.nitro = True
            self.player.nitro_end = time.time() + 4
            self.powerup_end = self.player.nitro_end
            self.powerup_label = "NITRO"
        elif kind == "shield":
            self.player.shield = True
            self.powerup_end = time.time() + 9999
            self.powerup_label = "SHIELD"
        elif kind == "repair":
            self.crashed = max(0, self.crashed - 1)
            self.active_powerup = None
            self.powerup_label = ""
 
    def handle_key(self, key):
        if key == pygame.K_LEFT:
            self.player.move(-1)
        elif key == pygame.K_RIGHT:
            self.player.move(1)
 
    def draw(self, screen):
        # background
        screen.fill((30, 30, 30))
 
        # road
        pygame.draw.rect(screen, (60, 60, 60), (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, H))
 
        # lane markings
        for lane_x in [ROAD_LEFT + LANE_W, ROAD_LEFT + LANE_W * 2]:
            for y in range(int(-80 + self.road_y), H, 80):
                pygame.draw.rect(screen, YELLOW, (lane_x - 2, y, 4, 40))
 
        # road edges
        pygame.draw.rect(screen, WHITE, (ROAD_LEFT - 4, 0, 4, H))
        pygame.draw.rect(screen, WHITE, (ROAD_RIGHT, 0, 4, H))
 
        for e in self.enemies:   e.draw(screen)
        for o in self.obstacles: o.draw(screen, self.font_small)
        for p in self.powerups:  p.draw(screen, self.font_small)
        for c in self.coins:     c.draw(screen, self.font_small)
        self.player.draw(screen)
 
        # HUD
        f = self.font_small
        screen.blit(f.render(f"Score: {self.score}", True, WHITE), (5, 5))
        screen.blit(f.render(f"Dist:  {self.distance // 10}m", True, WHITE), (5, 22))
        screen.blit(f.render(f"Coins: {self.coin_count}", True, YELLOW), (5, 39))
 
        if self.active_powerup:
            left = max(0, int(self.powerup_end - time.time()))
            label = f"{self.powerup_label}" + (f" {left}s" if left < 9999 else "")
            pygame.draw.rect(screen, (50, 50, 50), (ROAD_RIGHT + 5, 5, 70, 22), border_radius=4)
            screen.blit(f.render(label, True, ORANGE), (ROAD_RIGHT + 8, 8))
 
 