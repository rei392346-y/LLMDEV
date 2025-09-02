import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated
from typing_extensions import TypedDict

# 環境変数を読み込む
load_dotenv(".env")
os.environ['OPENAI_API_KEY'] = os.environ['API_KEY']

# 使用するモデル名
MODEL_NAME = "gpt-4o-mini" 

"""memory と graph をグローバル変数として定義します。
これは、Flaskアプリケーションの実行中にその状態を保持し、アプリケーションのライフサイクル全体にわたって利用し続けるためです。"""
# MemorySaverインスタンスの作成
memory = MemorySaver()

# グラフを保持する変数の初期化
graph = None

# ===== Stateクラスの定義 =====
# Stateクラス: メッセージのリストを保持する辞書型
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ===== グラフの構築 =====
def build_graph(model_name, memory):
    """
    グラフのインスタンスを作成し、ツールノードやチャットボットノードを追加します。
    モデル名とメモリを使用して、実行可能なグラフを作成します。
    """
    print("デバッグメッセージ: build_graph が呼び出されました")  # デバッグ用のログ
    # グラフのインスタンスを作成
    graph_builder = StateGraph(State)

    # ツールノードを作成（TavilySearchResultsを使用）
    tavily_tool = TavilySearchResults(max_results=2)
    tools = [tavily_tool]
    tool_node = ToolNode(tools)
    graph_builder.add_node("tools", tool_node)

    # チャットボットノードの作成
    llm = ChatOpenAI(model_name=model_name)
    llm_with_tools = llm.bind_tools(tools)
    
    # チャットボットの実行方法を定義
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    
    graph_builder.add_node("chatbot", chatbot)

    # 実行可能なグラフの作成
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.set_entry_point("chatbot")
    
    return graph_builder.compile(checkpointer=memory)

# ===== グラフを実行する関数 =====
def stream_graph_updates(graph: StateGraph, user_message: str):
    """
    ユーザーからのメッセージを元に、グラフを実行し、チャットボットの応答をストリーミングします。
    """
    print("デバッグメッセージ: stream_graph_updates が呼び出されました")  # デバッグ用のログ
    # グラフを実行し、ストリーミングモードで応答を取得
    response = graph.invoke(
        {"messages": [("user", user_message)]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="values"
    )
    return response["messages"][-1].content

# ===== 応答を返す関数 =====
"""最初にグラフが作成されていない場合は、新しいグラフを作成します。	
グラフが作成された後、stream_graph_updates を使って、ユーザーのメッセージに対するボットの応答を得ます。"""
def get_bot_response(user_message, memory):
    """
    ユーザーのメッセージに基づき、ボットの応答を取得します。
    初回の場合、新しいグラフを作成します。

    """
    print("デバッグメッセージ: get_bot_response が呼び出されました")  # デバッグ用のログ
    global graph
    # グラフがまだ作成されていない場合、新しいグラフを作成
    if graph is None:
        graph = build_graph(MODEL_NAME, memory)

    # グラフを実行してボットの応答を取得
    return stream_graph_updates(graph, user_message)

# ===== メッセージの一覧を取得する関数 =====
def get_messages_list(memory):
    """
    メモリからメッセージ一覧を取得し、ユーザーとボットのメッセージを分類します。
    """
    print("デバッグメッセージ: get_messages_list が呼び出されました")  # デバッグ用のログ
    messages = []
    # メモリからメッセージを取得
    memories = memory.get({"configurable": {"thread_id": "1"}})['channel_values']['messages']
    print("デバッグメッセージのmemories:", memories)  # デバッグ用にメモリの内容を出力
    # print("デバッグメッセージのtype(memories):", type(memories))  # デバッグ用にmemoriesの型を出力
    for message in memories:
        if isinstance(message, HumanMessage):
            # ユーザーからのメッセージ
            messages.append({'class': 'user-message', 'text': message.content})
        elif isinstance(message, AIMessage) and message.content != "":
            # ボットからのメッセージ（最終回答）
            messages.append({'class': 'bot-message', 'text': message.content})
        else:
            # その他のメッセージタイプ（必要に応じて処理を追加可能）
            print("get_messages_listのelse処理") 
        print("デバッグメッセージの追加されたmessage:", message)  # デバッグ用に各メッセージを出力
        print("デバッグメッセージの追加されたtype(message):", type(message))  # デバッグ用に各メッセージの型を出力

    # メッセージがなくても、必ずリストを返す
    return messages