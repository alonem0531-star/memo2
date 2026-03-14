# テストファイル
# pytest というライブラリを使って、app.py の動作を自動で確認するプログラムです
# ターミナルで `pytest` と実行すると、このファイルのテストが動きます

import app

# テストの中で使う一時ファイルを作るために使う
# tmp_path は pytest が自動で用意してくれる「テスト用の一時フォルダ」です
# テストが終わると自動的に削除されるので、本物の memo.json を汚しません


def test_save_and_load_memos(tmp_path):
    """メモを保存して、読み込んだら同じ内容が戻るかを確認するテスト"""

    # --- 準備 ---
    # テスト用の一時ファイルパスを作る（例: C:\Temp\pytest-xxx\memo.json）
    temp_file = tmp_path / "memo.json"

    # app.py が使うファイルパスを、一時ファイルに差し替える
    # こうすることで、本物の memo.json を書き換えずにテストできる
    app.memo_file = str(temp_file)

    # app.py が使うメモリストを空にする（他のテストの影響を受けないようにするため）
    app.memos.clear()

    # --- テストデータの準備 ---
    # 保存するメモを辞書形式で作る（app.py と同じ形式）
    test_memo = {
        "text": "テスト用のメモ",
        "created_at": "2026-01-01 12:00:00"
    }

    # メモをリストに追加する
    app.memos.append(test_memo)

    # --- 実行 ---
    # メモをファイルに保存する
    app.save_memos()

    # メモリストを空にして、「ファイルから読み込む前の状態」を再現する
    app.memos.clear()

    # ファイルからメモを読み込む
    app.load_memos()

    # --- 確認 ---
    # メモが1件だけ読み込まれているか確認する
    assert len(app.memos) == 1

    # 読み込まれたメモの内容が、保存したものと一致するか確認する
    assert app.memos[0]["text"] == "テスト用のメモ"
    assert app.memos[0]["created_at"] == "2026-01-01 12:00:00"


def test_search_memos_returns_matching():
    """キーワードに一致するメモだけが返るかを確認するテスト"""

    # --- テストデータの準備 ---
    # 検索対象のメモリストを用意する
    memos = [
        {"text": "牛乳を買う",        "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す",  "created_at": "2026-01-02 10:00:00"},
        {"text": "卵と牛乳を買う",    "created_at": "2026-01-03 10:00:00"},
    ]

    # --- 実行 ---
    # "牛乳" を含むメモを検索する
    results = app.search_memos(memos, "牛乳")

    # --- 確認 ---
    # "牛乳" を含むメモは2件のはず
    assert len(results) == 2

    # 返ってきたメモの本文に "牛乳" が含まれているか確認する
    for memo in results:
        assert "牛乳" in memo["text"]


def test_search_memos_returns_empty_when_no_match():
    """一致するメモがない場合、空のリストが返るかを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う",       "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す", "created_at": "2026-01-02 10:00:00"},
    ]

    # --- 実行 ---
    # どのメモにも含まれていないキーワードで検索する
    results = app.search_memos(memos, "ジム")

    # --- 確認 ---
    # 一致するメモがないので、空のリストが返るはず
    assert results == []


def test_delete_memo_removes_correct_memo():
    """正しいインデックスを指定したとき、そのメモが削除されるかを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う",       "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す", "created_at": "2026-01-02 10:00:00"},
        {"text": "運動する",         "created_at": "2026-01-03 10:00:00"},
    ]

    # --- 実行 ---
    # インデックス 1（「図書館に本を返す」）を削除する
    deleted = app.delete_memo(memos, 1)

    # --- 確認 ---
    # 削除後はメモが2件になるはず
    assert len(memos) == 2

    # 戻り値は削除されたメモ自身のはず
    assert deleted["text"] == "図書館に本を返す"

    # 残ったメモに削除したものが含まれていないことを確認する
    texts = [memo["text"] for memo in memos]
    assert "図書館に本を返す" not in texts


def test_delete_memo_returns_none_for_invalid_index():
    """不正なインデックスを指定したとき、None が返りリストが変わらないことを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う",       "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す", "created_at": "2026-01-02 10:00:00"},
    ]

    # --- 実行 ---
    # 存在しないインデックス（範囲外）を指定する
    result = app.delete_memo(memos, 99)

    # --- 確認 ---
    # 不正なインデックスなので None が返るはず
    assert result is None

    # リストの件数は変わっていないはず
    assert len(memos) == 2


def test_edit_memo_updates_text():
    """正しいインデックスを指定したとき、text が更新されるかを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う",       "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す", "created_at": "2026-01-02 10:00:00"},
    ]

    # --- 実行 ---
    # インデックス 0（「牛乳を買う」）を新しい内容に書き換える
    result = app.edit_memo(memos, 0, "卵も買う")

    # --- 確認 ---
    # 成功したので True が返るはず
    assert result is True

    # text が新しい内容に更新されているはず
    assert memos[0]["text"] == "卵も買う"


def test_edit_memo_does_not_change_created_at():
    """text を更新しても、created_at が変わらないことを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う", "created_at": "2026-01-01 10:00:00"},
    ]

    # --- 実行 ---
    app.edit_memo(memos, 0, "卵も買う")

    # --- 確認 ---
    # created_at は編集前のまま変わっていないはず
    assert memos[0]["created_at"] == "2026-01-01 10:00:00"


def test_edit_memo_returns_false_for_invalid_index():
    """不正なインデックスを指定したとき、False が返りリストが変わらないことを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "牛乳を買う", "created_at": "2026-01-01 10:00:00"},
    ]

    # --- 実行 ---
    # 存在しないインデックス（範囲外）を指定する
    result = app.edit_memo(memos, 99, "卵も買う")

    # --- 確認 ---
    # 不正なインデックスなので False が返るはず
    assert result is False

    # 元の text は変わっていないはず
    assert memos[0]["text"] == "牛乳を買う"
