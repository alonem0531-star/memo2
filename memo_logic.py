# memo_logic.py
# メモのデータ処理だけを担当するファイルです
# input() や print() は使わず、データを受け取って結果を返す関数だけを置きます

# 現在日時を取得するためのライブラリを使う
from datetime import datetime


# テキストからメモの辞書を作る関数
def make_memo(text):
    """テキストから新しいメモの辞書を作って返す関数"""
    return {
        "text": text,
        # datetime.now() で現在日時を取得し、strftime() で見やすい形式の文字列に変換する
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# メモリストを作成日時で並び替えて返す関数
def sort_memos_by_date(memo_list, order):
    """メモのリストを日時順に並び替えた新しいリストを返す関数"""
    # sorted() は元のリストを変えずに、並び替えた新しいリストを返す関数
    # key には「何を基準に並び替えるか」を指定する
    # lambda memo: memo["created_at"] は「各メモの created_at を基準にする」という意味
    if order == "new":
        # reverse=True にすると、大きい値（新しい日時）が先に来る
        return sorted(memo_list, key=lambda memo: memo["created_at"], reverse=True)
    else:
        # reverse=False（デフォルト）にすると、小さい値（古い日時）が先に来る
        return sorted(memo_list, key=lambda memo: memo["created_at"])


# 文字列の入力をメモの番号（整数）に変換する関数
def parse_memo_number(text, count):
    """入力文字列 text を 1〜count の範囲の整数に変換する関数。
    有効な番号なら整数を返す、数字でない・範囲外なら None を返す。"""

    # isdigit() で数字だけで構成された文字列かどうかを確認する
    # 例: "3".isdigit() → True、"abc".isdigit() → False
    if not text.isdigit():
        return None

    # 文字列を整数に変換する
    number = int(text)

    # 1 以上、メモの件数以下かどうかを確認する
    if number < 1 or number > count:
        return None

    # 有効な番号なのでそのまま返す
    return number


# 指定した位置のメモを削除する関数
def delete_memo(memos, index):
    """memos の index 番目のメモを削除する関数。
    成功したら削除したメモを返す、index が不正なら None を返す。"""

    # index が有効な範囲内かどうかを確認する
    # リストのインデックスは 0 から len(memos)-1 まで有効
    if index < 0 or index >= len(memos):
        # 不正な index の場合は何も変更せず None を返す
        return None

    # pop() はリストから要素を取り出して削除するメソッド
    return memos.pop(index)


# 指定した位置のメモを更新する関数
def edit_memo(memos, index, new_text):
    """memos の index 番目のメモを new_text に書き換える関数。
    成功したら True、index が不正なら False を返す。"""

    # index が有効な範囲内かどうかを確認する
    # リストのインデックスは 0 から len(memos)-1 まで有効
    if index < 0 or index >= len(memos):
        # 不正な index の場合は何も変更せず False を返す
        return False

    # text を新しい内容に書き換える（created_at はそのまま残す）
    memos[index]["text"] = new_text
    return True


# キーワードを含むメモだけを返す関数
def search_memos(memos, keyword):
    """memos の中から keyword を含むメモだけを返す関数"""
    # キーワードを含むメモだけを集めるリスト（最初は空）
    results = []

    # メモを1件ずつ確認して、キーワードが含まれているものを results に追加する
    for memo in memos:
        # in を使うと、文字列の中に別の文字列が含まれているか調べられる
        # 例: "買い物" in "牛乳を買い物リストに追加" → True
        if keyword in memo["text"]:
            results.append(memo)

    return results
