/**
 * Utility functions for otheller.
 */

/**
 * Display a status message on the UI.
 * @param {string} status - The status of the message.
 * @param {string} message - The message to display.
 */
const showStatus = function (status, message) {
  const statusDiv = document.getElementById("status");
  if (statusDiv) {
    statusDiv.innerHTML = `<div class="status ${status}">${message}</div>`;
  }
  console.log(`STATUS ${status.toUpperCase()}: ${message}`);
};

/**
 * Update the display of a file status.
 * @param {string} elementId - The ID of the element to update the display of.
 * @param {File} file - The file to update the status of.
 */
const updateFileStatusDisplay = function (elementId, file) {
  const statusDiv = document.getElementById(elementId);
  if (!statusDiv) return;

  if (file) {
    statusDiv.textContent = `✓ ${file.name}`;
    statusDiv.className = "file-status file-ready";
  } else {
    statusDiv.textContent = "ファイル未選択";
    statusDiv.className = "file-status file-empty";
  }
};

export { showStatus, updateFileStatusDisplay };
