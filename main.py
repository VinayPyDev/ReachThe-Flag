import pygame
import sys
import math

pygame.init()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Reach The Flag")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

Active = 1
Inactive = 0

bg = pygame.transform.scale(pygame.image.load("Data/bg3.png").convert_alpha(), (1280, 720))
cursor = pygame.image.load("Data/cursor3.png").convert_alpha()
inventory_img = pygame.transform.scale(pygame.image.load("Data/inventory.png").convert_alpha(), (400, 500))
inventory_img_rect = pygame.Rect(875, 260, 400, 500)
bridge_img = pygame.image.load("Data/bridge.png").convert_alpha()   
bridge_img2 = pygame.image.load("Data/bridge2.png").convert_alpha() 
grass_img = pygame.image.load("Data/grass-1.png").convert_alpha()

Inactive_grass = grass_img.copy()
Inactive_grass.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_MULT)

def grass_active(block):
    return len(block) == 3 and block[0] == grass_img

def SetGrassState(rect, add_state):
    for i, block in enumerate(placed_blocks):
        if grass_active(block):
            img, r, state = block
            if r == rect:
                placed_blocks[i] = (img, r, add_state)

b_front = pygame.image.load("Movement/Basic/B_Front.png").convert_alpha()
b_back = pygame.image.load("Movement/Basic/B_Back.png").convert_alpha()
b_left = pygame.image.load("Movement/Basic/B_Left.png").convert_alpha()
b_right = pygame.image.load("Movement/Basic/B_Right.png").convert_alpha()

m_front_2 = pygame.image.load("Movement/Multipliers/M_Front_2.png").convert_alpha()
m_front_3 = pygame.image.load("Movement/Multipliers/M_Front_3.png").convert_alpha()
m_front_4 = pygame.image.load("Movement/Multipliers/M_Front_4.png").convert_alpha()

m_back_2 = pygame.image.load("Movement/Multipliers/M_Back_2.png").convert_alpha()
m_back_3 = pygame.image.load("Movement/Multipliers/M_Back_3.png").convert_alpha()
m_back_4 = pygame.image.load("Movement/Multipliers/M_Back_4.png").convert_alpha()

m_left_2 = pygame.image.load("Movement/Multipliers/M_Left_2.png").convert_alpha()
m_left_3 = pygame.image.load("Movement/Multipliers/M_Left_3.png").convert_alpha()
m_left_4 = pygame.image.load("Movement/Multipliers/M_Left_4.png").convert_alpha()

m_right_2 = pygame.image.load("Movement/Multipliers/M_Right_2.png").convert_alpha()
m_right_3 = pygame.image.load("Movement/Multipliers/M_Right_3.png").convert_alpha()
m_right_4 = pygame.image.load("Movement/Multipliers/M_Right_4.png").convert_alpha()

cw_rotator_25 = pygame.image.load("Movement/Rotators/cw_rotator_25.png").convert_alpha()
cw_rotator_50 = pygame.image.load("Movement/Rotators/cw_rotator_50.png").convert_alpha()
cw_rotator_75 = pygame.transform.scale(pygame.image.load("Movement/Rotators/cw_rotator_75.png").convert_alpha(), (64, 64))

replay_btn = pygame.image.load("Data/replay_btn2.png").convert_alpha()
replay_btn_rect = replay_btn.get_rect(center=(1230, 50))

pause_btn = pygame.image.load("Data/pause_btn.png").convert_alpha()
pause_btn_rect = pause_btn.get_rect(center=(1080, 50))
paused = False

placed_blocks = []               
dragging = False
direction = None

current_inventory = []            
inventory_item_rects = []         
selected_item_idx = None          
selected_item_id = None

flag_img = pygame.transform.scale(pygame.image.load("Data/flag.png").convert_alpha(), (64, 64))
flag_placed = False
flag_pos = (432, 382)
flag_rect = flag_img.get_rect(center=flag_pos)

final_grass_tile = None

