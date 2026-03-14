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
    # テスト用の一時ファイルパスを文字列で作る（例: C:\Temp\pytest-xxx\memo.json）
    # str() に変換するのは、save_memos / load_memos が文字列パスを期待しているため
    temp_file = str(tmp_path / "memo.json")

    # --- テストデータの準備 ---
    # 保存するメモをローカルのリストとして用意する
    memos = [{"text": "テスト用のメモ", "created_at": "2026-01-01 12:00:00"}]

    # --- 実行 ---
    # memos と保存先ファイルを引数で渡して保存する
    app.save_memos(memos, temp_file)

    # ファイルから読み込んで、返ってきたリストを受け取る
    loaded = app.load_memos(temp_file)

    # --- 確認 ---
    # メモが1件だけ読み込まれているか確認する
    assert len(loaded) == 1

    # 読み込まれたメモの内容が、保存したものと一致するか確認する
    assert loaded[0]["text"] == "テスト用のメモ"
    assert loaded[0]["created_at"] == "2026-01-01 12:00:00"


def test_save_and_load_multiple_memos(tmp_path):
    """複数のメモを保存して、すべて正しく読み込まれるかを確認するテスト"""

    # --- 準備 ---
    temp_file = str(tmp_path / "memo.json")

    # --- テストデータの準備 ---
    # 複数のメモをローカルのリストとして用意する
    memos = [
        {"text": "牛乳を買う",       "created_at": "2026-01-01 10:00:00"},
        {"text": "図書館に本を返す", "created_at": "2026-01-02 11:00:00"},
        {"text": "運動する",         "created_at": "2026-01-03 12:00:00"},
    ]

    # --- 実行 ---
    # 3件まとめて保存する
    app.save_memos(memos, temp_file)

    # ファイルから読み込んで、返ってきたリストを受け取る
    loaded = app.load_memos(temp_file)

    # --- 確認 ---
    # 3件すべて読み込まれているはず
    assert len(loaded) == 3

    # 1件目：text と created_at の両方を確認する
    assert loaded[0]["text"] == "牛乳を買う"
    assert loaded[0]["created_at"] == "2026-01-01 10:00:00"

    # 2件目
    assert loaded[1]["text"] == "図書館に本を返す"
    assert loaded[1]["created_at"] == "2026-01-02 11:00:00"

    # 3件目
    assert loaded[2]["text"] == "運動する"
    assert loaded[2]["created_at"] == "2026-01-03 12:00:00"


def test_load_memos_with_broken_json(tmp_path):
    """memo.json が壊れていても、アプリが落ちずに空のリストになるかを確認するテスト"""

    # --- 準備 ---
    # 壊れた JSON を一時ファイルに書き込む
    # 正しい JSON は '[{"text": "..."}]' のような形だが、ここでは途中で切れた内容にする
    broken_file = tmp_path / "memo.json"
    broken_file.write_text("{ これは壊れた JSON です ", encoding="utf-8")

    # --- 実行 ---
    # 壊れたファイルを読み込もうとする（エラーで落ちないはず）
    result = app.load_memos(str(broken_file))

    # --- 確認 ---
    # 読み込みに失敗しても、空のリストが返ってくるはず
    assert len(result) == 0


def test_load_memos_when_file_does_not_exist(tmp_path):
    """memo.json がない状態で load_memos() を呼んでも、エラーにならないことを確認するテスト"""

    # --- 実行 ---
    # tmp_path にはまだファイルを作っていないので、存在しないパスを渡している
    # ファイルがなくても load_memos() がエラーなく終わるはず
    result = app.load_memos(str(tmp_path / "memo.json"))

    # --- 確認 ---
    # ファイルがないので、空のリストが返ってくるはず
    assert len(result) == 0


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


def test_show_help_prints_content(capsys):
    """show_help() を呼んだとき、何らかの内容が表示されるかを確認するテスト"""

    # capsys は pytest が用意する特別な引数で、
    # print() で出力された内容をテストの中で受け取れるようにしてくれる

    # --- 実行 ---
    app.show_help()

    # --- 確認 ---
    # capsys.readouterr() で、実行中に print() された内容を取得する
    # out には標準出力（画面に表示された文字列）が入る
    out = capsys.readouterr().out

    # 何も表示されていないのはおかしいので、空でないことを確認する
    assert out.strip() != ""

    # 各機能の名前がヘルプに含まれているかを確認する
    assert "追加" in out
    assert "削除" in out
    assert "検索" in out
    assert "編集" in out


