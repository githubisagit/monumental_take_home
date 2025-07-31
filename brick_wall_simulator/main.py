import sys
from .models.wall import Wall
from .models.brick import BrickState
from .visualization.ascii_renderer import ASCIIRenderer
from .optimization.robot_optimizer import RobotOptimizer


class WallSimulator:
    def __init__(self):
        self.wall = Wall()
        self.renderer = ASCIIRenderer(self.wall)
        self.optimizer = RobotOptimizer(self.wall)
        self.show_strides = True
        
    def initialize(self):
        """Initialize the wall and optimize build order"""
        print("Initializing wall construction simulator...")
        print("Generating stretcher bond pattern...")
        
        self.wall.generate_stretcher_bond()
        print(f"Generated {len(self.wall.bricks)} bricks")
        
        print("Optimizing robot build order...")
        optimized_order = self.optimizer.optimize_build_order()
        
        # Update wall brick order based on optimization
        self.wall.bricks = optimized_order
        self.wall.current_brick_index = 0
        
        num_strides, stride_info = self.optimizer.get_stride_info()
        print(f"Optimized into {num_strides} robot strides")
        
        for stride_id, brick_count in stride_info:
            print(f"  Stride {stride_id + 1}: {brick_count} bricks")
        
        total_movement = self.optimizer.calculate_total_movement(optimized_order)
        print(f"Total robot movement: {total_movement:.1f}mm")
        
        print("\nPress ENTER to start building...")
        input()
    
    def build_complete_wall(self):
        """Build all remaining bricks instantly"""
        while not self.wall.is_complete():
            self.wall.build_next_brick()
        print("Wall completed instantly!")
    
    def run_interactive_mode(self):
        """Run the interactive brick-by-brick building mode"""
        while not self.wall.is_complete():
            # Display current state
            self.renderer.display(self.show_strides)
            
            # Get user input
            user_input = input("\nPress ENTER to build next brick, 'f' to fast-forward to complete wall, 's' to toggle strides, 'q' to quit: ").strip().lower()
            
            if user_input == 'q':
                print("Exiting simulator...")
                return
            elif user_input == 's':
                self.show_strides = not self.show_strides
                continue
            elif user_input == 'f':
                self.build_complete_wall()
                break
            elif user_input == '':
                # Build next brick
                next_brick = self.wall.build_next_brick()
                if next_brick:
                    built, total = self.wall.get_progress()
                    print(f"Built brick {built}/{total} at position ({next_brick.position[0]:.0f}, {next_brick.position[1]:.0f})")
            else:
                print("Invalid input. Press ENTER to build, 'f' to fast-forward, 's' to toggle strides, 'q' to quit.")
        
        # Wall complete
        self.renderer.display(self.show_strides)
        print(f"\n🎉 Wall construction complete!")
        print(f"Total bricks built: {len(self.wall.bricks)}")
        
        num_strides, stride_info = self.optimizer.get_stride_info()
        print(f"Robot strides used: {num_strides}")
        
        total_movement = self.optimizer.calculate_total_movement(self.wall.bricks)
        print(f"Total robot movement: {total_movement:.1f}mm")


def main():
    """Main entry point for the brick wall simulator"""
    try:
        simulator = WallSimulator()
        simulator.initialize()
        simulator.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\nSimulator interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()