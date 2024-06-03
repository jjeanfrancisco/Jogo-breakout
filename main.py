import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GRAY = (169, 169, 169)

# Definir tamanhos da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definir tamanho dos blocos
BLOCK_WIDTH = 75
BLOCK_HEIGHT = 20

# Definir tamanho da raquete
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

# Definir tamanho da bola
BALL_SIZE = 10

# Criar a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Carregar sons
bounce_sounds = [
    pygame.mixer.Sound("bounce1.mp3"),
    pygame.mixer.Sound("bounce2.mp3"),
    pygame.mixer.Sound("bounce3.mp3")
]
hit_sound = pygame.mixer.Sound("hit.mp3")
background_music = "background.mp3"
universe_sound = pygame.mixer.Sound("universe.mp3")

# Carregar imagem de fundo
background_image = pygame.image.load("blackhole.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar imagens dos braços
arm_slim_image = pygame.image.load("arm_slim.jpg")
arm_slim_image = pygame.transform.scale(arm_slim_image, (200, 400))
arm_muscular_image = pygame.image.load("arm_muscular.png")
arm_muscular_image = pygame.transform.scale(arm_muscular_image, (200, 400))

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - (PADDLE_WIDTH // 2)
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_SIZE:
            self.speed_x = -self.speed_x
            random.choice(bounce_sounds).play()
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y
            random.choice(bounce_sounds).play()

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Portal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - 50
        self.rect.y = (SCREEN_HEIGHT // 2) - 50

def create_blocks():
    blocks = pygame.sprite.Group()
    colors = [GRAY, RED, BLUE, YELLOW, PURPLE, GREEN]
    for row in range(6):
        for column in range(10):
            block = Block(colors[row], column * (BLOCK_WIDTH + 2) + 1, row * (BLOCK_HEIGHT + 2) + 1)
            blocks.add(block)
    return blocks

def draw_button(text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.SysFont("Arial", 24)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
    return False

def show_start_screen():
    # Carregar imagem de fundo
    background_image = pygame.image.load("doom.jpg")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Carregar e reproduzir música de fundo
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

    while True:
        screen.blit(background_image, [0, 0])
        font = pygame.font.SysFont("Arial", 48)
        title_text = font.render("Breakout Game", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

        if draw_button("Iniciar", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50, GREEN, BLUE):
            pygame.mixer.music.stop()
            return

        if draw_button("Sair", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60, 100, 50, RED, BLUE):
            pygame.quit()
            quit()

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def next_level():
    # Tela preta e som do universo
    screen.fill(BLACK)
    pygame.display.flip()
    universe_sound.play()
    pygame.time.wait(5000)  # Espera 5 segundos
    universe_sound.stop()
    show_arm_screen()

def show_arm_screen():
    arm_rect = arm_slim_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    clicks = 0
    arm_image = arm_slim_image

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if arm_rect.collidepoint(event.pos):
                    clicks += 1
                    if clicks >= 3:
                        arm_image = arm_muscular_image

        screen.fill(BLACK)
        screen.blit(arm_image, arm_rect)
        pygame.display.flip()

        if clicks >= 3 and pygame.mouse.get_pressed()[0] == 0:
            pygame.time.wait(2000)
            running = False

def main():
    all_sprites = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()

    # Criar raquete
    paddle = Paddle()
    all_sprites.add(paddle)

    # Criar bola
    ball = Ball()
    all_sprites.add(ball)
    ball_group.add(ball)

    # Criar blocos
    blocks = create_blocks()
    all_sprites.add(blocks)

    # Criar portal
    portal = Portal()
    all_sprites.add(portal)

    # Variáveis de controle do jogo
    clock = pygame.time.Clock()
    running = True
    game_over = False
    paused = False

    # Variáveis para detectar giros do mouse
    previous_mouse_pos = pygame.mouse.get_pos()
    center_mouse_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    spins = 0
    clockwise = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if draw_button("Voltar ao Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50, GREEN, BLUE):
                    show_start_screen()
                    main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.speed_x = -6
            elif keys[pygame.K_RIGHT]:
                paddle.speed_x = 6
            else:
                paddle.speed_x = 0

            all_sprites.update()

            # Colisões entre a bola e a raquete
            if pygame.sprite.spritecollide(paddle, ball_group, False):
                ball.speed_y = -ball.speed_y
                hit_sound.play()

            # Colisões entre a bola e os blocos
            block_collisions = pygame.sprite.spritecollide(ball, blocks, True)
            if block_collisions:
                ball.speed_y = -ball.speed_y
                hit_sound.play()

            # Verificar se a bola caiu
            if ball.rect.y >= SCREEN_HEIGHT:
                game_over = True

            # Verificar colisão com o portal
            if pygame.sprite.collide_rect(ball, portal):
                ball.rect.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
                ball.rect.y = random.randint(0, SCREEN_HEIGHT - BALL_SIZE)
                ball.speed_x = random.choice([-4, 4])
                ball.speed_y = -4

            # Verificar giros do mouse
            current_mouse_pos = pygame.mouse.get_pos()
            if previous_mouse_pos != current_mouse_pos:
                current_direction = (current_mouse_pos[0] - center_mouse_pos[0], current_mouse_pos[1] - center_mouse_pos[1])
                if previous_mouse_pos == center_mouse_pos:
                    previous_direction = current_direction
                else:
                    if current_direction[0] > 0 and previous_direction[0] <= 0:
                        if clockwise is None or clockwise:
                            spins += 1
                            clockwise = True
                        else:
                            spins = 1
                            clockwise = True
                    elif current_direction[0] < 0 and previous_direction[0] >= 0:
                        if clockwise is None or not clockwise:
                            spins += 1
                            clockwise = False
                        else:
                            spins = 1
                            clockwise = False
                previous_direction = current_direction
                previous_mouse_pos = current_mouse_pos

                if spins >= 7:
                    # Transitar para a próxima fase
                    next_level()
                    spins = 0  # Reset spins count
                    # Reset the game objects for the new level
                    all_sprites.empty()
                    ball_group.empty()
                    paddle = Paddle()
                    ball = Ball()
                    all_sprites.add(paddle, ball)
                    ball_group.add(ball)
                    blocks = create_blocks()
                    all_sprites.add(blocks)
                    portal = Portal()
                    all_sprites.add(portal)

            screen.blit(background_image, [0, 0])  # Desenhar imagem de fundo
            all_sprites.draw(screen)

            if game_over:
                font = pygame.font.SysFont("Arial", 48)
                game_over_text = font.render("Game Over", True, RED)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
                draw_button("Voltar ao Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50, GREEN, BLUE)

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    show_start_screen()
    main()
