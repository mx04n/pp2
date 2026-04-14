import pygame

pygame.init()
screen=pygame.display.set_mode((500,500))
clock = pygame.time.Clock()


step=20

x=25
y=25
squere=pygame.Surface((50,50))
squere.fill('red')


player_input={
    "left": False,
    "right": False,
    "down": False,
    "up": False
}
x=25
y=25
def check_input(key, value):
    if key==pygame.K_UP:
        player_input["up"]=value
    elif key==pygame.K_DOWN:
        player_input["down"]=value
    elif key==pygame.K_RIGHT:
        player_input["right"]=value
    elif key==pygame.K_LEFT:
        player_input["left"]=value


player_velocity=[0,0]



running=True
while running:
    screen.fill((255,255,255))
    pygame.draw.circle(screen,'Red',(x,y),25)
    
    
    player_velocity[0]=player_input["right"]-player_input["left"]
    x+=player_velocity[0]*2
    
    player_velocity[1]=player_input["down"]-player_input["up"] 
    y+=player_velocity[1]*2
    
    if x<=500 and x>=0:
        x+=player_velocity[0]*2
    else:
        x-=player_velocity[0]*2
    
    if y<=500 and y>=0:
        y+=player_velocity[1]*2
    else:
        y-=player_velocity[1]*2
   



    
    


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            running=False
        elif event.type ==pygame.KEYDOWN:
            check_input(event.key, True)
        elif event.type ==pygame.KEYUP:
            check_input(event.key, False)


    clock.tick(60)