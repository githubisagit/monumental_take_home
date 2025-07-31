from typing import List, Tuple, Optional
from .brick import Brick, BrickType, BrickState, HEAD_JOINT, BED_JOINT, COURSE_HEIGHT


class Wall:
    def __init__(self, width: float = 2300, height: float = 2000):
        self.width = width  # mm
        self.height = height  # mm
        self.bricks: List[Brick] = []
        self.current_brick_index = 0
        
    def generate_stretcher_bond(self):
        """Generate all bricks for stretcher bond pattern"""
        self.bricks = []
        
        # Calculate number of courses
        num_courses = int(self.height / COURSE_HEIGHT)
        
        for course in range(num_courses):
            y_position = course * COURSE_HEIGHT
            
            # Stretcher bond: alternate courses offset by half brick
            if course % 2 == 0:
                # Even courses start with full brick
                self._add_course_bricks(course, y_position, 0)
            else:
                # Odd courses start with half brick offset
                self._add_course_bricks(course, y_position, BrickType.HALF.value)
    
    def _add_course_bricks(self, course: int, y_position: float, offset_type: str):
        """Add bricks for a single course"""
        x_position = 0
        brick_index = 0
        
        # Start with offset brick if needed
        if offset_type == BrickType.HALF.value:
            half_brick = Brick(
                brick_type=BrickType.HALF,
                position=(x_position, y_position),
                course=course
            )
            self.bricks.append(half_brick)
            x_position += half_brick.dimensions.length + HEAD_JOINT
            brick_index += 1
        
        # Add full bricks
        while x_position + 210 <= self.width:  # Full brick length
            brick = Brick(
                brick_type=BrickType.FULL,
                position=(x_position, y_position),
                course=course
            )
            self.bricks.append(brick)
            x_position += brick.dimensions.length + HEAD_JOINT
            brick_index += 1
        
        # Add final half brick if space remains
        remaining_space = self.width - x_position
        if remaining_space >= 100:  # Half brick length
            half_brick = Brick(
                brick_type=BrickType.HALF,
                position=(x_position, y_position),
                course=course
            )
            self.bricks.append(half_brick)
    
    def build_next_brick(self) -> Optional[Brick]:
        """Build the next brick in sequence"""
        if self.current_brick_index < len(self.bricks):
            brick = self.bricks[self.current_brick_index]
            brick.state = BrickState.BUILT
            self.current_brick_index += 1
            return brick
        return None
    
    def get_built_bricks(self) -> List[Brick]:
        """Get all built bricks"""
        return [brick for brick in self.bricks if brick.state == BrickState.BUILT]
    
    def get_unbuilt_bricks(self) -> List[Brick]:
        """Get all unbuilt bricks"""
        return [brick for brick in self.bricks if brick.state == BrickState.UNBUILT]
    
    def is_complete(self) -> bool:
        """Check if wall construction is complete"""
        return self.current_brick_index >= len(self.bricks)
    
    def get_progress(self) -> Tuple[int, int]:
        """Get construction progress (built, total)"""
        return (self.current_brick_index, len(self.bricks))