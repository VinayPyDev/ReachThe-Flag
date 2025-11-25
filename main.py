import pygame
import sys

pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reach The Flag")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

bg = pygame.transform.scale(pygame.image.load("Data/bg3.png").convert_alpha(), (1280, 720))
cursor = pygame.image.load("Data/cursor3.png").convert_alpha()
inventory_img = pygame.transform.scale(pygame.image.load("Data/inventory.png").convert_alpha(), (400, 400))
inventory_img_rect = pygame.Rect(875, 350, 400, 400)
bridge_img = pygame.image.load("Data/bridge.png").convert_alpha()
bridge_img2 = pygame.image.load("Data/bridge2.png").convert_alpha()
grass_img = pygame.image.load("Data/grass-1.png").convert_alpha()

b_front = pygame.image.load("Movement/Basic/B_Front.png").convert_alpha()
b_front_rect = b_front.get_rect(bottomright=(1000, 540))
b_back = pygame.image.load("Movement/Basic/B_Back.png").convert_alpha()
b_back_rect = b_back.get_rect(bottomright=(1200, 540))
b_left = pygame.image.load("Movement/Basic/B_Left.png").convert_alpha()
b_left_rect = b_left.get_rect(bottomright=(1000, 640))
b_right = pygame.image.load("Movement/Basic/B_Right.png").convert_alpha()
b_right_rect = b_right.get_rect(bottomright=(1200, 640))

placed_blocks = []
dragging = False
dragged_img = None
dragged_rect = None
direction = None

flag_img = pygame.transform.scale(pygame.image.load("Data/flag.png").convert_alpha(), (64, 64))
flag_placed = False
flag_pos = (432, 382)
flag_rect = flag_img.get_rect(center=flag_pos)

start_and_end_sound = pygame.mixer.Sound("Music/start.wav")
reach_sound = pygame.mixer.Sound("Music/Reach.wav")
place_sound = pygame.mixer.Sound("Music/place.wav")
quit_sound = pygame.mixer.Sound("Music/quit.wav")

level_1_track = pygame.mixer_music.load("Music/Sythum_edited.wav")
pygame.mixer_music.set_volume(0.5)

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    def update(self, screen):
        if self.image is None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def CheckForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    def ChangeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("Font/PixeloidSans-Bold.ttf", size)

def connect_with_bridge(s_rect, direction):
    global flag_placed, flag_pos
    under_grass = None
    for img, rect in placed_blocks:
        if img == grass_img and rect.collidepoint(s_rect.center):
            under_grass = rect
            break
    if not under_grass:
        return
    target_grass = None
    min_dist = float("inf")
    for img, rect in placed_blocks:
        if img == grass_img and rect != under_grass:
            dx = rect.centerx - under_grass.centerx
            dy = rect.centery - under_grass.centery
            if direction == "front" and abs(dx) < 20 and dy < -50 and abs(dy) < min_dist:
                min_dist = abs(dy)
                target_grass = rect
            elif direction == "back" and abs(dx) < 20 and dy > 50 and dy < min_dist:
                min_dist = dy
                target_grass = rect
            elif direction == "left" and abs(dy) < 20 and dx < -50 and abs(dx) < min_dist:
                min_dist = abs(dx)
                target_grass = rect
            elif direction == "right" and abs(dy) < 20 and dx > 50 and dx < min_dist:
                min_dist = dx
                target_grass = rect
    if not target_grass:
        return
    if direction in ("left", "right"):
        left = under_grass if under_grass.centerx < target_grass.centerx else target_grass
        right = target_grass if target_grass.centerx > under_grass.centerx else under_grass
        bridge_width = right.left - left.right
        if bridge_width > 10:
            bridge_surf = pygame.transform.scale(bridge_img2, (bridge_width, grass_img.get_height()))
            bridge_rect = bridge_surf.get_rect(topleft=(left.right, left.y))
            if target_grass.colliderect(flag_rect) or bridge_rect.colliderect(flag_rect):
                end_screen()
                reach_sound.play()
                pygame.mixer_music.stop()
            placed_blocks.append((bridge_surf, bridge_rect))
            place_sound.play()

    else:
        top = under_grass if under_grass.centery < target_grass.centery else target_grass
        bottom = target_grass if target_grass.centery > under_grass.centery else under_grass
        bridge_height = bottom.top - top.bottom
        if bridge_height > 10:
            bridge_surf = pygame.transform.scale(bridge_img, (grass_img.get_width(), bridge_height))
            bridge_rect = bridge_surf.get_rect(topleft=(top.x, top.bottom))
            if target_grass.colliderect(flag_rect) or bridge_rect.colliderect(flag_rect):
                end_screen()    
                reach_sound.play()
                pygame.mixer_music.stop()
            placed_blocks.append((bridge_surf, bridge_rect))
            place_sound.play()

