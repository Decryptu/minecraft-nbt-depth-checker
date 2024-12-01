# Minecraft NBT Depth Checker

A Python utility to analyze and diagnose NBT depth issues in Minecraft save files, particularly useful when encountering the "tried to allocate" error caused by excessive NBT tag depths.

## Overview

When Minecraft saves encounter NBT (Named Binary Tag) structures that are too deep or complex, they can trigger a `java.lang.RuntimeException` with a message about trying to allocate too many bytes. This tool helps identify which parts of your save file are reaching concerning depths, allowing you to track down and fix issues before they cause crashes.

## Features

- Analyzes Minecraft level.dat files for NBT tag depths
- Reports maximum depth found and the full path to the deepest tags
- Identifies all top-level tags with their respective depths
- Highlights potentially problematic deep structures
- Helps diagnose "tried to allocate" errors related to NBT complexity

## Requirements

- Python 3.6 or higher
- NBT library (`minecraft-nbt-lib`)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/minecraft-nbt-depth-checker
    cd minecraft-nbt-depth-checker
    ```

2. Install the required dependency:

    ```bash
    pip install minecraft-nbt-lib
    ```

## Usage

1. Place the script in a convenient location
2. Update the path to your level.dat file in the script:

    ```python
    nbtfile = nbt.NBTFile("path/to/your/level.dat", "rb")
    ```

3. Run the script:

    ```bash
    python nbt_depth_checker.py
    ```

The script will output:

- The maximum NBT depth found in the file
- The path to the deepest structure
- Depths of all top-level tags
- Detailed paths for any tags exceeding a specified depth threshold

## Example Output

```bash
Maximum depth: 147
Path to maximum depth: Data > Player > RecipBook > toBeDisplayed > [0] > ...
Data: 147
  Deep path in Data: Player > RecipBook > toBeDisplayed > [0] > ...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to [minecraft-nbt-lib](https://github.com/twoolie/NBT) for providing the NBT file parsing functionality
- Inspired by Minecraft save debugging challenges and community needs

## Technical Background

Minecraft uses NBT (Named Binary Tag) format to store various game data. The format allows for nested structures, but excessive nesting can lead to memory allocation issues. The default maximum NBT depth in Minecraft appears to be around 512 levels, though this can vary based on the specific version and implementation.
