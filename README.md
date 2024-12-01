# Minecraft NBT Depth Checker

A Python utility to analyze, diagnose, and fix NBT depth issues in Minecraft save files, particularly useful when encountering the "tried to read nbt tag that was too big tried to allocate" error caused by excessive NBT tag depths.

![Minecraft NBT Error](img/error.png)

## Overview

When Minecraft worlds become complex or corrupted, they can develop issues with NBT (Named Binary Tag) structures becoming too deep or complex. This commonly manifests as a `java.lang.RuntimeException` with a message about trying to allocate too many bytes when attempting to load the world.

This tool helps you identify which parts of your save file's `level.dat` are reaching concerning depths, and offers the option to automatically reduce the complexity of problematic structures while maintaining data integrity.

## Example Output

Here's what the tool's output looks like when analyzing a problematic level.dat file:

```
=================================================
                NBT Depth Analyzer               
=================================================

=================================================
               Analysis Results                   
=================================================

File: level.dat
Total tags: 1,432
Maximum depth: 11
Path to maximum depth: Data > ... > parameters > continentalness

=================================================
              Deepest Structures                 
=================================================

Depth 11:
  → Data > WorldGenSettings > ... > parameters > continentalness
  → Data > WorldGenSettings > ... > parameters > continentalness

⚠️  WARNING: Found 2 structure(s) exceeding recommended depth of 100
Would you like to attempt to reduce these deep structures? (yes/no):
```

With full paths enabled (--full-paths):

```
Path to maximum depth: Data > WorldGenSettings > dimensions > minecraft:overworld > generator > biome_source > original_biome_source > biomes > [0] > parameters > continentalness
```

## Features

- Analyzes Minecraft level.dat files for NBT tag depths
- Reports maximum depth found and the full path to the deepest tags
- Identifies all deep structures with their complete paths
- Highlights potentially problematic deep structures
- Cross-platform color-coded output support
- Configurable display options:
  - Full path display (--full-paths/-f)
  - Custom warning depth threshold (--warning-depth/-w)
- Offers automatic structure reduction with safety features:
  - Creates automatic backups before any modifications
  - Reduces complex structures while maintaining NBT integrity
  - Provides clear paths to backups for easy restoration
- Helps diagnose and fix "tried to allocate" errors related to NBT complexity

## Requirements

- Python 3.6 or higher
- NBT library (`NBT`)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/decryptu/minecraft-nbt-depth-checker
cd minecraft-nbt-depth-checker
```

2. Install the required dependency:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```bash
python nbt_depth_checker.py path/to/your/level.dat
```

With full paths displayed:

```bash
python nbt_depth_checker.py --full-paths path/to/your/level.dat
# or
python nbt_depth_checker.py -f path/to/your/level.dat
```

With custom warning depth:

```bash
python nbt_depth_checker.py --warning-depth 50 path/to/your/level.dat
# or
python nbt_depth_checker.py -w 50 path/to/your/level.dat
```

Combine options:

```bash
python nbt_depth_checker.py -f -w 50 path/to/your/level.dat
```

Show help:

```bash
python nbt_depth_checker.py --help
```

The level.dat file is typically found in your world save folder:

- Windows: `%appdata%/.minecraft/saves/[world_name]/level.dat`
- Linux: `~/.minecraft/saves/[world_name]/level.dat`
- macOS: `~/Library/Application Support/minecraft/saves/[world_name]/level.dat`

The script will:

1. Analyze the NBT structure
2. Show the maximum depth and paths to deep structures
3. If issues are found, offer to automatically reduce structure complexity
4. Create a backup before making any changes
5. Attempt to safely reduce deep structures
6. Provide backup restoration information if needed

## Display Options

- `--full-paths` or `-f`: Shows complete paths instead of truncated versions
- `--warning-depth` or `-w`: Sets custom depth threshold for warnings (default: 100)

## Safety Features

When reducing NBT structures, the tool:

1. Always creates a timestamped backup first
2. Reduces structures incrementally
3. Maintains NBT tag types and integrity
4. Provides clear backup paths for restoration
5. Reports any structures it couldn't safely reduce

## Common Issues

The "tried to allocate" error typically occurs in the level.dat file of your Minecraft save. This can happen due to:

- Complex redstone contraptions
- Large numbers of entities in a small area
- Corrupted chunks
- Mod-related issues
- World conversion issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to [minecraft-nbt-lib](https://github.com/twoolie/NBT) for providing the NBT file parsing functionality
- Inspired by Minecraft save debugging challenges and community needs

## Technical Background

Minecraft uses NBT (Named Binary Tag) format to store various game data in the level.dat file. While the format allows for nested structures, excessive nesting can lead to memory allocation issues. This tool helps identify and safely reduce such complex structures while maintaining data integrity.