def load_level():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(100, 200))),
        (grass_img, grass_img.get_rect(topleft=(250, 200))),
        (grass_img, grass_img.get_rect(topleft=(100, 350))),
        (grass_img, grass_img.get_rect(topleft=(100, 500))),
        (grass_img, grass_img.get_rect(topleft=(250, 350))),
        (grass_img, grass_img.get_rect(topleft=(400, 350))),
    ])
    final_grass = placed_blocks[-1][1]
    global flag_pos, flag_rect
    flag_pos = final_grass.center
    flag_rect.center = flag_pos

def play():
    global dragging, dragged_img, dragged_rect, direction, flag_rect
    while True:

        cursor_pos = pygame.mouse.get_pos()
        flag_rect.center = flag_pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_front_rect.collidepoint(event.pos):
                    dragging = True
                    dragged_img = b_front
                    dragged_rect = b_front.get_rect(center=event.pos)
                    direction = "front"
                elif b_back_rect.collidepoint(event.pos):
                    dragging = True
                    dragged_img = b_back
                    dragged_rect = b_back.get_rect(center=event.pos)
                    direction = "back"
                elif b_left_rect.collidepoint(event.pos):
                    dragging = True
                    dragged_img = b_left
                    dragged_rect = b_left.get_rect(center=event.pos)
                    direction = "left"
                elif b_right_rect.collidepoint(event.pos):
                    dragging = True
                    dragged_img = b_right
                    dragged_rect = b_right.get_rect(center=event.pos)
                    direction = "right"
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and dragged_img:
                    new_rect = dragged_img.get_rect(center=event.pos)
                    on_grass = any(img == grass_img and rect.collidepoint(new_rect.center) for img, rect in placed_blocks)
                    if on_grass:
                        connect_with_bridge(new_rect, direction)
                       
                dragging = False
                dragged_img = None
                dragged_rect = None
                direction = None
            elif event.type == pygame.MOUSEMOTION and dragging:
                dragged_rect.center = event.pos
        screen.blit(bg, (0, 0))
        screen.blit(inventory_img, inventory_img_rect)
        screen.blit(b_front, b_front_rect)
        screen.blit(b_back, b_back_rect)
        screen.blit(b_left, b_left_rect)
        screen.blit(b_right, b_right_rect)
        for img, rect in placed_blocks:
            screen.blit(img, rect)
        if dragging and dragged_img:
            screen.blit(dragged_img, dragged_rect)
        screen.blit(flag_img, flag_rect)
        screen.blit(cursor, cursor_pos)
        pygame.display.update()
        clock.tick(60)

def options():
    while True:
        screen.fill("black")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_TEXT = get_font(45).render("This is Made by VinayPyDev.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(75), base_color="Green", hovering_color="Green")
        OPTIONS_BACK.ChangeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)
        OPTIONS_MOUSE_IMG = pygame.image.load("Data/cursor3.png").convert_alpha()
        screen.blit(OPTIONS_MOUSE_IMG, OPTIONS_MOUSE_POS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.CheckForInput(OPTIONS_MOUSE_POS):
                    start_and_end_sound.play()
                    main_menu()
        pygame.display.update()

def end_screen():
    while True:

        END_TEXT = get_font(90).render("LEVEL COMPLETE!", True, "black")
        END_RECT = END_TEXT.get_rect(center=(640, 200))
        screen.blit(END_TEXT, END_RECT)

        BACK_TO_MENU = Button(image=None, pos=(640, 460), text_input="MENU",
                              font=get_font(75), base_color="Green", hovering_color="#84FF84")
        BACK_TO_MENU.ChangeColor(pygame.mouse.get_pos())
        BACK_TO_MENU.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_TO_MENU.CheckForInput(pygame.mouse.get_pos()):
                    return
                
        pygame.display.update()

def main_menu():
    while True:
        screen.fill((40, 40, 40))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("REACH THE FLAG", True, "#ff3300")
        MENU_RECT = MENU_TEXT.get_rect(topleft=(30, 50))
        PLAY_BUTTON = Button(image=pygame.image.load("Data/Play Rect.png"), pos=(150, 250), text_input="PLAY", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Data/Options Rect.png"), pos=(230, 400), text_input="OPTIONS", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")
        QUIT_BUTTON = Button(image=pygame.image.load("Data/Quit Rect.png"), pos=(140, 550), text_input="QUIT", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")
        screen.blit(MENU_TEXT, MENU_RECT)
        MENU_MOUSE_IMG = pygame.image.load("Data/cursor3.png").convert_alpha()
        screen.blit(MENU_MOUSE_IMG, MENU_MOUSE_POS)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.ChangeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    start_and_end_sound.play()
                    pygame.mixer_music.play()
                    play()
                if OPTIONS_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    start_and_end_sound.play()
                    options()
                if QUIT_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    quit_sound.play(100)
                    pygame.time.wait()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

load_level()
main_menu()