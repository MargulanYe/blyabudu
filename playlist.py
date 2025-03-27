import pygame
pygame.mixer.init()
pygame.init()

running = True
screen = pygame.display.set_mode((800, 750))

godz = pygame.transform.scale(pygame.image.load(r"C:\Users\zsxye\Downloads\dude.jpg"), (800, 750))
real = pygame.transform.scale(pygame.image.load(r"C:\Users\zsxye\Downloads\kairosh.jpg"), (800, 750))
without = pygame.transform.scale(pygame.image.load(r"C:\Users\zsxye\Downloads\tyler.jpg"), (800, 750))

arrP = [godz, real, without] 

arrM = [
    r"C:\Users\zsxye\Downloads\Dudeontheguitar - Osy jerlerdemiz.mp3",
    r"C:\Users\zsxye\Downloads\Кайрат Нуртас - Ламбада.mp3",
    r"C:\Users\zsxye\Downloads\Tyler, the Creator feat. ASAP Rocky & Santigold - New Magic Wand (1).mp3"
]

index = 0
pygame.mixer.music.load(arrM[index])
pygame.mixer.music.play()

paused = False
while running:
    screen.blit(arrP[index], (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                index = (index + 1) % 3
                pygame.mixer.music.load(arrM[index])
                pygame.mixer.music.play()
            if event.key == pygame.K_a:
                index = (index - 1) % 3
                pygame.mixer.music.load(arrM[index])
                pygame.mixer.music.play()
            if event.key == pygame.K_SPACE:
                if paused:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
                paused = not paused
