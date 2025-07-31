from typing import List, Tuple
from ..models.wall import Wall
from ..models.brick import Brick, BrickState


class RobotOptimizer:
    def __init__(self, wall: Wall, robot_reach: float = 1000):
        self.wall = wall
        self.robot_reach = robot_reach  # mm - how far robot can reach from one position
        
    def optimize_build_order(self) -> List[Brick]:
        """Optimize brick building order to minimize robot movement"""
        unbuilt_bricks = [brick for brick in self.wall.bricks if brick.state == BrickState.UNBUILT]
        
        if not unbuilt_bricks:
            return []
            
        optimized_order = []
        remaining_bricks = unbuilt_bricks.copy()
        current_position = 0.0  # Start at left edge
        stride_id = 0
        
        while remaining_bricks:
            # Find all bricks reachable from current position
            reachable_bricks = self._find_reachable_bricks(remaining_bricks, current_position)
            
            if not reachable_bricks:
                # Move to next closest brick
                closest_brick = min(remaining_bricks, key=lambda b: abs(b.position[0] - current_position))
                current_position = closest_brick.position[0]
                stride_id += 1
                continue
            
            # Sort reachable bricks by build priority (left to right, bottom to top)
            reachable_bricks.sort(key=lambda b: (b.course, b.position[0]))
            
            # Assign stride ID and add to optimized order
            for brick in reachable_bricks:
                brick.stride_id = stride_id
                optimized_order.append(brick)
                remaining_bricks.remove(brick)
            
            # Move to center of processed area for next stride
            if reachable_bricks:
                positions = [b.position[0] for b in reachable_bricks]
                current_position = (min(positions) + max(positions)) / 2
                stride_id += 1
        
        return optimized_order
    
    def _find_reachable_bricks(self, bricks: List[Brick], robot_position: float) -> List[Brick]:
        """Find all bricks reachable from current robot position"""
        reachable = []
        
        for brick in bricks:
            brick_center = brick.position[0] + brick.dimensions.length / 2
            distance = abs(brick_center - robot_position)
            
            if distance <= self.robot_reach:
                reachable.append(brick)
        
        return reachable
    
    def calculate_total_movement(self, build_order: List[Brick]) -> float:
        """Calculate total robot movement distance for given build order"""
        if len(build_order) < 2:
            return 0.0
            
        total_distance = 0.0
        current_stride = build_order[0].stride_id
        current_position = build_order[0].position[0]
        
        for brick in build_order[1:]:
            if brick.stride_id != current_stride:
                # Robot moved to new position
                new_position = brick.position[0]
                total_distance += abs(new_position - current_position)
                current_position = new_position
                current_stride = brick.stride_id
        
        return total_distance
    
    def get_stride_info(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Get stride information: (num_strides, [(stride_id, brick_count), ...])"""
        stride_counts = {}
        
        for brick in self.wall.bricks:
            stride_id = brick.stride_id
            stride_counts[stride_id] = stride_counts.get(stride_id, 0) + 1
        
        stride_list = [(stride_id, count) for stride_id, count in sorted(stride_counts.items())]
        return (len(stride_counts), stride_list)