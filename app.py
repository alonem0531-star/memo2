# メモ帳アプリケーション
# このプログラムは、コマンドラインでメモを管理するシンプルなアプリです

# メモを保存するためのリスト（空のリストで初期化）
memos = []

# メニューを表示する関数
def show_menu():
    """メニューを画面に表示する関数"""
    print("CLIメモ帳へようこそ！")
    print("\n=== メモ帳 ===")
    print("1. メモを追加")
    print("2. メモ一覧を表示")
    print("3. メモを削除")
    print("4. 全メモ削除")
    print("5. 終了")
    print("=============\n")

# メモを追加する関数
def add_memo():
    """新しいメモを追加する関数"""
    # ユーザーからメモの内容を入力してもらう
    memo_text = input("メモを入力してください: ")
    
    # 入力されたメモが空でない場合のみ追加
    if memo_text.strip() != "":
        # メモリストに追加
        memos.append(memo_text)
        print("メモを追加しました！")
    else:
        print("空のメモは追加できません。")

# メモ一覧を表示する関数
def show_memos():
    """保存されているメモの一覧を表示する関数"""
    # メモが1つもない場合
    if len(memos) == 0:
        print("メモはまだありません。")
    else:
        # メモがある場合、件数を表示してから番号を付けて表示
        # len(memos)でメモの数を取得できる
        print(f"\nメモは {len(memos)} 件あります")
        print("--- メモ一覧 ---")
        # 各メモを番号と一緒に表示
        for i, memo in enumerate(memos, start=1):
            print(f"{i}. {memo}")
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
        print(f"{i}. {memo}")
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
        print(f"メモ「{deleted_memo}」を削除しました。")
        # 正しい番号が入力されたので、ループを抜ける
        break

# 全メモを削除する関数
def delete_all_memos():
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
        print("すべてのメモを削除しました。")
    else:
        # "y" 以外（"n" など）が入力された場合はキャンセル
        print("削除をキャンセルしました。")


# メイン処理
def main():
    """プログラムのメイン処理"""
    print("メモ帳アプリケーションを起動しました。")
    
    # 無限ループ（ユーザーが終了を選ぶまで繰り返す）
    while True:
        # メニューを表示
        show_menu()
        
        # ユーザーからの入力を待つ
        choice = input("選択してください (1-5): ")

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
            delete_all_memos()
        elif choice == "5":
            # 5が選ばれた場合：終了
            print("メモ帳を終了します。")
            break
        else:
            # 1〜5以外が入力された場合
            print("無効な選択です。1, 2, 3, 4, 5のいずれかを入力してください。")

# プログラムの実行開始点
# このファイルが直接実行された場合のみ、main()関数を呼び出す
if __name__ == "__main__":
    main()
