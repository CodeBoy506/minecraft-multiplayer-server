import pygame
import random
import math
from enum import Enum
from collections import defaultdict
import json

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
BLOCK_SIZE = 32

# Colors
class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRASS = (34, 139, 34)
    DIRT = (139, 90, 43)
    STONE = (128, 128, 128)
    WOOD = (139, 69, 19)
    WATER = (30, 144, 255)
    SAND = (238, 203, 127)
    SKY = (135, 206, 235)
    DARK_GRAY = (64, 64, 64)
    LEAVES = (34, 177, 76)
    COAL = (50, 50, 50)
    IRON = (192, 192, 192)
    GOLD = (255, 215, 0)
    DIAMOND = (0, 255, 255)
    OBSIDIAN = (20, 20, 40)
    LAVA = (255, 69, 0)
    SNOW = (245, 245, 245)
    DARK_GREEN = (0, 100, 0)
    BROWN = (101, 67, 33)
    RED = (255, 0, 0)

class BlockType(Enum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4
    WATER = 5
    SAND = 6
    COAL = 7
    IRON = 8
    GOLD = 9
    DIAMOND = 10
    LEAVES = 11
    OBSIDIAN = 12
    LAVA = 13
    SNOW = 14
    GRAVEL = 15
    BEDROCK = 16

class Block:
    def __init__(self, block_type):
        self.block_type = block_type
        self.hardness = {
            BlockType.AIR: 0,
            BlockType.DIRT: 0.5,
            BlockType.GRASS: 0.6,
            BlockType.STONE: 1.5,
            BlockType.WOOD: 0.2,
            BlockType.WATER: 0,
            BlockType.SAND: 0.5,
            BlockType.COAL: 2.0,
            BlockType.IRON: 3.0,
            BlockType.GOLD: 2.5,
            BlockType.DIAMOND: 5.0,
            BlockType.LEAVES: 0.1,
            BlockType.OBSIDIAN: 50.0,
            BlockType.LAVA: 0,
            BlockType.SNOW: 0.2,
            BlockType.GRAVEL: 0.6,
            BlockType.BEDROCK: 999.0,
        }[block_type]
        self.is_solid = block_type not in [BlockType.AIR, BlockType.WATER, BlockType.LAVA]
    
    def get_color(self):
        color_map = {
            BlockType.AIR: Color.SKY.value,
            BlockType.GRASS: Color.GRASS.value,
            BlockType.DIRT: Color.DIRT.value,
            BlockType.STONE: Color.STONE.value,
            BlockType.WOOD: Color.WOOD.value,
            BlockType.WATER: Color.WATER.value,
            BlockType.SAND: Color.SAND.value,
            BlockType.COAL: Color.COAL.value,
            BlockType.IRON: Color.IRON.value,
            BlockType.GOLD: Color.GOLD.value,
            BlockType.DIAMOND: Color.DIAMOND.value,
            BlockType.LEAVES: Color.LEAVES.value,
            BlockType.OBSIDIAN: Color.OBSIDIAN.value,
            BlockType.LAVA: Color.LAVA.value,
            BlockType.SNOW: Color.SNOW.value,
            BlockType.GRAVEL: (169, 169, 169),
            BlockType.BEDROCK: (40, 40, 40),
        }
        return color_map.get(BlockType.AIR, Color.WHITE.value)

class Particle:
    def __init__(self, x, y, vx, vy, lifetime=30, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # gravity
        self.lifetime -= 1
    
    def draw(self, screen, camera_x, camera_y):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = max(1, int(3 * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(screen, self.color, 
                          (int(self.x - camera_x), int(self.y - camera_y)), size)

class World:
    def __init__(self, width, height, seed=None):
        if seed:
            random.seed(seed)
        self.width = width
        self.height = height
        self.blocks = [[Block(BlockType.AIR) for _ in range(width)] for _ in range(height)]
        self.particles = []
        self.generate_terrain()
        self.spawn_trees()
    
    def perlin_noise(self, x, y):
        """Simple noise function for terrain generation"""
        xi = int(x) & 255
        yi = int(y) & 255
        xf = x - int(x)
        yf = y - int(y)
        
        u = xf * xf * (3.0 - 2.0 * xf)
        v = yf * yf * (3.0 - 2.0 * yf)
        
        return ((xi + yi * 57) * 13789) % 256 / 256.0
    
    def generate_terrain(self):
        """Generate advanced terrain with multiple biomes"""
        for x in range(self.width):
            # Calculate height variations
            base_height = self.height - 20
            height_var = int(10 * math.sin(x * 0.05) + 5 * (hash(x) % 10) / 10)
            ground_level = base_height + height_var
            
            # Add caves and overhangs
            cave_threshold = 0.4
            
            for y in range(self.height):
                if y >= self.height - 1:
                    # Bedrock
                    self.blocks[y][x] = Block(BlockType.BEDROCK)
                elif y >= ground_level + 5:
                    self.blocks[y][x] = Block(BlockType.AIR)
                elif y >= ground_level + 2:
                    # Surface layer with caves
                    noise = self.perlin_noise(x * 0.1, y * 0.1)
                    if noise > cave_threshold:
                        self.blocks[y][x] = Block(BlockType.AIR)
                    else:
                        self.blocks[y][x] = Block(BlockType.STONE)
                elif y >= ground_level:
                    self.blocks[y][x] = Block(BlockType.STONE)
                elif y == ground_level:
                    self.blocks[y][x] = Block(BlockType.GRASS)
                elif y > ground_level - 3:
                    self.blocks[y][x] = Block(BlockType.DIRT)
                elif y > ground_level - 10:
                    self.blocks[y][x] = Block(BlockType.STONE)
                elif y > ground_level - 20:
                    # Ore distribution
                    ore_rand = random.random()
                    if ore_rand < 0.05:
                        self.blocks[y][x] = Block(BlockType.COAL)
                    elif ore_rand < 0.08:
                        self.blocks[y][x] = Block(BlockType.IRON)
                    elif ore_rand < 0.09:
                        self.blocks[y][x] = Block(BlockType.GOLD)
                    else:
                        self.blocks[y][x] = Block(BlockType.STONE)
                else:
                    # Deep ore distribution
                    ore_rand = random.random()
                    if ore_rand < 0.03:
                        self.blocks[y][x] = Block(BlockType.DIAMOND)
                    elif ore_rand < 0.05:
                        self.blocks[y][x] = Block(BlockType.GOLD)
                    else:
                        self.blocks[y][x] = Block(BlockType.STONE)
    
    def spawn_trees(self):
        """Spawn trees on the surface"""
        for x in range(0, self.width, random.randint(8, 15)):
            if x >= self.width:
                break
            # Find ground level
            for y in range(self.height):
                if self.blocks[y][x].block_type == BlockType.GRASS:
                    # Place tree
                    self.place_tree(x, y)
                    break
    
    def place_tree(self, x, y):
        """Place a tree at given coordinates"""
        trunk_height = random.randint(4, 7)
        
        # Trunk
        for i in range(trunk_height):
            if y - i >= 0:
                self.blocks[y - i][x] = Block(BlockType.WOOD)
        
        # Leaves
        leaves_start = y - trunk_height - 2
        leaves_radius = 3
        
        for lx in range(x - leaves_radius, x + leaves_radius + 1):
            for ly in range(leaves_start, y - trunk_height + 1):
                if 0 <= lx < self.width and 0 <= ly < self.height:
                    if (lx - x) ** 2 + (ly - (leaves_start + 1)) ** 2 <= leaves_radius ** 2:
                        if self.blocks[ly][lx].block_type == BlockType.AIR:
                            self.blocks[ly][lx] = Block(BlockType.LEAVES)
    
    def get_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[y][x]
        return Block(BlockType.AIR)
    
    def set_block(self, x, y, block):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.blocks[y][x] = block
    
    def create_particles(self, x, y, block_type, count=8):
        """Create particles when block is broken"""
        color = Block(block_type).get_color()
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2
            particle = Particle(x, y, vx, vy, lifetime=40, color=color)
            self.particles.append(particle)
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_SIZE * 0.8
        self.height = BLOCK_SIZE * 1.8
        self.velocity_y = 0
        self.velocity_x = 0
        self.is_jumping = False
        self.is_flying = False
        self.inventory = defaultdict(int)
        self.selected_tool = None
        self.mining_progress = defaultdict(float)
        self.health = 20  # 10 hearts
        self.hunger = 20  # 10 hunger bars
        self.experience = 0
        self.level = 0
        self.can_fly = False
        
        # Initialize inventory with some items
        self.inventory[BlockType.WOOD] = 10
        self.inventory[BlockType.STONE] = 5
        self.inventory[BlockType.DIRT] = 20
    
    def update(self, world, keys):
        # Horizontal movement
        self.velocity_x = 0
        speed = 5 if not self.is_flying else 8
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = speed
        
        self.x += self.velocity_x
        self.check_collisions(world)
        
        # Vertical movement
        if self.is_flying:
            if keys[pygame.K_SPACE]:
                self.velocity_y = -8
            elif keys[pygame.K_LSHIFT]:
                self.velocity_y = 8
            else:
                self.velocity_y = 0
            self.y += self.velocity_y
        else:
            self.velocity_y += 0.5
            self.y += self.velocity_y
            self.check_collisions(world)
        
        # Jump
        if (keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.is_jumping and not self.is_flying:
            if self.is_on_ground(world):
                self.velocity_y = -12
                self.is_jumping = True
        
        # Keep player in bounds horizontally
        if self.x < 0:
            self.x = 0
        if self.x + self.width > world.width * BLOCK_SIZE:
            self.x = world.width * BLOCK_SIZE - self.width
        
        # Death plane
        if self.y > world.height * BLOCK_SIZE:
            self.health = 0
    
    def is_on_ground(self, world):
        """Check if player is standing on a solid block"""
        player_rect = pygame.Rect(self.x, self.y + self.height, self.width, 2)
        
        for bx in range(int(self.x // BLOCK_SIZE) - 1, int((self.x + self.width) // BLOCK_SIZE) + 2):
            for by in range(int((self.y + self.height) // BLOCK_SIZE), int((self.y + self.height) // BLOCK_SIZE) + 2):
                block = world.get_block(bx, by)
                if block.is_solid:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if player_rect.colliderect(block_rect):
                        return True
        return False
    
    def check_collisions(self, world):
        """Check collisions with blocks"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for bx in range(int(self.x // BLOCK_SIZE) - 1, int((self.x + self.width) // BLOCK_SIZE) + 2):
            for by in range(int(self.y // BLOCK_SIZE) - 1, int((self.y + self.height) // BLOCK_SIZE) + 2):
                block = world.get_block(bx, by)
                if block.is_solid:
                    block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    if player_rect.colliderect(block_rect):
                        # Resolve collision
                        if self.velocity_y > 0:
                            self.y = by * BLOCK_SIZE - self.height
                            self.velocity_y = 0
                            self.is_jumping = False
                        elif self.velocity_y < 0:
                            self.y = (by + 1) * BLOCK_SIZE
                            self.velocity_y = 0
                        
                        if self.velocity_x > 0:
                            self.x = bx * BLOCK_SIZE - self.width
                        elif self.velocity_x < 0:
                            self.x = (bx + 1) * BLOCK_SIZE
    
    def mine_block(self, world, mx, my):
        """Mine a block at screen coordinates"""
        bx = mx // BLOCK_SIZE
        by = my // BLOCK_SIZE
        block = world.get_block(bx, by)
        
        if block.block_type != BlockType.AIR:
            block_key = (bx, by)
            self.mining_progress[block_key] += 0.08
            
            if self.mining_progress[block_key] >= block.hardness + 0.3:
                world.set_block(bx, by, Block(BlockType.AIR))
                self.inventory[block.block_type] += 1
                world.create_particles(bx * BLOCK_SIZE + BLOCK_SIZE // 2, 
                                      by * BLOCK_SIZE + BLOCK_SIZE // 2, 
                                      block.block_type)
                del self.mining_progress[block_key]
    
    def place_block(self, world, mx, my, block_type):
        """Place a block at screen coordinates"""
        if self.inventory[block_type] > 0:
            bx = mx // BLOCK_SIZE
            by = my // BLOCK_SIZE
            # Don't place inside player
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            block_rect = pygame.Rect(bx * BLOCK_SIZE, by * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if not player_rect.colliderect(block_rect):
                world.set_block(bx, by, Block(block_type))
                self.inventory[block_type] -= 1
    
    def draw(self, screen, camera_x, camera_y):
        # Draw body
        body_color = (200, 100, 100)
        pygame.draw.rect(screen, body_color, 
                        (self.x - camera_x, self.y - camera_y, self.width, self.height))
        
        # Draw head
        head_color = (255, 200, 180)
        pygame.draw.circle(screen, head_color, 
                          (int(self.x - camera_x + self.width / 2), 
                           int(self.y - camera_y - BLOCK_SIZE / 3)), 
                          int(BLOCK_SIZE / 3))
        
        # Draw eyes
        eye_y = int(self.y - camera_y - BLOCK_SIZE / 4)
        pygame.draw.circle(screen, Color.BLACK.value, 
                          (int(self.x - camera_x + self.width / 3), eye_y), 2)
        pygame.draw.circle(screen, Color.BLACK.value, 
                          (int(self.x - camera_x + 2 * self.width / 3), eye_y), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minecraft Clone - Advanced")
        self.clock = pygame.time.Clock()
        
        world_width = SCREEN_WIDTH // BLOCK_SIZE + 10
        world_height = SCREEN_HEIGHT // BLOCK_SIZE + 20
        self.world = World(world_width, world_height, seed=42)
        
        # Find spawn point
        spawn_x = world_width // 2
        spawn_y = 0
        for y in range(world_height):
            if self.world.blocks[y][spawn_x].block_type == BlockType.GRASS:
                spawn_y = y
                break
        
        self.player = Player(spawn_x * BLOCK_SIZE, spawn_y * BLOCK_SIZE - 64)
        self.camera_x = 0
        self.camera_y = 0
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)
        
        self.selected_blocks = [
            BlockType.WOOD, BlockType.STONE, BlockType.DIRT,
            BlockType.GRASS, BlockType.SAND, BlockType.WATER
        ]
        self.selected_index = 0
        self.running = True
        self.paused = False
        self.show_debug = False
        self.time_of_day = 0  # 0-1, 0=day, 0.5=night
        self.game_ticks = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Select blocks with number keys
                for i in range(len(self.selected_blocks)):
                    if event.key == pygame.K_1 + i:
                        self.selected_index = i
                
                # Other keys
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pygame.K_F3:
                    self.show_debug = not self.show_debug
                if event.key == pygame.K_f:
                    self.player.is_flying = not self.player.is_flying
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                mx, my = pygame.mouse.get_pos()
                world_mx = mx + self.camera_x
                world_my = my + self.camera_y
                
                if event.button == 1:  # Left click - mine
                    self.player.mine_block(self.world, world_mx, world_my)
                elif event.button == 3:  # Right click - place
                    selected = self.selected_blocks[self.selected_index]
                    self.player.place_block(self.world, world_mx, world_my, selected)
    
    def update(self):
        if not self.paused:
            keys = pygame.key.get_pressed()
            self.player.update(self.world, keys)
            
            # Update camera to follow player
            self.camera_x = int(self.player.x + self.player.width / 2 - SCREEN_WIDTH / 2)
            self.camera_y = int(self.player.y - SCREEN_HEIGHT / 3)
            
            # Clamp camera
            max_cam_x = self.world.width * BLOCK_SIZE - SCREEN_WIDTH
            max_cam_y = self.world.height * BLOCK_SIZE - SCREEN_HEIGHT
            self.camera_x = max(0, min(self.camera_x, max_cam_x)) if max_cam_x > 0 else 0
            self.camera_y = max(0, min(self.camera_y, max_cam_y)) if max_cam_y > 0 else 0
            
            # Update world
            self.world.update_particles()
            
            # Update game time
            self.game_ticks += 1
            self.time_of_day = (self.game_ticks / 24000) % 1
    
    def get_ambient_light(self):
        """Calculate ambient light based on time of day"""
        if self.time_of_day < 0.25:
            # Morning: 0.25 to 1.0
            return 0.25 + (self.time_of_day / 0.25) * 0.75
        elif self.time_of_day < 0.75:
            # Day: 1.0
            return 1.0
        else:
            # Evening/Night: 1.0 to 0.25
            return 1.0 - ((self.time_of_day - 0.75) / 0.25) * 0.75
    
    def draw(self):
        # Calculate lighting
        ambient = self.get_ambient_light()
        
        # Background
        sky_color = tuple(int(c * ambient) for c in Color.SKY.value)
        self.screen.fill(sky_color)
        
        # Draw world
        for by in range(int(self.camera_y // BLOCK_SIZE) - 1, 
                       int((self.camera_y + SCREEN_HEIGHT) // BLOCK_SIZE) + 2):
            for bx in range(int(self.camera_x // BLOCK_SIZE) - 1, 
                           int((self.camera_x + SCREEN_WIDTH) // BLOCK_SIZE) + 2):
                block = self.world.get_block(bx, by)
                if block.block_type != BlockType.AIR:
                    screen_x = bx * BLOCK_SIZE - self.camera_x
                    screen_y = by * BLOCK_SIZE - self.camera_y
                    
                    color = block.get_color()
                    lit_color = tuple(int(c * ambient) for c in color)
                    pygame.draw.rect(self.screen, lit_color, 
                                   (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, Color.DARK_GRAY.value, 
                                   (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # Draw particles
        for particle in self.world.particles:
            particle.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw player
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        # Draw mining progress
        mx, my = pygame.mouse.get_pos()
        world_mx = mx + self.camera_x
        world_my = my + self.camera_y
        bx = world_mx // BLOCK_SIZE
        by = world_my // BLOCK_SIZE
        
        if (bx, by) in self.player.mining_progress:
            progress = self.player.mining_progress[(bx, by)]
            block = self.world.get_block(bx, by)
            total_progress = block.hardness + 0.3
            
            screen_x = bx * BLOCK_SIZE - self.camera_x
            screen_y = by * BLOCK_SIZE - self.camera_y
            progress_width = int((progress / total_progress) * BLOCK_SIZE)
            
            pygame.draw.rect(self.screen, Color.RED.value,
                           (screen_x, screen_y - 10, progress_width, 5))
            pygame.draw.rect(self.screen, Color.WHITE.value,
                           (screen_x, screen_y - 10, BLOCK_SIZE, 5), 1)
        
        # Draw HUD
        self.draw_hud()
        
        # Draw pause menu
        if self.paused:
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_hud(self):
        # Hotbar
        hotbar_y = SCREEN_HEIGHT - 40
        hotbar_x_start = SCREEN_WIDTH // 2 - (len(self.selected_blocks) * 35) // 2
        
        for i, block_type in enumerate(self.selected_blocks):
            x = hotbar_x_start + i * 35
            color = (255, 255, 255) if i == self.selected_index else (100, 100, 100)
            pygame.draw.rect(self.screen, color, (x, hotbar_y, 32, 32), 2)
            
            block_color = Block(block_type).get_color()
            pygame.draw.rect(self.screen, block_color, (x + 2, hotbar_y + 2, 28, 28))
            
            # Count
            count = self.player.inventory[block_type]
            if count > 0:
                text = self.font.render(str(count), True, Color.WHITE.value)
                self.screen.blit(text, (x + 18, hotbar_y + 18))
        
        # Health and hunger
        health_text = f"Health: {self.player.health} / 20"
        hunger_text = f"Hunger: {self.player.hunger} / 20"
        exp_text = f"Level: {self.player.level} XP: {self.player.experience}"
        
        health_surf = self.font.render(health_text, True, (255, 0, 0))
        hunger_surf = self.font.render(hunger_text, True, (255, 165, 0))
        exp_surf = self.font.render(exp_text, True, (0, 255, 0))
        
        self.screen.blit(health_surf, (10, 10))
        self.screen.blit(hunger_surf, (10, 35))
        self.screen.blit(exp_surf, (10, 60))
        
        # Coordinates
        if self.show_debug:
            coords_text = f"X: {int(self.player.x // BLOCK_SIZE)} Y: {int(self.player.y // BLOCK_SIZE)} Z: 0"
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            time_text = f"Time: {int(self.game_ticks % 24000)} / 24000"
            
            coords_surf = self.font.render(coords_text, True, Color.WHITE.value)
            fps_surf = self.font.render(fps_text, True, Color.WHITE.value)
            time_surf = self.font.render(time_text, True, Color.WHITE.value)
            
            self.screen.blit(coords_surf, (10, SCREEN_HEIGHT - 60))
            self.screen.blit(fps_surf, (10, SCREEN_HEIGHT - 35))
            self.screen.blit(time_surf, (10, SCREEN_HEIGHT - 10))
    
    def draw_pause_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(Color.BLACK.value)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, Color.WHITE.value)
        resume_text = self.font.render("Press ESC to resume", True, Color.WHITE.value)
        
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(resume_text, resume_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
