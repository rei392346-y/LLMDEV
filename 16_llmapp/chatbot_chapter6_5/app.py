# VS Codeのデバッグ実行で `from chatbot.graph` でエラーを出さない対策
"""
VS Codeのデバッグ実行はプロジェクトのルートフォルダで実行されます。
その際、 from chatbot.graph でモジュールが読み込めないエラーとなるために、読み込みパスに chatbot フォルダを追加しています。
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, make_response 
# 対話履歴を、メモリから取得する関数をインポート
from chatbot.graph import get_bot_response, get_messages_list, memory

# Flaskアプリケーションのセットアップ
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    # GETリクエスト時は初期メッセージ表示
    if request.method == 'GET':
        # メモリをクリア
        ## 初期表示時に、対話履歴（メモリ）をクリアする GETリクエスト時に、メモリのクリアを追加
        memory.storage.clear()
        # 対話履歴を初期化
        response = make_response(render_template('index.html', messages=[]))
        return response

    # ユーザーからのメッセージを取得
    user_message = request.form['user_message']
    
    # 対話履歴をメモリから取得するように変更
    ## ボットのレスポンスを取得（メモリに保持）
    get_bot_response(user_message, memory)
    ## メモリからメッセージの取得
    messages = get_messages_list(memory)

    # レスポンスを返す
    return make_response(render_template('index.html', messages=messages))

if __name__ == '__main__':
    app.run(debug=True)
