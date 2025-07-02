/**
 * Game State Management Module
 * Handles game state management
 */

class GameState {
  constructor() {
    this.state = null;
    this.isGameEnd = false;
    this.isHumanVsAi = false;
    this.humanPlayer = 1;
    this.waitingForHuman = false;
    this.autoInterval = null;
  }

  // ゲーム状態を設定
  setState(newState) {
    this.state = newState;
    console.log("DEBUG: Game state updated:", this.state);
  }

  // ゲーム状態を取得
  getState() {
    return this.state;
  }

  // ゲーム終了状態を設定
  setGameEnd(isEnd) {
    this.isGameEnd = isEnd;
  }

  // ゲーム終了状態を確認
  isGameFinished() {
    return this.isGameEnd;
  }

  // 人間 vs AI モードを設定
  setHumanVsAiMode(isHuman, humanPlayerNumber = 1) {
    this.isHumanVsAi = isHuman;
    this.humanPlayer = humanPlayerNumber;
  }

  // 人間 vs AI モードかどうか確認
  isHumanVsAiMode() {
    return this.isHumanVsAi;
  }

  // 人間プレイヤー番号を取得
  getHumanPlayer() {
    return this.humanPlayer;
  }

  // 人間の入力待ちフラグを設定
  setWaitingForHuman(waiting) {
    this.waitingForHuman = waiting;
  }

  // 人間の入力待ちかどうか確認
  isWaitingForHuman() {
    return this.waitingForHuman;
  }

  // 自動再生インターバルを設定
  setAutoInterval(interval) {
    this.autoInterval = interval;
  }

  // 自動再生インターバルを取得
  getAutoInterval() {
    return this.autoInterval;
  }

  // 自動再生インターバルをクリア
  clearAutoInterval() {
    if (this.autoInterval) {
      clearInterval(this.autoInterval);
      this.autoInterval = null;
    }
  }

  // ゲーム状態をリセット
  reset() {
    this.state = null;
    this.isGameEnd = false;
    this.waitingForHuman = false;
    this.clearAutoInterval();
    console.log("DEBUG: Game state reset");
  }

  // 現在のプレイヤーが人間かどうか確認
  isCurrentPlayerHuman() {
    return this.isHumanVsAi && this.state && this.state.current_player === this.humanPlayer;
  }
}

// ESモジュールとしてエクスポート
export { GameState };
export default GameState;
