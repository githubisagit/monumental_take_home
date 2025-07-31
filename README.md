# Brick Wall Simulator

An interactive Python program that simulates brick wall construction with robot movement optimization. Build walls brick-by-brick while minimizing robot travel distance using an ASCII visualization interface.

## Features

- **Interactive Construction**: Build walls brick-by-brick using the ENTER key
- **Stretcher Bond Pattern**: Automatically generates proper stretcher bond layout
- **Robot Movement Optimization**: Minimizes robot travel distance through intelligent build ordering
- **ASCII Visualization**: Real-time wall display with color-coded built/unbuilt bricks  
- **Stride Visualization**: Color-coded display showing robot position groupings
- **Progress Tracking**: Real-time construction progress and statistics

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Install

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd monumental_take_home
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the package (optional):
   ```bash
   pip install -e .
   ```

## Usage

### Running the Simulator

From the project directory:

```bash
python -m brick_wall_simulator.main
```

Or if you installed the package:

```bash
brick-wall-simulator
```

### Interactive Controls

- **ENTER**: Build the next brick in the optimized sequence
- **'s'**: Toggle stride visualization (shows robot position groupings)  
- **'q'**: Quit the simulator

### Display Legend

- **Red blocks (█)**: Built bricks
- **Gray blocks (░)**: Unbuilt bricks  
- **Colored blocks**: Robot stride groups (when stride mode enabled)

## Technical Specifications

### Wall Dimensions
- **Width**: 2300mm
- **Height**: 2000mm  
- **Pattern**: Stretcher bond

### Brick Specifications
- **Full Brick**: 210mm × 100mm × 50mm
- **Half Brick**: 100mm × 100mm × 50mm
- **Head Joint**: 10mm
- **Bed Joint**: 12.5mm
- **Course Height**: 62.5mm

### Robot Optimization
- **Reach Distance**: 1000mm (configurable)
- **Optimization Goal**: Minimize total travel distance
- **Strategy**: Group bricks by reachable positions, optimize within groups

## Project Structure

```
brick_wall_simulator/
├── models/
│   ├── brick.py          # Brick data structures and dimensions
│   └── wall.py           # Wall generation and management
├── visualization/
│   └── ascii_renderer.py # ASCII art rendering system
├── optimization/
│   └── robot_optimizer.py # Robot movement optimization
├── utils/
└── main.py               # Main application entry point
```

## Algorithm Details

### Stretcher Bond Generation
- Alternating courses with half-brick offsets
- Dynamic brick placement based on wall dimensions
- Proper joint spacing maintained

### Robot Optimization
1. **Reachability Analysis**: Groups bricks by robot reach distance
2. **Stride Formation**: Creates "strides" of bricks buildable from single position
3. **Movement Minimization**: Optimizes robot position sequence
4. **Build Order**: Prioritizes bottom-to-top, left-to-right within strides

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Structure
The simulator follows a modular architecture:
- **Models**: Data structures for bricks and walls
- **Visualization**: ASCII rendering and display logic  
- **Optimization**: Robot movement algorithms
- **Main**: Interactive loop and user interface

## Future Enhancements

Possible extensions mentioned in the original specification:
- Alternative brick bonds (English Cross Bond, Flemish Bond)
- "Wild bond" pattern with complex placement constraints
- Web-based visualization interface
- 3D visualization capabilities
- Advanced robot path planning algorithms

## License

This project is created as a take-home assignment for Monumental.