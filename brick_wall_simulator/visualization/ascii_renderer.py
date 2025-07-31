import os
from typing import List, Dict
from colorama import init, Fore, Back, Style
from ..models.wall import Wall
from ..models.brick import Brick, BrickState, BrickType

init(autoreset=True)


class ASCIIRenderer:
    def __init__(self, wall: Wall, scale_factor: float = 0.1):
        self.wall = wall
        self.scale_factor = scale_factor  # mm to character ratio
        
        # Calculate display dimensions
        self.display_width = int(wall.width * scale_factor)
        self.display_height = int(wall.height * scale_factor)
        
        # Color mapping for stride visualization
        self.stride_colors = [
            Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, 
            Fore.MAGENTA, Fore.CYAN, Fore.WHITE
        ]
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_wall(self, show_strides: bool = False) -> str:
        """Render the wall as ASCII art"""
        # Create display grid
        grid = [[' ' for _ in range(self.display_width)] for _ in range(self.display_height)]
        
        # Draw each brick
        for brick in self.wall.bricks:
            self._draw_brick(grid, brick, show_strides)
        
        # Convert grid to string
        lines = []
        for row in reversed(grid):  # Reverse to show wall right-side up
            lines.append(''.join(row))
        
        return '\n'.join(lines)
    
    def _draw_brick(self, grid: List[List[str]], brick: Brick, show_strides: bool):
        """Draw a single brick on the grid"""
        # Scale brick position and dimensions
        x1 = int(brick.position[0] * self.scale_factor)
        y1 = int(brick.position[1] * self.scale_factor)
        x2 = int((brick.position[0] + brick.dimensions.length) * self.scale_factor)
        y2 = int((brick.position[1] + brick.dimensions.width) * self.scale_factor)
        
        # Clamp to grid bounds
        x1 = max(0, min(x1, self.display_width - 1))
        x2 = max(0, min(x2, self.display_width))
        y1 = max(0, min(y1, self.display_height - 1))
        y2 = max(0, min(y2, self.display_height))
        
        # Choose character and color based on brick state
        if brick.state == BrickState.BUILT:
            if show_strides:
                color = self.stride_colors[brick.stride_id % len(self.stride_colors)]
                char = f"{color}█{Style.RESET_ALL}"
            else:
                char = f"{Fore.RED}█{Style.RESET_ALL}"  # Built bricks in dark/red
        else:
            char = f"{Fore.LIGHTBLACK_EX}░{Style.RESET_ALL}"  # Unbuilt bricks in light
        
        # Fill brick area
        for y in range(y1, y2):
            for x in range(x1, x2):
                if y < len(grid) and x < len(grid[0]):
                    # Draw borders
                    if y == y1 or y == y2 - 1 or x == x1 or x == x2 - 1:
                        if brick.state == BrickState.BUILT:
                            grid[y][x] = f"{Fore.WHITE}─{Style.RESET_ALL}" if y == y1 or y == y2 - 1 else f"{Fore.WHITE}│{Style.RESET_ALL}"
                        else:
                            grid[y][x] = f"{Fore.LIGHTBLACK_EX}─{Style.RESET_ALL}" if y == y1 or y == y2 - 1 else f"{Fore.LIGHTBLACK_EX}│{Style.RESET_ALL}"
                    else:
                        grid[y][x] = char
    
    def render_info_panel(self) -> str:
        """Render information panel"""
        built, total = self.wall.get_progress()
        progress_percent = (built / total * 100) if total > 0 else 0
        
        info = [
            f"{Fore.CYAN}=== BRICK WALL SIMULATOR ==={Style.RESET_ALL}",
            f"Wall Dimensions: {self.wall.width}mm x {self.wall.height}mm",
            f"Progress: {built}/{total} bricks ({progress_percent:.1f}%)",
            f"Pattern: Stretcher Bond",
            "",
            f"{Fore.RED}█{Style.RESET_ALL} Built bricks",
            f"{Fore.LIGHTBLACK_EX}░{Style.RESET_ALL} Unbuilt bricks",
            "",
            "Press ENTER to build next brick, 'q' to quit"
        ]
        
        return '\n'.join(info)
    
    def render_stride_legend(self, num_strides: int) -> str:
        """Render legend for stride colors"""
        if num_strides == 0:
            return ""
            
        legend = [f"{Fore.CYAN}=== ROBOT STRIDES ==={Style.RESET_ALL}"]
        for i in range(min(num_strides, len(self.stride_colors))):
            color = self.stride_colors[i]
            legend.append(f"{color}█{Style.RESET_ALL} Stride {i + 1}")
        
        return '\n'.join(legend)
    
    def display(self, show_strides: bool = False):
        """Display the complete visualization"""
        self.clear_screen()
        
        # Render main display
        wall_display = self.render_wall(show_strides)
        info_panel = self.render_info_panel()
        
        print(info_panel)
        print()
        print(wall_display)
        
        # Show stride legend if needed
        if show_strides:
            max_stride = max([brick.stride_id for brick in self.wall.bricks] + [0])
            if max_stride > 0:
                print()
                print(self.render_stride_legend(max_stride + 1))