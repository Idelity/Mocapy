# 🛠️ Mocapy プロジェクト 初期セットアップ手順

GitHub上にあるリモートリポジトリ（README.md作成済み）の情報を、Macのローカル環境に持ってきて同期するまでの手順書です。

## 📋 実行コマンド一覧

ターミナルを開き、以下のコマンドを1行ずつ順番に実行します。

### 1. ローカルにディレクトリを作成して移動する
Macの「書類（Documents）」フォルダ配下に `Mocapy` ディレクトリを作成し、その中に移動します。
```bash
mkdir -p ~/Documents/Mocapy
cd ~/Documents/Mocapy
```

### 2. ローカルのGitリポジトリを初期化する
このディレクトリをGitの管理下に置きます。
```bash
git init
```

### 3. GitHubのリモートリポジトリと紐付ける
GitHub上で作成したリポジトリのURLを登録します。
※「あなたのユーザー名」の部分は、ご自身のGitHubアカウント名に書き換えてください。
```bash
git remote add origin https://github.com
```

### 4. GitHubから最新データをダウンロードする（同期）
GitHub側で作成済みの `README.md` をローカル環境に引っ張ってきます。
```bash
git pull origin main
```

---

## 🔍 接続の確認方法
上記がすべて完了したら、以下のコマンドでファイルが正しくダウンロードされているか確認します。
```bash
ls -la
```
画面に `README.md` が表示されていれば、ローカル環境の準備はすべて完了です！
