from otheller.core.state import BLACK_PLAYER, EMPTY_CELL, WHITE_PLAYER, BoardState


class ScoreCalculator:
    """
    Handles score calculation and winner determination.

    This class provides functionality to calculate the current score
    of each player and determine the winner of a completed game.
    Scores are based on the number of stones each player has on the board.

    Attributes
    ----------
    _state : BoardState
        Reference to the board state for stone counting
    """

    def __init__(self, state: BoardState) -> None:
        """
        Initialize the score calculator.

        Parameters
        ----------
        state : BoardState
            The board state object to calculate scores from
        """
        self._state = state

    def get_score(self) -> tuple[int, int]:
        """
        Get the current score of each player.

        Counts the number of stones for each player currently on the board.

        Returns
        -------
        tuple[int, int]
            A tuple containing (black_stones_count, white_stones_count)
            representing the current score for each player
        """
        black_count: int = self._state.count_stones(BLACK_PLAYER)
        white_count: int = self._state.count_stones(WHITE_PLAYER)
        return (black_count, white_count)

    def get_winner(self) -> int:
        """
        Get the winner of the game.

        Determines the winner based on who has more stones on the board.
        Should typically be called when the game has ended.

        Returns
        -------
        int
            The winner identifier:
            - 1 (BLACK_PLAYER) if black has more stones
            - 2 (WHITE_PLAYER) if white has more stones
            - 0 (EMPTY_CELL) if the game is tied

        Notes
        -----
        In standard Othello, the player with the most stones when
        neither player can make a valid move is declared the winner.
        """
        black_count, white_count = self.get_score()

        if black_count > white_count:
            return BLACK_PLAYER
        # Although using `elif` here is not required for performance,
        # it improves readability by clearly indicating that the conditions are mutually exclusive.
        elif white_count > black_count:  # noqa: RET505
            return WHITE_PLAYER
        else:
            return EMPTY_CELL  # Tie game
