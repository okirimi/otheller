/**
 * UI Controls Module
 * Handles UI control and event processing
 */

class UiControls {
  constructor(showStatus, updateFileStatusDisplay) {
    this.showStatus = showStatus;
    this.fileStatusUpdateFunction = updateFileStatusDisplay || this._defaultFileStatusUpdate;
  }

  initialize() {
    this._setupEventListeners();
    this._showInitialStatus();
  }

  _setupEventListeners() {
    this._setupFileInputs();

    this._setupModeSelectors();

    this._setupButtons();
  }

  _setupFileInputs() {
    const player1File = document.getElementById("player1File");
    const player2File = document.getElementById("player2File");
    const aiStrategyFile = document.getElementById("aiStrategyFile");

    if (player1File) {
      player1File.addEventListener("change", (e) => {
        this.fileStatusUpdateFunction("player1Status", e.target.files[0]);
      });
    }

    if (player2File) {
      player2File.addEventListener("change", (e) => {
        this.fileStatusUpdateFunction("player2Status", e.target.files[0]);
      });
    }

    if (aiStrategyFile) {
      aiStrategyFile.addEventListener("change", (e) => {
        this.fileStatusUpdateFunction("aiStrategyStatus", e.target.files[0]);
      });
    }
  }

  _setupModeSelectors() {
    const aiVsAiRadio = document.getElementById("aiVsAiRadio");
    const humanVsAiRadio = document.getElementById("humanVsAiRadio");

    if (aiVsAiRadio) {
      aiVsAiRadio.addEventListener("change", () => {
        if (aiVsAiRadio.checked) {
          this.showAiVsAiMode();
        }
      });
    }

    if (humanVsAiRadio) {
      humanVsAiRadio.addEventListener("change", () => {
        if (humanVsAiRadio.checked) {
          this.showHumanVsAiMode();
        }
      });
    }
  }

  _setupButtons() {
  }

  showAiVsAiMode() {
    const aiVsAiMode = document.getElementById("aiVsAiMode");
    const humanVsAiMode = document.getElementById("humanVsAiMode");

    if (aiVsAiMode) aiVsAiMode.style.display = "block";
    if (humanVsAiMode) humanVsAiMode.style.display = "none";
  }

  showHumanVsAiMode() {
    const aiVsAiMode = document.getElementById("aiVsAiMode");
    const humanVsAiMode = document.getElementById("humanVsAiMode");

    if (aiVsAiMode) aiVsAiMode.style.display = "none";
    if (humanVsAiMode) humanVsAiMode.style.display = "block";
  }

  showGameArea() {
    const gameArea = document.getElementById("gameArea");
    if (gameArea) {
      gameArea.style.display = "flex";

      setTimeout(() => {
        gameArea.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }, 300);
    }
  }

  hideGameArea() {
    const gameArea = document.getElementById("gameArea");
    if (gameArea) {
      gameArea.style.display = "none";
    }
  }

  showHumanPrompt(show) {
    const humanPrompt = document.getElementById("humanMovePrompt");
    if (humanPrompt) {
      humanPrompt.style.display = show ? "block" : "none";
    }
  }

  enableButton(buttonId, enabled) {
    const button = document.getElementById(buttonId);
    if (button) {
      button.disabled = !enabled;
    }
  }

  setAutoPlayButtonText(text) {
    const button = document.getElementById("autoPlayBtn");
    if (button) {
      button.textContent = text;
    }
  }

  getSelectedGameMode() {
    const modeRadio = document.querySelector('input[name="gameMode"]:checked');
    return modeRadio ? modeRadio.value : "ai-vs-ai";
  }

  getSelectedHumanColor() {
    const colorRadio = document.querySelector('input[name="humanColor"]:checked');
    return colorRadio ? colorRadio.value : "black";
  }

  getUploadFormData() {
    const form = document.getElementById("uploadForm");
    return form ? new FormData(form) : null;
  }

  getHumanVsAiFormData() {
    const form = document.getElementById("humanVsAiForm");
    const formData = form ? new FormData(form) : new FormData();

    const humanColor = this.getSelectedHumanColor();
    formData.append("human_color", humanColor);

    return formData;
  }

  _defaultFileStatusUpdate(statusId, file) {
    const statusDiv = document.getElementById(statusId);
    if (!statusDiv) return;

    if (file) {
      statusDiv.textContent = `✓ ${file.name}`;
      statusDiv.className = "file-status file-ready";
    } else {
      statusDiv.textContent = "ファイル未選択";
      statusDiv.className = "file-status file-empty";
    }
  }

  _showInitialStatus() {
    this.showStatus("loading", "対戦モードを選択してファイルを読み込んでください");
  }

  addMoveLog(message) {
    const logDiv = document.getElementById("moveLog");
    if (!logDiv) return;

    const logEntry = document.createElement("div");
    logEntry.className = "move-entry";
    logEntry.textContent = new Date().toLocaleTimeString() + " - " + message;

    logDiv.appendChild(logEntry);
    logDiv.scrollTop = logDiv.scrollHeight;
  }

  clearMoveLog() {
    const logDiv = document.getElementById("moveLog");
    if (logDiv) {
      logDiv.innerHTML = "";
    }
  }

  validateAiVsAiForm() {
    const player1File = document.getElementById("player1File");
    const player2File = document.getElementById("player2File");

    return player1File?.files.length > 0 && player2File?.files.length > 0;
  }

  validateHumanVsAiForm() {
    const aiStrategyFile = document.getElementById("aiStrategyFile");
    return aiStrategyFile?.files.length > 0;
  }
}

export { UiControls };
export default UiControls;
