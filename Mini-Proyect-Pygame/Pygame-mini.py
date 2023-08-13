
import pygame
import math
import sys

# Definiciones de constantes
MOUSE_BORDER_LEFT = 50
MOUSE_BORDER_RIGHT = 750
HALF_WIDTH = 400
HALF_HEIGHT = 300

class Player:
    def __init__(self, x, y, radius, speed):
        self.pos = [x, y]
        self.radius = radius
        self.speed = speed
        self.angle = 0  # Ángulo de movimiento
        self.rotation_speed = 3  # Velocidad de rotación

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dx, dy = self.calculate_movement(math.radians(self.angle), self.speed)
        if keys[pygame.K_s]:
            dx, dy = self.calculate_movement(math.radians(self.angle + 180), self.speed)
        if keys[pygame.K_a]:
            dx, dy = self.calculate_movement(math.radians(self.angle + 90), self.speed)
        if keys[pygame.K_d]:
            dx, dy = self.calculate_movement(math.radians(self.angle - 90), self.speed)
        self.pos[0] += dx
        self.pos[1] += dy

    def calculate_movement(self, angle, speed):
        dx = speed * math.cos(angle)
        dy = -speed * math.sin(angle)
        return dx, dy

    def update_angle(self, mouse_pos):
        dx = mouse_pos[0] - self.pos[0]
        dy = self.pos[1] - mouse_pos[1]
        self.angle = math.degrees(math.atan2(dy, dx))
        self.angle %= 360  # Asegurar que el ángulo esté en el rango de 0 a 360 grados

    def rotate(self, direction):
        self.angle += self.rotation_speed * direction
        self.angle %= 360  # Asegurar que el ángulo esté en el rango de 0 a 360 grados

    def mouse_control(self):
        # Posicion del Mouse
        mx, my = pygame.mouse.get_pos()
        # Si está cerca de los bordes, mueve el mouse al centro
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
  
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Triángulo Rectángulo Interactivo")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self, player):
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Capturar el movimiento del mouse en el eje X
        mouse_movement = pygame.mouse.get_rel()[0]

        # Rotar en sentido antihorario si el mouse se mueve a la izquierda,
        # y en sentido horario si se mueve a la derecha
        if mouse_movement < 0:
            player.rotate(1)
        elif mouse_movement > 0:
            player.rotate(-1)

        player.mouse_control()

    def draw(self, player):
        self.screen.fill(self.white)

        end_x = player.pos[0] + 100 * math.cos(math.radians(player.angle))
        end_y = player.pos[1] - 100 * math.sin(math.radians(player.angle))

        # Dibujar la línea roja (hipotenusa) con una longitud predeterminada
        hypotenuse_length = 100
        hypotenuse_x = player.pos[0] + hypotenuse_length * math.cos(math.radians(player.angle))
        hypotenuse_y = player.pos[1] - hypotenuse_length * math.sin(math.radians(player.angle))
        pygame.draw.line(self.screen, self.red, player.pos, (hypotenuse_x, hypotenuse_y))

        pygame.draw.line(self.screen, self.black, player.pos, (end_x, player.pos[1]))
        pygame.draw.line(self.screen, self.black, (end_x, player.pos[1]), (end_x, end_y))
        pygame.draw.circle(self.screen, self.black, player.pos, player.radius)

        angle_text = f"Ángulo: {player.angle:.1f} grados"
        font = pygame.font.Font(None, 36)
        text = font.render(angle_text, True, self.black)
        self.screen.blit(text, (10, 10))

        pygame.display.flip()

    def run(self):
        player = Player(self.width // 2, self.height // 2, 20, 5)

        running = True
        while running:
            running = self.handle_events()

            self.update(player)
            self.draw(player)

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    game = Game(800, 600)
    game.run()