start_and_end_sound = pygame.mixer.Sound("Music/start.wav")
reach_sound = pygame.mixer.Sound("Music/Reach.wav")
place_sound = pygame.mixer.Sound("Music/place.wav")
quit_sound = pygame.mixer.Sound("Music/quit.wav")

current_level = 1
max_level = 12

ICON_SIZE = 54

TILE = 150

CwRotator = {25: (TILE, TILE), 50: (0, TILE * 2), 75: (-TILE, TILE)}

def stop_level_tracks():
    pygame.mixer.music.stop()

def menu_track():
    pygame.mixer.music.load("Music/Calm Wind.wav")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)

def level_1_track():
    pygame.mixer.music.load("Music/Sythum_edited.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def level_2_track():
    pygame.mixer.music.load("Music/Mocker.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_3_track():
    pygame.mixer.music.load("Music/Kick 3.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_4_track():
    pygame.mixer.music.load("Music/Shining Smiles.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_5_track():
    pygame.mixer.music.load("Music/Leviathan's Tale.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_6_track():
    pygame.mixer.music.load("Music/Chase on Cliff.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_7_track():
    pygame.mixer.music.load("Music/Yes, I am Insane.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def level_8_track():
    pygame.mixer.music.load("Music/Silent Sorrow.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

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

    def update(self, screen, draw_image=True):
        if draw_image and self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def CheckForInput(self, position):
        return position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)
    
    def ChangeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("Font/PixeloidSans-Bold.ttf", size)

def layout_inventory():
    global inventory_item_rects
    inventory_item_rects = []

    n = len(current_inventory)
    if n == 0:
        return

    cols = 4
    rows = math.ceil(n / cols)

    INNER_LEFT   = 32
    INNER_RIGHT  = 32
    INNER_TOP    = 48
    INNER_BOTTOM = 32

    ICON = 58
    GAP = 8  

    usable_w = inventory_img_rect.width - INNER_LEFT - INNER_RIGHT
    usable_h = inventory_img_rect.height - INNER_TOP - INNER_BOTTOM

    grid_w = cols * ICON + (cols - 1) * GAP
    grid_h = rows * ICON + (rows - 1) * GAP

    start_x = inventory_img_rect.left + INNER_LEFT + (usable_w - grid_w) // 2
    start_y = inventory_img_rect.top + INNER_TOP + (usable_h - grid_h) // 2

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break

            x = start_x + c * (ICON + GAP)
            y = start_y + r * (ICON + GAP)

            inventory_item_rects.append(
                pygame.Rect(x, y, ICON, ICON)
            )
            idx += 1

def connect_with_bridge(s_rect, direction):
    global final_grass_tile, current_level
    under_grass = None
    for block in placed_blocks:
        if grass_active(block):
            img, rect, state = block
            if state == Active and rect.collidepoint(s_rect.center):
                under_grass = rect
                break
    if not under_grass:
        return
    target_grass = None
    min_dist = float("inf")
    for block in placed_blocks:
            if not grass_active(block):
                continue

            img, rect, state = block
            if rect == under_grass:
                continue

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
    place_bridge_between(under_grass, target_grass)

def place_bridge_between(under_rect, target_rect):
    if abs(under_rect.centery - target_rect.centery) < 10:
        left = under_rect if under_rect.centerx < target_rect.centerx else target_rect
        right = target_rect if target_rect.centerx > under_rect.centerx else under_rect
        bridge_width = right.left - left.right
        if bridge_width > 10:
            bridge_surf = pygame.transform.scale(bridge_img2, (bridge_width, grass_img.get_height()))
            bridge_rect = bridge_surf.get_rect(topleft=(left.right, left.y))
            placed_blocks.append((bridge_surf, bridge_rect))
            place_sound.play()
            if target_rect and target_rect != under_rect:
                SetGrassState(under_rect, Inactive)
                SetGrassState(target_rect, Active)

            if left == final_grass_tile or right == final_grass_tile:
                reach_sound.play()
                next_level()
    else:
        top = under_rect if under_rect.centery < target_rect.centery else target_rect
        bottom = target_rect if target_rect.centery > under_rect.centery else under_rect
        bridge_height = bottom.top - top.bottom
        if bridge_height > 10:
            bridge_surf = pygame.transform.scale(bridge_img, (grass_img.get_width(), bridge_height))
            bridge_rect = bridge_surf.get_rect(topleft=(top.x, top.bottom))
            placed_blocks.append((bridge_surf, bridge_rect))
            place_sound.play()
            if target_rect and target_rect != under_rect:
                SetGrassState(under_rect, Inactive)
                SetGrassState(target_rect, Active)

            if top == final_grass_tile or bottom == final_grass_tile:
                reach_sound.play()
                next_level()

def place_multiplier_bridges(under_grass_rect, direction, count):
    
    start = under_grass_rect
    tolerance = max(grass_img.get_width(), grass_img.get_height()) // 2 

    for _ in range(count):
        candidate = None
        best_dist = float("inf")

        for block in placed_blocks:
            if not grass_active(block):
                continue

            img, rect, state = block
            if rect == start:
                continue

            dx = rect.centerx - start.centerx
            dy = rect.centery - start.centery

            if direction == "front":
                if dy < -10 and abs(dx) < tolerance:
                    dist = abs(dy)
                    if dist < best_dist:
                        best_dist = dist
                        candidate = rect
            elif direction == "back":
                if dy > 10 and abs(dx) < tolerance:
                    dist = dy
                    if dist < best_dist:
                        best_dist = dist
                        candidate = rect
            elif direction == "left":
                if dx < -10 and abs(dy) < tolerance:
                    dist = abs(dx)
                    if dist < best_dist:
                        best_dist = dist
                        candidate = rect
            elif direction == "right":
                if dx > 10 and abs(dy) < tolerance:
                    dist = dx
                    if dist < best_dist:
                        best_dist = dist
                        candidate = rect

        if candidate is None:
            break

        place_bridge_between(start, candidate)

        start = candidate

def RotateActiveBlock(percentage):
    global placed_blocks, flag_rect

    new_blocks = []

    for block in placed_blocks:
        if len(block) == 3:
            img, rect, state = block

            if state == Active:
                cx, cy = rect.center
                x, y = rect.center

                rel_x = x - cx
                rel_y = y - cy

                if percentage == 25:      
                    new_x = cx + rel_y
                    new_y = cy - rel_x
                elif percentage == 50:    
                    new_x = cx - rel_x
                    new_y = cy - rel_y
                elif percentage == 75:    
                    new_x = cx - rel_y
                    new_y = cy + rel_x
                else:
                    new_x, new_y = x, y

                new_rect = rect.copy()
                new_rect.center = (new_x, new_y)

                if rect.colliderect(flag_rect):
                    flag_rect.center = new_rect.center

                new_blocks.append((img, new_rect, state))
            else:
                new_blocks.append(block)
        else:
            new_blocks.append(block)

    placed_blocks[:] = new_blocks

def reset_level():
    global placed_blocks, dragging, dragged_img, dragged_rect, direction, selected_item_idx, selected_item_id
    placed_blocks = []
    dragging = False
    if 'dragged_img' in globals():
        del globals()['dragged_img']
    if 'dragged_rect' in globals():
        del globals()['dragged_rect']
    dragged_img = None
    dragged_rect = None
    direction = None
    selected_item_idx = None
    selected_item_id = None

def load_level_1():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(100, 200)), Active),
        (grass_img, grass_img.get_rect(topleft=(250, 200)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(100, 350)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(100, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(250, 350)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(400, 350)), Inactive),
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_2():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(200, 250)), Active),
        (grass_img, grass_img.get_rect(topleft=(500, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 550)), Inactive),
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_3():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(200, 250)), Active),
        (grass_img, grass_img.get_rect(topleft=(350, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 550)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_4():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(700, 250)), Active),
        (grass_img, grass_img.get_rect(topleft=(550, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(400, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(400, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(400, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(250, 550)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_5():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(200, 550)), Active),
        (grass_img, grass_img.get_rect(topleft=(200, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 250)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 550)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_6():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(500, 250)), Active),
        (grass_img, grass_img.get_rect(topleft=(500, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 550)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 400)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 250)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_7():
    placed_blocks.extend([
        (grass_img,grass_img.get_rect(topleft=(50, 50)), Active),
        (grass_img,grass_img.get_rect(topleft=(50, 200)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(50, 350)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(50, 500)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(200, 500)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(350, 500)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(500, 500)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(650, 500)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(650, 350)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(650, 200)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(650, 50)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(500, 50)), Inactive),
        (grass_img,grass_img.get_rect(topleft=(350, 50)), Inactive),
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_8():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(350, 200)), Active),
        (grass_img, grass_img.get_rect(topleft=(350, 350)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(200, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(50, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(50, 350)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(50, 200)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(50, 50)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_9():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(350, 50)), Active),
        (grass_img, grass_img.get_rect(topleft=(350, 150)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 450)), Inactive)    
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_10():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(200, 150)), Active),
        (grass_img, grass_img.get_rect(topleft=(200, 600)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(50, 600)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos    

def load_level_11():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(450, 150)), Active),
        (grass_img, grass_img.get_rect(topleft=(300, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(150, 300)), Inactive)
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def load_level_12():
    placed_blocks.extend([
        (grass_img, grass_img.get_rect(topleft=(50, 150)), Active),
        (grass_img, grass_img.get_rect(topleft=(50, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(350, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 300)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(500, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(650, 500)), Inactive),
        (grass_img, grass_img.get_rect(topleft=(800, 500)), Inactive),
    ])
    global final_grass_tile, flag_pos, flag_rect
    final_grass_tile = placed_blocks[-1][1]
    flag_pos = final_grass_tile.center
    flag_rect.center = flag_pos

def next_level():
    global current_level
    current_level += 1

    if current_level > max_level:
        stop_level_tracks()
        end_screen()
        return "END"

    reset_level()
    load_level(current_level)
    return "NEXT"

def check_level_completion():
    global current_level
    for block in placed_blocks:
        if len(block) == 2:
            img, rect = block
            if rect.colliderect(flag_rect):
                pygame.mixer.music.stop()
                reach_sound.play()
                result = next_level()
                return result
    return None

def Inventory_system(level):
    global current_inventory, inventory_item_rects

    current_inventory = []
    inventory_item_rects = []

    def add_item(item_id, surf):
        inv_surf = pygame.transform.smoothscale(surf, (ICON_SIZE, ICON_SIZE))
        current_inventory.append((item_id, inv_surf))

    if 1 <= level <= 4:
        add_item("front", b_front)
        add_item("back", b_back)
        add_item("left", b_left)
        add_item("right", b_right)

        add_item("front2", m_front_2)
        add_item("front3", m_front_3)
        add_item("front4", m_front_4)

        add_item("back2", m_back_2)
        add_item("back3", m_back_3)
        add_item("back4", m_back_4)

        add_item("left2", m_left_2)
        add_item("left3", m_left_3)
        add_item("left4", m_left_4)

        add_item("right2", m_right_2)
        add_item("right3", m_right_3)
        add_item("right4", m_right_4)

    elif 5 <= level <= 8:
        add_item("front2", m_front_2)
        add_item("front3", m_front_3)
        add_item("front4", m_front_4)

        add_item("back2", m_back_2)
        add_item("back3", m_back_3)
        add_item("back4", m_back_4)

        add_item("left2", m_left_2)
        add_item("left3", m_left_3)
        add_item("left4", m_left_4)

        add_item("right2", m_right_2)
        add_item("right3", m_right_3)
        add_item("right4", m_right_4)
    
    elif level == 9:
        add_item("rot_cw_25", cw_rotator_25)
        add_item("back", b_back)
        add_item("right", b_right)
        add_item("left", b_left)

    elif level == 10:
        add_item("rot_cw_50", cw_rotator_50)
        add_item("left", b_left)

    elif level == 11:
        add_item("rot_cw_75", cw_rotator_75)
        add_item("left", b_left)

    elif level == 12:
        add_item("rot_cw_50", cw_rotator_50)
        add_item("rot_cw_25", cw_rotator_25)
        add_item("right2", m_right_2)
        add_item("back3", m_back_3)

    layout_inventory()

def load_level(level):
    global placed_blocks, flag_pos, flag_rect

    placed_blocks = []

    Inventory_system(level)

    if level == 1:
        load_level_1()
        level_1_track()
    elif level == 2:
        load_level_2()
        level_2_track()
    elif level == 3:
        load_level_3()
        level_3_track()
    elif level == 4:
        load_level_4()
        level_4_track()
    elif level == 5:
        load_level_5()
        level_5_track()
    elif level == 6:
        load_level_6()
        level_6_track()
    elif level == 7:
        load_level_7()
        level_7_track()
    elif level == 8:
        load_level_8()
        level_8_track()
    elif level == 9:
        load_level_9()

    elif level == 10:
        load_level_10()

    elif level == 11:
        load_level_11()

    elif level == 12:
        load_level_12()


    flag_rect.center = flag_pos

def play():
    global dragging, direction, selected_item_idx, selected_item_id

    while True:
        cursor_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, (item_id, surf) in enumerate(current_inventory):
                    if idx >= len(inventory_item_rects):
                        continue
                    rect = inventory_item_rects[idx]
                    if rect.collidepoint(event.pos):
                        dragging = True
                        selected_item_idx = idx
                        selected_item_id = item_id
                        orig_map = {
                            "front": b_front, "back": b_back, "left": b_left, "right": b_right,
                            "front2": m_front_2, "front3": m_front_3, "front4": m_front_4,
                            "back2": m_back_2, "back3": m_back_3, "back4": m_back_4,
                            "left2": m_left_2, "left3": m_left_3, "left4": m_left_4,
                            "right2": m_right_2, "right3": m_right_3, "right4": m_right_4
                        }
                        source_surf = orig_map.get(item_id, surf)
                        globals()['dragged_img'] = source_surf
                        globals()['dragged_rect'] = source_surf.get_rect(center=event.pos)
                        if item_id.startswith("front"):
                            direction = "front"
                        elif item_id.startswith("back"):
                            direction = "back"
                        elif item_id.startswith("left"):
                            direction = "left"
                        elif item_id.startswith("right"):
                            direction = "right"
                        else:
                            direction = None
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and 'dragged_img' in globals() and selected_item_id is not None:
                    new_rect = globals()['dragged_img'].get_rect(center=event.pos)
                    under_grass = None
                    for block in placed_blocks:
                        if grass_active(block):
                            img, rect, state = block
                            if state == Active and rect.collidepoint(new_rect.center):
                                under_grass = rect
                                break

                    if selected_item_id.startswith("rot"):
                        try:
                            percentage = int(''.join(ch for ch in selected_item_id if ch.isdigit()))
                        except:
                            percentage = None
                        if percentage is not None:
                            RotateActiveBlock(percentage)

                            if selected_item_idx is not None and 0 <= selected_item_idx < len(current_inventory):
                                current_inventory.pop(selected_item_idx)
                                layout_inventory()
                    
                    elif under_grass and direction:
                        num = None
                        try:
                            num = int(''.join(ch for ch in selected_item_id if ch.isdigit()))
                        except:
                            num = None

                        if num is not None:
                            place_multiplier_bridges(under_grass, direction, num)
                            if selected_item_idx is not None and 0 <= selected_item_idx < len(current_inventory):
                                current_inventory.pop(selected_item_idx)
                                layout_inventory()
                        else:
                            connect_with_bridge(new_rect, direction)  

                dragging = False
                if 'dragged_img' in globals():
                    del globals()['dragged_img']
                if 'dragged_rect' in globals():
                    del globals()['dragged_rect']
                direction = None
                selected_item_idx = None
                selected_item_id = None

            elif event.type == pygame.MOUSEMOTION and dragging:
                if 'dragged_rect' in globals():
                    globals()['dragged_rect'].center = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_btn_rect.collidepoint(event.pos):
                    reset_level()
                    load_level(current_level)

        check_level_completion()

        screen.blit(bg, (0, 0))
        screen.blit(inventory_img, inventory_img_rect)

        level_text = get_font(64).render(f"Level {current_level}", True, "#161616")
        screen.blit(level_text, (10, 0))        

        screen.blit(replay_btn, replay_btn_rect)

        for idx, (item_id, surf) in enumerate(current_inventory):
            if idx < len(inventory_item_rects):
                rect = inventory_item_rects[idx]
                screen.blit(surf, rect)

        for block in placed_blocks:
            if grass_active(block):
                img, rect, state = block
                if state == Active:
                    screen.blit(grass_img, rect)
                else:
                    screen.blit(Inactive_grass, rect)

            else:
                img, rect = block
                screen.blit(img, rect)

        if dragging and 'dragged_img' in globals() and 'dragged_rect' in globals():
            screen.blit(globals()['dragged_img'], globals()['dragged_rect'])

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
        OPTIONS_BACK.update(screen, draw_image=False)
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
    end_screen_flag = pygame.transform.scale(flag_img, (100, 100))
    end_screen_flag_rect = end_screen_flag.get_rect(center=(640, 360))
    while True:
        screen.blit(bg, (0, 0))
        screen.blit(cursor, (pygame.mouse.get_pos()))
        screen.blit(end_screen_flag, end_screen_flag_rect)

        END_TEXT = get_font(75).render("LEVEL COMPLETE!", True, "black")
        END_RECT = END_TEXT.get_rect(center=(640, 170))
        screen.blit(END_TEXT, END_RECT)

        BACK_TO_MENU = Button(image=None, pos=(640, 575), text_input="MENU",
                              font=get_font(75), base_color="Green", hovering_color="#84FF84")
        BACK_TO_MENU.ChangeColor(pygame.mouse.get_pos())
        BACK_TO_MENU.update(screen, draw_image=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_TO_MENU.CheckForInput(pygame.mouse.get_pos()):
                    start_and_end_sound.play()
                    reset_level()
                    load_level_1()
                    main_menu()
                    return
        pygame.display.update()

def main_menu():
    menu_track()

    while True:
        screen.fill((40, 40, 40))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("REACH THE FLAG", True, "#ff3300")
        MENU_RECT = MENU_TEXT.get_rect(topleft=(30, 50))

        CREATOR_TITLE = get_font(60).render("VinayPyDev", True, "#d3d3d3")
        CREATOR_TITLE_RECT = CREATOR_TITLE.get_rect(topleft=(800, 640))

        PLAY_BUTTON = Button(image=None, pos=(150, 250), text_input="PLAY", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")
        OPTIONS_BUTTON = Button(image=None, pos=(230, 400), text_input="OPTIONS", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")
        QUIT_BUTTON = Button(image=None, pos=(140, 550), text_input="QUIT", font=get_font(75), base_color="#FBFF00", hovering_color="#EBEBEB")

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(CREATOR_TITLE, CREATOR_TITLE_RECT)
        MENU_MOUSE_IMG = pygame.image.load("Data/cursor3.png").convert_alpha()
        screen.blit(MENU_MOUSE_IMG, MENU_MOUSE_POS)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.ChangeColor(MENU_MOUSE_POS)
            button.update(screen, draw_image=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    global current_level
                    menu_track()
                    current_level = 1
                    start_and_end_sound.play()
                    load_level(1)
                    play()
                if OPTIONS_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    start_and_end_sound.play()
                    options()
                if QUIT_BUTTON.CheckForInput(MENU_MOUSE_POS):
                    quit_sound.play()
                    pygame.time.wait(100)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

load_level(1)
main_menu()