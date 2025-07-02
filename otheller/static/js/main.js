/**
 * Main Entry Point
 * Handles application initialization and module integration
 */

import { BoardRenderer } from "./boardRenderer.js";
import { GameLogic } from "./gameLogic.js";
import { UiControls } from "./uiControls.js";
import { GameState } from "./gameState.js";
import { ApiClient } from "./apiClient.js";
import { HumanPlayer } from "./humanPlayer.js";
import { showStatus, updateFileStatusDisplay } from "./utils.js";

class OthellerApp {
  constructor() {
    this.boardRenderer = new BoardRenderer();
    this.gameState = new GameState();
    this.apiClient = new ApiClient();
    this.uiControls = new UiControls(showStatus, updateFileStatusDisplay);
    this.humanPlayer = new HumanPlayer(this.gameState, this.uiControls);
    this.gameLogic = new GameLogic({
      boardRenderer: this.boardRenderer,
      gameState: this.gameState,
      apiClient: this.apiClient,
      uiControls: this.uiControls,
      humanPlayer: this.humanPlayer,
      showStatus: showStatus,
    });
  }

  initialize() {
    this.gameLogic.initialize();

    console.log("Otheller application initialized successfully");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const app = new OthellerApp();
  app.initialize();
});

export { OthellerApp };
export default OthellerApp;
