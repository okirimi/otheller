# Otheller

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg?logo=python&logoColor=white&style=flat&labelColor=24292e)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E.svg?logo=javascript&logoColor=black&style=flat)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-3b808b.svg?logo=flask&logoColor=white&labelColor=24292e)](https://flask.palletsprojects.com/)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Otheller**は、Pythonの学習者がオリジナルのオセロ戦略を実装してプログラミングスキルを向上させるためのWebアプリケーションです。

## 🚀 Getting Started

### 事前準備

Python のバージョン管理とパッケージ管理を一元的に行えるツールとして、uv の利用を推奨します。詳しい情報や導入手順は[公式サイト](https://docs.astral.sh/uv/getting-started/installation/)を参照してください。

### インストールと環境設定

#### With `uv`

```bash
# Clone repository
git clone https://github.com/okirimi/otheller.git && cd otheller/

# Creates `.venv` based on the dependencies in `uv.lock`.
uv sync
```

#### Without `uv`

`.python-versions` に指定された Python バージョンを使っていることを確認してください。以下のコマンドで仮想環境を作成し、依存関係をインストールしてください。

```bash
python -m venv .venv

source .venv/bin/acvibate

pip install -r requirements.lock
```

### アプリの起動

```
python -m otheller.main --log <log_level>
```

ブラウザで `http://127.0.0.1:5001` にアクセスしてください。

> [!NOTE]
> `--log <log_level>` は任意のパラメーターで、ログレベルを設定することができます。有効な値は `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` です（大文字と小文字は区別されません）。指定しない場合は `INFO` が使用されます。

## 📗 Hands-On Example

独自のオセロ戦略を実装して、対戦することができます。

### Step 1: 戦略ファイルの準備

```bash
# strategy.pyをコピーして新しい戦略ファイルを作成
cp otheller/strategy.py otheller/my_custom_strategy.py
```

### Step 2: 戦略の実装

`otheller/my_custom_strategy.py` ファイルを開き、`MyStrategy` クラスの `choose_move` メソッドを編集します。

> [!IMPORTANT]
> **クラス名** `MyStrategy` **は変更しないでください。** システムがこの名前を期待しているため、変更すると動作しません。

#### 実装する場所

```python
class MyStrategy(StrategyBase):
    def choose_move(self, board: Board) -> tuple[int, int] | None:
        # ===========================================
        # ここから下を編集してください
        # ===========================================

        # Example: ランダムに手を選ぶ
        import random
        return random.choice(valid_moves)
```

#### 簡単な実装例

```python
# Example_1: 角を優先する戦略
corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
for corner in corners:
    if corner in valid_moves:
        return corner

# Example_2: 最も多くの石をひっくり返せる手を選ぶ
from otheller.core.simulator import GameSimulator

best_move = None
max_flips = 0

for move in valid_moves:
    success, flipped_positions = GameSimulator.simulate_move_preview(
        board, move[0], move[1], self.player
    )
    if success and len(flipped_positions) > max_flips:
        max_flips = len(flipped_positions)
        best_move = move

return best_move
```

### Step 3: 戦略のテスト

1. アプリケーションを起動:

   ```bash
   python -m otheller.main
   ```

2. ブラウザで `http://127.0.0.1:5001` にアクセス

3. 「ファイルを選択」ボタンで作成した戦略ファイル（例: `my_custom_strategy.py`）をアップロード

4. 「Human vs AI」または「AI vs AI」モードで対戦開始
