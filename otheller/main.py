import importlib.util
import sys
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request

from otheller.cli import logger
from otheller.strategy import StrategyBase
from otheller.web.controller import WebGameController

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

GAME_STATE_FILE = UPLOAD_FOLDER / "game_state.pkl"


web_controller = WebGameController(str(GAME_STATE_FILE))


def _load_strategy(file_path: str, player: str) -> None:
    try:
        uploads_dir = str(Path(file_path).parent)
        if uploads_dir not in sys.path:
            sys.path.insert(0, uploads_dir)

        # Load module dynamically
        spec = importlib.util.spec_from_file_location("strategy_module", file_path)
        strategy_module = importlib.util.module_from_spec(spec)

        # Execute module
        spec.loader.exec_module(strategy_module)

        if hasattr(strategy_module, "MyStrategy"):
            return strategy_module.MyStrategy(player)
        logger.error(f"MyStrategyクラスが見つかりません: {file_path}")

    except Exception as e:
        logger.error(f"戦略読み込みエラー: {e}")
        return None


@app.route("/")
def index() -> str:
    """Render the HTML page after attempting to restore a previous state."""
    # When the server starts, attempt to restore the previous game state.
    web_controller.load_state()
    return render_template("index.html")


@app.route("/get_state")
def get_state() -> Response:
    if web_controller.board is None:
        web_controller.load_state()
    return jsonify({"state": web_controller.get_current_state()})


@app.route("/upload_strategies", methods=["POST"])
def upload_strategies() -> Response:
    player1_file = request.files["player1_file"]
    player2_file = request.files["player2_file"]

    if player1_file.filename == "" or player2_file.filename == "":
        return jsonify({"success": False, "error": "ファイルが選択されていません"})

    # Temporary save the files to the upload folder.
    player1_path = UPLOAD_FOLDER / f"player1_{player1_file.filename}"
    player2_path = UPLOAD_FOLDER / f"player2_{player2_file.filename}"

    player1_file.save(player1_path)
    player2_file.save(player2_path)

    # Load strategies via the singleton manager.
    strategy_1 = _load_strategy(str(player1_path), 1)
    strategy_2 = _load_strategy(str(player2_path), 2)

    if strategy_1 is None or strategy_2 is None:
        return jsonify({"success": False, "error": "Failed to load strategies"})

    name_1 = player1_file.filename.replace(".py", "")
    name_2 = player2_file.filename.replace(".py", "")

    web_controller.start_game(
        strategy_1,
        strategy_2,
        name_1,
        name_2,
        strategy1_file=str(player1_path),
        strategy2_file=str(player2_path),
    )

    state = web_controller.get_current_state()

    return jsonify(
        {
            "success": True,
            "player1_name": name_1,
            "player2_name": name_2,
            "state": state,
        },
    )


@app.route("/upload_human_vs_ai", methods=["POST"])
def upload_human_vs_ai() -> Response:
    """Upload one AI strategy file and start a Human-vs-AI match."""

    if "ai_file" not in request.files:
        return jsonify({"success": False, "error": "AI file not selected"})

    ai_file = request.files["ai_file"]
    human_color = request.form.get("human_color", "black")

    if not ai_file.filename:
        return jsonify({"success": False, "error": "No file selected"})

    ai_path = UPLOAD_FOLDER / f"ai_{ai_file.filename}"
    ai_file.save(ai_path)

    # Load the AI strategy.
    human_player = 1 if human_color == "black" else 2
    ai_player = 2 if human_color == "black" else 1

    ai_strategy = _load_strategy(str(ai_path), ai_player)
    if ai_strategy is None:
        return jsonify({"success": False, "error": "Failed to load AI strategy"})

    # A dummy strategy that simply waits for human input.
    class HumanStrategy(StrategyBase):
        def choose_move(self, _board) -> None:  # noqa: ANN001
            return None  # Waiting for human input.

    human_strategy = HumanStrategy(human_player)

    if human_player == 1:
        strategy1, strategy2 = human_strategy, ai_strategy
        name1, name2 = "Human", ai_file.filename.replace(".py", "")
        strategy1_file, strategy2_file = None, str(ai_path)
    else:
        strategy1, strategy2 = ai_strategy, human_strategy
        name1, name2 = ai_file.filename.replace(".py", ""), "Human"
        strategy1_file, strategy2_file = str(ai_path), None

    web_controller.start_game(
        strategy1,
        strategy2,
        name1,
        name2,
        human_vs_ai=True,
        human_player=human_player,
        strategy1_file=strategy1_file,
        strategy2_file=strategy2_file,
    )

    state = web_controller.get_current_state()

    return jsonify(
        {
            "success": True,
            "ai_name": ai_file.filename.replace(".py", ""),
            "human_player": human_player,
            "state": state,
        },
    )


@app.route("/next_move", methods=["POST"])
def next_move() -> Response:
    """Advance the game by one move."""

    data = request.get_json() or {}
    human_move = data.get("human_move")

    # If the board is missing, attempt to restore it from persisted state.
    if web_controller.board is None and not web_controller.load_state():
        return jsonify(
            {
                "success": False,
                "error": "Game state not found. Please upload the file again.",
            },
        )

    state = web_controller.make_next_move(human_move)
    if state is None:
        return jsonify({"success": False, "error": "Failed to execute move"})

    return jsonify({"success": True, "state": state})


@app.route("/reset_game", methods=["POST"])
def reset_game() -> Response:
    """Reset the game and clear persisted state."""

    web_controller.reset_game()
    return jsonify({"success": True})


if __name__ == "__main__":
    # On macOS, port 5000 is used by AirPlay receiver
    app.run(port=5001, use_reloader=False)
