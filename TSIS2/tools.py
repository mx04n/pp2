import pygame
from collections import deque
 
 
def draw_pencil(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)
 
 
def draw_line(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)
 
 
def draw_rect(surface, start, end, color, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    pygame.draw.rect(surface, color, (x, y, w, h), size)
 
 
def draw_circle(surface, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    r = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2
    pygame.draw.circle(surface, color, (cx, cy), r, size)
 
 
def flood_fill(surface, pos, new_color):
    x, y = pos
    w, h = surface.get_size()
    old_color = surface.get_at((x, y))[:3]
    if old_color == new_color[:3]:
        return
    queue = deque()
    queue.append((x, y))
    while queue:
        cx, cy = queue.popleft()
        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue
        if surface.get_at((cx, cy))[:3] != old_color:
            continue
        surface.set_at((cx, cy), new_color)
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))