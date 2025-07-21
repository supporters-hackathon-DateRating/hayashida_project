# デート偏差値アプリ - バックエンド

## セットアップ手順

### 1. PostgreSQLのインストールと設定

```bash
# macOS (Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# PostgreSQLの公式サイトからダウンロード
```

### 2. データベースの作成

```bash
# PostgreSQLにログイン
psql postgres

# データベースユーザーとデータベースを作成
CREATE USER dateapp_user WITH PASSWORD 'your_password';
CREATE DATABASE dateapp OWNER dateapp_user;
\q
```

### 3. Python環境のセットアップ

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 4. 環境変数の設定

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集して以下を設定
# DATABASE_URL=postgresql://dateapp_user:your_password@localhost:5432/dateapp
# GEMINI_API_KEY=your_gemini_api_key
```

### 5. サーバーの起動

```bash
# データベーステーブルの作成
python database.py

# サーバーの起動
python run.py
```

## API エンドポイント

- `GET /api/health` - ヘルスチェック
- `POST /api/posts` - 新しい投稿の作成
- `GET /api/posts` - 全投稿の取得（偏差値順）
