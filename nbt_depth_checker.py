from nbt import nbt

def get_max_depth(tag, current_depth=0, path=[]):
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

# Load your level.dat file
nbtfile = nbt.NBTFile("C:/Users/gurva/Desktop/level.dat", "rb")

# Get the maximum depth and its path
max_depth, max_path = get_max_depth(nbtfile)
print(f"Maximum depth: {max_depth}")
print(f"Path to maximum depth: {' > '.join(map(str, max_path))}")

# Optionally, print depths of top-level tags
for name, tag in nbtfile.items():
    depth, path = get_max_depth(tag, path=[name])
    print(f"{name}: {depth}")
    if depth > 100:  # Adjust this threshold as needed
        print(f"  Deep path in {name}: {' > '.join(map(str, path))}")