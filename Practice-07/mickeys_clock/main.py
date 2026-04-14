import pygame 

pygame.init()
screen = pygame.display.set_mode ((800,600)) #flags=pygame.NOFRAME
pygame.display.set_caption("Sigma")

icon=pygame.image.load('images/clock.png')
pygame.display.set_icon(icon)




#body hand
body=pygame.image.load('images/body.JPG')


#minute hand
minute=pygame.image.load('images/minute1.png')
minute=pygame.transform.scale(minute, (800,600))





#sec hand
sec=pygame.image.load('images/sec1.png')
sec=pygame.transform.scale(sec, (800,600))


clock = pygame.time.Clock()











running=True
angle_minute=0
angle_sec=0



while running:

    screen.blit(body,(0,0))

    #roptate the copy image of sec hand
    angle_sec-=0.1
    sec_copy=pygame.transform.rotate(sec,angle_sec)
    screen.blit(sec_copy, ( 400-int(sec_copy.get_width() / 2), 300-int(sec_copy.get_height() / 2) ))



    #rotate the copy image of minute hand
    angle_minute-=1/120
    min_copy = pygame.transform.rotate(minute, angle_minute)
    screen.blit(min_copy, ( 400-int(min_copy.get_width() / 2), 300-int(min_copy.get_height() / 2) ))


    


    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            running=False
        keys=pygame.key.get_pressed()
    pygame.display.update()
    clock.tick(60)
    
    

    