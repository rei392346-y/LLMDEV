# VS Codeのデバッグ実行で `from chatbot.graph` でエラーを出さない対策
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# セッションごとにメモリを保持（複数人の利用に対応）
"""
メモリのキーとなる thread_id をセッションごとに管理するため、 uuid と session のインポートを追加します。
・uuid：ユニークなIDを生成
・session：セッション（ユーザー）の管理
"""
import uuid
from flask import Flask, render_template, request, make_response, session 
from original.graph import get_bot_response, get_messages_list, memory

# Flaskアプリケーションのセットアップ
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション用の秘密鍵

@app.route('/', methods=['GET', 'POST'])
def index():
    # セッションからthread_idを取得、なければ新しく生成してセッションに保存
    ## セッションごとにユニークなIDを生成し、メモリのキーとして使用します。
    if 'thread_id' not in session:
        session['thread_id'] = str(uuid.uuid4())  # ユーザー毎にユニークなIDを生成

    # キャラクター設定のデフォルト値を設定
    if 'character' not in session:
        session['character'] = {
            'name': 'ChatBot',
            'description': '汎用的なチャットボット',
            'system_prompt': 'あなたは親切で丁寧なアシスタントです。ユーザーの質問に対して正確で分かりやすい回答を提供してください。'
        }

    # GETリクエスト時は初期メッセージ表示
    if request.method == 'GET':
        # メモリをクリア
        memory.storage.clear()
        # 対話履歴を初期化
        response = make_response(render_template('index.html', 
                                               messages=[], 
                                               character=session['character']))
        return response

    # ユーザーからのメッセージを取得
    user_message = request.form['user_message']
    
    # それぞれの関数の引数で session['thread_id'] を追加で渡します。
    ## ボットのレスポンスを取得（メモリに保持）
    get_bot_response(user_message, memory, session['thread_id'], session['character']['system_prompt'])
    ## メモリからメッセージの取得
    messages = get_messages_list(memory, session['thread_id'])

    # レスポンスを返す
    return make_response(render_template('index.html', 
                                       messages=messages, 
                                       character=session['character']))

# キャラクター設定の更新機能を追加
@app.route('/update_character', methods=['POST'])
def update_character():
    # フォームからキャラクター設定を取得
    character_name = request.form.get('character_name', '').strip()
    character_description = request.form.get('character_description', '').strip()
    character_system_prompt = request.form.get('character_system_prompt', '').strip()

    # 空の場合はデフォルト値を設定
    if not character_name:
        character_name = 'ChatBot'
    if not character_description:
        character_description = '汎用的なチャットボット'
    if not character_system_prompt:
        character_system_prompt = 'あなたは親切で丁寧なアシスタントです。ユーザーの質問に対して正確で分かりやすい回答を提供してください。'

    # セッションに保存
    session['character'] = {
        'name': character_name,
        'description': character_description,
        'system_prompt': character_system_prompt
    }

    # メモリをクリア（新しいキャラクター設定を反映するため）
    memory.storage.clear()

    # 対話履歴を初期化してメインページにリダイレクト
    response = make_response(render_template('index.html', 
                                           messages=[], 
                                           character=session['character']))
    return response

# 履歴の削除機能を追加
##「履歴を削除」ボタンに対応した機能を追加しています。
@app.route('/clear', methods=['POST'])
def clear():
    # セッションからthread_idを削除
    session.pop('thread_id', None)

    # メモリをクリア
    memory.storage.clear()
    # 対話履歴を初期化
    response = make_response(render_template('index.html', 
                                           messages=[], 
                                           character=session.get('character', {
                                               'name': 'ChatBot',
                                               'description': '汎用的なチャットボット',
                                               'system_prompt': 'あなたは親切で丁寧なアシスタントです。ユーザーの質問に対して正確で分かりやすい回答を提供してください。'
                                           })))
    return response

if __name__ == '__main__':
    app.run(debug=True)