import pygame
import sys
from datetime import datetime
from tools import draw_pencil, draw_line, draw_rect, draw_circle, flood_fill
 
pygame.init()
 
WIDTH = 1000
HEIGHT = 600
PANEL = 150
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
 
canvas = pygame.Surface((WIDTH - PANEL, HEIGHT))
canvas.fill((255, 255, 255))
 
font = pygame.font.SysFont("Arial", 14)
 
# colors to choose from
colors = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128),
    (0, 255, 255), (139, 69, 19), (255, 192, 203), (128, 128, 128)
]
 
current_color = (0, 0, 0)
current_tool = "pencil"
brush_size = 5
drawing = False
start_pos = None
prev_pos = None
snapshot = None
 
text_active = False
text_pos = None
text_input = ""
 
 
def get_canvas_pos(pos):
    return (pos[0] - PANEL, pos[1])
 
 
def is_on_canvas(pos):
    return pos[0] > PANEL
 
 
def draw_panel():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, PANEL, HEIGHT))
 
    # tools
    y = 10
    screen.blit(font.render("Tools:", True, (0, 0, 0)), (10, y))
    y += 20
 
    tools = ["pencil", "line", "rect", "circle", "fill", "text"]
    for t in tools:
        color = (100, 149, 237) if t == current_tool else (255, 255, 255)
        pygame.draw.rect(screen, color, (5, y, 140, 25))
        pygame.draw.rect(screen, (0, 0, 0), (5, y, 140, 25), 1)
        screen.blit(font.render(t, True, (0, 0, 0)), (15, y + 5))
        y += 30
 
    # brush size
    y += 10
    screen.blit(font.render("Brush (1/2/3):", True, (0, 0, 0)), (10, y))
    y += 20
    sizes = [2, 5, 10]
    for i, s in enumerate(sizes):
        color = (100, 149, 237) if s == brush_size else (255, 255, 255)
        pygame.draw.rect(screen, color, (5 + i * 45, y, 40, 25))
        pygame.draw.rect(screen, (0, 0, 0), (5 + i * 45, y, 40, 25), 1)
        screen.blit(font.render(str(i + 1), True, (0, 0, 0)), (20 + i * 45, y + 5))
    y += 35
 
    # colors
    screen.blit(font.render("Colors:", True, (0, 0, 0)), (10, y))
    y += 20
    for i, c in enumerate(colors):
        cx = 5 + (i % 4) * 35
        cy = y + (i // 4) * 35
        pygame.draw.rect(screen, c, (cx, cy, 30, 30))
        pygame.draw.rect(screen, (0, 0, 0), (cx, cy, 30, 30), 1)
        if c == current_color:
            pygame.draw.rect(screen, (100, 149, 237), (cx - 2, cy - 2, 34, 34), 2)
 
 
def click_panel(pos):
    global current_tool, brush_size, current_color
 
    x, y = pos
 
    # tools
    ty = 30
    tools = ["pencil", "line", "rect", "circle", "fill", "text"]
    for t in tools:
        if 5 <= x <= 145 and ty <= y <= ty + 25:
            current_tool = t
            return
        ty += 30
 
    # brush
    by = ty + 30
    sizes = [2, 5, 10]
    for i, s in enumerate(sizes):
        if 5 + i * 45 <= x <= 45 + i * 45 and by <= y <= by + 25:
            brush_size = s
            return
 
    # colors
    cy_start = by + 55
    for i, c in enumerate(colors):
        cx = 5 + (i % 4) * 35
        cy = cy_start + (i // 4) * 35
        if cx <= x <= cx + 30 and cy <= y <= cy + 30:
            current_color = c
            return
 
 
clock = pygame.time.Clock()
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
 
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
 
            if event.key == pygame.K_s and mods & pygame.KMOD_CTRL:
                name = "drawing_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                pygame.image.save(canvas, name)
                pygame.display.set_caption("Saved: " + name)
 
            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10
 
            elif text_active:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input, True, current_color)
                    canvas.blit(txt, text_pos)
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if event.unicode.isprintable():
                        text_input += event.unicode
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if not is_on_canvas(pos):
                click_panel(pos)
            else:
                cp = get_canvas_pos(pos)
                if current_tool == "fill":
                    flood_fill(canvas, cp, current_color)
                elif current_tool == "text":
                    if text_active:
                        txt = font.render(text_input, True, current_color)
                        canvas.blit(txt, text_pos)
                    text_active = True
                    text_pos = cp
                    text_input = ""
                else:
                    drawing = True
                    start_pos = cp
                    prev_pos = cp
                    snapshot = canvas.copy()
 
        if event.type == pygame.MOUSEMOTION and drawing:
            cp = get_canvas_pos(event.pos)
            if current_tool == "pencil":
                draw_pencil(canvas, prev_pos, cp, current_color, brush_size)
                prev_pos = cp
            elif current_tool in ("line", "rect", "circle"):
                canvas.blit(snapshot, (0, 0))
                if current_tool == "line":
                    draw_line(canvas, start_pos, cp, current_color, brush_size)
                elif current_tool == "rect":
                    draw_rect(canvas, start_pos, cp, current_color, brush_size)
                elif current_tool == "circle":
                    draw_circle(canvas, start_pos, cp, current_color, brush_size)
 
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            cp = get_canvas_pos(event.pos)
            drawing = False
            if current_tool == "line":
                canvas.blit(snapshot, (0, 0))
                draw_line(canvas, start_pos, cp, current_color, brush_size)
            elif current_tool == "rect":
                canvas.blit(snapshot, (0, 0))
                draw_rect(canvas, start_pos, cp, current_color, brush_size)
            elif current_tool == "circle":
                canvas.blit(snapshot, (0, 0))
                draw_circle(canvas, start_pos, cp, current_color, brush_size)
            snapshot = None
 
    screen.fill((150, 150, 150))
    screen.blit(canvas, (PANEL, 0))
    draw_panel()
 
    if text_active and text_pos:
        preview = font.render(text_input + "|", True, current_color)
        screen.blit(preview, (PANEL + text_pos[0], text_pos[1]))
 
    pygame.display.flip()
    clock.tick(60)
 