# CLIメモ帳

コマンドラインで動くシンプルなメモ帳アプリです。
メモの追加・一覧表示・削除・編集・検索ができます。

---

## セットアップ

### 1. 仮想環境を作る

```bash
python -m venv .venv
```

### 2. 仮想環境を有効にする

**Mac / Linux**
```bash
source .venv/bin/activate
```

**Windows（コマンドプロンプト）**
```bat
.venv\Scripts\activate
```

**Windows（PowerShell）**
```powershell
.venv\Scripts\Activate.ps1
```

### 3. 必要なライブラリをインストールする

```bash
pip install -r requirements.txt
```

---

## 起動方法

```bash
python app.py
```

起動するとメニューが表示されます。番号を入力して操作してください。

---

## できること

- **メモを追加** ─ テキストを入力して保存する
- **メモ一覧を表示** ─ 保存中のメモを番号付きで一覧表示する
- **メモを削除** ─ 番号を指定して1件削除する
- **全メモ削除** ─ 保存中のメモをすべて削除する
- **メモを編集** ─ 番号を指定して内容を書き換える
- **メモを検索** ─ キーワードを含むメモだけを表示する
- **並び替え** ─ 新しい順・古い順を選んで表示する

メモは `memo.json` に自動で保存されます。

---

## テストの実行

```bash
pytest
```

`tests/test_app.py` に書かれたテストが実行されます。
