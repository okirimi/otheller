from typing import Any


class UIHighlightTracker:
    """Manages UI highlight information."""

    def __init__(self) -> None:
        self.last_move: list[int] | None = None
        self.flipped_stones: list[list[int]] = []

    def update_highlights(
        self,
        last_move: list[int] | None,
        flipped_stones: list[tuple[int, int]],
    ) -> None:
        """
        Update highlight information.

        Parameters
        ----------
        last_move : list[int] | None
            Last move coordinates [row, col]
        flipped_stones : list[tuple[int, int]]
            List of flipped stone coordinates
        """
        self.last_move = last_move
        # Convert to [row, col] format for UI
        self.flipped_stones = [[row, col] for row, col in flipped_stones] if flipped_stones else []

    def clear_highlights(self) -> None:
        """Clear highlight information."""
        self.last_move = None
        self.flipped_stones = []

    def get_highlight_data(self) -> dict[str, Any]:
        """
        Get highlight information.

        Returns
        -------
        dict[str, Any]
            Highlight information dictionary
        """
        return {"last_move": self.last_move, "flipped_stones": self.flipped_stones}
