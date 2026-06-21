import pygame
import random
import math
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Set

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
COLOR_SKY = (135, 206, 235)
COLOR_GROUND = (34, 139, 34)
COLOR_DIRT = (139, 69, 19)
COLOR_STONE = (128, 128, 128)
COLOR_SAND = (238, 214, 175)
COLOR_WOOD = (139, 69, 19)
COLOR_LEAVES = (34, 177, 76)
COLOR_WATER = (64, 164, 223)
COLOR_PLAYER = (255, 100, 100)
COLOR_MOB = (50, 150, 50)
COLOR_TEXT = (0, 0, 0)
COLOR_HUD_BG = (50, 50, 50)
COLOR_HUD_TEXT = (255, 255, 255)

# Block types
class BlockType(Enum):
    AIR = 0
    STONE = 1
    DIRT = 2
    GRASS = 3
    SAND = 4
    WATER = 5
    WOOD = 6
    LEAVES = 7

@dataclass
class Block:
    x: int
    y: int
    block_type: BlockType
    metadata: int = 0

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.health = 20
        self.max_health = 20
        self.hunger = 20
        self.max_hunger = 20
        self.inventory = {BlockType.DIRT: 64, BlockType.STONE: 32, BlockType.WOOD: 16}
        self.selected_block = BlockType.DIRT
        self.exp_level = 0
        self.exp_points = 0

    def update(self, blocks: List[Block], gravity: float = 0.6):
        # Apply gravity
        self.velocity_y += gravity
        
        # Move horizontally
        self.x += self.velocity_x
        self.velocity_x *= 0.9  # Friction
        
        # Check collisions and move vertically
        self.y += self.velocity_y
        
        # Simple ground collision
        if self.y + self.height >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - self.height
            self.velocity_y = 0
            self.is_jumping = False
        
        # Keep player in bounds
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

    def move_left(self):
        self.velocity_x = -5

    def move_right(self):
        self.velocity_x = 5

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLOR_PLAYER, (self.x, self.y, self.width, self.height))
        # Draw eyes
        pygame.draw.circle(screen, COLOR_TEXT, (int(self.x + 7), int(self.y + 8)), 2)
        pygame.draw.circle(screen, COLOR_TEXT, (int(self.x + 13), int(self.y + 8)), 2)

    def draw_hud(self, screen: pygame.Surface, font: pygame.font.Font):
        # Draw HUD background
        pygame.draw.rect(screen, COLOR_HUD_BG, (10, 10, 300, 120))
        
        # Draw health
        health_text = font.render(f"Health: {self.health}/{self.max_health}", True, COLOR_HUD_TEXT)
        screen.blit(health_text, (20, 20))
        pygame.draw.rect(screen, (255, 0, 0), (20, 40, self.health * 4, 10))
        pygame.draw.rect(screen, COLOR_TEXT, (20, 40, self.max_health * 4, 10), 2)
        
        # Draw hunger
        hunger_text = font.render(f"Hunger: {self.hunger}/{self.max_hunger}", True, COLOR_HUD_TEXT)
        screen.blit(hunger_text, (20, 60))
        pygame.draw.rect(screen, (255, 165, 0), (20, 80, self.hunger * 4, 10))
        pygame.draw.rect(screen, COLOR_TEXT, (20, 80, self.max_hunger * 4, 10), 2)
        
        # Draw experience
        exp_text = font.render(f"Level: {self.exp_level} XP: {self.exp_points}", True, COLOR_HUD_TEXT)
        screen.blit(exp_text, (20, 100))

class Mob:
    def __init__(self, x: float, y: float, mob_type: str = "zombie"):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 24
        self.velocity_x = 0
        self.velocity_y = 0
        self.mob_type = mob_type
        self.health = 20
        self.max_health = 20
        self.speed = random.uniform(1, 2)
        self.direction = random.choice([-1, 1])
        self.animation_frame = 0

    def update(self, player: Player, gravity: float = 0.6):
        # Apply gravity
        self.velocity_y += gravity
        self.y += self.velocity_y
        
        # Ground collision
        if self.y + self.height >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - self.height
            self.velocity_y = 0
        
        # AI: Chase player if nearby
        distance = abs(self.x - player.x)
        if distance < 150:
            if self.x < player.x:
                self.direction = 1
            else:
                self.direction = -1
        
        self.x += self.direction * self.speed
        
        # Boundary wrap
        if self.x < -20:
            self.x = SCREEN_WIDTH
        if self.x > SCREEN_WIDTH:
            self.x = -20
        
        self.animation_frame += 0.1

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, COLOR_MOB, (self.x, self.y, self.width, self.height))
        # Draw eyes
        pygame.draw.circle(screen, COLOR_TEXT, (int(self.x + 5), int(self.y + 6)), 1)
        pygame.draw.circle(screen, COLOR_TEXT, (int(self.x + 11), int(self.y + 6)), 1)