def test_parse_memo_number_valid():
    """有効な番号の文字列を渡したとき、整数に変換されて返るかを確認するテスト"""

    # count=3 のとき、"1"〜"3" はすべて有効な番号のはず
    assert app.parse_memo_number("1", 3) == 1
    assert app.parse_memo_number("2", 3) == 2
    assert app.parse_memo_number("3", 3) == 3


def test_parse_memo_number_not_a_digit():
    """数字以外の文字列を渡したとき、None が返るかを確認するテスト"""

    # 文字列や空文字は数字ではないので None が返るはず
    assert app.parse_memo_number("abc", 3) is None
    assert app.parse_memo_number("",    3) is None
    assert app.parse_memo_number("！",  3) is None


def test_parse_memo_number_out_of_range():
    """範囲外の番号を渡したとき、None が返るかを確認するテスト"""

    # 0 以下、または count より大きい番号は範囲外なので None が返るはず
    assert app.parse_memo_number("0",  3) is None  # 小さすぎる
    assert app.parse_memo_number("4",  3) is None  # 大きすぎる
    assert app.parse_memo_number("99", 3) is None  # 大きすぎる


def test_sort_memos_by_date_new_order():
    """new（新しい順）を指定したとき、created_at の降順に並ぶかを確認するテスト"""

    # --- テストデータの準備 ---
    # あえて古い順に並べておく（並び替え前後の違いが分かるようにするため）
    memos = [
        {"text": "一番古いメモ", "created_at": "2026-01-01 10:00:00"},
        {"text": "真ん中のメモ", "created_at": "2026-01-02 10:00:00"},
        {"text": "一番新しいメモ", "created_at": "2026-01-03 10:00:00"},
    ]

    # --- 実行 ---
    # "new"（新しい順）で並び替える
    result = app.sort_memos_by_date(memos, "new")

    # --- 確認 ---
    # 新しい順なので、一番新しいメモが先頭に来るはず
    assert result[0]["text"] == "一番新しいメモ"
    assert result[1]["text"] == "真ん中のメモ"
    assert result[2]["text"] == "一番古いメモ"


def test_sort_memos_by_date_old_order():
    """old（古い順）を指定したとき、created_at の昇順に並ぶかを確認するテスト"""

    # --- テストデータの準備 ---
    # あえて新しい順に並べておく（並び替え前後の違いが分かるようにするため）
    memos = [
        {"text": "一番新しいメモ", "created_at": "2026-01-03 10:00:00"},
        {"text": "真ん中のメモ",   "created_at": "2026-01-02 10:00:00"},
        {"text": "一番古いメモ",   "created_at": "2026-01-01 10:00:00"},
    ]

    # --- 実行 ---
    # "old"（古い順）で並び替える
    result = app.sort_memos_by_date(memos, "old")

    # --- 確認 ---
    # 古い順なので、一番古いメモが先頭に来るはず
    assert result[0]["text"] == "一番古いメモ"
    assert result[1]["text"] == "真ん中のメモ"
    assert result[2]["text"] == "一番新しいメモ"


def test_sort_memos_by_date_does_not_change_original():
    """並び替えをしても、元のリストの順番が変わらないことを確認するテスト"""

    # --- テストデータの準備 ---
    memos = [
        {"text": "一番古いメモ",   "created_at": "2026-01-01 10:00:00"},
        {"text": "一番新しいメモ", "created_at": "2026-01-03 10:00:00"},
    ]

    # --- 実行 ---
    # 新しい順で並び替える
    app.sort_memos_by_date(memos, "new")

    # --- 確認 ---
    # 元のリスト（memos）の順番は変わっていないはず
    # sort_memos_by_date は sorted() を使うので、元のリストを変更しない
    assert memos[0]["text"] == "一番古いメモ"
    assert memos[1]["text"] == "一番新しいメモ"
