from nbt import nbt
import os
import sys

def get_max_depth(tag, current_depth=0, path=[]):
    """
    Recursively calculate the maximum depth of an NBT structure.
    
    Args:
        tag: The NBT tag to analyze
        current_depth (int): The current depth in the recursion
        path (list): The current path in the NBT structure
    
    Returns:
        tuple: (max_depth, path_to_max_depth)
    """
    if isinstance(tag, nbt.TAG_Compound):
        depths = [get_max_depth(child, current_depth + 1, path + [name])
                  for name, child in tag.items()
                  if isinstance(child, (nbt.TAG_Compound, nbt.TAG_List))]
    elif isinstance(tag, nbt.TAG_List):
        depths = [get_max_depth(child, current_depth + 1, path + [f"[{i}]"])
                  for i, child in enumerate(tag)
                  if isinstance(child, (nbt.TAG_Compound, nbt.TAG_List))]
    else:
        return current_depth, path
    
    if not depths:
        return current_depth, path
    return max(depths, key=lambda x: x[0])

def analyze_nbt_file(file_path):
    """
    Analyze an NBT file for depth issues.
    
    Args:
        file_path (str): Path to the level.dat file
    """
    try:
        nbtfile = nbt.NBTFile(file_path, "rb")
        
        # Get the maximum depth and its path
        max_depth, max_path = get_max_depth(nbtfile)
        print(f"Maximum depth: {max_depth}")
        print(f"Path to maximum depth: {' > '.join(map(str, max_path))}")
        
        # Print depths of top-level tags
        print("\nDepths of top-level tags:")
        for name, tag in nbtfile.items():
            depth, path = get_max_depth(tag, path=[name])
            print(f"{name}: {depth}")
            if depth > 100:  # Adjust this threshold as needed
                print(f"  Deep path in {name}: {' > '.join(map(str, path))}")
                
    except Exception as e:
        print(f"Error analyzing NBT file: {str(e)}")

if __name__ == "__main__":
    # Default to example level.dat if no file is provided
    default_path = os.path.join("example", "level.dat")
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = default_path
        print(f"No file specified, using example file: {default_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        print("Usage: python nbt_depth_checker.py [path_to_level.dat]")
        sys.exit(1)
        
    analyze_nbt_file(file_path)