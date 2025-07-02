from typing import Any

from otheller.cli import logger
from otheller.core.board import Board
from otheller.core.simulator import GameSimulator
from otheller.web.highlight import UIHighlightTracker
from otheller.web.persistence import GameStatePersistence
from otheller.web.vs_ai import HumanVsAIController


class WebGameController:
    """
    Main game controller for Web API.

    Combines other classes to provide game control for Web API.
    """

    def __init__(self, state_file_path: str) -> None:
        self.board: Board | None = None
        self.strategy1 = None
        self.strategy2 = None
        self.player1_name = ""
        self.player2_name = ""
        self.move_count = 0
        self.strategy1_file = None
        self.strategy2_file = None

        # Dependency injection for separated responsibilities
        self.state_persistence = GameStatePersistence(state_file_path)
        self.highlight_tracker = UIHighlightTracker()
        self.human_vs_ai_controller = HumanVsAIController()

    def start_game(  # noqa: PLR0913
        self,
        strategy1: Any,  # noqa: ANN401
        strategy2: Any,  # noqa: ANN401
        name1: str,
        name2: str,
        *,
        human_vs_ai: bool = False,
        human_player: int = 1,
        strategy1_file: str | None = None,
        strategy2_file: str | None = None,
    ) -> None:
        """
        Start a new game.

        Parameters
        ----------
        strategy1 : Any
            Strategy for player 1
        strategy2 : Any
            Strategy for player 2
        name1 : str
            Name of player 1
        name2 : str
            Name of player 2
        human_vs_ai : bool, optional
            Whether this is human vs AI mode
        human_player : int, optional
            Human player number
                 strategy1_file : str | None, optional
             Strategy file path for player 1
         strategy2_file : str | None, optional
             Strategy file path for player 2
        """
        self.board = Board()
        self.strategy1 = strategy1
        self.strategy2 = strategy2
        self.player1_name = name1
        self.player2_name = name2
        self.move_count = 0
        self.strategy1_file = strategy1_file
        self.strategy2_file = strategy2_file

        # Setup human vs AI control
        if human_vs_ai:
            self.human_vs_ai_controller.setup_human_vs_ai(human_player)
        else:
            self.human_vs_ai_controller.setup_ai_vs_ai()

        # Initialize highlight information
        self.highlight_tracker.clear_highlights()

        # Save state
        self.save_state()

    def save_state(self) -> bool:
        """
        Save current game state.

        Returns
        -------
        bool
            True if save was successful
        """
        state_data = {
            "board_state": self.board.board if self.board else None,
            "current_player": self.board.current_player if self.board else None,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "move_count": self.move_count,
            "strategy1_file": self.strategy1_file,
            "strategy2_file": self.strategy2_file,
            **self.highlight_tracker.get_highlight_data(),
            **self.human_vs_ai_controller.get_state_data(),
        }
        return self.state_persistence.save_state(state_data)

    def load_state(self) -> bool:
        """
        Restore game state from saved data.

        Returns
        -------
        bool
            True if restore was successful
        """
        state_data = self.state_persistence.load_state()
        if not state_data:
            return False

        try:
            # Restore basic information
            self.player1_name = state_data.get("player1_name", "")
            self.player2_name = state_data.get("player2_name", "")
            self.move_count = state_data.get("move_count", 0)
            self.strategy1_file = state_data.get("strategy1_file")
            self.strategy2_file = state_data.get("strategy2_file")

            # Restore highlight information
            self.highlight_tracker.last_move = state_data.get("last_move")
            self.highlight_tracker.flipped_stones = state_data.get("flipped_stones", [])

            # Restore human vs AI information
            if state_data.get("is_human_vs_ai", False):
                self.human_vs_ai_controller.setup_human_vs_ai(state_data.get("human_player", 1))
            else:
                self.human_vs_ai_controller.setup_ai_vs_ai()
            self.human_vs_ai_controller.set_waiting_for_human(
                waiting=state_data.get("waiting_for_human", False),
            )

            # Restore board state
            if state_data.get("board_state"):
                self.board = Board()
                snapshot = {
                    "board": state_data["board_state"],
                    "current_player": state_data.get("current_player", 1),
                }
                self.board.restore_from_snapshot(snapshot)

                # Reload strategies
                if self.strategy_manager is not None:
                    if self.strategy1_file:
                        self.strategy1 = self.strategy_manager.load_strategy_from_file(
                            self.strategy1_file,
                            1,
                        )
                    if self.strategy2_file:
                        self.strategy2 = self.strategy_manager.load_strategy_from_file(
                            self.strategy2_file,
                            2,
                        )

        except Exception as e:
            msg = f"Failed to load game state: {e}"
            logger.exception(msg)
            return False
        else:
            return True

    def make_move_with_tracking(self, row: int, col: int, player: int) -> bool:
        """
        Execute a move and record highlight information.

        Parameters
        ----------
        row : int
            Row coordinate
        col : int
            Column coordinate
        player : int
            Player number

        Returns
        -------
        bool
            True if successful
        """
        if not self.board or not self.board.is_valid_move(row, col, player):
            return False

        # Use core/simulator to preview flipped stones for UI display
        success, flipped_stones_tuples = GameSimulator.simulate_move_preview(
            self.board,
            row,
            col,
            player,
        )
        if not success:
            return False

        # Update highlight information
        self.highlight_tracker.update_highlights([row, col], flipped_stones_tuples)

        # Actually execute the move
        return self.board.make_move(row, col, player)

    def get_current_state(self) -> dict[str, Any] | None:
        """
        Get current game state.

        Returns
        -------
                 dict[str, Any] | None
             Game state dictionary, None if board doesn't exist
        """
        if not self.board:
            return None

        # Calculate scores using core/ScoreCalculator
        black_score, white_score = self.board.get_score()

        # Get valid moves for current player
        valid_moves = []
        if self.board.current_player > 0:
            valid_moves_tuples = self.board.get_valid_moves(self.board.current_player)
            valid_moves = [[row, col] for row, col in valid_moves_tuples]

        # Check game end and winner using core/ logic
        is_game_over = self.board.is_game_ended()
        winner = None
        if is_game_over:
            winner = self.board.get_winner()

        return {
            "board": [row[:] for row in self.board.board],  # Board copy
            "current_player": self.board.current_player,
            "black_score": black_score,
            "white_score": white_score,
            "valid_moves": valid_moves,
            "is_game_over": is_game_over,
            "winner": winner,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "move_count": self.move_count,
            **self.highlight_tracker.get_highlight_data(),
            **self.human_vs_ai_controller.get_state_data(),
        }

    def make_next_move(self, human_move: list[int] | None = None) -> dict[str, Any] | None:  # noqa: PLR0911
        """
        Execute the next move.

        Parameters
        ----------
                 human_move : list[int] | None, optional
             Human move [row, col]

         Returns
         -------
         dict[str, Any] | None
             Game state after move execution
        """
        if not self.board or self.board.is_game_ended():
            return None

        current_player = self.board.current_player

        # Determine if it's human or AI turn
        if self.human_vs_ai_controller.is_human_turn(current_player):
            if human_move is None:
                self.human_vs_ai_controller.set_waiting_for_human(waiting=True)
                self.save_state()
                return self.get_current_state()
            # Execute human move
            row, col = human_move
            if self.make_move_with_tracking(row, col, current_player):
                self.move_count += 1
                self.human_vs_ai_controller.set_waiting_for_human(waiting=False)
                self.save_state()
                return self.get_current_state()
            return None
        # Execute AI move
        strategy = self.strategy1 if current_player == 1 else self.strategy2

        try:
            # Check valid moves
            valid_moves_tuples = self.board.get_valid_moves(current_player)
            valid_moves = [[row, col] for row, col in valid_moves_tuples]

            if not valid_moves:
                # Pass handling is done automatically by core/GameManager
                # Clear highlight information for pass
                self.highlight_tracker.clear_highlights()
                self.save_state()
                return self.get_current_state()

            move = strategy.choose_move(self.board)

            # Check if move has at least row and column coordinates
            if (
                move and len(move) >= 2  # noqa: PLR2004
            ):
                row, col = move[0], move[1]

                success = self.make_move_with_tracking(row, col, current_player)

                if success:
                    self.move_count += 1
                    self.save_state()
                    return self.get_current_state()
                return None
            # Pass handling
            self.highlight_tracker.clear_highlights()
            self.save_state()
            return self.get_current_state()

        except Exception as e:
            msg = f"Failed to make next move: {e}"
            logger.exception(msg)
            return None

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = None
        self.strategy1 = None
        self.strategy2 = None
        self.strategy1_file = None
        self.strategy2_file = None
        self.human_vs_ai_controller.setup_ai_vs_ai()
        self.highlight_tracker.clear_highlights()

        # Clear saved state file
        self.state_persistence.clear_state()
