import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS = [RED, BLUE, GREEN, YELLOW]

# Game constants
GRID_SIZE = 40
BUBBLE_RADIUS = 20
CANNON_WIDTH = 50
CANNON_HEIGHT = 20
CANNON_SPEED = 10
BULLET_RADIUS = 5  # Adjusted bullet size
BUBBLE_SPAWN_RATE = 60  # Spawn a new bubble every 60 frames (2 seconds at 30 FPS)
MAX_BUBBLES = 100  # Maximum number of bubbles on screen

# Game objects
class Cannon:
    def __init__(self):
        self.position = [WIDTH // 2, HEIGHT - 50]
        self.angle = 0
        self.color = BLUE

    def update_angle(self, mouse_pos):
        self.angle = math.atan2(self.position[1] - mouse_pos[1], mouse_pos[0] - self.position[0])

    def shoot(self):
        return Bullet(self.position.copy(), self.angle, random.choice(COLORS))

    def draw(self, surface):
        cannon_end = (self.position[0] + CANNON_WIDTH * math.cos(self.angle),
                      self.position[1] - CANNON_WIDTH * math.sin(self.angle))
        pygame.draw.rect(surface, self.color, (*self.position, CANNON_WIDTH, CANNON_HEIGHT))
        pygame.draw.line(surface, self.color, self.position, cannon_end, 5)

class Bullet:
    def __init__(self, start_position, angle, color):
        self.position = start_position
        self.angle = angle
        self.color = color
        self.speed = CANNON_SPEED * 2  # Increased speed for smaller bullets

    def move(self):
        self.position[0] += self.speed * math.cos(self.angle)
        self.position[1] -= self.speed * math.sin(self.angle)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), BULLET_RADIUS)

class Bubble:
    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.radius = BUBBLE_RADIUS
        self.speed = 2

    def move(self):
        self.position[1] += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

def create_bubbles(num_bubbles):
    bubbles = []
    for _ in range(num_bubbles):
        x = random.randint(BUBBLE_RADIUS, WIDTH - BUBBLE_RADIUS)
        y = random.randint(-HEIGHT, 0)
        color = random.choice(COLORS)
        bubbles.append(Bubble([x, y], color))
    return bubbles

def respawn_bubble():
    x = random.randint(BUBBLE_RADIUS, WIDTH - BUBBLE_RADIUS)
    y = random.randint(-HEIGHT, 0)
    color = random.choice(COLORS)
    return Bubble([x, y], color)

def main():
    clock = pygame.time.Clock()
    cannon = Cannon()
    bullets = []
    bubbles = create_bubbles(10)  # Initial creation of 10 bubbles
    score = 0
    frames_since_last_spawn = 0  # Counter to track frames for bubble spawning

    running = True
    while running:
        try:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    bullets.append(cannon.shoot())

            mouse_pos = pygame.mouse.get_pos()
            cannon.update_angle(mouse_pos)

            for bullet in bullets[:]:
                bullet.move()
                bullet.draw(screen)
                if bullet.position[1] < -BULLET_RADIUS:
                    bullets.remove(bullet)

            for bubble in bubbles[:]:
                bubble.move()
                bubble.draw(screen)
                if bubble.position[1] > HEIGHT + BUBBLE_RADIUS:
                    bubbles.remove(bubble)

            # Increment the frame counter and spawn a new bubble if enough frames have passed
            frames_since_last_spawn += 1
            if frames_since_last_spawn >= BUBBLE_SPAWN_RATE and len(bubbles) < MAX_BUBBLES:
                bubbles.append(respawn_bubble())
                frames_since_last_spawn = 0

            for bullet in bullets[:]:
                for bubble in bubbles[:]:
                    if math.sqrt((bullet.position[0] - bubble.position[0]) ** 2 + (bullet.position[1] - bubble.position[1]) ** 2) < BUBBLE_RADIUS + BULLET_RADIUS:
                        bullets.remove(bullet)
                        bubbles.remove(bubble)
                        score += 1

            cannon.draw(screen)

            # Display score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(30)

        except Exception as e:
            print(f"An error occurred: {e}")
            running = False

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e
