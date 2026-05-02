import pygame
import sys
import json
import os
from game import Game
from db import init_db, get_or_create_player, save_session, get_personal_best, get_leaderboard
from config import W, H
 
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
 
font_big = pygame.font.SysFont("Arial", 36, bold=True)
font     = pygame.font.SysFont("Arial", 18)
font_sm  = pygame.font.SysFont("Arial", 14)
 
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (180, 180, 180)
DARK   = (30, 30, 30)
YELLOW = (240, 200, 0)
RED    = (200, 50, 50)
GREEN  = (0, 200, 0)
 
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"grid": True, "sound": True, "snake_color": [0, 200, 0]}
 
 
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()
 
 
def save_settings(s):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)
 
 
def draw_button(rect, text, hover=False):
    col = GRAY if hover else (60, 60, 60)
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=6)
    t = font.render(text, True, WHITE)
    screen.blit(t, (rect[0] + (rect[2]-t.get_width())//2, rect[1] + (rect[3]-t.get_height())//2))
 
 
def hovered(rect):
    return pygame.Rect(rect).collidepoint(pygame.mouse.get_pos())
 
 
# ── init ──────────────────────────────────────────────────
try:
    init_db()
    db_ok = True
except Exception as e:
    print(f"DB error: {e}")
    db_ok = False
 
settings = load_settings()
STATE = "menu"
username = ""
player_id = None
personal_best = 0
game = None
 
 
# ── screens ───────────────────────────────────────────────
def screen_menu():
    global username, player_id, personal_best, game, STATE
    screen.fill(DARK)
    title = font_big.render("SNAKE", True, GREEN)
    screen.blit(title, (W//2 - title.get_width()//2, 60))
 
    # name input
    screen.blit(font.render("Username:", True, WHITE), (W//2-140, 140))
    box = pygame.Rect(W//2-140, 165, 280, 38)
    pygame.draw.rect(screen, (60,60,60), box, border_radius=4)
    pygame.draw.rect(screen, WHITE, box, 2, border_radius=4)
    screen.blit(font.render(username + "|", True, WHITE), (box.x+8, box.y+8))
 
    btns = {
        "play":        pygame.Rect(W//2-80, 230, 160, 42),
        "leaderboard": pygame.Rect(W//2-80, 285, 160, 42),
        "settings":    pygame.Rect(W//2-80, 340, 160, 42),
        "quit":        pygame.Rect(W//2-80, 395, 160, 42),
    }
    labels = {"play":"Play","leaderboard":"Leaderboard","settings":"Settings","quit":"Quit"}
    for k, r in btns.items():
        draw_button(r, labels[k], hovered(r))
    return btns
 
 
def screen_leaderboard():
    screen.fill(DARK)
    title = font_big.render("Top 10", True, YELLOW)
    screen.blit(title, (W//2 - title.get_width()//2, 20))
 
    screen.blit(font_sm.render("#   Name              Score  Lvl  Date", True, GRAY), (20, 75))
    pygame.draw.line(screen, GRAY, (20, 95), (W-20, 95))
 
    try:
        board = get_leaderboard() if db_ok else []
    except:
        board = []
 
    for i, (name, score, level, played_at) in enumerate(board):
        date = played_at.strftime("%m/%d") if played_at else ""
        line = f"{i+1:<3} {name[:16]:<17} {score:<7} {level:<4} {date}"
        color = YELLOW if i == 0 else WHITE
        screen.blit(font_sm.render(line, True, color), (20, 105 + i*30))
 
    back = pygame.Rect(W//2-80, H-70, 160, 42)
    draw_button(back, "Back", hovered(back))
    return {"back": back}
 
 
def screen_settings():
    screen.fill(DARK)
    title = font_big.render("Settings", True, WHITE)
    screen.blit(title, (W//2 - title.get_width()//2, 30))
 
    btns = {}
 
    # grid toggle
    btns["grid"] = pygame.Rect(W//2-140, 120, 280, 40)
    draw_button(btns["grid"], f"Grid: {'ON' if settings['grid'] else 'OFF'}", hovered(btns["grid"]))
 
    # sound toggle
    btns["sound"] = pygame.Rect(W//2-140, 175, 280, 40)
    draw_button(btns["sound"], f"Sound: {'ON' if settings['sound'] else 'OFF'}", hovered(btns["sound"]))
 
    # snake color
    screen.blit(font.render("Snake color:", True, WHITE), (W//2-140, 235))
    color_options = [[0,200,0],[50,100,220],[240,200,0],[200,50,50]]
    for i, c in enumerate(color_options):
        r = pygame.Rect(W//2-140 + i*75, 265, 60, 35)
        pygame.draw.rect(screen, c, r, border_radius=4)
        if settings["snake_color"] == c:
            pygame.draw.rect(screen, WHITE, r, 3, border_radius=4)
        btns[f"col_{i}"] = (r, c)
 
    btns["save"] = pygame.Rect(W//2-80, H-100, 160, 42)
    draw_button(btns["save"], "Save & Back", hovered(btns["save"]))
    return btns, color_options
 
 
def screen_gameover():
    screen.fill(DARK)
    title = font_big.render("Game Over", True, RED)
    screen.blit(title, (W//2 - title.get_width()//2, 60))
 
    lines = [
        f"Score:  {game.score}",
        f"Level:  {game.level}",
        f"Best:   {personal_best}",
    ]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, WHITE), (W//2-100, 160 + i*40))
 
    btns = {
        "retry": pygame.Rect(W//2-80, 320, 160, 42),
        "menu":  pygame.Rect(W//2-80, 378, 160, 42),
    }
    draw_button(btns["retry"], "Retry",     hovered(btns["retry"]))
    draw_button(btns["menu"],  "Main Menu", hovered(btns["menu"]))
    return btns
 
 
def start_game():
    global game, personal_best
    try:
        pb = get_personal_best(player_id) if db_ok and player_id else 0
    except:
        pb = 0
    personal_best = pb
    game = Game(settings, personal_best)
 
 
# ── main loop ─────────────────────────────────────────────
move_timer = 0
color_options_cache = []
 
while True:
    dt = clock.tick(60)
    clicks = []
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicks.append(event.pos)
 
        if event.type == pygame.KEYDOWN:
            if STATE == "menu":
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 20 and event.unicode.isprintable():
                    username += event.unicode
 
            elif STATE == "game" and game:
                game.handle_key(event.key)
 
    # ── MENU ────────────────────────────────────────────────
    if STATE == "menu":
        btns = screen_menu()
        for pos in clicks:
            if btns["play"].collidepoint(pos):
                if username.strip():
                    if db_ok:
                        try:
                            player_id = get_or_create_player(username.strip())
                        except:
                            player_id = None
                    start_game()
                    STATE = "game"
                    move_timer = 0
            elif btns["leaderboard"].collidepoint(pos): STATE = "leaderboard"
            elif btns["settings"].collidepoint(pos):   STATE = "settings"
            elif btns["quit"].collidepoint(pos):       pygame.quit(); sys.exit()
 
    # ── LEADERBOARD ─────────────────────────────────────────
    elif STATE == "leaderboard":
        btns = screen_leaderboard()
        for pos in clicks:
            if btns["back"].collidepoint(pos): STATE = "menu"
 
    # ── SETTINGS ────────────────────────────────────────────
    elif STATE == "settings":
        btns, color_options_cache = screen_settings()
        for pos in clicks:
            if isinstance(btns.get("grid"), pygame.Rect) and btns["grid"].collidepoint(pos):
                settings["grid"] = not settings["grid"]
            elif isinstance(btns.get("sound"), pygame.Rect) and btns["sound"].collidepoint(pos):
                settings["sound"] = not settings["sound"]
            elif btns["save"].collidepoint(pos):
                save_settings(settings); STATE = "menu"
            for i, c in enumerate(color_options_cache):
                r, col = btns[f"col_{i}"]
                if r.collidepoint(pos):
                    settings["snake_color"] = col
 
    # ── GAME ────────────────────────────────────────────────
    elif STATE == "game" and game:
        move_timer += dt
        interval = 1000 // game.get_speed()
        while move_timer >= interval:
            game.update()
            move_timer -= interval
 
        game.draw(screen)
 
        if not game.alive:
            if db_ok and player_id:
                try:
                    save_session(player_id, game.score, game.level)
                    personal_best = get_personal_best(player_id)
                except:
                    pass
            STATE = "gameover"
 
    # ── GAME OVER ───────────────────────────────────────────
    elif STATE == "gameover":
        btns = screen_gameover()
        for pos in clicks:
            if btns["retry"].collidepoint(pos):
                start_game(); STATE = "game"; move_timer = 0
            elif btns["menu"].collidepoint(pos):
                STATE = "menu"
 
    pygame.display.flip()