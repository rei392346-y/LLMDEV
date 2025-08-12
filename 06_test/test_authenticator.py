import pytest
# authenticator.pyからAuthenticatorクラスをインポート
from authenticator import Authenticator

def test_register_success():
    """
    ユーザーが正しく登録されるかのテスト。
    """
    auth = Authenticator()
    auth.register("testuser", "password123")
    # ユーザーが辞書に正しく登録されたかを確認
    assert "testuser" in auth.users
    assert auth.users["testuser"] == "password123"

def test_register_duplicate_user():
    """
    既に存在するユーザー名で登録しようとした場合に、
    正しくValueErrorが発生するかのテスト。
    """
    auth = Authenticator()
    auth.register("testuser", "password123")
    # pytest.raisesを使用して、特定の例外が発生することを検証
    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        auth.register("testuser", "anotherpassword")

def test_login_success():
    """
    正しいユーザー名とパスワードでログインできるかのテスト。
    """
    auth = Authenticator()
    auth.register("testuser", "password123")
    # loginメソッドが"ログイン成功"の文字列を返すことを確認
    assert auth.login("testuser", "password123") == "ログイン成功"

def test_login_failure():
    """
    誤ったパスワードでログインしようとした場合に、
    正しくValueErrorが発生するかのテスト。
    """
    auth = Authenticator()
    auth.register("testuser", "password123")
    # 誤ったパスワードでログインを試み、例外が発生することを確認
    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません。"):
        auth.login("testuser", "wrongpassword")
