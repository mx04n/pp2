import pygame


pygame.init()
screen = pygame.display.set_mode((636,444))
pygame.display.set_caption("Music_player")

#image
image=pygame.image.load('images/spanch_bob.jpg')

#icon
icon = pygame.image.load('images/music_icon.png')
pygame.display.set_icon(icon)

stores=['mp3/chadilier.ogg','mp3/sigma.ogg']





running = True
a=0
now=0
clock = pygame.time.Clock()

def player(now):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(stores[now])
    pygame.mixer.music.play(-1)



while running:
    screen.blit(image,(0,0))

    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit
            running=False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        player(now)
    elif keys[pygame.K_SPACE]:
        pygame.mixer.music.stop()
    elif keys[pygame.K_LEFT]:
        now=(now-1)%2
        player(now)
    elif keys[pygame.K_RIGHT]:
        now=(now+1)%2
        player(now)
    


    pygame.display.update()
    clock.tick(60)