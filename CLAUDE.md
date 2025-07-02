# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup

```bash
# Install dependencies using uv
uv sync

# Install development dependencies (included in uv sync)
# Includes: mypy>=1.16.1, ruff>=0.12.0
```

### Running the Application

```bash
# Start the Flask web server (default port 5001)
python -m otheller.main

# With specific log level
python -m otheller.main --log DEBUG
python -m otheller.main --log INFO    # default
python -m otheller.main --log ERROR
```

### Code Quality & Linting

```bash
# Format code with ruff (99 char line length, double quotes)
ruff format

# Lint with ruff (comprehensive ruleset with ALL rules enabled)
ruff check

# Fix auto-fixable lint issues
ruff check --fix

# Type check with mypy (strict type checking enabled)
mypy otheller/

# Format JavaScript/CSS with prettier
yarn prettier --write .
```

### Testing

The codebase does not appear to have a formal test suite configured. Tests would need to be added manually.

## Architecture Overview

Otheller is a web-based Othello game platform with a layered architecture designed for AI strategy development and gameplay.

### Core Architecture Pattern: Facade + Strategy

The system uses a **Facade pattern** where `Board` (otheller/core/board.py) serves as the main interface to all game functionality. This facade coordinates between:

- **BoardState**: 8x8 game board representation
- **GameManager**: Turn management and move execution
- **Placement**: Move validation and legality checking
- **ScoreCalculator**: Scoring and winner determination
- **GameSimulator**: Move preview and simulation capabilities

### Strategy System

AI strategies implement the **Strategy pattern** via `StrategyBase` (otheller/strategy.py):

- Users upload custom `.py` files with `MyStrategy` class
- Strategies receive `Board` facade and return `(row, col)` moves
- System supports both AI vs AI and Human vs AI gameplay

### Web Architecture

**Flask Application** (otheller/main.py):

- REST API endpoints for game operations
- Dynamic strategy loading from uploaded files
- File upload handling for custom AI strategies

**WebGameController** (otheller/web/controller.py):

- Main orchestrator using dependency injection
- Coordinates: game state persistence, UI highlighting, human vs AI control
- Manages game flow between frontend and core engine

**Frontend** (otheller/static/):

- Modular JavaScript architecture with separate concerns:
  - `apiClient.js`: HTTP communication
  - `boardRenderer.js`: Visual board rendering
  - `gameLogic.js`: Client-side game rules
  - `gameState.js`: State management
  - `humanPlayer.js`: Human input handling

### Key Data Flow

1. **Strategy Upload**: Users upload `.py` files → Flask validates → Dynamically imports `MyStrategy` class
2. **Move Execution**: Strategy returns move → `WebGameController` → `Board` facade → Core engine components
3. **State Persistence**: Game state automatically saved/restored via `GameStatePersistence`
4. **UI Updates**: Core state changes → `WebGameController` → JSON API → Frontend rendering

### Critical Implementation Details

**Board Facade Interface**:

- `board.get_valid_moves(player)` - Returns list of legal moves
- `board.make_move(row, col, player)` - Executes move with validation
- `board.is_game_ended()` - Checks for game termination
- `Board.create_copy(board)` - Creates simulation copy

**Strategy Development**:

- Custom strategies must implement `choose_move(board: Board) -> tuple[int, int] | None`
- Return `None` for pass/no valid moves
- Access board state via facade methods, not direct board access

**Game State Management**:

- Automatic pass handling when no valid moves available
- Turn switching managed by `GameManager`
- Game end detection when neither player can move
- State persistence across web sessions

## Configuration Notes

- **Python**: Requires >=3.12
- **Code Style**: 99 character line length, double quotes, 4-space indentation
- **Type Checking**: Strict mypy configuration with untyped definitions disallowed
- **Linting**: Comprehensive ruff rules (ALL enabled) with specific ignores for docstrings and print statements
- **Package Management**: Uses `uv` for dependency management
- **Web Server**: Flask runs on port 5001 (avoiding macOS AirPlay receiver on 5000)

The system prioritizes clean separation of concerns, type safety, and extensibility for AI strategy development.
