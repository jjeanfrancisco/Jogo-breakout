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

    # Variáveis de controle do jogo
    clock = pygame.time.Clock()
    running = True
    game_over = False
    paused = False

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

            if not game_over:
                all_sprites.update()

                if pygame.sprite.spritecollide(paddle, ball_group, False):
                    ball.speed_y = -ball.speed_y
                    random.choice(bounce_sounds).play()

                blocks_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
                for block in blocks_hit_list:
                    ball.speed_y = -ball.speed_y
                    hit_sound.play()

                if ball.rect.y > SCREEN_HEIGHT:
                    game_over = True

                screen.fill(BLACK)
                all_sprites.draw(screen)
            else:
                font = pygame.font.SysFont("Arial", 36)
                text = font.render("Game Over", True, WHITE)
                screen.blit(text, [SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2])

                restart_font = pygame.font.SysFont("Arial", 24)
                restart_text = restart_font.render("Clique para reiniciar ou", True, WHITE)
                screen.blit(restart_text, [SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 40])
                if draw_button("Voltar ao Menu", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 50, GREEN, BLUE):
                    show_start_screen()
                    main()

        if paused:
            font = pygame.font.SysFont("Arial", 36)
            paused_text = font.render("Jogo Pausado", True, WHITE)
            screen.blit(paused_text, [SCREEN_WIDTH // 2 - paused_text.get_width() // 2, SCREEN_HEIGHT // 2])

        if draw_button("Sair", SCREEN_WIDTH - 110, 10, 100, 50, RED, BLUE):
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Mostrar a tela inicial
show_start_screen()

# Iniciar o jogo
main()
