import pygame, sys
pygame.init()

# [Basic] Constantes
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,225,0)
RED   = (225,0,0)
BLUE   = (0,0,225)

# [Basic] Pantalla
size = (800, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# [Basic] Variables

# [Basic] Game-Loop [Update]
while True:
    
    # [01] Event's Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # [02] Logica
    # [03] Zona de Dibujo
    # [04] Colisiones
    # [05] Codigo Del Juego   
    # [06] Extra   
    pygame.display.flip()
    clock.tick(60)