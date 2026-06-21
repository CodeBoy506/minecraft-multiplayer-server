# Minecraft Multiplayer Server - Game Implementation

A Python-based Minecraft-inspired game with core gameplay mechanics.

## Features

- **Player Movement**: Walk left/right with arrow keys or A/D
- **Jumping**: Space bar to jump
- **Block Breaking**: Left-click to break blocks and collect materials
- **Block Placing**: Right-click to place blocks from inventory
- **Terrain Generation**: Procedurally generated terrain with grass, dirt, stone, and trees
- **Mobs**: Zombie mobs that wander and chase the player
- **Health & Hunger System**: Track health and hunger points
- **Experience System**: Earn XP by breaking blocks
- **Inventory Management**: Collect and manage different block types
- **HUD Display**: Real-time health, hunger, and inventory tracking

## Controls

- **A/D or Arrow Keys**: Move left/right
- **Space**: Jump
- **Left Click**: Break blocks
- **Right Click**: Place blocks
- **1/2/3**: Select block type (Dirt/Stone/Wood)
- **Shift**: Sprint (increases hunger)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python game.py
```

## Game Mechanics

### Health System
- Start with 20 health points
- Take damage from mobs
- Hunger decreases over time and affects health

### Block Types
- **Dirt**: Common building material
- **Stone**: Durable building material
- **Grass**: Decorative surface blocks
- **Wood**: From trees, used for building
- **Leaves**: Tree foliage
- **Water**: Environmental hazard
- **Sand**: Decorative terrain

### Experience
- Gain XP by breaking blocks
- Level up as XP accumulates (100 XP per level)

## Future Enhancements

- Multiplayer networking
- More mob types
- Crafting system
- Mining different materials
- Combat system
- NPCs and trading
- Dungeons and caves
- Weather system
