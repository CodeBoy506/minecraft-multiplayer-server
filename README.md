# Minecraft Clone - Advanced Edition

A feature-rich Minecraft-inspired sandbox game built with Python and Pygame. Create, explore, and survive in a procedurally generated world!

## Features

### Core Gameplay
- **Block Building & Destruction**: Place and mine various block types with realistic hardness mechanics
- **Procedurally Generated Terrain**: Infinite landscape with varied biomes, caves, and natural structures
- **Physics & Collision**: Realistic gravity, jumping, and collision detection
- **Particle Effects**: Visual feedback when breaking blocks

### Block Types
- **Solid Blocks**: Grass, Dirt, Stone, Wood, Sand, Gravel, Snow
- **Ores**: Coal, Iron, Gold, Diamond (found at different depths)
- **Special**: Leaves, Obsidian, Water, Lava, Bedrock

### Player Mechanics
- **Movement**: Walk left/right with smooth physics
- **Jumping**: Jump to reach higher areas
- **Flight Mode**: Toggle flight mode to explore freely (Press F)
- **Inventory System**: Collect blocks and manage resources
- **Health & Hunger**: Track player status (expandable for future gameplay)

### World Features
- **Dynamic Trees**: Randomly generated trees with trunks and leaves
- **Day/Night Cycle**: Lighting changes based on time of day (24,000 ticks per cycle)
- **Ambient Lighting**: World brightness changes throughout the day
- **Cave Systems**: Procedurally generated caves for exploration
- **Ore Distribution**: Ores appear at specific depths - deeper = rarer

### UI & Controls
- **Hotbar**: Select from 6 different block types (1-6 keys)
- **Health/Hunger Display**: Top-left corner status indicators
- **Debug Mode**: Press F3 to view coordinates, FPS, and time
- **Pause Menu**: Press ESC to pause/resume
- **Mining Progress**: Visual indicator showing block break progress

## Controls

| Key | Action |
|-----|--------|
| **A/D** or **Arrow Keys** | Move left/right |
| **W/UP** or **SPACE** | Jump |
| **F** | Toggle Flight Mode |
| **1-6** | Select block type |
| **Left Click** | Mine block |
| **Right Click** | Place block |
| **ESC** | Pause/Resume |
| **F3** | Toggle Debug Info |

## Installation

### Requirements
- Python 3.7+
- Pygame

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/CodeBoy506/minecraft-multiplayer-server.git
cd minecraft-multiplayer-server
```

2. **Install dependencies**
```bash
pip install pygame
```

3. **Run the game**
```bash
python minecraft_game.py
```

## Game Guide

### Getting Started
1. The game spawns you on a grass block
2. Use **A/D** or **Arrow Keys** to walk around
3. Press **SPACE** or **W** to jump

### Mining Blocks
- **Left-click** on any block to mine it
- Different blocks take different times to break (harder blocks = longer)
- Mined blocks appear in your inventory

### Building
- Select a block type using **1-6** keys
- **Right-click** to place the selected block
- You have starting inventory of Wood, Stone, and Dirt

### Exploration
- Explore caves to find rare ores
- Diamond is the rarest ore, found deep underground
- Each ore has different mining times

### Flight Mode
- Press **F** to toggle flight mode
- In flight mode: SPACE to go up, SHIFT to go down, A/D to move
- Useful for exploring and building large structures

### Debug Information
- Press **F3** to show your coordinates and current FPS
- Check the day/night cycle timer

## Game Mechanics

### Block Hardness
Each block type has different hardness values:
- **Leaves**: 0.1 (fastest to break)
- **Wood**: 0.2
- **Dirt**: 0.5
- **Grass**: 0.6
- **Sand**: 0.5
- **Stone**: 1.5
- **Coal**: 2.0
- **Iron**: 3.0
- **Gold**: 2.5
- **Diamond**: 5.0 (slowest to break)
- **Obsidian**: 50.0 (extremely hard)

### Terrain Generation
- **Surface Layer**: Grass and dirt blocks
- **Stone Layer**: Main terrain foundation
- **Ore Distribution**: 
  - Coal: Mid-level ores
  - Iron: Mid-level ores
  - Gold: Deep ores (rarer)
  - Diamond: Very deep ores (very rare)

### Lighting System
- Time cycle affects ambient light
- 0:00 - 6:00: Night (darker)
- 6:00 - 18:00: Day (full brightness)
- 18:00 - 24:00: Evening/Night (darker)

## Project Structure

```
minecraft-multiplayer-server/
├── minecraft_game.py       # Main game file
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## Future Enhancements

- [ ] Crafting system
- [ ] Different biomes (desert, forest, snow)
- [ ] Mobs (zombies, creepers, animals)
- [ ] Multiplayer support
- [ ] Inventory management interface
- [ ] Tool progression (wooden → stone → iron → diamond)
- [ ] Better graphics and animations
- [ ] Sound effects and music
- [ ] Save/Load game world
- [ ] Redstone mechanics
- [ ] Advanced lighting system

## Code Overview

### Main Classes

**Block**: Represents a single block with properties like hardness and color

**Particle**: Visual effects when blocks are broken

**World**: Manages terrain generation, block storage, and particle system

**Player**: Player character with physics, collision, and inventory

**Game**: Main game loop handling rendering, input, and updates

## Performance Tips

- The game runs at 60 FPS by default
- Particle effects are limited to maintain performance
- Only visible blocks are rendered (frustum culling)

## Troubleshooting

### Game won't start
- Make sure Pygame is installed: `pip install pygame`
- Check Python version is 3.7 or higher

### Low FPS
- Close other applications
- The game optimizes by only rendering visible chunks
- Particle effects may impact performance on slower systems

### Can't mine blocks
- Ensure you're clicking on a visible block
- Some blocks like Obsidian take very long to break
- Check the mining progress bar

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## Author

Created by CodeBoy506

---

**Enjoy building and exploring!** 🎮✨
