# Study Time Manager（勉強時間管理アプリ）

Flask と SQLite を使ったサーバーサイドWebアプリです。

## 主な機能
- 日付・科目・勉強時間・メモの登録
- 今日の合計勉強時間の表示
- 今日取り組んだ科目数の表示
- これまでの合計勉強時間の表示
- 勉強記録の一覧表示と削除
- SQLiteによるデータ保存

## ローカルでの起動
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
ブラウザで http://127.0.0.1:5000 を開きます。

## Renderでの公開
1. このフォルダの内容をGitHubの新しいリポジトリにアップロードします。
2. Renderで New > Web Service を選び、GitHubリポジトリを接続します。
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`
5. Deployを実行し、発行された `https://...onrender.com` のURLを確認します。

## データ保存について
初期設定ではSQLiteファイルをアプリ内に作成します。Renderの無料Webサービスではローカルファイルが再起動・再デプロイ時に消える場合があります。記録を長期保存したい場合は、永続ディスクを設定して `DATABASE_PATH` にその保存先を指定してください。
