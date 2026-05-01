import pygame
import sys
from racer import Game
from ui import (draw_main_menu, draw_settings, draw_leaderboard,
                draw_gameover, draw_name_input)
from persistence import load_settings, save_settings, load_leaderboard, save_score
 
pygame.init()
 
W, H = 480, 640
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer")
 
font_big = pygame.font.SysFont("Arial", 36, bold=True)
font     = pygame.font.SysFont("Arial", 18)
 
clock = pygame.time.Clock()
 
STATE = "menu"
settings = load_settings()
game = None
player_name = ""
 
 
def switch(state):
    global STATE
    STATE = state
 
 
while True:
    mouse = pygame.mouse.get_pos()
    clicks = []
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicks.append(event.pos)
 
        # name input
        if STATE == "name_input" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and player_name.strip():
                game = Game(settings)
                switch("game")
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif len(player_name) < 15 and event.unicode.isprintable():
                player_name += event.unicode
 
        # game keys
        if STATE == "game" and event.type == pygame.KEYDOWN:
            if game:
                game.handle_key(event.key)
 
    # ── MENU ────────────────────────────────────────────────
    if STATE == "menu":
        btns = draw_main_menu(screen, font_big, font, mouse)
        for pos in clicks:
            if btns["play"].collidepoint(pos):       switch("name_input"); player_name = ""
            elif btns["leaderboard"].collidepoint(pos): switch("leaderboard")
            elif btns["settings"].collidepoint(pos): switch("settings")
            elif btns["quit"].collidepoint(pos):     pygame.quit(); sys.exit()
 
    # ── NAME INPUT ──────────────────────────────────────────
    elif STATE == "name_input":
        draw_name_input(screen, font_big, font, player_name)
 
    # ── SETTINGS ────────────────────────────────────────────
    elif STATE == "settings":
        btns = draw_settings(screen, font_big, font, settings, mouse)
        for pos in clicks:
            if btns["sound"].collidepoint(pos):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            elif btns["back"].collidepoint(pos):
                switch("menu")
            for c in ["red", "blue", "green"]:
                if btns[f"color_{c}"].collidepoint(pos):
                    settings["car_color"] = c
                    save_settings(settings)
            for d in ["easy", "normal", "hard"]:
                if btns[f"diff_{d}"].collidepoint(pos):
                    settings["difficulty"] = d
                    save_settings(settings)
 
    # ── LEADERBOARD ─────────────────────────────────────────
    elif STATE == "leaderboard":
        board = load_leaderboard()
        btns = draw_leaderboard(screen, font_big, font, board, mouse)
        for pos in clicks:
            if btns["back"].collidepoint(pos):
                switch("menu")
 
    # ── GAME ────────────────────────────────────────────────
    elif STATE == "game":
        game.update()
        game.draw(screen)
        if not game.alive:
            save_score(player_name, game.score, game.distance // 10, game.coin_count)
            switch("gameover")
 
    # ── GAME OVER ───────────────────────────────────────────
    elif STATE == "gameover":
        btns = draw_gameover(screen, font_big, font,
                             game.score, game.distance // 10, game.coin_count, mouse)
        for pos in clicks:
            if btns["retry"].collidepoint(pos):
                game = Game(settings)
                switch("game")
            elif btns["menu"].collidepoint(pos):
                switch("menu")
 
    pygame.display.flip()
    clock.tick(60)
 