/**
 * API Client Module
 * Handles server communication
 */

class ApiClient {
  constructor() {
    this.baseUrl = "";
  }

  // AI vs AI strategy upload
  async uploadStrategies(formData) {
    try {
      console.log("DEBUG: Sending upload request...");
      const response = await fetch("/upload_strategies", {
        method: "POST",
        body: formData,
      });

      console.log("DEBUG: Upload response received:", response.status);
      const data = await response.json();
      console.log("DEBUG: Upload response data:", data);

      return data;
    } catch (error) {
      console.log("DEBUG: Upload error:", error);
      throw error;
    }
  }

  // Human vs AI strategy upload
  async uploadHumanVsAi(formData) {
    try {
      const response = await fetch("/upload_human_vs_ai", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.log("DEBUG: Human vs AI upload error:", error);
      throw error;
    }
  }

  // Execute next move
  async nextMove(humanMove = null) {
    try {
      const requestData = humanMove ? { human_move: humanMove } : {};
      console.log("DEBUG: Sending request data:", requestData);

      const response = await fetch("/next_move", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      console.log("DEBUG: Next move response:", response.status);
      const data = await response.json();
      console.log("DEBUG: Next move data:", data);

      return data;
    } catch (error) {
      console.log("DEBUG: Next move error:", error);
      throw error;
    }
  }

  // Reset game
  async resetGame() {
    try {
      const response = await fetch("/reset_game", {
        method: "POST",
      });

      const data = await response.json();
      return data;
    } catch (error) {
      console.log("DEBUG: Reset game error:", error);
      throw error;
    }
  }
}

// ES module export
export { ApiClient };
export default ApiClient;
