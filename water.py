import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sparse Vertical Water Stream")

clock = pygame.time.Clock()

# Stream parameters
stream_x = WIDTH // 2
stream_top = 50
stream_bottom = HEIGHT - 50
stream_thickness = 20

# Particles: [x, y, radius, lifetime, dx]
particle_list = []

frame_count = 0

def draw_water():
    pygame.draw.line(screen, (0, 100, 255), (stream_x, stream_top), (stream_x, stream_bottom), stream_thickness)

def generate_particles():
    global frame_count
    frame_count += 1
    # only generate particles every 10 frames (≈0.16 sec at 60 FPS)
    if frame_count % 10 == 0:
        y = random.randint(stream_top, stream_bottom)
        # left particle
        particle_list.append([stream_x, y, random.randint(2,3), 60, random.uniform(-1.5, -0.5)])
        # right particle
        particle_list.append([stream_x, y, random.randint(2,3), 60, random.uniform(0.5, 1.5)])

def draw_particles():
    for particle in particle_list[:]:
        x, y, r, lifetime, dx = particle
        pygame.draw.circle(screen, (0, 150, 255), (int(x), int(y)), r)
        particle[0] += dx
        particle[1] += 1  # slight downward drift
        particle[3] -= 1
        if particle[3] <= 0:
            particle_list.remove(particle)

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_water()
    generate_particles()
    draw_particles()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()