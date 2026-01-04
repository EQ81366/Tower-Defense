import pygame

pygame.init()
running = True

screen = pygame.display.set_mode((1280, 720))
image = pygame.image.load("assets/enemy_images/1_basic_enemy.png")
#image = pygame.image.load("assets/enemy_images/b_bullet.png")

damage_image = image.copy()
with pygame.PixelArray(damage_image) as pixel_array:
    pixel_array.replace(image.get_at((int(image.get_width()/2), int(image.get_height()/2))), (255, 0, 0))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    screen.blit(image, (640, 360))
    screen.blit(damage_image, (640, 360))
    pygame.display.flip()