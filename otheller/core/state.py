# constants
BOARD_SIZE: int = 8
EMPTY_CELL: int = 0
BLACK_PLAYER: int = 1
WHITE_PLAYER: int = 2
GAME_ENDED_MARKER: int = 0


class BoardState:
    """
    Represents the state of an Othello board.

    This class manages the internal representation of the game board,
    including the positions of all stones and basic board operations.
    It maintains the 8x8 grid and provides methods for accessing and
    modifying board positions while ensuring data integrity.

    Attributes
    ----------
    _size : int
        The dimension of the square board (8 for standard Othello)
    _board : list[list[int]]
        A 2D list representing the board state where:
        - 0 represents empty cells
        - 1 represents black player stones
        - 2 represents white player stones
    """

    def __init__(self) -> None:
        """
        Initialize the board with the standard Othello starting position.

        Creates an 8x8 board with four stones in the center:
        - White stones at positions (3,3) and (4,4)
        - Black stones at positions (3,4) and (4,3)
        """
        self._size: int = BOARD_SIZE
        self._board: list[list[int]] = self._initialize_board()

    def _initialize_board(self) -> list[list[int]]:
        """
        Create the initial board state.

        Sets up a standard Othello starting position with four stones
        placed in the center of the board in a diagonal pattern.

        Returns
        -------
        list[list[int]]
            A 2D list representing the initial board configuration
        """
        board: list[list[int]] = [
            [EMPTY_CELL for _ in range(self._size)] for _ in range(self._size)
        ]

        # Initial stone placement
        center: int = self._size // 2
        board[center - 1][center - 1] = WHITE_PLAYER
        board[center - 1][center] = BLACK_PLAYER
        board[center][center - 1] = BLACK_PLAYER
        board[center][center] = WHITE_PLAYER

        return board

    @property
    def size(self) -> int:
        """
        Get the board size.

        Returns
        -------
        int
            The dimension of the square board (8 for standard Othello)
        """
        return self._size

    @property
    def board(self) -> list[list[int]]:
        """
        Get a copy of the board state.

        Returns a defensive copy to prevent external modification
        of the internal board state.

        Returns
        -------
        list[list[int]]
            A deep copy of the current board state where each cell contains:
            - 0 for empty cells
            - 1 for black player stones
            - 2 for white player stones
        """
        return [row[:] for row in self._board]

    def count_stones(self, player: int) -> int:
        """
        Count the number of stones for a specific player.

        Scans the entire board and counts how many cells contain
        stones belonging to the specified player.

        Parameters
        ----------
        player : int
            The player to count stones for (1 for black, 2 for white)

        Returns
        -------
        int
            The total number of stones the player has on the board
        """
        return sum(row.count(player) for row in self._board)

    def get_cell_value(self, row: int, col: int) -> int:
        """
        Get the value of a specific cell.

        Parameters
        ----------
        row : int
            The row index (0-based)
        col : int
            The column index (0-based)

        Returns
        -------
        int
            The value at the specified position:
            - 0 for empty cell
            - 1 for black player stone
            - 2 for white player stone

        Notes
        -----
        No bounds checking is performed. Use is_within_board() first
        to ensure the coordinates are valid.
        """
        return self._board[row][col]

    def is_within_board(self, row: int, col: int) -> bool:
        """
        Check if the given position is within board boundaries.

        Parameters
        ----------
        row : int
            The row index to check
        col : int
            The column index to check

        Returns
        -------
        bool
            True if the position is within the board boundaries,
            False otherwise
        """
        return 0 <= row < self._size and 0 <= col < self._size

    def set_cell_value(self, row: int, col: int, value: int) -> None:
        """
        Set the value of a specific cell.

        Directly modifies the board state at the specified position.
        This method should be used carefully as it does not perform
        validation of the move according to game rules.

        Parameters
        ----------
        row : int
            The row index (0-based)
        col : int
            The column index (0-based)
        value : int
            The value to set:
            - 0 for empty cell
            - 1 for black player stone
            - 2 for white player stone

        Notes
        -----
        No bounds checking is performed. Use is_within_board() first
        to ensure the coordinates are valid.
        """
        self._board[row][col] = value
