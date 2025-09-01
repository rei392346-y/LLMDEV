from flask import Flask, render_template, request, make_response 

# メッセージを保存するグローバル変数

messages = []
"""チャットのやりとりを保存するためのリストです。"""
# Flaskアプリケーションのセットアップ
app = Flask(__name__)

# 応答を作成する関数
"""ユーザーからのメッセージを受け取って、そのまま返す簡単な関数です。"""
def get_bot_response(user_message):
    return f"あなたが言ったのは: {user_message}"

@app.route('/', methods=['GET', 'POST'])
def index():

    # GETリクエスト時は初期メッセージ表示
    """ユーザーがページをはじめて開いたとき、GETリクエストが送信されます。
    その場合、メッセージ履歴を空のリストで初期化し、index.html をレンダリングして返します。"""
    if request.method == 'GET':
        # 対話履歴を初期化
        response = make_response(render_template('index.html', messages=[]))
        return response

    # ユーザーからのメッセージを取得
    """ユーザーが送信したメッセージ（user_message）をフォームから取得します。"""
    user_message = request.form['user_message']
    
    # ボットのレスポンスを取得
    """get_bot_response() 関数でボットの回答を生成します。"""
    bot_message = get_bot_response(user_message)

    # 対話履歴に追加
    """messages リストに追加します。"""
    messages.append(user_message)
    messages.append(bot_message)

    # レスポンスを返す
    """ messages を index.html に渡してレスポンスを返します。"""
    return make_response(render_template('index.html', messages=messages))

if __name__ == '__main__':
    app.run(debug=True)