class World:
    def __init__(self):
        self.blocks: List[Block] = []
        self.mobs: List[Mob] = []
        self.particles: List[dict] = []
        self.generate_terrain()
        self.spawn_mobs(3)

    def generate_terrain(self):
        """Generate simple terrain with hills"""
        height_map = [SCREEN_HEIGHT - 100]
        
        for x in range(0, SCREEN_WIDTH, 20):
            height = height_map[-1] + random.randint(-20, 20)
            height = max(200, min(SCREEN_HEIGHT - 100, height))
            height_map.append(height)
        
        # Create blocks based on height map
        for i, height in enumerate(height_map):
            x = i * 20
            # Grass/dirt layer
            for y in range(int(height), SCREEN_HEIGHT, 20):
                if y == int(height):
                    block_type = BlockType.GRASS
                elif y < int(height) + 60:
                    block_type = BlockType.DIRT
                else:
                    block_type = BlockType.STONE
                
                self.blocks.append(Block(x, y, block_type))
            
            # Add trees randomly
            if random.random() < 0.15:
                self.add_tree(x, int(height) - 80)
            
            # Add water
            if random.random() < 0.05:
                for y in range(int(height), int(height) + 100, 20):
                    self.blocks.append(Block(x, y, BlockType.WATER))

    def add_tree(self, x: float, y: float):
        """Add a tree at the given position"""
        # Trunk
        for i in range(4):
            self.blocks.append(Block(x, y + i * 20, BlockType.WOOD))
        
        # Leaves
        for dx in [-20, 0, 20]:
            for dy in [-60, -40, -20]:
                self.blocks.append(Block(x + dx, y + dy, BlockType.LEAVES))

    def spawn_mobs(self, count: int):
        """Spawn mobs at random positions"""
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(100, 300)
            self.mobs.append(Mob(x, y, "zombie"))

    def draw(self, screen: pygame.Surface):
        """Draw all blocks"""
        for block in self.blocks:
            color = {
                BlockType.STONE: COLOR_STONE,
                BlockType.DIRT: COLOR_DIRT,
                BlockType.GRASS: COLOR_GROUND,
                BlockType.SAND: COLOR_SAND,
                BlockType.WATER: COLOR_WATER,
                BlockType.WOOD: COLOR_WOOD,
                BlockType.LEAVES: COLOR_LEAVES,
            }.get(block.block_type, COLOR_STONE)
            
            pygame.draw.rect(screen, color, (block.x, block.y, 20, 20))
            pygame.draw.rect(screen, (0, 0, 0), (block.x, block.y, 20, 20), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.running = True
        
        self.world = World()
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_1:
                    self.player.selected_block = BlockType.DIRT
                elif event.key == pygame.K_2:
                    self.player.selected_block = BlockType.STONE
                elif event.key == pygame.K_3:
                    self.player.selected_block = BlockType.WOOD
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_LSHIFT]:
            self.player.health -= 0.01  # Lose health over time
        
        # Mouse click for breaking/placing blocks
        if pygame.mouse.get_pressed()[0]:  # Left click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.break_block(mouse_x, mouse_y)
        elif pygame.mouse.get_pressed()[2]:  # Right click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.place_block(mouse_x, mouse_y)

    def break_block(self, x: float, y: float):
        """Remove a block at the given position"""
        for block in self.world.blocks[:]:
            if (block.x < x < block.x + 20 and
                block.y < y < block.y + 20):
                self.world.blocks.remove(block)
                self.player.exp_points += 10
                if self.player.exp_points >= 100:
                    self.player.exp_level += 1
                    self.player.exp_points = 0
                break

    def place_block(self, x: float, y: float):
        """Place a block at the given position"""
        if self.player.inventory.get(self.player.selected_block, 0) > 0:
            # Snap to grid
            snap_x = (int(x) // 20) * 20
            snap_y = (int(y) // 20) * 20
            
            # Check if position is empty
            for block in self.world.blocks:
                if block.x == snap_x and block.y == snap_y:
                    return
            
            self.world.blocks.append(Block(snap_x, snap_y, self.player.selected_block))
            self.player.inventory[self.player.selected_block] -= 1

    def update(self):
        self.player.update(self.world.blocks)
        
        for mob in self.world.mobs:
            mob.update(self.player)
        
        # Check collisions with mobs
        for mob in self.world.mobs:
            if (abs(self.player.x - mob.x) < 25 and
                abs(self.player.y - mob.y) < 35):
                self.player.health -= 0.1
        
        # Hunger over time
        self.player.hunger -= 0.01
        if self.player.hunger <= 0:
            self.player.health -= 0.05

    def draw(self):
        self.screen.fill(COLOR_SKY)
        
        # Draw world
        self.world.draw(self.screen)
        
        # Draw mobs
        for mob in self.world.mobs:
            mob.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw HUD
        self.player.draw_hud(self.screen, self.font)
        
        # Draw inventory
        inv_x = SCREEN_WIDTH - 250
        pygame.draw.rect(self.screen, COLOR_HUD_BG, (inv_x, 10, 240, 120))
        inv_text = self.font.render("Inventory:", True, COLOR_HUD_TEXT)
        self.screen.blit(inv_text, (inv_x + 10, 20))
        
        y_offset = 50
        for block_type, count in self.player.inventory.items():
            text = self.font.render(f"{block_type.name}: {count}", True, COLOR_HUD_TEXT)
            self.screen.blit(text, (inv_x + 10, y_offset))
            y_offset += 25
        
        # Draw FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, COLOR_TEXT)
        self.screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
