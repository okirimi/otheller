from otheller.cli import logger
from otheller.core.board import Board


class StrategyBase:
    """Base class for Othello strategies."""

    def __init__(self, player: int) -> None:
        self.player = player  # 1: black, 2: white

    def choose_move(self, board: Board) -> tuple[int, int] | None:
        """Choose a move based on the board state."""
        # Subclass must be implement this method
        msg = "Subclass must implement this method"
        raise NotImplementedError(msg)


class ManualStrategy(StrategyBase):
    def choose_move(self, board: Board) -> tuple[int, int] | None:
        valid_moves: list[tuple[int, int]] = board.get_valid_moves(self.player)
        if not valid_moves:
            logger.debug("打てる場所がありません。パスします。")
            return None

        # Build the message with valid moves
        move_strs = [f"{move}" for move in valid_moves]
        logger.debug("打てる場所: " + ", ".join(move_strs))

        while True:
            try:
                row = int(input("行を入力してください: "))
                col = int(input("列を入力してください: "))

                if (row, col) in valid_moves:
                    return (row, col)
                logger.debug("その場所には置けません。もう一度選んでください。")
            except ValueError:
                logger.debug("数字を入力してください。")
