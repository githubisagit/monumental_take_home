from enum import Enum
from dataclasses import dataclass
from typing import Tuple


class BrickType(Enum):
    FULL = "full"
    HALF = "half"


class BrickState(Enum):
    UNBUILT = "unbuilt"
    BUILT = "built"


@dataclass
class BrickDimensions:
    length: float
    width: float  
    height: float


BRICK_DIMENSIONS = {
    BrickType.FULL: BrickDimensions(210, 100, 50),  # mm
    BrickType.HALF: BrickDimensions(100, 100, 50),  # mm
}

HEAD_JOINT = 10  # mm
BED_JOINT = 12.5  # mm
COURSE_HEIGHT = 50 + BED_JOINT  # brick height + bed joint = 62.5mm


@dataclass
class Brick:
    brick_type: BrickType
    position: Tuple[float, float]  # (x, y) in mm
    course: int  # course number (0-based)
    state: BrickState = BrickState.UNBUILT
    stride_id: int = 0  # for robot movement optimization
    
    @property
    def dimensions(self) -> BrickDimensions:
        return BRICK_DIMENSIONS[self.brick_type]
    
    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Returns (x1, y1, x2, y2) bounds of the brick"""
        dims = self.dimensions
        x1, y1 = self.position
        x2 = x1 + dims.length
        y2 = y1 + dims.width
        return (x1, y1, x2, y2)