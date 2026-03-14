# メモ帳アプリケーション
# このプログラムは、コマンドラインでメモを管理するシンプルなアプリです

# .env ファイルの内容を読み込むためのライブラリを使う
import os

# JSON ファイルを読み書きするためのライブラリを使う
import json

# 現在日時を取得するためのライブラリを使う
from datetime import datetime

from dotenv import load_dotenv


# .env ファイルを読み込んで、環境変数として使えるようにする
load_dotenv()

# APP_NAME は起動時の表示に使う
app_name = os.getenv("APP_NAME", "メモ帳アプリ")

# SECRET_WORD も読み込めるようにしておく
# ただし、秘密の値なので画面には表示しない
secret_word = os.getenv("SECRET_WORD")

# メモを保存するファイル名（JSON形式）
memo_file = "memo.json"


# メモを保存するためのリスト（空のリストで初期化）
memos = []

# memo.json からメモを読み込む関数
def load_memos():
    """保存済みのメモをJSONファイルから読み込む関数"""
    # 先に今のリストを空にして、同じ内容が二重に入らないようにする
    memos.clear()
    # memo.json がある場合だけ読み込む
    if os.path.exists(memo_file):
        # JSON ファイルを開いて、中身を Python のリストに変換する
        with open(memo_file, "r", encoding="utf-8") as file:
            # json.load() は JSON ファイルを読み込んでリストや辞書に変換する関数
            data = json.load(file)
            # 読み込んだデータをメモリスト（memos）に追加する
            for item in data:
                # 古い形式（文字列）のメモが残っている場合、辞書形式に変換して読み込む
                if isinstance(item, str):
                    memos.append({"text": item, "created_at": "不明"})
                else:
                    memos.append(item)

# メモを memo.json に保存し直す関数
def save_memos():
    """今のメモ一覧をJSONファイルに保存する関数"""
    # "w" モードは、ファイルの内容を新しく書き直すときに使う
    with open(memo_file, "w", encoding="utf-8") as file:
        # json.dump() は Python のリストを JSON 形式に変換してファイルに書き込む関数
        # ensure_ascii=False にすると、日本語がそのまま保存される
        # indent=2 にすると、ファイルを開いたときに見やすく整形される
        json.dump(memos, file, ensure_ascii=False, indent=2)

# メニューを表示する関数
def show_menu():
    """メニューを画面に表示する関数"""
    print("CLIメモ帳へようこそ！")
    print("\n=== メモ帳 ===")
    print("1. メモを追加")
    print("2. メモ一覧を表示")
    print("3. メモを削除")
    print("4. 全メモ削除")
    print("5. メモを検索")
    print("6. 終了")
    print("=============\n")

