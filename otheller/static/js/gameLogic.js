/**
 * Game Logic Module
 * Handles game flow control
 */

class GameLogic {
  constructor(dependencies) {
    this.initialized = false;

    this.boardRenderer = dependencies.boardRenderer;
    this.gameState = dependencies.gameState;
    this.apiClient = dependencies.apiClient;
    this.uiControls = dependencies.uiControls;
    this.humanPlayer = dependencies.humanPlayer;
    this.showStatus = dependencies.showStatus;
  }

  initialize() {
    if (this.initialized) return;

    console.log("DEBUG: Initializing game logic");

    this.uiControls.initialize();

    const boardElement = document.getElementById("board");
    if (boardElement) {
      this.boardRenderer.setBoardElement(boardElement);
    }

    this._setupButtonEvents();

    this.initialized = true;
    console.log("DEBUG: Game logic initialized");
  }

  _setupButtonEvents() {
    const loadStrategiesBtn = document.getElementById("loadStrategiesBtn");
    const loadHumanVsAiBtn = document.getElementById("loadHumanVsAiBtn");
    const nextMoveBtn = document.getElementById("nextMoveBtn");
    const autoPlayBtn = document.getElementById("autoPlayBtn");
    const resetGameBtn = document.querySelector(".reset-button");

    if (loadStrategiesBtn) {
      loadStrategiesBtn.addEventListener("click", () => this.uploadStrategies());
    }
    if (loadHumanVsAiBtn) {
      loadHumanVsAiBtn.addEventListener("click", () => this.uploadHumanVsAi());
    }
    if (nextMoveBtn) {
      nextMoveBtn.addEventListener("click", () => this.nextMove());
    }
    if (autoPlayBtn) {
      autoPlayBtn.addEventListener("click", () => this.autoPlay());
    }
    if (resetGameBtn) {
      resetGameBtn.addEventListener("click", () => this.resetGame());
    }
  }

  async uploadStrategies() {
    console.log("DEBUG: uploadStrategies called");

    if (!this.uiControls.validateAiVsAiForm()) {
      this.showStatus("error", "両方のプレイヤーのファイルを選択してください");
      console.log("DEBUG: File validation failed");
      return;
    }

    const formData = this.uiControls.getUploadFormData();
    if (!formData) {
      this.showStatus("error", "フォームデータの取得に失敗しました");
      return;
    }

    this.showStatus("loading", "戦略ファイル読み込み中...");
    console.log("DEBUG: Sending upload request...");

    try {
      const data = await this.apiClient.uploadStrategies(formData);

      if (data.success) {
        this.showStatus("success", `戦略読み込み完了: ${data.player1_name} vs ${data.player2_name}`);
        this.gameState.setState(data.state);
        this.gameState.setHumanVsAiMode(false);
        console.log("DEBUG: Game state set");
        this.startGameDisplay();
      } else {
        this.showStatus("error", `エラー: ${data.error}`);
        console.log("DEBUG: Upload failed:", data.error);
      }
    } catch (error) {
      this.showStatus("error", `通信エラー: ${error.message}`);
      console.log("DEBUG: Upload error:", error);
    }
  }

  async uploadHumanVsAi() {
    if (!this.uiControls.validateHumanVsAiForm()) {
      this.showStatus("error", "AIファイルを選択してください");
      return;
    }

    const formData = this.uiControls.getHumanVsAiFormData();
    if (!formData) {
      this.showStatus("error", "フォームデータの取得に失敗しました");
      return;
    }

    this.showStatus("loading", "AI戦略読み込み中...");

    try {
      const data = await this.apiClient.uploadHumanVsAi(formData);

      if (data.success) {
        this.showStatus("success", `対戦準備完了: 人間 vs ${data.ai_name}`);
        this.gameState.setState(data.state);
        this.gameState.setHumanVsAiMode(true, data.human_player);
        this.startGameDisplay();

        this.checkHumanTurn();
      } else {
        this.showStatus("error", `エラー: ${data.error}`);
      }
    } catch (error) {
      this.showStatus("error", `通信エラー: ${error.message}`);
    }
  }

  checkHumanTurn() {
    if (!this.gameState.isHumanVsAiMode() || this.gameState.isGameFinished()) {
      return;
    }

    const isHumanTurn = this.humanPlayer.checkAndHandleHumanTurn((move) => {
      this.nextMove(move);
    });

    if (isHumanTurn) {
      this.nextMove();
    }
  }

  startGameDisplay() {
    this.uiControls.showGameArea();
    this.updateDisplay();
    this.uiControls.addMoveLog("ゲーム開始！");
  }

