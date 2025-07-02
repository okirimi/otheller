from typing import Any


class HumanVsAIController:
    """Controller for human vs AI game logic."""

    def __init__(self) -> None:
        self.is_human_vs_ai = False
        self.human_player = 1
        self.waiting_for_human = False

    def setup_human_vs_ai(self, human_player: int) -> None:
        """
        Setup human vs AI game.

        Parameters
        ----------
        human_player : int
            Human player number (1: black, 2: white)
        """
        self.is_human_vs_ai = True
        self.human_player = human_player
        self.waiting_for_human = False

    def setup_ai_vs_ai(self) -> None:
        """Setup AI vs AI game."""
        self.is_human_vs_ai = False
        self.waiting_for_human = False

    def is_human_turn(self, current_player: int) -> bool:
        """
        Check if current turn belongs to human player.

        Parameters
        ----------
        current_player : int
            Current player

        Returns
        -------
        bool
            True if it's human's turn
        """
        return self.is_human_vs_ai and current_player == self.human_player

    def set_waiting_for_human(self, *, waiting: bool) -> None:
        """
        Set waiting for human input state.

        Parameters
        ----------
        waiting : bool
            Waiting state
        """
        self.waiting_for_human = waiting

    def get_state_data(self) -> dict[str, Any]:
        """
        Get human vs AI control state data.

        Returns
        -------
        dict[str, Any]
            State data dictionary
        """
        return {
            "is_human_vs_ai": self.is_human_vs_ai,
            "human_player": self.human_player,
            "waiting_for_human": self.waiting_for_human,
        }
