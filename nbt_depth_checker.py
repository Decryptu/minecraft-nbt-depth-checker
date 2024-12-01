from nbt import nbt
import os
import sys
import argparse
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import shutil
from datetime import datetime

# ANSI Color codes that work across platforms
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'

class NBTAnalyzer:
    def __init__(self, warning_depth: int = 100, show_full_paths: bool = False):
        self.warning_depth = warning_depth
        self.show_full_paths = show_full_paths
        self.paths: Dict[int, List[str]] = defaultdict(list)
        self.problematic_tags: List[Dict[str, Any]] = []
        
        # Enable ANSI escape sequences for Windows
        if os.name == 'nt':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def print_header(self, text: str) -> None:
        """Print a formatted header."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(50)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}\n")

    def print_info(self, label: str, value: Any) -> None:
        """Print formatted information."""
        print(f"{Colors.CYAN}{label}:{Colors.ENDC} {Colors.BOLD}{value}{Colors.ENDC}")

    def print_warning(self, text: str) -> None:
        """Print a warning message."""
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  WARNING: {text}{Colors.ENDC}")

    def print_error(self, text: str) -> None:
        """Print an error message."""
        print(f"{Colors.RED}{Colors.BOLD}❌ ERROR: {text}{Colors.ENDC}")

    def print_success(self, text: str) -> None:
        """Print a success message."""
        print(f"{Colors.GREEN}{Colors.BOLD}✔ {text}{Colors.ENDC}")

    def format_path(self, path: str) -> str:
        """Format path based on full path setting."""
        if self.show_full_paths:
            return path
        else:
            parts = path.split(" > ")
            if len(parts) > 4:
                return f"{' > '.join(parts[:2])} > ... > {' > '.join(parts[-2:])}"
            return path

    def get_tag_path_and_length(self, tag: Any, current_depth: int = 0, path: List[str] = [], parent=None, key_in_parent=None) -> Tuple[int, List[str], int]:
        """
        Get the depth, path, and length of NBT tags.
        Also stores problematic tag references for potential modification.
        """
        tag_length = 1
        
        if isinstance(tag, nbt.TAG_Compound):
            depths = []
            for name, child in tag.items():
                child_depth, child_path, child_length = self.get_tag_path_and_length(
                    child, current_depth + 1, path + [name], tag, name
                )
                tag_length += child_length
                depths.append((child_depth, child_path, child_length))
                
                if child_depth >= self.warning_depth:
                    self.problematic_tags.append({
                        'tag': child,
                        'parent': tag,
                        'key': name,
                        'depth': child_depth,
                        'path': ' > '.join(child_path)
                    })
                
                self.paths[child_depth].append(" > ".join(child_path))
                
        elif isinstance(tag, nbt.TAG_List):
            depths = []
            for i, child in enumerate(tag):
                child_depth, child_path, child_length = self.get_tag_path_and_length(
                    child, current_depth + 1, path + [f"[{i}]"], tag, i
                )
                tag_length += child_length
                depths.append((child_depth, child_path, child_length))
                
                if child_depth >= self.warning_depth:
                    self.problematic_tags.append({
                        'tag': child,
                        'parent': tag,
                        'key': i,
                        'depth': child_depth,
                        'path': ' > '.join(child_path)
                    })
                
                self.paths[child_depth].append(" > ".join(child_path))
                
        else:
            return current_depth, path, tag_length
            
        if not depths:
            return current_depth, path, tag_length
            
        max_depth_info = max(depths, key=lambda x: x[0])
        return max_depth_info[0], max_depth_info[1], tag_length

    def create_backup(self, file_path: str) -> str:
        """Create a backup of the original file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def reduce_tag_length(self, tag: Any) -> Any:
        """Reduce the length of a tag while maintaining NBT tag types."""
        if isinstance(tag, nbt.TAG_List):
            mid = len(tag) // 2
            if len(tag) > 0:
                tag_type = type(tag[0])
                new_list = nbt.TAG_List(name=tag.name, type=tag_type)
                for i in range(mid):
                    new_list.append(tag[i])
                return new_list
            return tag
            
        elif isinstance(tag, nbt.TAG_Compound):
            keys = list(tag.keys())
            mid = len(keys) // 2
            new_compound = nbt.TAG_Compound(name=tag.name)
            for key in keys[:mid]:
                new_compound[key] = tag[key]
            return new_compound
            
        return tag

    def analyze_and_fix_nbt_file(self, file_path: str) -> None:
        """Analyze an NBT file and optionally reduce problematic structures."""
        try:
            # Print welcome message
            self.print_header("NBT Depth Analyzer by Decrypt")
            if self.show_full_paths:
                print(f"{Colors.CYAN}Full path display: {Colors.GREEN}Enabled{Colors.ENDC}")
            
            nbtfile = nbt.NBTFile(file_path, "rb")
            max_depth, max_path, total_length = self.get_tag_path_and_length(nbtfile)
            
            # Print analysis results
            self.print_header("Analysis Results")
            self.print_info("File", os.path.basename(file_path))
            self.print_info("Total tags", f"{total_length:,}")
            self.print_info("Maximum depth", max_depth)
            self.print_info("Path to maximum depth", self.format_path(' > '.join(max_path)))
            
            # Show deepest paths
            deep_paths = sorted(self.paths.items(), key=lambda x: x[0], reverse=True)[:3]
            if deep_paths:
                self.print_header("Deepest Structures")
                for depth, paths in deep_paths:
                    print(f"{Colors.BLUE}{Colors.BOLD}Depth {depth}:{Colors.ENDC}")
                    unique_paths = set(paths)
                    for path in list(unique_paths)[:3]:
                        print(f"  {Colors.CYAN}→{Colors.ENDC} {self.format_path(path)}")
            
            # Handle problematic tags
            if self.problematic_tags:
                self.print_warning(
                    f"Found {len(self.problematic_tags)} structure(s) exceeding recommended depth of {self.warning_depth}"
                )
                
                if self.show_full_paths:
                    self.print_header("Problematic Structures")
                    for tag_info in self.problematic_tags[:5]:  # Show first 5 problematic paths
                        print(f"{Colors.YELLOW}Depth {tag_info['depth']}:{Colors.ENDC}")
                        print(f"  {Colors.CYAN}→{Colors.ENDC} {tag_info['path']}")
                    if len(self.problematic_tags) > 5:
                        print(f"\n{Colors.CYAN}... and {len(self.problematic_tags) - 5} more{Colors.ENDC}")
                
                while True:
                    response = input(f"\n{Colors.BOLD}Would you like to attempt to reduce these deep structures? (yes/no):{Colors.ENDC} ").lower()
                    if response in ['yes', 'no']:
                        break
                    self.print_error("Please answer 'yes' or 'no'")
                
                if response == 'yes':
                    backup_path = self.create_backup(file_path)
                    self.print_success(f"Created backup at: {backup_path}")
                    
                    try:
                        modified_count = 0
                        for tag_info in self.problematic_tags:
                            try:
                                reduced_tag = self.reduce_tag_length(tag_info['tag'])
                                if isinstance(tag_info['parent'], nbt.TAG_List):
                                    tag_info['parent'][tag_info['key']] = reduced_tag
                                else:  # TAG_Compound
                                    tag_info['parent'][tag_info['key']] = reduced_tag
                                modified_count += 1
                            except Exception as e:
                                self.print_error(f"Skipped reduction for path {self.format_path(tag_info['path'])}: {str(e)}")
                                continue
                        
                        if modified_count > 0:
                            nbtfile.write_file(file_path)
                            self.print_success(f"Successfully reduced {modified_count} deep structure(s)")
                            print(f"\n{Colors.CYAN}NOTE:{Colors.ENDC} Please verify your game/application still works as expected")
                            print(f"{Colors.CYAN}NOTE:{Colors.ENDC} If you encounter issues, you can restore from the backup: {backup_path}")
                        else:
                            self.print_warning("No structures could be safely reduced")
                            
                    except Exception as e:
                        self.print_error(f"Error while reducing structures: {str(e)}")
                        print(f"\n{Colors.CYAN}NOTE:{Colors.ENDC} No changes were made to your original file")
                        print(f"{Colors.CYAN}NOTE:{Colors.ENDC} The backup is still available at: {backup_path}")
                
        except Exception as e:
            self.print_error(f"Error analyzing NBT file: {str(e)}")
            raise

def main():
    parser = argparse.ArgumentParser(description='NBT Depth Analyzer - Analyze and fix deep NBT structures')
    parser.add_argument('file', help='Path to the NBT file to analyze')
    parser.add_argument('--full-paths', '-f', action='store_true', 
                      help='Show full paths instead of truncated versions')
    parser.add_argument('--warning-depth', '-w', type=int, default=100,
                      help='Depth at which to start warning about deep structures (default: 100)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"{Colors.RED}{Colors.BOLD}Error: File not found: {args.file}{Colors.ENDC}")
        sys.exit(1)
        
    analyzer = NBTAnalyzer(warning_depth=args.warning_depth, show_full_paths=args.full_paths)
    analyzer.analyze_and_fix_nbt_file(args.file)

if __name__ == "__main__":
    main()