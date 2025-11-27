import pygame

pygame.init()
running = True

screen = pygame.display.set_mode((1280, 720))

o_image = pygame.image.load("enemy_images/enemy1.png")
pixel_array = pygame.PixelArray(o_image)
pixel_array.replace((0, 0, 0), (255, 0, 0))
del pixel_array

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    screen.blit(o_image, (640, 360))
    pygame.display.flip()