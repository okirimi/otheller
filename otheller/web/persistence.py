import pickle
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from otheller.cli import logger


class GameStatePersistence:
    """Handles game state persistence."""

    def __init__(self, state_file_path: str) -> None:
        self.state_file_path = state_file_path
        self.key_file_path = state_file_path + ".key"
        self._cipher = self._get_or_create_cipher()

    def _get_or_create_cipher(self) -> Fernet:
        """Get or create encryption cipher."""
        key_path = Path(self.key_file_path)
        if key_path.exists():
            with key_path.open("rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with key_path.open("wb") as f:
                f.write(key)
        return Fernet(key)

    def save_state(self, game_data: dict[str, Any]) -> bool:
        """
        Save game state to file.

        Parameters
        ----------
        game_data : dict[str, Any]
            Game data to save

        Returns
        -------
        bool
            True if save was successful
        """
        try:
            # Pickle data first, then encrypt
            pickled_data = pickle.dumps(game_data)
            encrypted_data = self._cipher.encrypt(pickled_data)

            with Path(self.state_file_path).open("wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            msg = f"Failed to save game state: {e}"
            logger.exception(msg)
            return False
        else:
            return True

    def load_state(self) -> dict[str, Any] | None:
        """
        Restore game state from file.

        Returns
        -------
                 dict[str, Any] | None
             Restored game data, None if file doesn't exist or error occurs
        """
        try:
            if not Path(self.state_file_path).exists():
                return None

            with Path(self.state_file_path).open("rb") as f:
                encrypted_data = f.read()

            decrypted_data = self._cipher.decrypt(encrypted_data)

            # the payload is verified using a shared secret before deserialization,
            # mitigating the security risk
            return pickle.loads(decrypted_data)  # noqa: S301
        except Exception as e:
            msg = f"Failed to load game state: {e}"
            logger.exception(msg)
            return None

    def clear_state(self) -> bool:
        """
        Delete saved state file.

        Returns
        -------
        bool
            True if deletion was successful
        """
        try:
            if Path(self.state_file_path).exists():
                Path(self.state_file_path).unlink()
            if Path(self.key_file_path).exists():
                Path(self.key_file_path).unlink()
        except Exception as e:
            msg = f"Failed to clear game state: {e}"
            logger.exception(msg)
            return False
        else:
            return True