# メモを追加する関数
def add_memo():
    """新しいメモを追加する関数"""
    # ユーザーからメモの内容を入力してもらう
    memo_text = input("メモを入力してください: ")
    
    # 入力されたメモが空でない場合のみ追加
    if memo_text.strip() != "":
        # メモを辞書形式で作る
        # 辞書とは、キーと値のペアでデータを管理するPythonのデータ構造
        # 例: {"text": "買い物", "created_at": "2024-01-01 12:00:00"}
        memo = {
            "text": memo_text,
            # datetime.now() で現在日時を取得し、strftime() で見やすい形式の文字列に変換する
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # メモリストに辞書を追加
        memos.append(memo)
        # JSON はファイル全体を書き直す必要があるため、save_memos() で保存する
        save_memos()
        print("メモを追加しました！")
    else:
        print("空のメモは追加できません。")

# 並び替え順をユーザーに選んでもらう関数
def ask_sort_order():
    """新しい順か古い順かをユーザーに選んでもらい、選択結果を返す関数"""
    print("並び替え順を選んでください")
    print("  1. 新しい順")
    print("  2. 古い順")
    order_input = input("選択 (1 or 2): ")

    if order_input == "2":
        return "old"
    else:
        # 1 以外が入力された場合も新しい順にする
        return "new"

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

# メモ一覧を表示する関数
def show_memos():
    """保存されているメモの一覧を表示する関数"""
    # メモが1つもない場合
    if len(memos) == 0:
        print("メモはまだありません。")
    else:
        # 並び替え順をユーザーに選んでもらう
        order = ask_sort_order()
        # 選んだ順番でメモを並び替える（元の memos リストは変更しない）
        sorted_list = sort_memos_by_date(memos, order)

        # メモがある場合、件数を表示してから番号を付けて表示
        print(f"\nメモは {len(sorted_list)} 件あります")
        print("--- メモ一覧 ---")
        # 各メモを番号と一緒に表示
        for i, memo in enumerate(sorted_list, start=1):
            # memo は辞書なので、キーを使って値を取り出す
            print(f"{i}. {memo['text']}  （作成日時: {memo['created_at']}）")
        print("----------------\n")

# メモを削除する関数
def delete_memo():
    """メモを削除する関数"""
    # メモが1つもない場合
    if len(memos) == 0:
        print("削除するメモがありません。")
        return
    
    # メモ一覧を表示して、どのメモを削除するか選んでもらう
    print("\n--- 削除するメモを選んでください ---")
    # 各メモを番号と一緒に表示
    for i, memo in enumerate(memos, start=1):
        # memo は辞書なので、キーを使って値を取り出す
        print(f"{i}. {memo['text']}  （作成日時: {memo['created_at']}）")
    print("------------------------------------\n")
    
    # 正しい番号が入力されるまで繰り返す
    while True:
        # ユーザーから削除したいメモの番号を入力してもらう
        number_input = input("削除するメモの番号を入力してください: ")
        
        # 入力が数字かどうかを確認
        # isdigit()は文字列が数字のみで構成されているかチェックする関数
        if not number_input.isdigit():
            # 数字でない場合、再入力を促す
            print("数字を入力してください。")
            continue
        
        # 文字列を整数に変換
        number = int(number_input)
        
        # 番号が有効な範囲内かどうかを確認
        # 番号は1以上、メモの数以下でなければならない
        if number < 1 or number > len(memos):
            # 範囲外の番号の場合、再入力を促す
            print(f"1から{len(memos)}までの番号を入力してください。")
            continue
        
        # 有効な番号が入力された場合
        # リストのインデックスは0から始まるので、番号から1を引く
        deleted_memo = memos.pop(number - 1)
        # 削除後の状態を、そのままファイルに保存し直す
        save_memos()
        print(f"メモ「{deleted_memo['text']}」を削除しました。")
        # 正しい番号が入力されたので、ループを抜ける
        break

# 全メモを削除する関数
def clear_memos():
    """保存されているメモをすべて削除する関数"""
    # メモが1つもない場合は何もしない
    if len(memos) == 0:
        print("削除するメモがありません。")
        return

    # 誤操作を防ぐために、削除前に確認メッセージを表示する
    confirm = input(f"保存中の {len(memos)} 件のメモをすべて削除しますか？ (y/n): ")

    # "y" が入力された場合のみ削除を実行する
    if confirm == "y":
        # clear()はリストの中身をすべて空にするメソッド
        memos.clear()
        # 全削除した結果をファイルにも反映する
        save_memos()
        print("すべてのメモを削除しました。")
    else:
        # "y" 以外（"n" など）が入力された場合はキャンセル
        print("削除をキャンセルしました。")


# メモを検索する関数
def search_memos():
    """キーワードを含むメモを検索して表示する関数"""
    # ユーザーから検索キーワードを入力してもらう
    keyword = input("検索キーワードを入力してください: ")

    # 空のキーワードは検索しない
    if keyword.strip() == "":
        print("キーワードを入力してください。")
        return

    # キーワードを含むメモだけを集めるリスト（最初は空）
    results = []

    # メモを1件ずつ確認して、キーワードが含まれているものを results に追加する
    for memo in memos:
        # in を使うと、文字列の中に別の文字列が含まれているか調べられる
        # 例: "買い物" in "牛乳を買い物リストに追加" → True
        if keyword in memo["text"]:
            results.append(memo)

    # 検索結果を表示する
    if len(results) == 0:
        # 1件もヒットしなかった場合
        print(f"「{keyword}」に一致するメモは見つかりませんでした。")
    else:
        # 並び替え順をユーザーに選んでもらう
        order = ask_sort_order()
        # 選んだ順番で検索結果を並び替える
        sorted_results = sort_memos_by_date(results, order)

        # ヒットした件数を表示してから、内容を表示する
        print(f"\n「{keyword}」の検索結果: {len(sorted_results)} 件")
        print("--- 検索結果 ---")
        for i, memo in enumerate(sorted_results, start=1):
            print(f"{i}. {memo['text']}  （作成日時: {memo['created_at']}）")
        print("----------------\n")


# メイン処理
def main():
    """プログラムのメイン処理"""
    # .env から読み込んだアプリ名を、起動時に表示する
    print(f"{app_name} を起動しました。")
    # 起動時に memo.json があれば読み込む
    load_memos()
    
    # 無限ループ（ユーザーが終了を選ぶまで繰り返す）
    while True:
        # メニューを表示
        show_menu()
        
        # ユーザーからの入力を待つ
        choice = input("選択してください (1-6): ")

        # 選択に応じて処理を分岐
        if choice == "1":
            # 1が選ばれた場合：メモを追加
            add_memo()
        elif choice == "2":
            # 2が選ばれた場合：メモ一覧を表示
            show_memos()
        elif choice == "3":
            # 3が選ばれた場合：メモを削除
            delete_memo()
        elif choice == "4":
            # 4が選ばれた場合：全メモ削除
            clear_memos()
        elif choice == "5":
            # 5が選ばれた場合：メモを検索
            search_memos()
        elif choice == "6":
            # 6が選ばれた場合：終了
            print("メモ帳を終了します。")
            break
        else:
            # 1〜6以外が入力された場合
            print("無効な選択です。1, 2, 3, 4, 5, 6のいずれかを入力してください。")

# プログラムの実行開始点
# このファイルが直接実行された場合のみ、main()関数を呼び出す
if __name__ == "__main__":
    main()