  async nextMove(humanMove = null) {
    console.log("DEBUG: nextMove called with:", humanMove);
    console.log("DEBUG: isGameEnd:", this.gameState.isGameFinished());
    console.log("DEBUG: gameState exists:", this.gameState.getState() !== null);

    if (this.gameState.isGameFinished()) {
      console.log("DEBUG: Game is end, returning");
      return;
    }

    if (!this.gameState.getState()) {
      console.log("DEBUG: No game state, cannot proceed");
      this.showStatus("error", "ゲームが開始されていません");
      return;
    }

    try {
      const data = await this.apiClient.nextMove(humanMove);

      if (data.success) {
        this.gameState.setState(data.state);
        console.log("DEBUG: Updated game state");
        this.updateDisplay();

        if (data.state.is_game_over) {
          this.handleGameEnd();
        } else if (this.gameState.isHumanVsAiMode()) {
          this._handleHumanVsAiTurn();
        }
      } else {
        this.showStatus("error", `手の実行エラー: ${data.error}`);
        console.log("DEBUG: Next move failed:", data.error);
      }
    } catch (error) {
      this.showStatus("error", `通信エラー: ${error.message}`);
      console.log("DEBUG: Next move error:", error);
    }
  }

  _handleHumanVsAiTurn() {
    const isHumanTurn = this.humanPlayer.checkAndHandleHumanTurn((move) => {
      this.nextMove(move);
    });

    if (!isHumanTurn) {
      setTimeout(() => this.nextMove(), 1000);
    }
  }

  handleGameEnd() {
    this.gameState.setGameEnd(true);
    this.uiControls.enableButton("nextMoveBtn", false);
    this.humanPlayer.onHumanTurnEnd();

    const autoInterval = this.gameState.getAutoInterval();
    if (autoInterval) {
      this.gameState.clearAutoInterval();
      this.uiControls.setAutoPlayButtonText("自動再生");
      this.uiControls.enableButton("autoPlayBtn", false);
    }

    const gameState = this.gameState.getState();
    if (gameState) {
      this.boardRenderer.displayGameEnd(gameState);

      const winner = gameState.winner;
      let resultText = "";
      if (winner === 1) {
        resultText = `🎉 ${gameState.player1_name} の勝利！`;
      } else if (winner === 2) {
        resultText = `🎉 ${gameState.player2_name} の勝利！`;
      } else {
        resultText = "🤝 引き分け！";
      }

      this.uiControls.addMoveLog(`🏆 ゲーム終了: ${resultText}`);
    }
  }

  async autoPlay() {
    console.log("DEBUG: autoPlay called");

    const currentInterval = this.gameState.getAutoInterval();
    if (currentInterval) {
      this.gameState.clearAutoInterval();
      this.uiControls.setAutoPlayButtonText("自動再生");
      console.log("DEBUG: Auto play stopped");
      return;
    }

    if (this.gameState.isGameFinished()) {
      console.log("DEBUG: Game is end, cannot start auto play");
      return;
    }

    if (!this.gameState.getState()) {
      console.log("DEBUG: No game state, cannot start auto play");
      this.showStatus("error", "ゲームが開始されていません。まず戦略ファイルを読み込んでください。");
      return;
    }

    if (this.gameState.isHumanVsAiMode()) {
      console.log("DEBUG: Human vs AI mode, auto play not available");
      this.showStatus("error", "人間 vs AI モードでは自動再生は使用できません");
      return;
    }

    console.log("DEBUG: Starting auto play");
    this.uiControls.setAutoPlayButtonText("停止");

    const interval = setInterval(() => {
      console.log("DEBUG: Auto play interval tick");
      if (this.gameState.isGameFinished() || !this.gameState.getState()) {
        console.log("DEBUG: Stopping auto play - game end or no state");
        this.gameState.clearAutoInterval();
        this.uiControls.setAutoPlayButtonText("自動再生");
        return;
      }
      this.nextMove();
    }, 1500);

    this.gameState.setAutoInterval(interval);
  }

  makeHumanMove(row, col) {
    if (!this.gameState.isHumanVsAiMode() || this.gameState.isGameFinished()) {
      return;
    }

    if (!this.gameState.isCurrentPlayerHuman()) {
      return;
    }

    this.humanPlayer.makeMove(row, col);
  }

  async resetGame() {
    this.gameState.clearAutoInterval();

    try {
      const data = await this.apiClient.resetGame();

      if (data.success) {
        this.uiControls.hideGameArea();
        this.uiControls.showHumanPrompt(false);
        this.uiControls.setAutoPlayButtonText("自動再生");
        this.uiControls.enableButton("autoPlayBtn", false);
        this.uiControls.enableButton("nextMoveBtn", false);
        this.uiControls.clearMoveLog();

        this.boardRenderer.resetDisplay();

        this.gameState.reset();
        this.humanPlayer.stopWaitingForMove();

        this.showStatus("loading", "新しい対戦の準備ができました");
      }
    } catch (error) {
      this.showStatus("error", `リセットエラー: ${error.message}`);
    }
  }

  updateDisplay() {
    const gameState = this.gameState.getState();
    if (!gameState) return;

    const clickHandler =
      this.gameState.isHumanVsAiMode() &&
      this.gameState.isCurrentPlayerHuman() &&
      !this.gameState.isGameFinished()
        ? this.humanPlayer.createBoardClickHandler()
        : null;

    this.boardRenderer.renderBoard(gameState, clickHandler);
    this.boardRenderer.updateScoreDisplay(gameState);
    this.boardRenderer.updatePlayerNames(gameState);
  }
}

export { GameLogic };
export default GameLogic;
