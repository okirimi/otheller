/**
 * Board Renderer Module
 * Handles board rendering and visual effects
 */

class BoardRenderer {
  constructor() {
    this.boardElement = null;
  }

  setBoardElement(element) {
    this.boardElement = element;
  }

  renderBoard(gameState, onCellClick = null) {
    if (!this.boardElement || !gameState) return;

    this.boardElement.innerHTML = "";

    for (let r = 0; r < 8; r++) {
      for (let c = 0; c < 8; c++) {
        const cell = document.createElement("div");
        cell.className = "cell";

        if (gameState.last_move && gameState.last_move[0] === r && gameState.last_move[1] === c) {
          cell.classList.add("last-move");
        }

        if (gameState.board[r][c] === 1) {
          this._renderBlackStone(cell, gameState, r, c);
        } else if (gameState.board[r][c] === 2) {
          this._renderWhiteStone(cell, gameState, r, c);
        } else if (gameState.valid_moves && gameState.valid_moves.some(([mr, mc]) => mr === r && mc === c)) {
          this._renderValidMove(cell, r, c, onCellClick);
        }

        this.boardElement.appendChild(cell);
      }
    }
  }

  _renderBlackStone(cell, gameState, r, c) {
    const stone = document.createElement("div");
    stone.className = "stone black-stone";
    stone.textContent = "●";

    this._applyStoneEffects(stone, gameState, r, c);
    cell.appendChild(stone);
  }

  _renderWhiteStone(cell, gameState, r, c) {
    const stone = document.createElement("div");
    stone.className = "stone white-stone";
    stone.textContent = "○";

    this._applyStoneEffects(stone, gameState, r, c);
    cell.appendChild(stone);
  }

  _renderValidMove(cell, r, c, onCellClick) {
    cell.classList.add("valid-move");
    cell.innerHTML = '<div style="color: white; font-size: 20px;">✓</div>';

    if (onCellClick) {
      cell.style.cursor = "pointer";
      cell.onclick = () => onCellClick(r, c);
    }
  }

  _applyStoneEffects(stone, gameState, r, c) {
    if (gameState.last_move && gameState.last_move[0] === r && gameState.last_move[1] === c) {
      stone.classList.add("new-stone", "highlight-new");
      setTimeout(() => stone.classList.remove("highlight-new"), 3000);
    }

    if (gameState.flipped_stones && gameState.flipped_stones.some(([fr, fc]) => fr === r && fc === c)) {
      stone.classList.add("flipped-stone", "highlight-flipped");
      setTimeout(() => stone.classList.remove("highlight-flipped"), 3000);
    }
  }

  updateScoreDisplay(gameState) {
    if (!gameState) return;

    const blackScoreElement = document.getElementById("blackScore");
    const whiteScoreElement = document.getElementById("whiteScore");
    const moveCountElement = document.getElementById("moveCount");
    const currentPlayerElement = document.getElementById("currentPlayer");

    if (blackScoreElement) blackScoreElement.textContent = gameState.black_score;
    if (whiteScoreElement) whiteScoreElement.textContent = gameState.white_score;
    if (moveCountElement) moveCountElement.textContent = gameState.move_count;

    if (currentPlayerElement) {
      const currentPlayerText =
        gameState.current_player === 1 ? "● 黒番" : gameState.current_player === 2 ? "○ 白番" : "ゲーム終了";
      currentPlayerElement.textContent = currentPlayerText;
    }
  }

  updatePlayerNames(gameState) {
    if (!gameState) return;

    const currentMatchElement = document.getElementById("currentMatch");
    const player1NameElement = document.getElementById("player1Name");
    const player2NameElement = document.getElementById("player2Name");

    if (currentMatchElement) {
      currentMatchElement.textContent = `${gameState.player1_name} (●) vs ${gameState.player2_name} (○)`;
    }

    if (player1NameElement) player1NameElement.textContent = gameState.player1_name;
    if (player2NameElement) player2NameElement.textContent = gameState.player2_name;
  }

  displayGameEnd(gameState) {
    const gameEndElement = document.getElementById("gameEndStatus");
    if (!gameEndElement || !gameState) return;

    const winner = gameState.winner;
    let resultText = "";
    if (winner === 1) {
      resultText = `🎉 ${gameState.player1_name} の勝利！`;
    } else if (winner === 2) {
      resultText = `🎉 ${gameState.player2_name} の勝利！`;
    } else {
      resultText = "🤝 引き分け！";
    }

    gameEndElement.innerHTML = `<div class="game-end">${resultText}<br>最終スコア: 黒 ${gameState.black_score} - 白 ${gameState.white_score}</div>`;
  }

  resetDisplay() {
    if (this.boardElement) {
      this.boardElement.innerHTML = "";
    }

    const blackScoreElement = document.getElementById("blackScore");
    const whiteScoreElement = document.getElementById("whiteScore");
    const moveCountElement = document.getElementById("moveCount");
    const currentPlayerElement = document.getElementById("currentPlayer");
    const player1NameElement = document.getElementById("player1Name");
    const player2NameElement = document.getElementById("player2Name");
    const currentMatchElement = document.getElementById("currentMatch");
    const gameEndElement = document.getElementById("gameEndStatus");

    if (blackScoreElement) blackScoreElement.textContent = "2";
    if (whiteScoreElement) whiteScoreElement.textContent = "2";
    if (moveCountElement) moveCountElement.textContent = "0";
    if (currentPlayerElement) currentPlayerElement.textContent = "●";
    if (player1NameElement) player1NameElement.textContent = "プレイヤー1";
    if (player2NameElement) player2NameElement.textContent = "プレイヤー2";
    if (currentMatchElement) currentMatchElement.textContent = "対戦準備中...";
    if (gameEndElement) gameEndElement.innerHTML = "";
  }
}

export { BoardRenderer };
export default BoardRenderer;
