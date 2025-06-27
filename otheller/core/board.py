from otheller.core.manager import GameManager
from otheller.core.placement import Placement
from otheller.core.score import ScoreCalculator
from otheller.core.state import BoardState


class Board:
    """
    Facade for the Othello game service.

    This class provides a simplified interface to the Othello game system,
    encapsulating all core game functionality including board state management,
    move validation, scoring, and game flow control.

    Attributes
    ----------
    _state : BoardState
        The internal board state representation
    _placement : Placement
        Handler for move validation and placement logic
    _score_calculator : ScoreCalculator
        Calculator for game scores and winner determination
    _game_manager : GameManager
        Manager for game flow and turn control
    """

    def __init__(self) -> None:
        """
        Initialize the Othello board with default starting configuration.

        Sets up all necessary components for game play including board state,
        placement validation, score calculation, and game management.
        """
        self._state = BoardState()
        self._placement = Placement(self._state)
        self._score_calculator = ScoreCalculator(self._state)
        self._game_manager = GameManager(self._state, self._placement)

    @property
    def board(self) -> list[list[int]]:
        """
        Get a copy of the board state to prevent direct modification.

        Returns
        -------
        list[list[int]]
            A 2D list representing the current board state where:
            - 0 represents empty cells
            - 1 represents black player stones
            - 2 represents white player stones
        """
        return self._state.board

    @property
    def size(self) -> int:
        """
        Get the board size.

        Returns
        -------
        int
            The dimension of the square board (typically 8 for standard Othello)
        """
        return self._state.size

    @property
    def current_player(self) -> int:
        """
        Get the current player.

        Returns
        -------
        int
            The current player identifier:
            - 1 for black player
            - 2 for white player
            - 0 if game has ended
        """
        return self._game_manager.current_player

    def is_valid_move(
        self,
        target_row: int,
        target_col: int,
        current_player: int | None = None,
    ) -> bool:
        """
        Check if placing a stone at the specified position is a valid move.

        Parameters
        ----------
        target_row : int
            The row index where the stone would be placed (0-based)
        target_col : int
            The column index where the stone would be placed (0-based)
        current_player : int, optional
            The player making the move. If None, uses the current active player

        Returns
        -------
        bool
            True if the move is valid and would capture at least one opponent stone,
            False otherwise
        """
        if self._game_manager.is_game_ended():
            return False

        if current_player is None:
            current_player = self._game_manager.current_player

        return self._placement.is_valid_placement(target_row, target_col, current_player)

    def get_score(self) -> tuple[int, int]:
        """
        Get the current score as (black_count, white_count).

        Returns
        -------
        tuple[int, int]
            A tuple containing (black_stones_count, white_stones_count)
        """
        return self._score_calculator.get_score()

    def make_move(
        self,
        target_row: int,
        target_col: int,
        current_player: int | None = None,
    ) -> bool:
        """
        Place a stone at the specified position and flip captured stones.

        Parameters
        ----------
        target_row : int
            The row index where the stone will be placed (0-based)
        target_col : int
            The column index where the stone will be placed (0-based)
        current_player : int, optional
            The player making the move. If None, uses the current active player

        Returns
        -------
        bool
            True if the move was successfully executed, False if invalid

        Notes
        -----
        This method will automatically flip all captured opponent stones
        and advance the turn to the next player. If the next player has
        no valid moves, the turn will pass back. If neither player can
        move, the game ends.
        """
        if self._game_manager.is_game_ended():
            return False

        return self._game_manager.place_and_flip(target_row, target_col, current_player)

    def is_game_ended(self) -> bool:
        """
        Check if the game has ended.

        Returns
        -------
        bool
            True if neither player can make a valid move, False otherwise
        """
        return self._game_manager.is_game_ended()

    def get_valid_moves(self, player: int | None = None) -> list[tuple[int, int]]:
        """
        Get all valid moves for the specified player.

        Parameters
        ----------
        player : int, optional
            The player to get valid moves for. If None, uses the current active player

        Returns
        -------
        list[tuple[int, int]]
            A list of (row, col) tuples representing all valid move positions
            for the specified player
        """
        if player is None:
            player = self._game_manager.current_player
        return self._placement.get_valid_placements(player)
