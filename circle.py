import pygame
pygame.init()
running=True
screen=pygame.display.set_mode((500,500))
fon=(255,255,255)
screen.fill(fon)
cordX=250
cordY=250
while running:
    screen.fill(fon)
    pygame.draw.circle(screen,"red",(cordX,cordY),25)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w and cordY>15:
                    cordY-=20
            if event.key==pygame.K_s and cordY<485:
                    cordY+=20
            if event.key==pygame.K_d and cordX<485:
                    cordX+=20
            if event.key==pygame.K_a and cordX>15:
                    cordX-=20