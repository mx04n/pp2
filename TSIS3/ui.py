import pygame
 
W, H = 480, 640
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (180, 180, 180)
DARK   = (40, 40, 40)
RED    = (220, 50, 50)
GREEN  = (50, 200, 50)
BLUE   = (50, 100, 220)
YELLOW = (240, 200, 0)
 
 
def draw_button(screen, text, rect, font, hover=False):
    color = GRAY if hover else DARK
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=6)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect[0] + (rect[2] - label.get_width()) // 2,
                         rect[1] + (rect[3] - label.get_height()) // 2))
 
 
def is_hovered(rect, mouse):
    return pygame.Rect(rect).collidepoint(mouse)
 
 
def draw_main_menu(screen, font_big, font, mouse):
    screen.fill(DARK)
    title = font_big.render("RACER", True, YELLOW)
    screen.blit(title, (W // 2 - title.get_width() // 2, 80))
 
    buttons = {
        "play":        pygame.Rect(160, 200, 160, 45),
        "leaderboard": pygame.Rect(160, 260, 160, 45),
        "settings":    pygame.Rect(160, 320, 160, 45),
        "quit":        pygame.Rect(160, 380, 160, 45),
    }
    labels = {"play": "Play", "leaderboard": "Leaderboard", "settings": "Settings", "quit": "Quit"}
    for key, rect in buttons.items():
        draw_button(screen, labels[key], rect, font, is_hovered(rect, mouse))
    return buttons
 
 
def draw_settings(screen, font_big, font, settings, mouse):
    screen.fill(DARK)
    title = font_big.render("Settings", True, WHITE)
    screen.blit(title, (W // 2 - title.get_width() // 2, 40))
 
    buttons = {}
 
    # sound toggle
    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    buttons["sound"] = pygame.Rect(140, 140, 200, 40)
    draw_button(screen, sound_text, buttons["sound"], font, is_hovered(buttons["sound"], mouse))
 
    # car color
    screen.blit(font.render("Car color:", True, WHITE), (140, 200))
    colors = ["red", "blue", "green"]
    for i, c in enumerate(colors):
        r = pygame.Rect(140 + i * 70, 225, 60, 35)
        col = {"red": RED, "blue": BLUE, "green": GREEN}[c]
        pygame.draw.rect(screen, col, r, border_radius=4)
        if settings["car_color"] == c:
            pygame.draw.rect(screen, WHITE, r, 3, border_radius=4)
        buttons[f"color_{c}"] = r
 
    # difficulty
    screen.blit(font.render("Difficulty:", True, WHITE), (140, 280))
    diffs = ["easy", "normal", "hard"]
    for i, d in enumerate(diffs):
        r = pygame.Rect(100 + i * 95, 305, 85, 35)
        draw_button(screen, d.capitalize(), r, font,
                    settings["difficulty"] == d or is_hovered(r, mouse))
        buttons[f"diff_{d}"] = r
 
    buttons["back"] = pygame.Rect(160, 400, 160, 40)
    draw_button(screen, "Back", buttons["back"], font, is_hovered(buttons["back"], mouse))
    return buttons
 
 
def draw_leaderboard(screen, font_big, font, board, mouse):
    screen.fill(DARK)
    title = font_big.render("Top 10", True, YELLOW)
    screen.blit(title, (W // 2 - title.get_width() // 2, 30))
 
    headers = font.render("#   Name          Score   Dist", True, GRAY)
    screen.blit(headers, (30, 90))
    pygame.draw.line(screen, GRAY, (30, 110), (450, 110))
 
    for i, entry in enumerate(board):
        line = f"{i+1:<3} {entry['name'][:12]:<13} {entry['score']:<8} {entry['distance']}m"
        color = YELLOW if i == 0 else WHITE
        screen.blit(font.render(line, True, color), (30, 120 + i * 28))
 
    back = pygame.Rect(160, 580, 160, 40)
    draw_button(screen, "Back", back, font, is_hovered(back, mouse))
    return {"back": back}
 
 
def draw_gameover(screen, font_big, font, score, distance, coins, mouse):
    screen.fill(DARK)
    title = font_big.render("Game Over", True, RED)
    screen.blit(title, (W // 2 - title.get_width() // 2, 60))
 
    lines = [f"Score:    {score}", f"Distance: {distance}m", f"Coins:    {coins}"]
    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, WHITE), (160, 160 + i * 35))
 
    buttons = {
        "retry": pygame.Rect(160, 310, 160, 45),
        "menu":  pygame.Rect(160, 370, 160, 45),
    }
    draw_button(screen, "Retry",     buttons["retry"], font, is_hovered(buttons["retry"], mouse))
    draw_button(screen, "Main Menu", buttons["menu"],  font, is_hovered(buttons["menu"],  mouse))
    return buttons
 
 
def draw_name_input(screen, font_big, font, name):
    screen.fill(DARK)
    title = font_big.render("Enter your name", True, WHITE)
    screen.blit(title, (W // 2 - title.get_width() // 2, 180))
 
    box = pygame.Rect(100, 260, 280, 45)
    pygame.draw.rect(screen, WHITE, box, 2, border_radius=4)
    label = font.render(name + "|", True, WHITE)
    screen.blit(label, (box.x + 10, box.y + 10))
 
    hint = font.render("Press Enter to start", True, GRAY)
    screen.blit(hint, (W // 2 - hint.get_width() // 2, 330))
 