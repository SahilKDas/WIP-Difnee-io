import pygame
from pygame.locals import *

pygame.init()

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 3, 0, 0, 7, 0, 0, 0, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 7, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

tile_size = 48
screen_width = tile_size * len(world_data[0])
screen_height = tile_size * len(world_data)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('DifneeIO')

pygame.mixer.music.load('assets/music/retroindiejosh_air.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

class Player():
    def __init__(self, x, y):
        self.index = 0
        self.counter = 0
        self.image_right = pygame.image.load('assets/player.svg')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 5

        # get keypresses
        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]) and not self.jumped:
            self.vel_y = -20  # Increased jump power
            self.jumped = True
        if not (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]):
            self.jumped = False
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 5
            self.counter += 1
            self.direction = -1
            self.image = self.image_left
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 5
            self.counter += 1
            self.direction = 1
            self.image = self.image_right

        # handle animation
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1

        # add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class Enemy():
    def __init__(self, x, y):
        self.index = 0
        self.counter = 0
        self.image_right = pygame.image.load('assets/enemy.svg')
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.speed = 3 #speed for the enemy
        self.gravity = 0.25  # Adjust gravity if needed
        self.jump_power = -20  #jump power for the enemy

    def update(self, player):
        dx = 0
        dy = 0

        # move towards player
        if self.rect.x < player.rect.x:
            dx = self.speed
            self.image = self.image_right
        elif self.rect.x > player.rect.x:
            dx = -self.speed
            self.image = self.image_left

        # Check if the player is above the enemy
        if player.rect.y < self.rect.y and not self.jumped:
            self.vel_y = self.jump_power  # Set jump power
            self.jumped = True

        # add gravity
        self.vel_y += self.gravity
        if self.vel_y > 15:  # Adjust max gravity if needed
            self.vel_y = 15
        dy += self.vel_y

        # check for collision
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumped = False  # Reset jump status when touching the ground

        self.rect.x += dx
        self.rect.y += dy

        # draw enemy onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        grass_img = pygame.image.load('assets/Grass.png')
        leaf_img = pygame.image.load('assets/Leaf.png')
        brick_img = pygame.image.load('assets/Brick.png')
        coin_img = pygame.image.load('assets/Coin.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    img = pygame.transform.scale(leaf_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(brick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(coin_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def update(self, player):
        if hasattr(self, 'enemy_clone'):
            self.enemy_clone.update(player)

player = Player(100, screen_height - 130)
enemy = Enemy(200, screen_height - 130)
world = World(world_data)

run = True
while run:
    bg_img = pygame.image.load('assets/background/Forest_Background.png')
    scaled_image = pygame.transform.scale(bg_img, screen.get_size())
    screen.blit(scaled_image, (0, 0))

    world.draw()
    player.update()
    enemy.update(player)
    world.update(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
