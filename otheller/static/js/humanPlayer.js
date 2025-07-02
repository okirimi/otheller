/**
 * Human Player Module
 * Handles human player interaction
 */

class HumanPlayer {
  constructor(gameState, uiControls) {
    this.isWaitingForMove = false;
    this.onMoveCallback = null;

    this.gameState = gameState;
    this.uiControls = uiControls;
  }

  startWaitingForMove(callback) {
    this.isWaitingForMove = true;
    this.onMoveCallback = callback;

    this.uiControls.showHumanPrompt(true);

    console.log("DEBUG: Waiting for human move");
  }

  stopWaitingForMove() {
    this.isWaitingForMove = false;
    this.onMoveCallback = null;

    this.uiControls.showHumanPrompt(false);

    console.log("DEBUG: Stopped waiting for human move");
  }

  makeMove(row, col) {
    if (!this.isWaitingForMove) {
      console.log("DEBUG: Not waiting for human move");
      return false;
    }

    if (!this._isValidMove(row, col)) {
      console.log("DEBUG: Invalid move attempted:", row, col);
      return false;
    }

    console.log(`DEBUG: Human move at (${row}, ${col})`);

    this.uiControls.addMoveLog(`👤 人間が (${row}, ${col}) に配置`);

    this.uiControls.showHumanPrompt(false);

    if (this.onMoveCallback) {
      this.onMoveCallback([row, col]);
    }

    this.stopWaitingForMove();

    return true;
  }

  _isValidMove(row, col) {
    const gameState = this.gameState.getState();
    if (!gameState || !gameState.valid_moves) {
      return false;
    }

    return gameState.valid_moves.some(([mr, mc]) => mr === row && mc === col);
  }

  isCurrentPlayerHuman() {
    return this.gameState.isCurrentPlayerHuman() || false;
  }

  onHumanTurn(callback) {
    if (!this.isCurrentPlayerHuman()) {
      console.log("DEBUG: Not human turn");
      return;
    }

    console.log("DEBUG: Human turn started");
    this.startWaitingForMove(callback);
  }

  onHumanTurnEnd() {
    console.log("DEBUG: Human turn ended");
    this.stopWaitingForMove();
  }

  isWaiting() {
    return this.isWaitingForMove;
  }

  createBoardClickHandler() {
    return (row, col) => {
      if (this.isWaitingForMove && this.isCurrentPlayerHuman()) {
        this.makeMove(row, col);
      }
    };
  }

  checkAndHandleHumanTurn(callback) {
    if (!this.gameState.isHumanVsAiMode() || this.gameState.isGameFinished()) {
      return false;
    }

    if (this.gameState.isCurrentPlayerHuman()) {
      this.onHumanTurn(callback);
      return true;
    } else {
      this.onHumanTurnEnd();
      return false;
    }
  }
}

export { HumanPlayer };
export default HumanPlayer;
